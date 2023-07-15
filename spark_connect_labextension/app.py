from jupyter_server.extension.application import ExtensionApp
from spark_connect_labextension.handlers.cluster.start_cluster import StartClusterRouteHandler
from spark_connect_labextension.handlers.cluster.stop_cluster import StopClusterRouteHandler
from spark_connect_labextension.handlers.cluster.get_cluster_logs import GetClusterLogRouteHandler
from spark_connect_labextension.handlers.cluster.get_cluster_error_suggestions import GetClusterErrorSuggestionsRouteHandler
from spark_connect_labextension.handlers.cluster.get_cluster_status import GetClusterStatusRouteHandler
from spark_connect_labextension.handlers.cluster.get_clusters import GetClustersRouteHandler
from spark_connect_labextension.handlers.cluster.get_config_bundles import GetConfigBundlesRouteHandler
from spark_connect_labextension.handlers.cluster.get_config_options import GetConfigOptionsRouteHandler
from spark_connect_labextension.handlers.ui_proxy_redirect import SparkUIProxyRedirectHandler
from spark_connect_labextension.handlers.ui_proxy import SparkUIProxyHandler
from spark_connect_labextension.handlers.remote_ui_proxy import RemoteUIProxyHandler
from spark_connect_labextension.config import EXTENSION_ID


class SparkConnectExtensionApp(ExtensionApp):
    name = "spark_connect_labextension"
    default_url = f"/{EXTENSION_ID}"
    # base_url = f"${self.base_url}{EXTENSION_ID}"
    load_other_extensions = True
    file_url_prefix = "/render"

    settings = {}
    handlers = []
    static_paths = []
    template_paths = []

    def initialize_settings(self):
        self.settings.update(
            {"spark_connect_config": self.config["SparkConnectConfig"]}
        )

    def initialize_handlers(self):
        base_url = f"/{EXTENSION_ID}"
        handlers = [
            (f"{base_url}/clusters", GetClustersRouteHandler),
            (f"{base_url}/config-bundles", GetConfigBundlesRouteHandler),
            (f"{base_url}/config-options", GetConfigOptionsRouteHandler),
            (f"{base_url}/cluster/start", StartClusterRouteHandler),
            (f"{base_url}/cluster/stop", StopClusterRouteHandler),
            (f"{base_url}/cluster/logs", GetClusterLogRouteHandler),
            (f"{base_url}/cluster/errors", GetClusterErrorSuggestionsRouteHandler),
            (f"{base_url}/cluster/status", GetClusterStatusRouteHandler),
            (f"{base_url}/ui", SparkUIProxyRedirectHandler),
            (f"{base_url}/ui/", SparkUIProxyRedirectHandler),
            (f"{base_url}/ui(?P<proxied_path>.*)", SparkUIProxyHandler),
            (f"{base_url}/remote/(?P<host>[^/:@]+):(?P<port>\d+)(?P<proxied_path>/.*)", RemoteUIProxyHandler),
        ]
        self.handlers.extend(handlers)
