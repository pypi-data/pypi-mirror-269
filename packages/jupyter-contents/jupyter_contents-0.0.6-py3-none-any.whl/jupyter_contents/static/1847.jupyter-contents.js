"use strict";(self.webpackChunk_datalayer_jupyter_contents=self.webpackChunk_datalayer_jupyter_contents||[]).push([[1847],{71847:(e,t,n)=>{n.r(t),n.d(t,{Commands:()=>pe,default:()=>Ee,tabSpaceStatus:()=>be});var o=n(44041),i=n(2245),r=n(99190),a=n(67335),d=n(22290),s=n(35884),l=n(68337),c=n(31786),u=n(58280),m=n(11097),g=n(45331),h=n(29246),p=n(21110),f=n(68471),v=n(18168),y=n(55616),C=n(56769);function _(e){const t=(e.translator||v.Sr).load("jupyterlab"),n="number"==typeof e.tabSpace?t.__("Spaces"):t.__("Tab Indent");return C.createElement(f.Jy,{onClick:e.handleClick,source:"number"==typeof e.tabSpace?`${n}: ${e.tabSpace}`:n,title:t.__("Change the indentation…")})}class b extends y.UB{constructor(e){super(new b.Model),this._popup=null,this._menu=e.menu,this.translator=e.translator||v.Sr,this.addClass("jp-mod-highlighted")}render(){var e;if(null===(e=this.model)||void 0===e?void 0:e.indentUnit){const e="Tab"===this.model.indentUnit?null:parseInt(this.model.indentUnit,10);return C.createElement(_,{tabSpace:e,handleClick:()=>this._handleClick(),translator:this.translator})}return null}_handleClick(){const e=this._menu;this._popup&&this._popup.dispose(),e.aboutToClose.connect(this._menuClosed,this),this._popup=(0,f.U)({body:e,anchor:this,align:"right"}),e.update()}_menuClosed(){this.removeClass("jp-mod-clicked")}}!function(e){class t extends y.I_{get indentUnit(){return this._indentUnit}set indentUnit(e){e!==this._indentUnit&&(this._indentUnit=e,this.stateChanged.emit())}}e.Model=t}(b||(b={}));var w=n(71514),x=n(87104),k=n(48860),T=n(77727),E=n(47963),M=n(92279);class S extends M.$L{constructor(e){super(),this._ready=new E.PromiseDelegate,this.addClass("jp-FileEditor");const t=this._context=e.context;this._mimeTypeService=e.mimeTypeService;const n=this._editorWidget=new x.A({factory:e.factory,model:t.model,editorOptions:{config:S.defaultEditorConfig}});this._editorWidget.addClass("jp-FileEditorCodeWrapper"),this._editorWidget.node.dataset.jpCodeRunner="true",this._editorWidget.node.dataset.jpUndoer="true",this.editor=n.editor,this.model=n.model,t.ready.then((()=>{this._onContextReady()})),this._onPathChanged(),t.pathChanged.connect(this._onPathChanged,this),(this.layout=new M.Qb).addWidget(n)}get context(){return this._context}get ready(){return this._ready.promise}handleEvent(e){this.model&&"mousedown"===e.type&&this._ensureFocus()}onAfterAttach(e){super.onAfterAttach(e),this.node.addEventListener("mousedown",this)}onBeforeDetach(e){this.node.removeEventListener("mousedown",this)}onActivateRequest(e){this._ensureFocus()}_ensureFocus(){this.editor.hasFocus()||this.editor.focus()}_onContextReady(){this.isDisposed||(this.editor.clearHistory(),this._ready.resolve(void 0))}_onPathChanged(){const e=this.editor,t=this._context.localPath;e.model.mimeType=this._mimeTypeService.getMimeTypeByFilePath(t)}}!function(e){e.defaultEditorConfig={lineNumbers:!0,scrollPastEnd:!0}}(S||(S={}));class W extends k.Ry{async setFragment(e){const t=e.split("=");if("#line"!==t[0])return;const n=t[1];let o;return o=n.includes(",")?n.split(",")[0]||"0":n,this.context.ready.then((()=>{const e={line:parseInt(o,10),column:0};this.content.editor.setCursorPosition(e),this.content.editor.revealPosition(e)}))}}class N extends k.GA{constructor(e){super(e.factoryOptions),this._services=e.editorServices}createNewWidget(e){const t=this._services.factoryService.newDocumentEditor,n=new S({factory:e=>t(e),context:e,mimeTypeService:this._services.mimeTypeService});return n.title.icon=T._6,new W({content:n,context:e})}}class P extends c.su{constructor(e){super(),this.widget=e,this._searchActive=!1}get isReadOnly(){return this.editor.getOption("readOnly")}get replaceOptionsSupport(){return{preserveCase:!0}}get editor(){return this.widget.content.editor}get model(){return this.widget.content.model}async startQuery(e,t){this._searchActive=!0,await super.startQuery(e,t),await this.highlightNext(!0,{from:"selection-start",scroll:!1,select:!1})}async endQuery(){this._searchActive=!1,await super.endQuery()}async onSharedModelChanged(e,t){if(this._searchActive)return super.onSharedModelChanged(e,t)}static createNew(e,t){return new P(e)}static isApplicable(e){return e instanceof w.k&&e.content instanceof S&&e.content.editor instanceof c.sI}getInitialQuery(){const e=this.editor;return e.state.sliceDoc(e.state.selection.main.from,e.state.selection.main.to)}}var A=n(96734),I=n(3053),L=n(51840);class B extends L.w{createNew(e,t){const n=super.createNew(e,t),o=(t,n)=>{n&&e.content.editor.setCursorPosition({line:n.line,column:0})};return n.activeHeadingChanged.connect(o),e.disposed.connect((()=>{n.activeHeadingChanged.disconnect(o)})),n}}const F={part:1,chapter:1,section:1,subsection:2,subsubsection:3,paragraph:4,subparagraph:5},O=/^\s*\\(section|subsection|subsubsection){(.+)}/;class j extends A.U{get documentType(){return"latex"}get supportedOptions(){return["maximalDepth","numberHeaders"]}getHeadings(){if(!this.isActive)return Promise.resolve(null);const e=this.widget.content.model.sharedModel.getSource().split("\n"),t=new Array;let n=t.length;const o=new Array;for(let i=0;i<e.length;i++){const r=e[i].match(O);if(r){const e=F[r[1]];if(e<=this.configuration.maximalDepth){const a=I.Gn(e,n,t,{...this.configuration,baseNumbering:1,numberingH1:!0});n=e,o.push({text:r[2],prefix:a,level:e,line:i})}}}return Promise.resolve(o)}}class R extends B{isApplicable(e){var t,n;if(super.isApplicable(e)){let o=null===(n=null===(t=e.content)||void 0===t?void 0:t.model)||void 0===n?void 0:n.mimeType;return o&&("text/x-latex"===o||"text/x-stex"===o)}return!1}_createNew(e,t){return new j(e,t)}}var z=n(83331);class U extends A.U{get documentType(){return"markdown"}getHeadings(){if(!this.isActive)return Promise.resolve(null);const e=this.widget.content.model.sharedModel.getSource(),t=I.tF(z.o3(e),{...this.configuration,numberHeaders:!1});return Promise.resolve(t)}}class $ extends B{isApplicable(e){var t,n;if(super.isApplicable(e)){let o=null===(n=null===(t=e.content)||void 0===t?void 0:t.model)||void 0===n?void 0:n.mimeType;return o&&z.kb(o)}return!1}_createNew(e,t){return new U(e,t)}}let D;try{D=new RegExp("^\\s*(class |def |from |import )","d")}catch(e){D=new RegExp("^\\s*(class |def |from |import )")}class V extends A.U{get documentType(){return"python"}async getHeadings(){if(!this.isActive)return Promise.resolve(null);const e=this.widget.content.model.sharedModel.getSource().split("\n");let t=new Array,o=!1,i=1,r=-1;for(const a of e){let e;if(r++,D.flags.includes("d"))e=D.exec(a);else{const{default:t}=await n.e(622).then(n.t.bind(n,40622,23));e=t(D,a)}if(e){const[n]=e.indices[1];1===i&&n>0&&(i=n);const d=["from ","import "].includes(e[1]);if(d&&o)continue;o=d;const s=1+n/i;if(s>this.configuration.maximalDepth)continue;t.push({text:a.slice(n),level:s,line:r})}}return Promise.resolve(t)}}class H extends B{isApplicable(e){var t,n;if(super.isApplicable(e)){let o=null===(n=null===(t=e.content)||void 0===t?void 0:t.model)||void 0===n?void 0:n.mimeType;return o&&("application/x-python-code"===o||"text/x-python"===o)}return!1}_createNew(e,t){return new V(e,t)}}var q=n(88132),K=n(73568),Q=n(63060);class G extends K.s{constructor(e,t){const{docRegistry:n,...o}=t;super(e,o),this._readyDelegate=new E.PromiseDelegate,this.editor=e.content,this._docRegistry=n,this._virtualEditor=Object.freeze({getEditor:()=>this.editor.editor,ready:()=>Promise.resolve(this.editor.editor),reveal:()=>Promise.resolve(this.editor.editor)}),Promise.all([this.editor.context.ready,this.connectionManager.ready]).then((async()=>{await this.initOnceReady(),this._readyDelegate.resolve()})).catch(console.error)}get ready(){return this._readyDelegate.promise}get documentPath(){return this.widget.context.path}get mimeType(){var e;const t=this.editor.model.mimeType,n=Array.isArray(t)?null!==(e=t[0])&&void 0!==e?e:q.N.defaultMimeType:t,o=this.editor.context.contentsModel;return n!=q.N.defaultMimeType?n:o?this._docRegistry.getFileTypeForModel(o).mimeTypes[0]:n}get languageFileExtension(){let e=this.documentPath.split(".");return e[e.length-1]}get ceEditor(){return this.editor.editor}get activeEditor(){return this._virtualEditor}get wrapperElement(){return this.widget.node}get path(){return this.widget.context.path}get editors(){var e,t;return[{ceEditor:this._virtualEditor,type:"code",value:null!==(t=null===(e=this.editor)||void 0===e?void 0:e.model.sharedModel.getSource())&&void 0!==t?t:""}]}dispose(){this.isDisposed||(this.editor.model.mimeTypeChanged.disconnect(this.reloadConnection),super.dispose())}createVirtualDocument(){return new Q.lr({language:this.language,foreignCodeExtractors:this.options.foreignCodeExtractorsManager,path:this.documentPath,fileExtension:this.languageFileExtension,standalone:!0,hasLspSupportedFile:!0})}getEditorIndexAt(e){return 0}getEditorIndex(e){return 0}getEditorWrapper(e){return this.wrapperElement}async initOnceReady(){this.initVirtual(),await this.connectDocument(this.virtualDocument,!1),this.editor.model.mimeTypeChanged.connect(this.reloadConnection,this)}}var J=n(47415),Y=n(73748),X=n(43043),Z=n(35909),ee=n(80882),te=n(56276),ne=n(36e3),oe=n(46931),ie=n(45671),re=n(55654),ae=n(21488),de=n(46638);class se extends M.$L{constructor(e){var t;super(),this.model=e.model;const n=new x.A({factory:e.factory,model:this.model,editorOptions:{...e.editorOptions,config:{...null===(t=e.editorOptions)||void 0===t?void 0:t.config,readOnly:!0}}});this.editor=n.editor,(this.layout=new M.Qb).addWidget(n)}static createCodeViewer(e){const{content:t,mimeType:n,...o}=e,i=new de.p.Model({mimeType:n});i.sharedModel.setSource(t);const r=new se({...o,model:i});return r.disposed.connect((()=>{i.dispose()})),r}get content(){return this.model.sharedModel.getSource()}get mimeType(){return this.model.mimeType}}var le=n(48425),ce=n(55343);const ue="notebook:toggle-autoclosing-brackets",me="console:toggle-autoclosing-brackets";var ge;!function(e){e.createNew="fileeditor:create-new",e.createNewMarkdown="fileeditor:create-new-markdown-file",e.changeFontSize="fileeditor:change-font-size",e.lineNumbers="fileeditor:toggle-line-numbers",e.currentLineNumbers="fileeditor:toggle-current-line-numbers",e.lineWrap="fileeditor:toggle-line-wrap",e.currentLineWrap="fileeditor:toggle-current-line-wrap",e.changeTabs="fileeditor:change-tabs",e.matchBrackets="fileeditor:toggle-match-brackets",e.currentMatchBrackets="fileeditor:toggle-current-match-brackets",e.autoClosingBrackets="fileeditor:toggle-autoclosing-brackets",e.autoClosingBracketsUniversal="fileeditor:toggle-autoclosing-brackets-universal",e.createConsole="fileeditor:create-console",e.replaceSelection="fileeditor:replace-selection",e.restartConsole="fileeditor:restart-console",e.runCode="fileeditor:run-code",e.runAllCode="fileeditor:run-all",e.markdownPreview="fileeditor:markdown-preview",e.undo="fileeditor:undo",e.redo="fileeditor:redo",e.cut="fileeditor:cut",e.copy="fileeditor:copy",e.paste="fileeditor:paste",e.selectAll="fileeditor:select-all",e.invokeCompleter="completer:invoke-file",e.selectCompleter="completer:select-file",e.openCodeViewer="code-viewer:open",e.changeTheme="fileeditor:change-theme",e.changeLanguage="fileeditor:change-language",e.find="fileeditor:find",e.goToLine="fileeditor:go-to-line"}(ge||(ge={}));const he="Editor";var pe;!function(e){let t={},n=!0;function o(e){e.editor.setOptions({...t,scrollPastEnd:n})}function i(e){const t=e.getSelection(),{start:n,end:o}=t;return n.column!==o.column||n.line!==o.line}function r(e){const t=e.getSelection(),n=e.getOffsetAt(t.start),o=e.getOffsetAt(t.end);return e.model.sharedModel.getSource().substring(n,o)}async function a(e,t,n="txt"){const o=await e.execute("docmanager:new-untitled",{path:t,type:"file",ext:n});if(null!=o){const t=await e.execute("docmanager:open",{path:o.path,factory:he});return t.isUntitled=!0,t}}function d(e,t){e.add({command:ge.createNew,category:t.__("Other"),rank:1})}function s(e,t){e.add({command:ge.createNewMarkdown,category:t.__("Other"),rank:2})}function l(e,t){const n=t.__("Text Editor"),o=ge.changeTabs;e.addItem({command:o,args:{size:4},category:n});for(const t of[1,2,4,8]){const i={size:t};e.addItem({command:o,args:i,category:n})}}function c(e,t){const n=t.__("Text Editor");e.addItem({command:ge.createNew,args:{isPalette:!0},category:n})}function u(e,t){const n=t.__("Text Editor");e.addItem({command:ge.createNewMarkdown,args:{isPalette:!0},category:n})}function m(e,t){const n=t.__("Text Editor"),o=ge.changeFontSize;let i={delta:1};e.addItem({command:o,args:i,category:n}),i={delta:-1},e.addItem({command:o,args:i,category:n})}function g(e,t,n){const o=e=>n()&&e.context&&!!t.find((t=>{var n;return(null===(n=t.sessionContext.session)||void 0===n?void 0:n.path)===e.context.path}));e.runMenu.codeRunners.restart.add({id:ge.restartConsole,isEnabled:o}),e.runMenu.codeRunners.run.add({id:ge.runCode,isEnabled:o}),e.runMenu.codeRunners.runAll.add({id:ge.runAllCode,isEnabled:o})}e.updateSettings=function(e,o){var i;t=null!==(i=e.get("editorConfig").composite)&&void 0!==i?i:{},n=e.get("scrollPasteEnd").composite,o.notifyCommandChanged(ge.lineNumbers),o.notifyCommandChanged(ge.currentLineNumbers),o.notifyCommandChanged(ge.lineWrap),o.notifyCommandChanged(ge.currentLineWrap),o.notifyCommandChanged(ge.changeTabs),o.notifyCommandChanged(ge.matchBrackets),o.notifyCommandChanged(ge.currentMatchBrackets),o.notifyCommandChanged(ge.autoClosingBrackets),o.notifyCommandChanged(ge.changeLanguage)},e.updateTracker=function(e){e.forEach((e=>{o(e.content)}))},e.updateWidget=o,e.addCommands=function(e,n,o,d,s,l,c,u,m,g,h){e.addCommand(ge.changeFontSize,{execute:e=>{var o;const i=Number(e.delta);if(Number.isNaN(i))return void console.error(`${ge.changeFontSize}: delta arg must be a number`);const r=window.getComputedStyle(document.documentElement),a=parseInt(r.getPropertyValue("--jp-code-font-size"),10),s=(null!==(o=t.customStyles.fontSize)&&void 0!==o?o:u.baseConfiguration.customStyles.fontSize)||a;return t.fontSize=s+i,n.set(d,"editorConfig",t).catch((e=>{console.error(`Failed to set ${d}: ${e.message}`)}))},label:e=>{const t=Number(e.delta);return Number.isNaN(t)&&console.error(`${ge.changeFontSize}: delta arg must be a number`),t>0?e.isMenu?o.__("Increase Text Editor Font Size"):o.__("Increase Font Size"):e.isMenu?o.__("Decrease Text Editor Font Size"):o.__("Decrease Font Size")}}),e.addCommand(ge.lineNumbers,{execute:async()=>{var e;t.lineNumbers=!(null!==(e=t.lineNumbers)&&void 0!==e?e:u.baseConfiguration.lineNumbers);try{return await n.set(d,"editorConfig",t)}catch(e){console.error(`Failed to set ${d}: ${e.message}`)}},isEnabled:s,isToggled:()=>{var e;return null!==(e=t.lineNumbers)&&void 0!==e?e:u.baseConfiguration.lineNumbers},label:o.__("Show Line Numbers")}),e.addCommand(ge.currentLineNumbers,{label:o.__("Show Line Numbers"),caption:o.__("Show the line numbers for the current file."),execute:()=>{const e=l.currentWidget;if(!e)return;const t=!e.content.editor.getOption("lineNumbers");e.content.editor.setOption("lineNumbers",t)},isEnabled:s,isToggled:()=>{var e;const t=l.currentWidget;return null!==(e=null==t?void 0:t.content.editor.getOption("lineNumbers"))&&void 0!==e&&e}}),e.addCommand(ge.lineWrap,{execute:async e=>{var o;t.lineWrap=null!==(o=e.mode)&&void 0!==o&&o;try{return await n.set(d,"editorConfig",t)}catch(e){console.error(`Failed to set ${d}: ${e.message}`)}},isEnabled:s,isToggled:e=>{var n,o;return(null!==(n=e.mode)&&void 0!==n&&n)===(null!==(o=t.lineWrap)&&void 0!==o?o:u.baseConfiguration.lineWrap)},label:o.__("Word Wrap")}),e.addCommand(ge.currentLineWrap,{label:o.__("Wrap Words"),caption:o.__("Wrap words for the current file."),execute:()=>{const e=l.currentWidget;if(!e)return;const t=e.content.editor.getOption("lineWrap");e.content.editor.setOption("lineWrap",!t)},isEnabled:s,isToggled:()=>{var e;const t=l.currentWidget;return null!==(e=null==t?void 0:t.content.editor.getOption("lineWrap"))&&void 0!==e&&e}}),e.addCommand(ge.changeTabs,{label:e=>{var t;return e.size?o._p("v4","Spaces: %1",null!==(t=e.size)&&void 0!==t?t:""):o.__("Indent with Tab")},execute:async e=>{var o;t.indentUnit=void 0!==e.size?(null!==(o=e.size)&&void 0!==o?o:"4").toString():"Tab";try{return await n.set(d,"editorConfig",t)}catch(e){console.error(`Failed to set ${d}: ${e.message}`)}},isToggled:e=>{var n;const o=null!==(n=t.indentUnit)&&void 0!==n?n:u.baseConfiguration.indentUnit;return e.size?e.size===o:"Tab"==o}}),e.addCommand(ge.matchBrackets,{execute:async()=>{var e;t.matchBrackets=!(null!==(e=t.matchBrackets)&&void 0!==e?e:u.baseConfiguration.matchBrackets);try{return await n.set(d,"editorConfig",t)}catch(e){console.error(`Failed to set ${d}: ${e.message}`)}},label:o.__("Match Brackets"),isEnabled:s,isToggled:()=>{var e;return null!==(e=t.matchBrackets)&&void 0!==e?e:u.baseConfiguration.matchBrackets}}),e.addCommand(ge.currentMatchBrackets,{label:o.__("Match Brackets"),caption:o.__("Change match brackets for the current file."),execute:()=>{const e=l.currentWidget;if(!e)return;const t=!e.content.editor.getOption("matchBrackets");e.content.editor.setOption("matchBrackets",t)},isEnabled:s,isToggled:()=>{var e;const t=l.currentWidget;return null!==(e=null==t?void 0:t.content.editor.getOption("matchBrackets"))&&void 0!==e&&e}}),e.addCommand(ge.autoClosingBrackets,{execute:async e=>{var o,i;t.autoClosingBrackets=!!(null!==(o=e.force)&&void 0!==o?o:!(null!==(i=t.autoClosingBrackets)&&void 0!==i?i:u.baseConfiguration.autoClosingBrackets));try{return await n.set(d,"editorConfig",t)}catch(e){console.error(`Failed to set ${d}: ${e.message}`)}},label:o.__("Auto Close Brackets in Text Editor"),isToggled:()=>{var e;return null!==(e=t.autoClosingBrackets)&&void 0!==e?e:u.baseConfiguration.autoClosingBrackets}}),e.addCommand(ge.autoClosingBracketsUniversal,{execute:()=>{e.isToggled(ge.autoClosingBrackets)||e.isToggled(ue)||e.isToggled(me)?(e.execute(ge.autoClosingBrackets,{force:!1}),e.execute(ue,{force:!1}),e.execute(me,{force:!1})):(e.execute(ge.autoClosingBrackets,{force:!0}),e.execute(ue,{force:!0}),e.execute(me,{force:!0}))},label:o.__("Auto Close Brackets"),isToggled:()=>e.isToggled(ge.autoClosingBrackets)||e.isToggled(ue)||e.isToggled(me)}),e.addCommand(ge.changeTheme,{label:e=>{var n,i,r,a;return null!==(a=null!==(r=null!==(i=null!==(n=e.displayName)&&void 0!==n?n:e.theme)&&void 0!==i?i:t.theme)&&void 0!==r?r:u.baseConfiguration.theme)&&void 0!==a?a:o.__("Editor Theme")},execute:async e=>{var o;t.theme=null!==(o=e.theme)&&void 0!==o?o:t.theme;try{return await n.set(d,"editorConfig",t)}catch(e){console.error(`Failed to set theme - ${e.message}`)}},isToggled:e=>{var n;return e.theme===(null!==(n=t.theme)&&void 0!==n?n:u.baseConfiguration.theme)}}),e.addCommand(ge.find,{label:o.__("Find…"),execute:()=>{const e=l.currentWidget;e&&e.content.editor.execCommand(re.g)},isEnabled:s}),e.addCommand(ge.goToLine,{label:o.__("Go to Line…"),execute:e=>{const t=l.currentWidget;if(!t)return;const n=t.content.editor,o=e.line,i=e.column;void 0!==o||void 0!==i?n.setCursorPosition({line:(null!=o?o:1)-1,column:(null!=i?i:1)-1}):n.execCommand(re.zo)},isEnabled:s}),e.addCommand(ge.changeLanguage,{label:e=>{var t,n;return null!==(n=null!==(t=e.displayName)&&void 0!==t?t:e.name)&&void 0!==n?n:o.__("Change editor language.")},execute:e=>{var t;const n=e.name,o=l.currentWidget;if(n&&o){const e=m.findByName(n);e&&(Array.isArray(e.mime)?o.content.model.mimeType=null!==(t=e.mime[0])&&void 0!==t?t:q.N.defaultMimeType:o.content.model.mimeType=e.mime)}},isEnabled:s,isToggled:e=>{const t=l.currentWidget;if(!t)return!1;const n=t.content.model.mimeType,o=m.findByMIME(n),i=o&&o.name;return e.name===i}}),e.addCommand(ge.replaceSelection,{execute:e=>{var t,n;const o=e.text||"",i=l.currentWidget;i&&(null===(n=(t=i.content.editor).replaceSelection)||void 0===n||n.call(t,o))},isEnabled:s,label:o.__("Replace Selection in Editor")}),e.addCommand(ge.createConsole,{execute:t=>{const n=l.currentWidget;if(n)return function(e,t){return async function(n,o){var i,r,a;const d=o||{},s=await e.execute("console:create",{activate:d.activate,name:null===(i=n.context.contentsModel)||void 0===i?void 0:i.name,path:n.context.path,preferredLanguage:n.context.model.defaultKernelLanguage||(null!==(a=null===(r=t.findByFileName(n.context.path))||void 0===r?void 0:r.name)&&void 0!==a?a:""),ref:n.id,insertMode:"split-bottom"});n.context.pathChanged.connect(((e,t)=>{var o;s.session.setPath(t),s.session.setName(null===(o=n.context.contentsModel)||void 0===o?void 0:o.name)}))}}(e,m)(n,t)},isEnabled:s,icon:T.fO,label:o.__("Create Console for Editor")}),e.addCommand(ge.restartConsole,{execute:async()=>{var e;const t=null===(e=l.currentWidget)||void 0===e?void 0:e.content;if(!t||null===g)return;const n=g.find((e=>{var n;return(null===(n=e.sessionContext.session)||void 0===n?void 0:n.path)===t.context.path}));return n?h.restart(n.sessionContext):void 0},label:o.__("Restart Kernel"),isEnabled:()=>null!==g&&s()}),e.addCommand(ge.runCode,{execute:()=>{var t;const n=null===(t=l.currentWidget)||void 0===t?void 0:t.content;if(!n)return;let o="";const i=n.editor,r=n.context.path,a=le.PathExt.extname(r),d=i.getSelection(),{start:s,end:c}=d;let u=s.column!==c.column||s.line!==c.line;if(u){const e=i.getOffsetAt(d.start),t=i.getOffsetAt(d.end);o=i.model.sharedModel.getSource().substring(e,t)}else if(le.MarkdownCodeBlocks.isMarkdown(a)){const e=i.model.sharedModel.getSource(),t=le.MarkdownCodeBlocks.findMarkdownCodeBlocks(e);for(const e of t)if(e.startLine<=s.line&&s.line<=e.endLine){o=e.code,u=!0;break}}if(!u){o=i.getLine(d.start.line);const e=i.getCursorPosition();if(e.line+1===i.lineCount){const e=i.model.sharedModel.getSource();i.model.sharedModel.setSource(e+"\n")}i.setCursorPosition({line:e.line+1,column:e.column})}return o?e.execute("console:inject",{activate:!1,code:o,path:r}):Promise.resolve(void 0)},isEnabled:s,label:o.__("Run Selected Code")}),e.addCommand(ge.runAllCode,{execute:()=>{var t;const n=null===(t=l.currentWidget)||void 0===t?void 0:t.content;if(!n)return;let o="";const i=n.editor.model.sharedModel.getSource(),r=n.context.path,a=le.PathExt.extname(r);if(le.MarkdownCodeBlocks.isMarkdown(a)){const e=le.MarkdownCodeBlocks.findMarkdownCodeBlocks(i);for(const t of e)o+=t.code}else o=i;return o?e.execute("console:inject",{activate:!1,code:o,path:r}):Promise.resolve(void 0)},isEnabled:s,label:o.__("Run All Code")}),e.addCommand(ge.markdownPreview,{execute:()=>{const t=l.currentWidget;if(!t)return;const n=t.context.path;return e.execute("markdownviewer:open",{path:n,options:{mode:"split-right"}})},isVisible:()=>{const e=l.currentWidget;return e&&".md"===le.PathExt.extname(e.context.path)||!1},icon:T.pl,label:o.__("Show Markdown Preview")}),e.addCommand(ge.createNew,{label:e=>{var t,n;return e.isPalette?null!==(t=e.paletteLabel)&&void 0!==t?t:o.__("New Text File"):null!==(n=e.launcherLabel)&&void 0!==n?n:o.__("Text File")},caption:e=>{var t;return null!==(t=e.caption)&&void 0!==t?t:o.__("Create a new text file")},icon:e=>{var t;return e.isPalette?void 0:ce.zZ.resolve({icon:null!==(t=e.iconName)&&void 0!==t?t:T._6})},execute:t=>{var n;const o=t.cwd||c.model.path;return a(e,o,null!==(n=t.fileExt)&&void 0!==n?n:"txt")}}),e.addCommand(ge.createNewMarkdown,{label:e=>e.isPalette?o.__("New Markdown File"):o.__("Markdown File"),caption:o.__("Create a new markdown file"),icon:e=>e.isPalette?void 0:T.pl,execute:t=>{const n=t.cwd||c.model.path;return a(e,n,"md")}}),e.addCommand(ge.undo,{execute:()=>{var e;const t=null===(e=l.currentWidget)||void 0===e?void 0:e.content;t&&t.editor.undo()},isEnabled:()=>{var e;if(!s())return!1;const t=null===(e=l.currentWidget)||void 0===e?void 0:e.content;return!!t&&t.editor.model.sharedModel.canUndo()},icon:T.s_.bindprops({stylesheet:"menuItem"}),label:o.__("Undo")}),e.addCommand(ge.redo,{execute:()=>{var e;const t=null===(e=l.currentWidget)||void 0===e?void 0:e.content;t&&t.editor.redo()},isEnabled:()=>{var e;if(!s())return!1;const t=null===(e=l.currentWidget)||void 0===e?void 0:e.content;return!!t&&t.editor.model.sharedModel.canRedo()},icon:T.Nz.bindprops({stylesheet:"menuItem"}),label:o.__("Redo")}),e.addCommand(ge.cut,{execute:()=>{var e;const t=null===(e=l.currentWidget)||void 0===e?void 0:e.content;if(!t)return;const n=t.editor,o=r(n);ae.T.copyToSystem(o),n.replaceSelection&&n.replaceSelection("")},isEnabled:()=>{var e;if(!s())return!1;const t=null===(e=l.currentWidget)||void 0===e?void 0:e.content;return!!t&&i(t.editor)},icon:T.xi.bindprops({stylesheet:"menuItem"}),label:o.__("Cut")}),e.addCommand(ge.copy,{execute:()=>{var e;const t=null===(e=l.currentWidget)||void 0===e?void 0:e.content;if(!t)return;const n=r(t.editor);ae.T.copyToSystem(n)},isEnabled:()=>{var e;if(!s())return!1;const t=null===(e=l.currentWidget)||void 0===e?void 0:e.content;return!!t&&i(t.editor)},icon:T.UI.bindprops({stylesheet:"menuItem"}),label:o.__("Copy")}),e.addCommand(ge.paste,{execute:async()=>{var e;const t=null===(e=l.currentWidget)||void 0===e?void 0:e.content;if(!t)return;const n=t.editor,o=window.navigator.clipboard,i=await o.readText();i&&n.replaceSelection&&n.replaceSelection(i)},isEnabled:()=>{var e;return Boolean(s()&&(null===(e=l.currentWidget)||void 0===e?void 0:e.content))},icon:T.bG.bindprops({stylesheet:"menuItem"}),label:o.__("Paste")}),e.addCommand(ge.selectAll,{execute:()=>{var e;const t=null===(e=l.currentWidget)||void 0===e?void 0:e.content;t&&t.editor.execCommand(ie.td)},isEnabled:()=>{var e;return Boolean(s()&&(null===(e=l.currentWidget)||void 0===e?void 0:e.content))},label:o.__("Select All")})},e.addCompleterCommands=function(e,t,n,o){const i=(null!=o?o:v.Sr).load("jupyterlab");e.addCommand(ge.invokeCompleter,{label:i.__("Display the completion helper."),execute:()=>{const e=t.currentWidget&&t.currentWidget.id;if(e)return n.invoke(e)}}),e.addCommand(ge.selectCompleter,{label:i.__("Select the completion suggestion."),execute:()=>{const e=t.currentWidget&&t.currentWidget.id;if(e)return n.select(e)}}),e.addKeyBinding({command:ge.selectCompleter,keys:["Enter"],selector:".jp-FileEditor .jp-mod-completer-active"})},e.addLauncherItems=function(e,t){d(e,t),s(e,t)},e.addCreateNewToLauncher=d,e.addCreateNewMarkdownToLauncher=s,e.addKernelLanguageLauncherItems=function(e,t,n){for(let o of n)e.add({command:ge.createNew,category:t.__("Other"),rank:3,args:o})},e.addPaletteItems=function(e,t){l(e,t),c(e,t),u(e,t),m(e,t)},e.addChangeTabsCommandsToPalette=l,e.addCreateNewCommandToPalette=c,e.addCreateNewMarkdownCommandToPalette=u,e.addChangeFontSizeCommandsToPalette=m,e.addKernelLanguagePaletteItems=function(e,t,n){const o=t.__("Text Editor");for(let t of n)e.addItem({command:ge.createNew,args:{...t,isPalette:!0},category:o})},e.addMenuItems=function(e,t,n,o){e.editMenu.undoers.redo.add({id:ge.redo,isEnabled:o}),e.editMenu.undoers.undo.add({id:ge.undo,isEnabled:o}),e.viewMenu.editorViewers.toggleLineNumbers.add({id:ge.currentLineNumbers,isEnabled:o}),e.viewMenu.editorViewers.toggleMatchBrackets.add({id:ge.currentMatchBrackets,isEnabled:o}),e.viewMenu.editorViewers.toggleWordWrap.add({id:ge.currentLineWrap,isEnabled:o}),e.fileMenu.consoleCreators.add({id:ge.createConsole,isEnabled:o}),n&&g(e,n,o)},e.addKernelLanguageMenuItems=function(e,t){for(let n of t)e.fileMenu.newMenu.addItem({command:ge.createNew,args:n,rank:31})},e.addCodeRunnersToRunMenu=g,e.addOpenCodeViewerCommand=function(e,t,n,o){e.commands.addCommand(ge.openCodeViewer,{label:o.__("Open Code Viewer"),execute:i=>(async i=>{var r;const a=t.factoryService.newDocumentEditor;let d=i.mimeType;!d&&i.extension&&(d=t.mimeTypeService.getMimeTypeByFilePath(`temp.${i.extension.replace(/\\.$/,"")}`));const s=se.createCodeViewer({factory:e=>a(e),content:i.content,mimeType:d});s.title.label=i.label||o.__("Code Viewer"),s.title.caption=s.title.label;const l=(0,oe.sE)(e.docRegistry.fileTypes(),(e=>!!d&&e.mimeTypes.includes(d)));s.title.icon=null!==(r=null==l?void 0:l.icon)&&void 0!==r?r:T._6,i.widgetId&&(s.id=i.widgetId);const c=new w.k({content:s});return await n.add(c),e.shell.add(c,"main"),s})(i)})}}(pe||(pe={}));var fe=n(83243);function ve(e){return C.createElement(f.Jy,{source:e.language,onClick:e.handleClick})}class ye extends y.UB{constructor(e){var t;super(new ye.Model(e.languages)),this._handleClick=()=>{const e=new M.v2({commands:this._commands});this._popup&&this._popup.dispose(),this.model.languages.getLanguages().sort(((e,t)=>{var n,o;const i=null!==(n=e.displayName)&&void 0!==n?n:e.name,r=null!==(o=t.displayName)&&void 0!==o?o:t.name;return i.localeCompare(r)})).forEach((t=>{var n;if(0===t.name.toLowerCase().indexOf("brainf"))return;const o={name:t.name,displayName:null!==(n=t.displayName)&&void 0!==n?n:t.name};e.addItem({command:"fileeditor:change-language",args:o})})),this._popup=(0,f.U)({body:e,anchor:this,align:"left"})},this._popup=null,this._commands=e.commands,this.translator=null!==(t=e.translator)&&void 0!==t?t:v.Sr;const n=this.translator.load("jupyterlab");this.addClass("jp-mod-highlighted"),this.title.caption=n.__("Change text editor syntax highlighting")}render(){return this.model?C.createElement(ve,{language:this.model.language,handleClick:this._handleClick}):null}}!function(e){class t extends y.I_{constructor(e){super(),this.languages=e,this._onMIMETypeChange=(e,t)=>{var n;const o=this._language,i=this.languages.findByMIME(t.newValue);this._language=null!==(n=null==i?void 0:i.name)&&void 0!==n?n:q.N.defaultMimeType,this._triggerChange(o,this._language)},this._language="",this._editor=null}get language(){return this._language}get editor(){return this._editor}set editor(e){var t;const n=this._editor;null!==n&&n.model.mimeTypeChanged.disconnect(this._onMIMETypeChange);const o=this._language;if(this._editor=e,null===this._editor)this._language="";else{const e=this.languages.findByMIME(this._editor.model.mimeType);this._language=null!==(t=null==e?void 0:e.name)&&void 0!==t?t:q.N.defaultMimeType,this._editor.model.mimeTypeChanged.connect(this._onMIMETypeChange)}this._triggerChange(o,this._language)}_triggerChange(e,t){e!==t&&this.stateChanged.emit(void 0)}}e.Model=t}(ye||(ye={}));const Ce={id:"@jupyterlab/fileeditor-extension:editor-syntax-status",description:"Adds a file editor syntax status widget.",autoStart:!0,requires:[p.W,c.db,fe.r,v.gv],optional:[f.WQ],activate:(e,t,n,o,i,r)=>{if(!r)return;const a=new ye({commands:e.commands,languages:n,translator:i});o.currentChanged.connect((()=>{const e=o.currentWidget;e&&t.has(e)&&a.model&&(a.model.editor=e.content.editor)})),r.registerStatusItem(Ce.id,{item:a,align:"left",rank:0,isActive:()=>!!o.currentWidget&&!!t.currentWidget&&o.currentWidget===t.currentWidget})}},_e={activate:function(e,t,n,o,i,s,l,c,u,m,g,h,p,f,y,C,_){const b=_e.id,w=null!=C?C:v.Sr,x=null!=p?p:new r.H({translator:w}),k=w.load("jupyterlab");let T;y&&(T=(0,a._)(y,l,he,b,w));const E=new N({editorServices:t,factoryOptions:{name:he,label:k.__("Editor"),fileTypes:["markdown","*"],defaultFor:["markdown","*"],toolbarFactory:T,translator:w}}),{commands:M,restored:S,shell:W}=e,P=new d.u({namespace:"editor"}),A=()=>null!==P.currentWidget&&P.currentWidget===W.currentWidget,I=new Map([["python",[{fileExt:"py",iconName:"ui-components:python",launcherLabel:k.__("Python File"),paletteLabel:k.__("New Python File"),caption:k.__("Create a new Python file")}]],["julia",[{fileExt:"jl",iconName:"ui-components:julia",launcherLabel:k.__("Julia File"),paletteLabel:k.__("New Julia File"),caption:k.__("Create a new Julia file")}]],["R",[{fileExt:"r",iconName:"ui-components:r-kernel",launcherLabel:k.__("R File"),paletteLabel:k.__("New R File"),caption:k.__("Create a new R file")}]]]);if(h&&h.restore(P,{command:"docmanager:open",args:e=>({path:e.context.path,factory:he}),name:e=>e.context.path}),Promise.all([l.load(b),S]).then((([e])=>{var t,n,r;if(g){const e=null===(t=g.viewMenu.items.find((e=>{var t;return"submenu"===e.type&&"jp-mainmenu-view-codemirror-language"===(null===(t=e.submenu)||void 0===t?void 0:t.id)})))||void 0===t?void 0:t.submenu;e&&o.getLanguages().sort(((e,t)=>{const n=e.name,o=t.name;return n.localeCompare(o)})).forEach((t=>{0!==t.name.toLowerCase().indexOf("brainf")&&e.addItem({command:ge.changeLanguage,args:{...t}})}));const a=null===(n=g.settingsMenu.items.find((e=>{var t;return"submenu"===e.type&&"jp-mainmenu-settings-codemirror-theme"===(null===(t=e.submenu)||void 0===t?void 0:t.id)})))||void 0===n?void 0:n.submenu;if(a)for(const e of i.themes)a.addItem({command:ge.changeTheme,args:{theme:e.name,displayName:null!==(r=e.displayName)&&void 0!==r?r:e.name}});g.editMenu.goToLiners.add({id:ge.goToLine,isEnabled:e=>null!==P.currentWidget&&P.has(e)})}pe.updateSettings(e,M),pe.updateTracker(P),e.changed.connect((()=>{pe.updateSettings(e,M),pe.updateTracker(P)}))})).catch((e=>{console.error(e.message),pe.updateTracker(P)})),_){const e=_.getRenderer("@jupyterlab/codemirror-extension:plugin.defaultConfig");e&&_.addRenderer("@jupyterlab/fileeditor-extension:plugin.editorConfig",e)}E.widgetCreated.connect(((e,t)=>{t.context.pathChanged.connect((()=>{P.save(t)})),P.add(t),pe.updateWidget(t.content)})),e.docRegistry.addWidgetFactory(E),P.widgetAdded.connect(((e,t)=>{pe.updateWidget(t.content)})),pe.addCommands(e.commands,l,k,b,A,P,s,n,o,c,x);const L=new d.u({namespace:"codeviewer"});return h&&h.restore(L,{command:ge.openCodeViewer,args:e=>({content:e.content.content,label:e.content.title.label,mimeType:e.content.mimeType,widgetId:e.content.id}),name:e=>e.content.id}),pe.addOpenCodeViewerCommand(e,t,L,k),m&&pe.addLauncherItems(m,k),u&&pe.addPaletteItems(u,k),g&&pe.addMenuItems(g,P,c,A),(async()=>{var t,n;const o=e.serviceManager.kernelspecs;await o.ready;let i=new Set;const r=null!==(n=null===(t=o.specs)||void 0===t?void 0:t.kernelspecs)&&void 0!==n?n:{};return Object.keys(r).forEach((e=>{const t=r[e];if(t){const e=I.get(t.language);null==e||e.forEach((e=>i.add(e)))}})),i})().then((e=>{m&&pe.addKernelLanguageLauncherItems(m,k,e),u&&pe.addKernelLanguagePaletteItems(u,k,e),g&&pe.addKernelLanguageMenuItems(g,e)})).catch((e=>{console.error(e.message)})),f&&(f.add(new R(P)),f.add(new $(P)),f.add(new H(P))),P},id:"@jupyterlab/fileeditor-extension:plugin",description:"Provides the file editor widget tracker.",requires:[l.D3,c.$G,c.db,c.L0,h.iH,Z.O],optional:[m.E,i.WW,J.B,X.O,o.L,i.oj,ee.wk,i.RX,v.gv,te.C],provides:p.W,autoStart:!0},be={id:"@jupyterlab/fileeditor-extension:tab-space-status",description:"Adds a file editor indentation status widget.",autoStart:!0,requires:[p.W,c.$G,Z.O,v.gv],optional:[f.WQ],activate:(e,t,n,o,i,r)=>{const a=i.load("jupyterlab");if(!r)return;const d=new ne.q({commands:e.commands}),s="fileeditor:change-tabs",{shell:l}=e,c={name:a.__("Indent with Tab")};d.addItem({command:s,args:c});for(const e of["1","2","4","8"]){const t={size:e,name:a._p("v4","Spaces: %1",e)};d.addItem({command:s,args:t})}const u=new b({menu:d,translator:i}),m=e=>{var t,o,i;u.model.indentUnit=null!==(i=null!==(o=null===(t=e.get("editorConfig").composite)||void 0===t?void 0:t.indentUnit)&&void 0!==o?o:n.baseConfiguration.indentUnit)&&void 0!==i?i:null};Promise.all([o.load("@jupyterlab/fileeditor-extension:plugin"),e.restored]).then((([e])=>{m(e),e.changed.connect(m)})),r.registerStatusItem("@jupyterlab/fileeditor-extension:tab-space-status",{item:u,align:"right",rank:1,isActive:()=>!!l.currentWidget&&t.has(l.currentWidget)})}},we={id:"@jupyterlab/fileeditor-extension:cursor-position",description:"Adds a file editor cursor position status widget.",activate:(e,t,n)=>{n.addEditorProvider((e=>Promise.resolve(e&&t.has(e)?e.content.editor:null)))},requires:[p.W,l.fY],autoStart:!0},xe={id:"@jupyterlab/fileeditor-extension:completer",description:"Adds the completer capability to the file editor.",requires:[p.W],optional:[u.pl,v.gv,i.hd],activate:function(e,t,n,o,i){if(!n)return;pe.addCompleterCommands(e.commands,t,n,o);const r=e.serviceManager.sessions,a=null!=i?i:new s.T,d=new Map,l=async(e,t)=>{const o={editor:t.content.editor,widget:t};await n.updateCompleter(o);const i=(e,o)=>{const i=d.get(t.id),s=(0,oe.sE)(o,(e=>e.path===t.context.path));if(s){if(i&&i.id===s.id)return;i&&(d.delete(t.id),i.dispose());const e=r.connectTo({model:s}),o={editor:t.content.editor,widget:t,session:e,sanitizer:a};n.updateCompleter(o).catch(console.error),d.set(t.id,e)}else i&&(d.delete(t.id),i.dispose())};i(0,Array.from(r.running())),r.runningChanged.connect(i),t.disposed.connect((()=>{r.runningChanged.disconnect(i);const e=d.get(t.id);e&&(d.delete(t.id),e.dispose())}))};t.widgetAdded.connect(l),n.activeProvidersChanged.connect((()=>{t.forEach((e=>{l(0,e).catch(console.error)}))}))},autoStart:!0},ke={id:"@jupyterlab/fileeditor-extension:search",description:"Adds search capability to the file editor.",requires:[g.x],autoStart:!0,activate:(e,t)=>{t.add("jp-fileeditorSearchProvider",P)}},Te={id:"@jupyterlab/fileeditor-extension:language-server",description:"Adds Language Server capability to the file editor.",requires:[p.W,Y.aY,Y.bW,Y.fE,Y.PW],activate:function(e,t,n,o,i,r){t.widgetAdded.connect((async(t,a)=>{const d=new G(a,{connectionManager:n,featureManager:o,foreignCodeExtractorsManager:i,docRegistry:e.docRegistry});r.add(d)}))},autoStart:!0},Ee=[_e,we,xe,Te,ke,Ce,be]},11097:(e,t,n)=>{n.d(t,{E:()=>o});const o=new(n(47963).Token)("@jupyterlab/console:IConsoleTracker","A widget tracker for code consoles.\n  Use this if you want to be able to iterate over and interact with code consoles\n  created by the application.")}}]);