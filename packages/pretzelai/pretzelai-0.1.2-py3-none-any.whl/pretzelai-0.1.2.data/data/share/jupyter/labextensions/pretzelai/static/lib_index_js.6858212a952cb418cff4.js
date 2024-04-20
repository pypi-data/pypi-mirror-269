"use strict";
(self["webpackChunkpretzelai"] = self["webpackChunkpretzelai"] || []).push([["lib_index_js"],{

/***/ "./lib/index.js":
/*!**********************!*\
  !*** ./lib/index.js ***!
  \**********************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/apputils */ "webpack/sharing/consume/default/@jupyterlab/apputils");
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @jupyterlab/notebook */ "webpack/sharing/consume/default/@jupyterlab/notebook");
/* harmony import */ var _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var monaco_editor__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! monaco-editor */ "webpack/sharing/consume/default/monaco-editor/monaco-editor");
/* harmony import */ var monaco_editor__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(monaco_editor__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var openai__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! openai */ "webpack/sharing/consume/default/openai/openai");
/* harmony import */ var openai__WEBPACK_IMPORTED_MODULE_3___default = /*#__PURE__*/__webpack_require__.n(openai__WEBPACK_IMPORTED_MODULE_3__);
/* harmony import */ var _jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! @jupyterlab/settingregistry */ "webpack/sharing/consume/default/@jupyterlab/settingregistry");
/* harmony import */ var _jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_4___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_4__);





