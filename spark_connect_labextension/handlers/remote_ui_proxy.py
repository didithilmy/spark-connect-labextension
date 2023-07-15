import re
from jupyter_server_proxy.handlers import RemoteProxyHandler, url_path_join
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
        return current_cluster.get('spark_webui_proxy_host_allowlist', ['localhost', 'didithilmy.free.beeceptor.com'])

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.host_allowlist = self.spark_webui_proxy_host_allowlist

        def rewrite_response(response, request=None):
            uri = request.uri
            capture_group = url_path_join(self.base_url, EXTENSION_ID, 'remote', f"(.+)(/.*)")
            result = re.search(capture_group, uri)
            remote_host = result.group(1)

            if response.headers.get('Location'):
                location = response.headers['Location']
                print("Location", location)
                location_parsed = urlparse(location)
                if location_parsed.netloc == '' or location_parsed.netloc == request.host:
                    if location_parsed.path.startswith('/'):
                        print("Parsing absolute URL, incomplete", location)
                        # Absolute URL, incomplete
                        proxy_base = self._get_proxy_base(remote_host)
                        location = proxy_base + location_parsed.path
                        
                else:
                    # Full URL
                    proxy_base = self._get_proxy_base(location_parsed.netloc)
                    path_q = [location_parsed.path]
                    if location_parsed.query:
                        path_q.append(location_parsed.query)

                    location = proxy_base + '?'.join(path_q)

                response.headers['Location'] = location

            return response
        
        self.rewrite_response = rewrite_response
    
    def _get_context_path(self, host, port):
        return self._get_proxy_base(f"{host}:{port}")
    
    def _get_proxy_base(self, hostname):
        return url_path_join(self.base_url, EXTENSION_ID, 'remote', f"{hostname}")
