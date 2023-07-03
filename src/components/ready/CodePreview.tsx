import React, { useState } from 'react';
import { copyIcon, addIcon } from '@jupyterlab/ui-components';
import { NotebookActions } from '@jupyterlab/notebook';
import CodeMirror from '@uiw/react-codemirror';
import { jupyterTheme } from '@jupyterlab/codemirror';
import { python } from '@codemirror/lang-python';
import useStatus from '../../hooks/useStatus';
import { UIStore } from '../../store/UIStore';

const CODE = `
%load_ext spark_connect_labextension.kernelextension
spark = get_spark_session()
`.trim();

export default function CodePreview() {
  const [copied, setCopied] = useState<boolean>(false);
  const { data } = useStatus();
  const port = data?.port ?? 15002;
  const code = CODE.replace('{PORT}', `${port}`);

  const activeNotebookPanel = UIStore.useState(s => s.activeNotebookPanel);
  const addCellToNotebook = () => {
    if (activeNotebookPanel) {
      NotebookActions.insertBelow(activeNotebookPanel.content);
      setTimeout(() => {
        activeNotebookPanel.content.activeCell?.editor?.model.sharedModel.setSource(CODE);
      }, 10);
    }
  };

  return (
    <div>
      <div style={{ border: '1px solid var(--jp-border-color2)' }}>
        <CodeMirror
          value={code}
          height="200px"
          extensions={[python()]}
          theme={jupyterTheme}
          editable={false}
          basicSetup={{
            highlightActiveLine: false,
            lineNumbers: false,
            highlightActiveLineGutter: false
          }}
        />
      </div>
      <div style={{ marginTop: 4, display: 'flex', flexDirection: 'row', justifyContent: 'end' }}>
        <button
          className="jp-ToolbarButtonComponent jp-mod-minimal jp-Button"
          onClick={() => {
            navigator.clipboard.writeText(CODE);
            setCopied(true);
            setTimeout(() => setCopied(false), 2000);
          }}
        >
          <copyIcon.react tag="span" width={16} height={16} marginTop={4} />{' '}
          <span className="jp-ToolbarButtonComponent-label" style={{ color: 'var(--jp-ui-font-color2)' }}>
            {copied ? 'Copied!' : 'Copy'}
          </span>
        </button>
        {!!activeNotebookPanel && (
          <button className="jp-ToolbarButtonComponent jp-mod-minimal jp-Button" onClick={addCellToNotebook}>
            <addIcon.react tag="span" width={16} height={16} marginTop={4} />{' '}
            <span className="jp-ToolbarButtonComponent-label" style={{ color: 'var(--jp-ui-font-color2)' }}>
              Add to Notebook
            </span>
          </button>
        )}
      </div>
    </div>
  );
}