async function calculateHash(input) {
    const encoder = new TextEncoder();
    const data = encoder.encode(input);
    const hashBuffer = await crypto.subtle.digest('SHA-256', data);
    const hashArray = Array.from(new Uint8Array(hashBuffer));
    const hashHex = hashArray.map(b => b.toString(16).padStart(2, '0')).join('');
    return hashHex;
}
const cosineSimilarity = (vecA, vecB) => {
    const dotProduct = vecA.reduce((acc, current, index) => acc + current * vecB[index], 0);
    const magnitudeA = Math.sqrt(vecA.reduce((acc, val) => acc + val * val, 0));
    const magnitudeB = Math.sqrt(vecB.reduce((acc, val) => acc + val * val, 0));
    return dotProduct / (magnitudeA * magnitudeB);
};
const PLUGIN_ID = 'pretzelai:plugin';
const extension = {
    id: PLUGIN_ID,
    autoStart: true,
    requires: [_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__.ICommandPalette, _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_1__.INotebookTracker, _jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_4__.ISettingRegistry],
    activate: async (app, palette, notebookTracker, settingRegistry) => {
        const { commands } = app;
        const command = 'pretzelai:replace-code';
        let apiKey = '';
        let openai;
        // Function to load settings
        function loadSettings() {
            settingRegistry
                .load(extension.id)
                .then(settings => {
                apiKey = settings.get('apiKey').composite || '';
            })
                .catch(reason => {
                console.error('Failed to load settings for Pretzel', reason);
            });
        }
        loadSettings();
        function loadOpenai() {
            if (apiKey) {
                openai = new (openai__WEBPACK_IMPORTED_MODULE_3___default())({
                    apiKey: apiKey,
                    dangerouslyAllowBrowser: true
                });
            }
            else {
                setTimeout(loadOpenai, 1000);
            }
        }
        loadOpenai();
        // Listen for future changes in settings
        settingRegistry.pluginChanged.connect((sender, plugin) => {
            if (plugin === extension.id) {
                loadSettings();
            }
        });
        let embeddings;
        async function createEmbeddings(embeddingsJSON, cells) {
            embeddings = embeddingsJSON;
            const promises = cells.map(cell => {
                return (async () => {
                    const index = embeddings.findIndex(e => e.id === cell.id);
                    if (index !== -1) {
                        const hash = await calculateHash(cell.source);
                        if (hash !== embeddings[index].hash) {
                            try {
                                const response = await openai.embeddings.create({
                                    model: 'text-embedding-3-large',
                                    input: cell.source
                                });
                                embeddings[index] = {
                                    id: cell.id,
                                    source: cell.source,
                                    hash,
                                    embedding: response.data[0].embedding
                                };
                            }
                            catch (error) {
                                console.error('Error generating embedding:', error);
                            }
                        }
                    }
                    else {
                        console.log('creating embedding for: ', cell.id, cell.source);
                        try {
                            const response = await openai.embeddings.create({
                                model: 'text-embedding-3-large',
                                input: cell.source
                            });
                            const hash = await calculateHash(cell.source);
                            embeddings.push({
                                id: cell.id,
                                source: cell.source,
                                hash,
                                embedding: response.data[0].embedding
                            });
                        }
                        catch (error) {
                            console.error('Error generating embedding:', error);
                        }
                    }
                })();
            });
            await Promise.allSettled(promises);
        }
        // Function to print the source of all cells once the notebook is defined
        function getEmbeddings() {
            const notebook = notebookTracker.currentWidget;
            if ((notebook === null || notebook === void 0 ? void 0 : notebook.model) && openai) {
                const currentNotebookPath = notebook.context.path;
                const embeddingsPath = currentNotebookPath.replace('.ipynb', '') + '_embeddings.json';
                app.serviceManager.contents
                    .get(embeddingsPath)
                    .then(file => {
                    try {
                        const embJSON = JSON.parse(file.content);
                        createEmbeddings(embJSON, notebook.model.sharedModel.cells).then(() => {
                            app.serviceManager.contents.save(embeddingsPath, {
                                type: 'file',
                                format: 'text',
                                content: JSON.stringify(embeddings)
                            });
                        });
                    }
                    catch (error) {
                        console.error('Error parsing embeddings JSON:', error);
                    }
                })
                    .catch(async (error) => {
                    createEmbeddings([], notebook.model.sharedModel.cells).then(() => {
                        app.serviceManager.contents.save(embeddingsPath, {
                            type: 'file',
                            format: 'text',
                            content: JSON.stringify(embeddings)
                        });
                    });
                });
            }
            else {
                setTimeout(getEmbeddings, 1000);
            }
        }
        getEmbeddings();
        async function getVariableValue(variableName) {
            var _a;
            const notebook = notebookTracker.currentWidget;
            if (notebook && ((_a = notebook.sessionContext.session) === null || _a === void 0 ? void 0 : _a.kernel)) {
                const kernel = notebook.sessionContext.session.kernel;
                try {
                    // get the type - if dataframe, we get columns
                    // if other, we get the string representation
                    const executeRequest = kernel.requestExecute({
                        code: `print(${variableName})`
                    });
                    let variableValue = null;
                    // Registering a message hook to intercept messages
                    kernel.registerMessageHook(executeRequest.msg.header.msg_id, (msg) => {
                        if (msg.header.msg_type === 'stream' &&
                            // @ts-expect-error tserror
                            msg.content.name === 'stdout') {
                            // @ts-expect-error tserror
                            variableValue = msg.content.text.trim();
                        }
                        return true;
                    });
                    // Await the completion of the execute request
                    const reply = await executeRequest.done;
                    if (reply && reply.content.status === 'ok') {
                        return variableValue;
                    }
                    else {
                        console.error('Failed to retrieve variable value');
                        return null;
                    }
                }
                catch (error) {
                    console.error('Error retrieving variable value:', error);
                    return null;
                }
            }
            else {
                console.error('No active kernel found');
                return null;
            }
        }
        commands.addCommand(command, {
            label: 'Replace Cell Code',
            execute: () => {
                const activeCell = notebookTracker.activeCell;
                if (activeCell) {
                    // Cmd K twice should toggle the box
                    // Check if an existing div with ID pretzelParentContainerAI exists on activeCell.node
                    const existingDiv = activeCell.node.querySelector('#pretzelParentContainerAI');
                    if (existingDiv) {
                        // If so, delete that div
                        existingDiv.remove();
                        // Switch focus back to the Jupyter cell
                        activeCell.editor.focus();
                        return;
                    }
                    const oldCode = activeCell.model.sharedModel.source;
                    // Create a parent container for all dynamically created elements
                    const parentContainer = document.createElement('div');
                    parentContainer.id = 'pretzelParentContainerAI';
                    activeCell.node.appendChild(parentContainer);
                    // Create an input field and append it below the cell
                    const inputContainer = document.createElement('div');
                    inputContainer.style.marginTop = '10px';
                    inputContainer.style.marginLeft = '70px';
                    inputContainer.style.display = 'flex';
                    inputContainer.style.flexDirection = 'column';
                    parentContainer.appendChild(inputContainer);
                    const inputField = document.createElement('textarea');
                    inputField.placeholder = 'Enter your text';
                    inputField.style.width = '100%';
                    inputField.style.height = '100px';
                    inputContainer.appendChild(inputField);
                    inputField.addEventListener('keydown', event => {
                        if (event.key === 'Escape') {
                            // TODO: this doesn't work - the Escape key isn't being captured
                            // but every other key press is being captured
                            event.preventDefault(); // Prevent any default behavior
                            // Shift focus back to the editor of the active cell
                            const activeCell = notebookTracker.activeCell;
                            if (activeCell && activeCell.editor) {
                                activeCell.editor.focus(); // Focus the editor of the active cell
                            }
                        }
                    });
                    const inputFieldButtonsContainer = document.createElement('div');
                    inputFieldButtonsContainer.style.marginTop = '10px';
                    inputFieldButtonsContainer.style.display = 'flex';
                    inputFieldButtonsContainer.style.flexDirection = 'row';
                    inputContainer.appendChild(inputFieldButtonsContainer);
                    inputField.focus();
                    const submitButton = document.createElement('button');
                    submitButton.textContent = 'Submit';
                    submitButton.style.backgroundColor = 'lightblue';
                    submitButton.style.borderRadius = '5px';
                    submitButton.style.border = '1px solid darkblue';
                    submitButton.style.maxWidth = '100px';
                    submitButton.style.minHeight = '25px';
                    submitButton.style.marginTop = '10px';
                    submitButton.style.marginRight = '10px';
                    inputFieldButtonsContainer.appendChild(submitButton);
                    // write code to add a button the removed the inputField and submitButton
                    const removeButton = document.createElement('button');
                    removeButton.textContent = 'Remove';
                    removeButton.style.backgroundColor = 'lightcoral';
                    removeButton.style.borderRadius = '5px';
                    removeButton.style.border = '1px solid darkred';
                    removeButton.style.maxWidth = '100px';
                    removeButton.style.minHeight = '25px';
                    removeButton.style.marginTop = '10px';
                    inputFieldButtonsContainer.appendChild(removeButton);
                    removeButton.addEventListener('click', () => {
                        activeCell.node.removeChild(parentContainer);
                    });
                    const handleAccept = async () => {
                        let userInput = inputField.value;
                        if (userInput !== '') {
                            parentContainer.removeChild(inputContainer);
                            let diffEditor = null;
                            const renderEditor = (gen) => {
                                try {
                                    if (!diffEditor) {
                                        createEditorComponents();
                                    }
                                    const modifiedModel = diffEditor.getModel().modified;
                                    const endLineNumber = modifiedModel.getLineCount();
                                    const endColumn = modifiedModel.getLineMaxColumn(endLineNumber);
                                    modifiedModel.applyEdits([
                                        {
                                            range: new monaco_editor__WEBPACK_IMPORTED_MODULE_2__.Range(endLineNumber, endColumn, endLineNumber, endColumn),
                                            text: gen,
                                            forceMoveMarkers: true
                                        }
                                    ]);
                                }
                                catch (error) {
                                    console.log('Error rendering editor:', error);
                                }
                            };
                            const createEditorComponents = () => {
                                // generate the editor components
                                // first, top level container to hold all diff related items
                                const diffContainer = document.createElement('div');
                                diffContainer.style.marginTop = '10px';
                                diffContainer.style.display = 'flex';
                                diffContainer.style.flexDirection = 'column';
                                parentContainer.appendChild(diffContainer);
                                // next, container to hold the diff editor
                                const diffEditorContainer = document.createElement('div');
                                diffEditorContainer.style.height = '200px';
                                diffContainer.appendChild(diffEditorContainer);
                                // finally, the diff editor itself
                                const currentTheme = document.body.getAttribute('data-jp-theme-light') === 'true'
                                    ? 'vs'
                                    : 'vs-dark';
                                diffEditor = monaco_editor__WEBPACK_IMPORTED_MODULE_2__.editor.createDiffEditor(diffEditorContainer, {
                                    readOnly: true,
                                    theme: currentTheme
                                });
                                diffEditor.setModel({
                                    original: monaco_editor__WEBPACK_IMPORTED_MODULE_2__.editor.createModel(oldCode, 'python'),
                                    modified: monaco_editor__WEBPACK_IMPORTED_MODULE_2__.editor.createModel('', 'python')
                                });
                                const diffButtonsContainer = document.createElement('div');
                                diffButtonsContainer.style.marginTop = '10px';
                                diffButtonsContainer.style.marginLeft = '70px';
                                diffButtonsContainer.style.display = 'flex';
                                diffButtonsContainer.style.flexDirection = 'row';
                                diffContainer.appendChild(diffButtonsContainer);
                                // Create "Accept" and "Reject" buttons
                                const acceptButton = document.createElement('button');
                                acceptButton.textContent = 'Accept';
                                acceptButton.style.backgroundColor = 'lightblue';
                                acceptButton.style.borderRadius = '5px';
                                acceptButton.style.border = '1px solid darkblue';
                                acceptButton.style.maxWidth = '100px';
                                acceptButton.style.minHeight = '25px';
                                acceptButton.style.marginRight = '10px';
                                acceptButton.addEventListener('click', () => {
                                    const modifiedCode = diffEditor
                                        .getModel()
                                        .modified.getValue();
                                    activeCell.model.sharedModel.source = modifiedCode;
                                    commands.execute('notebook:run-cell');
                                    activeCell.node.removeChild(parentContainer);
                                });
                                diffButtonsContainer.appendChild(acceptButton);
                                const rejectButton = document.createElement('button');
                                rejectButton.textContent = 'Reject';
                                rejectButton.style.backgroundColor = 'lightblue';
                                rejectButton.style.borderRadius = '5px';
                                rejectButton.style.border = '1px solid darkblue';
                                rejectButton.style.maxWidth = '100px';
                                rejectButton.style.minHeight = '25px';
                                rejectButton.style.marginRight = '10px';
                                rejectButton.addEventListener('click', () => {
                                    activeCell.node.removeChild(parentContainer);
                                    activeCell.model.sharedModel.source = oldCode;
                                });
                                diffButtonsContainer.appendChild(rejectButton);
                                const editPromptButton = document.createElement('button');
                                editPromptButton.textContent = 'Edit Prompt';
                                editPromptButton.style.backgroundColor = 'lightblue';
                                editPromptButton.style.borderRadius = '5px';
                                editPromptButton.style.border = '1px solid darkblue';
                                editPromptButton.style.maxWidth = '100px';
                                editPromptButton.style.minHeight = '25px';
                                editPromptButton.style.marginRight = '10px';
                                editPromptButton.addEventListener('click', () => {
                                    parentContainer.removeChild(diffContainer);
                                    parentContainer.appendChild(inputContainer);
                                    diffEditor = null;
                                });
                                diffButtonsContainer.appendChild(editPromptButton);
                                // Handle Enter key press to trigger accept on accept/reject buttons
                                diffButtonsContainer.addEventListener('keydown', event => {
                                    if (event.key === 'Enter') {
                                        event.preventDefault();
                                        const activeElement = document.activeElement;
                                        if (activeElement === acceptButton) {
                                            acceptButton.click();
                                        }
                                        else if (activeElement === rejectButton) {
                                            rejectButton.click();
                                        }
                                    }
                                });
                                // Handle Escape key press to trigger reject on accept/reject buttons
                                diffButtonsContainer.addEventListener('keydown', event => {
                                    if (event.key === 'Escape') {
                                        event.preventDefault();
                                        rejectButton.click();
                                    }
                                });
                            };
                            // TODO: Use a better way to determine which source is used
                            const isLocalhost = window.location.hostname === 'localhost';
                            const variablePattern = /@(\w+)/g;
                            let match;
                            let modifiedUserInput = userInput;
                            while ((match = variablePattern.exec(userInput)) !== null) {
                                try {
                                    const variableName = match[1];
                                    // get value of var using the getVariableValue function
                                    const variableType = await getVariableValue(`type(${variableName})`);
                                    // check if variableType is dataframe
                                    // if it is, get columns and add to modifiedUserInput
                                    if (variableType === null || variableType === void 0 ? void 0 : variableType.includes('DataFrame')) {
                                        const variableColumns = await getVariableValue(`${variableName}.columns`);
                                        modifiedUserInput += `\n${variableName} is a dataframe with the following columns: ${variableColumns}\n`;
                                    }
                                    else if (variableType) {
                                        const variableValue = await getVariableValue(variableName);
                                        modifiedUserInput += `\nPrinting ${variableName} in Python returns the string ${variableValue}\n`;
                                    }
                                }
                                catch (error) {
                                    console.error(`Error accessing variable ${match[1]}:`, error);
                                }
                            }
                            userInput = modifiedUserInput;
                            if (isLocalhost) {
                                try {
                                    const complete = async () => {
                                        var _a, _b;
                                        const response = await openai.embeddings.create({
                                            model: 'text-embedding-3-large',
                                            input: userInput
                                        });
                                        const userInputEmbedding = response.data[0].embedding;
                                        const similarities = embeddings.map(embedding => cosineSimilarity(embedding.embedding, userInputEmbedding));
                                        const topThreeSimilarities = similarities
                                            .map((value, index) => ({ value, index }))
                                            .sort((a, b) => b.value - a.value)
                                            .slice(0, 3)
                                            .map(e => embeddings[e.index].source);
                                        const prompt = `Write python code to do
                    """
                    ${userInput}
                    """
                    The previous code is
                    """${oldCode}"""
                    Related code cells are:
                    """
                    ${topThreeSimilarities.join('\n"""\n')}
                    """
                    Return ONLY executable python code, no backticks`;
                                        const stream = await openai.chat.completions.create({
                                            model: 'gpt-4-turbo-preview',
                                            messages: [
                                                {
                                                    role: 'user',
                                                    content: prompt
                                                }
                                            ],
                                            stream: true
                                        });
                                        for await (const chunk of stream) {
                                            renderEditor(((_b = (_a = chunk.choices[0]) === null || _a === void 0 ? void 0 : _a.delta) === null || _b === void 0 ? void 0 : _b.content) || '');
                                        }
                                    };
                                    complete();
                                }
                                catch (error) {
                                    activeCell.node.removeChild(parentContainer);
                                }
                            }
                            else {
                                const options = {
                                    method: 'POST',
                                    headers: {
                                        'Content-Type': 'application/json'
                                    },
                                    body: JSON.stringify({
                                        oldCode,
                                        userInput
                                    })
                                };
                                try {
                                    const response = await fetch('https://q8qeei2tn4.execute-api.us-west-1.amazonaws.com/default/pretzel_notebook', options);
                                    const data = await response.json();
                                    const gen = data.message;
                                    renderEditor(gen);
                                }
                                catch (error) {
                                    activeCell.model.sharedModel.source = `# Error: ${error}\n${oldCode}`;
                                    activeCell.node.removeChild(parentContainer);
                                }
                            }
                        }
                    };
                    // Handle Enter key press to trigger submit
                    inputField.addEventListener('keydown', event => {
                        if (event.key === 'Enter') {
                            event.preventDefault();
                            handleAccept();
                        }
                    });
                    // Handle submit button click to trigger accept
                    submitButton.addEventListener('click', handleAccept);
                }
            }
        });
        const category = 'Cell Operations';
        palette.addItem({ command, category });
        app.commands.addKeyBinding({
            command,
            keys: ['Accel K'],
            selector: '.jp-Notebook'
        });
    }
};
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (extension);


/***/ })

}]);
//# sourceMappingURL=lib_index_js.6858212a952cb418cff4.js.map