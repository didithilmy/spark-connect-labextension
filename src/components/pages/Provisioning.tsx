import React, { useEffect } from 'react';
import MoonLoader from 'react-spinners/MoonLoader';
import SparkLogo from '../SparkLogo';
import useStatus from '../../hooks/useStatus';
import useCluster from '../../hooks/useCluster';
import useJupyterLabApp from '../../hooks/useJupyterLabApp';

const Provisioning: React.FC = () => {
  const { mutate } = useStatus();

  useEffect(() => {
    const handle = setInterval(mutate, 1000);
    return () => clearInterval(handle);
  }, []);

  const cluster = useCluster();

  const app = useJupyterLabApp();
  const viewLogs = () => {
    app?.commands.execute('sparkconnect:viewLogs');
  };

  return (
    <div style={{ flex: 1, display: 'flex', flexDirection: 'column' }}>
      <div style={{ flex: 1, display: 'flex', flexDirection: 'column', textAlign: 'center', alignItems: 'center', justifyContent: 'center' }}>
        <SparkLogo />
        <h3 className="jp-SparkConnectExtension-heading">Connecting</h3>
        <p style={{ marginTop: 8 }}>
          Please wait, we're connecting to <b>{cluster?.displayName}</b>.
        </p>
        <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', width: 120, marginTop: 8 }}>
          <MoonLoader size={36} color="var(--jp-ui-font-color1)" />
        </div>
      </div>
      <div style={{ padding: 8 }}>
        <button className="jp-Button jp-mod-styled jp-mod-accept" style={{ width: '100%' }} onClick={viewLogs}>
          View logs
        </button>
      </div>
    </div>
  );
};

export default Provisioning;