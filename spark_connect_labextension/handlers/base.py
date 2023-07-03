import json
from jupyter_server.base.handlers import APIHandler
from jupyter_server.extension.handler import ExtensionHandlerMixin
from jsonpath_ng import jsonpath, parse

class SparkConnectAPIHandler(ExtensionHandlerMixin, APIHandler):
    @property
    def ext_config(self):
        return self.settings['spark_connect_config']
    
    @property
    def spark_clusters(self):
        return self.ext_config['clusters']
    
    @property
    def spark_config_bundles(self):
        config_bundles = self.ext_config.get('config_bundles', {})
        from_file_options = self.ext_config.get('config_bundles_from_file')
        if from_file_options:
            file_path = from_file_options['file']
            with open(file_path, 'r') as f:
                json_data = json.load(f)
                jsonpath_expr = parse(from_file_options['json_path'])
                matches = jsonpath_expr.find(json_data)
                first_match = matches[0]
                out_config_bundles = {**config_bundles, **first_match.value}
                config_bundles = out_config_bundles
            
        return config_bundles
    
    @property
    def spark_options(self):
        options = self.ext_config.get('spark_options', [])
        from_file_options = self.ext_config.get('spark_options_from_file')
        if from_file_options:
            file_path = from_file_options['file']
            with open(file_path, 'r') as f:
                json_data = json.load(f)
                jsonpath_expr = parse(from_file_options['json_path'])
                matches = jsonpath_expr.find(json_data)
                first_match = matches[0]
                out_options = options + first_match.value
                options = out_options

        return options
    
    @property
    def error_suggestions(self):
        return self.ext_config.get('error_suggestions', [])