export enum ExtensionState {
  CONFIGURING = 'CONFIGURING',
  PROVISIONING = 'PROVISIONING',
  READY = 'READY',
  ERROR = 'ERROR'
}

export interface SparkCluster {
  name: string;
  displayName: string;
}

export interface SparkConfigBundle {
  name: string;
  displayName: string;
  options: Array<{
    name: string;
    value: string;
    concatenate?: string;
  }>;
  clusterFilter?: string[];
}

export interface SparkConfigOption {
  category?: string;
  name: string;
}

export interface ExtensionConfig {
  preselectedClusterName?: string;
  disableClusterSelectionOnPreselected: boolean;
}

export interface SparkClusterStatus {
  status: string;
  clusterName: string;
  port: number;
  configBundles: string[];
  extraConfig: { [key: string]: string };
  sparkOptions: { [key: string]: string };
  extensionConfig: ExtensionConfig;
}

export interface SparkClusterErrorSuggestion {
  pattern: string;
  type: 'error' | 'info' | 'warn';
  message: string;
}
