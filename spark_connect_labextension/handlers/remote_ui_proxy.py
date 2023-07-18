import re
from jupyter_server_proxy.handlers import RemoteProxyHandler, RewritableResponse, UnixResolver, call_with_asked_args, url_path_join
from tornado import httpclient, web, httputil
from tornado.simple_httpclient import SimpleAsyncHTTPClient
from urllib.parse import urlparse
from jupyter_server.extension.handler import ExtensionHandlerMixin
from spark_connect_labextension.config import EXTENSION_ID
from spark_connect_labextension.sparkconnectserver.cluster import cluster


class RemoteUIProxyHandler(ExtensionHandlerMixin, RemoteProxyHandler):
    @property
    def ext_config(self):
        return self.settings['spark_connect_config']
    
    @property
    def spark_clusters(self):
        return self.ext_config['clusters']
    
    @property
    def spark_webui_proxy_host_allowlist(self):
        current_cluster = self.spark_clusters[cluster.cluster_name]
        return current_cluster.get('spark_webui_proxy_host_allowlist', ['localhost', '127.0.0.1'])

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.host_allowlist = self.spark_webui_proxy_host_allowlist

        def rewrite_response(response, request=None):
            uri = request.uri
            protocol, remote_host, path = self._parse_path(uri)

            print(response.headers)

            if response.headers.get('Location'):
                location = response.headers['Location']
                location_parsed = urlparse(location)
                if location_parsed.netloc == '' or location_parsed.netloc == request.host:
                    if location_parsed.path.startswith('/'):
                        # Absolute URL, incomplete
                        proxy_base = self._get_proxy_base(protocol, remote_host)
                        location = proxy_base + location_parsed.path
                        
                else:
                    # Full URL
                    proxy_base = self._get_proxy_base(protocol, location_parsed.netloc)
                    path_q = [location_parsed.path]
                    if location_parsed.query:
                        path_q.append(location_parsed.query)

                    location = proxy_base + '?'.join(path_q)

                response.headers['Location'] = location

            return response
        
        self.rewrite_response = rewrite_response
    
    def _get_context_path(self, protocol, host, port):
        return self._get_proxy_base(protocol, f"{host}:{port}")
    
    def _get_proxy_base(self, protocol, hostname):
        return url_path_join(self.base_url, EXTENSION_ID, 'remote', protocol, f"{hostname}")
    
    async def http_get(self, protocol, host, port, proxied_path):
        return await self.proxy(host, port, proxied_path)

    def post(self, protocol, host, port, proxied_path):
        return self.proxy(host, port, proxied_path)

    def put(self, protocol, host, port, proxied_path):
        return self.proxy(host, port, proxied_path)

    def delete(self, protocol, host, port, proxied_path):
        return self.proxy(host, port, proxied_path)

    def head(self, protocol, host, port, proxied_path):
        return self.proxy(host, port, proxied_path)

    def patch(self, protocol, host, port, proxied_path):
        return self.proxy(host, port, proxied_path)

    def options(self, protocol, host, port, proxied_path):
        return self.proxy(host, port, proxied_path)
    
    async def open(self, protocol, host, port, proxied_path):
        return await self.proxy_open(host, port, proxied_path)
    
    def _build_proxy_request(self, host, port, proxied_path, body):
        headers = self.proxy_request_headers()
        protocol, remote_host, path = self._parse_path(self.request.uri)
        print(protocol, remote_host, path)

        client_uri = self.get_client_uri(protocol, host, port, proxied_path)
        # Some applications check X-Forwarded-Context and X-ProxyContextPath
        # headers to see if and where they are being proxied from.
        if not self.absolute_url:
            context_path = self._get_context_path(protocol, host, port)
            headers["Host"] = f"{host}:{port}"
            headers["X-Forwarded-Context"] = context_path
            headers["X-ProxyContextPath"] = context_path
            # to be compatible with flask/werkzeug wsgi applications
            headers["X-Forwarded-Prefix"] = context_path

        req = httpclient.HTTPRequest(
            client_uri,
            method=self.request.method,
            body=body,
            decompress_response=False,
            headers=headers,
            **self.proxy_request_options(),
        )
        return req
    
    def _parse_path(self, uri):
        capture_group = url_path_join(self.base_url, EXTENSION_ID, 'remote', f"([^/:@]+)/([^/@]+)(/.*)")
        result = re.search(capture_group, uri)
        protocol = result.group(1)
        remote_host = result.group(2)
        path = result.group(3)

        return protocol, remote_host, path
