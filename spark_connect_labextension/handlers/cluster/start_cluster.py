from spark_connect_labextension.handlers.base import SparkConnectAPIHandler
import tornado
import json
import traceback
from spark_connect_labextension.sparkconnectserver.cluster import cluster


class StartClusterRouteHandler(SparkConnectAPIHandler):
    @tornado.web.authenticated
    def post(self):
        json_body = self.get_json_body()
        cluster_name = json_body['cluster']
        config_bundles = json_body.get('configBundles', [])
        extra_config = json_body.get('extraConfig', {})
        options = json_body.get('options', {})
        cluster_metadata = self.spark_clusters[cluster_name]
        cluster_env = cluster_metadata.get('env', {})
        pre_script = cluster_metadata.get('pre_script')

        try:
            cluster.start(cluster_name=cluster_name, options=options, envs=cluster_env, config_bundles=config_bundles, extra_config=extra_config, pre_script=pre_script)
            self.finish(json.dumps({
                "success": True,
                "message": "STARTED_SPARK_CONNECT_SERVER"
            }))
        except:
            traceback.print_exc()
            self.set_status(500)
            self.finish(json.dumps({
                "error": "FAILED_TO_START_SPARK_CONNECT_SERVER"
            }))
