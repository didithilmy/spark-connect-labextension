from jupyter_server.extension.application import ExtensionApp
from spark_connect_labextension.handlers.cluster.start_cluster import StartClusterRouteHandler
from spark_connect_labextension.handlers.cluster.stop_cluster import StopClusterRouteHandler
from spark_connect_labextension.handlers.cluster.get_cluster_logs import GetClusterLogRouteHandler
from spark_connect_labextension.handlers.cluster.get_cluster_error_suggestions import GetClusterErrorSuggestionsRouteHandler
from spark_connect_labextension.handlers.cluster.get_cluster_status import GetClusterStatusRouteHandler
from spark_connect_labextension.handlers.cluster.get_clusters import GetClustersRouteHandler
from spark_connect_labextension.handlers.cluster.get_config_bundles import GetConfigBundlesRouteHandler
from spark_connect_labextension.handlers.cluster.get_config_options import GetConfigOptionsRouteHandler
from spark_connect_labextension.handlers.ui_proxy import SparkUIProxyHandler
from spark_connect_labextension.config import EXTENSION_ID


class SparkConnectExtensionApp(ExtensionApp):
    name = "spark_connect_labextension"
    default_url = f"/{EXTENSION_ID}"
    base_url = f"/{EXTENSION_ID}"
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
        handlers = [
            (f"{self.base_url}/clusters", GetClustersRouteHandler),
            (f"{self.base_url}/config-bundles", GetConfigBundlesRouteHandler),
            (f"{self.base_url}/config-options", GetConfigOptionsRouteHandler),
            (f"{self.base_url}/cluster/start", StartClusterRouteHandler),
            (f"{self.base_url}/cluster/stop", StopClusterRouteHandler),
            (f"{self.base_url}/cluster/logs", GetClusterLogRouteHandler),
            (f"{self.base_url}/cluster/errors", GetClusterErrorSuggestionsRouteHandler),
            (f"{self.base_url}/cluster/status", GetClusterStatusRouteHandler),
            (f"{self.base_url}/ui(?P<proxied_path>.*)", SparkUIProxyHandler),
        ]
        self.handlers.extend(handlers)
