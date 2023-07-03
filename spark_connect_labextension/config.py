import os

EXTENSION_ID = 'spark-connect-labextension'

SPARK_HOME = os.getenv('SPARK_HOME')
SPARK_CONNECT_PACKAGE = os.getenv('SPARK_CONNECT_PACKAGE', 'org.apache.spark:spark-connect_2.12:3.4.0')
SPARK_CONNECT_PORT = int(os.getenv('SPARK_CONNECT_PORT', '15002'))
ENABLE_JOB_MONITORING = os.getenv('ENABLE_JOB_MONITORING', '1') != '0'
LISTENER_JAR_PATH = os.path.join(os.path.dirname(__file__), 'listener_2.12.jar')
LISTENER_CLASS_NAME = "ch.cern.sparkconnectlistener.SparkConnectExtensionListener"

SPARK_CLUSTER_NAME = os.getenv('SPARK_CLUSTER_NAME')
