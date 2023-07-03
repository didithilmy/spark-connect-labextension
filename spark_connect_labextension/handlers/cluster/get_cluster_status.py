from spark_connect_labextension.handlers.base import SparkConnectAPIHandler
import tornado
import json
from spark_connect_labextension.sparkconnectserver.cluster import cluster
from spark_connect_labextension.config import SPARK_CLUSTER_NAME


class GetClusterStatusRouteHandler(SparkConnectAPIHandler):
    @tornado.web.authenticated
    def get(self):
        status = cluster.get_status()
        self.finish(json.dumps({
            'status': status.name, 
            'clusterName': cluster.cluster_name,
            'port': cluster.get_port(),
            'configBundles': cluster.config_bundles,
            'extraConfig': cluster.extra_config,
            'sparkOptions': cluster.get_options(),
            'extensionConfig': {
                'preselectedClusterName': SPARK_CLUSTER_NAME,
                'disableClusterSelectionOnPreselected': self.ext_config.get('disable_cluster_selection_on_preselected', False)
            }
        }))
