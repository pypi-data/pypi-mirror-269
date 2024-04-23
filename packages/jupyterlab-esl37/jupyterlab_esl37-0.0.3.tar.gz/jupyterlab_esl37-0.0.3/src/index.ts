import {
    JupyterFrontEnd,
    JupyterFrontEndPlugin
} from '@jupyterlab/application';

import {
    IEditorLanguageRegistry
} from '@jupyterlab/codemirror';

import {esl37} from './esl37';

/**
 * Initialization data for the jupyterlab-esl37 extension.
 */
const plugin: JupyterFrontEndPlugin<void> = {
    id: 'jupyterlab-esl37:plugin',
    description: 'ESL37 support for jupyterlab',
    autoStart: true,
    requires: [IEditorLanguageRegistry],
    activate: (app: JupyterFrontEnd, registry: IEditorLanguageRegistry) => {
        console.log('JupyterLab extension jupyterlab-esl37 is activated!');

        registry.addLanguage({
            name: 'ESL37',
            mime: 'text/esl37',
            extensions: ['esl37'],
            support: esl37()
        });
    }
};

export default plugin;
