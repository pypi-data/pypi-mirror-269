"use strict";(self.webpackChunk_datalayer_jupyter_contents=self.webpackChunk_datalayer_jupyter_contents||[]).push([[4825],{44825:(t,e,s)=>{s.r(e),s.d(e,{default:()=>B});var r,o=s(35909),a=s(38522),i=s(18168),n=s(56276),c=s(63070),l=s(47963),h=s(16781),u=s(27258),p=s(92279),d=s(56769),m=s(46931),S=s(60775),y=s(77727);class g{constructor(){this.commandName="",this.label="",this.keys={},this.source="",this.selector="",this.category="",this.id="",this.numberOfShortcuts=0,this.hasConflict=!1}get(t){return"label"===t?this.label:"selector"===t?this.selector:"category"===t?this.category:"source"===t?this.source:""}}class f extends g{constructor(){super(),this.takenBy=new C}}class C{constructor(t){t?(this.takenBy=t,this.takenByKey="",this.takenByLabel=t.category+": "+t.label,this.id=t.commandName+"_"+t.selector):(this.takenBy=new g,this.takenByKey="",this.takenByLabel="",this.id="")}}class k extends d.Component{constructor(t){super(t),this.handleUpdate=()=>{let t=this.state.keys;t.push(this.state.currentChain),this.setState({keys:t}),this.props.handleUpdate(this.props.shortcut,this.state.keys)},this.handleOverwrite=async()=>{this.props.deleteShortcut(this.state.takenByObject.takenBy,this.state.takenByObject.takenByKey).then(this.handleUpdate())},this.handleReplace=async()=>{let t=this.state.keys;t.push(this.state.currentChain),this.props.toggleInput(),await this.props.deleteShortcut(this.props.shortcut,this.props.shortcutId),this.props.handleUpdate(this.props.shortcut,t)},this.parseChaining=(t,e,s,r,o)=>{let a=S.eC.keyForKeydownEvent(t.nativeEvent);const i=["Shift","Control","Alt","Meta","Ctrl","Accel"];if("Backspace"===t.key)s="",r=[],o="",this.setState({value:"",userInput:s,keys:r,currentChain:o});else if("CapsLock"!==t.key){const e=s.substr(s.lastIndexOf(" ")+1,s.length).trim();-1===i.lastIndexOf(e)&&""!=e?(s+=",",r.push(o),o="",t.ctrlKey&&"Control"!=t.key&&(s=(s+" Ctrl").trim(),o=(o+" Ctrl").trim()),t.metaKey&&"Meta"!=t.key&&(s=(s+" Accel").trim(),o=(o+" Accel").trim()),t.altKey&&"Alt"!=t.key&&(s=(s+" Alt").trim(),o=(o+" Alt").trim()),t.shiftKey&&"Shift"!=t.key&&(s=(s+" Shift").trim(),o=(o+" Shift").trim()),-1===i.lastIndexOf(t.key)?(s=(s+" "+a).trim(),o=(o+" "+a).trim()):"Meta"===t.key?(s=(s+" Accel").trim(),o=(o+" Accel").trim()):"Control"===t.key?(s=(s+" Ctrl").trim(),o=(o+" Ctrl").trim()):"Shift"===t.key?(s=(s+" Shift").trim(),o=(o+" Shift").trim()):"Alt"===t.key?(s=(s+" Alt").trim(),o=(o+" Alt").trim()):(s=(s+" "+t.key).trim(),o=(o+" "+t.key).trim())):"Control"===t.key?(s=(s+" Ctrl").trim(),o=(o+" Ctrl").trim()):"Meta"===t.key?(s=(s+" Accel").trim(),o=(o+" Accel").trim()):"Shift"===t.key?(s=(s+" Shift").trim(),o=(o+" Shift").trim()):"Alt"===t.key?(s=(s+" Alt").trim(),o=(o+" Alt").trim()):(s=(s+" "+a).trim(),o=(o+" "+a).trim())}return this.setState({keys:r,currentChain:o}),[s,r,o]},this.checkNonFunctional=t=>{const e=["Ctrl","Alt","Accel","Shift"],s=this.state.currentChain.split(" "),r=s[s.length-1];return this.setState({isFunctional:!(-1!==e.indexOf(r))}),-1!==e.indexOf(r)},this.checkShortcutAvailability=(t,e,s)=>{let r=-1===Object.keys(this.props.keyBindingsUsed).indexOf(e.join(" ")+s+"_"+this.props.shortcut.selector)||""===t,o=new C;if(r){for(let t of e)if(-1!==Object.keys(this.props.keyBindingsUsed).indexOf(t+"_"+this.props.shortcut.selector)&&""!==t){r=!1,o=this.props.keyBindingsUsed[t+"_"+this.props.shortcut.selector];break}r&&-1!==Object.keys(this.props.keyBindingsUsed).indexOf(s+"_"+this.props.shortcut.selector)&&""!==s&&(r=!1,o=this.props.keyBindingsUsed[s+"_"+this.props.shortcut.selector])}else o=this.props.keyBindingsUsed[e.join(" ")+s+"_"+this.props.shortcut.selector];return r||o.takenBy.id===this.props.shortcut.id&&"replace"===this.props.newOrReplace&&(r=!0,o=new C),this.setState({isAvailable:r}),o},this.handleInput=t=>{t.preventDefault(),this.setState({selected:!1});const e=this.parseChaining(t,this.state.value,this.state.userInput,this.state.keys,this.state.currentChain),s=e[0],r=e[1],o=e[2],a=this.props.toSymbols(s);let i=this.checkShortcutAvailability(s,r,o);this.checkConflict(i,r),this.setState({value:a,userInput:s,takenByObject:i,keys:r,currentChain:o},(()=>this.checkNonFunctional(this.state.userInput)))},this.handleBlur=t=>{(null===t.relatedTarget||"no-blur"!==t.relatedTarget.id&&"overwrite"!==t.relatedTarget.id)&&(this.props.toggleInput(),this.setState({value:"",userInput:""}),this.props.clearConflicts())},this.state={value:this.props.placeholder,userInput:"",isAvailable:!0,isFunctional:"replace"===this.props.newOrReplace,takenByObject:new C,keys:new Array,currentChain:"",selected:!0}}checkConflict(t,e){""!==t.id&&t.takenBy.id!==this.props.shortcut.id?this.props.sortConflict(this.props.shortcut,t,t.takenByLabel,""):this.props.clearConflicts()}render(){const t=this.props.translator.load("jupyterlab");let e="jp-Shortcuts-Input";return this.state.isAvailable||(e+=" jp-mod-unavailable-Input"),d.createElement("div",{className:this.props.displayInput?"new"===this.props.newOrReplace?"jp-Shortcuts-InputBox jp-Shortcuts-InputBoxNew":"jp-Shortcuts-InputBox":"jp-mod-hidden",onBlur:t=>this.handleBlur(t)},d.createElement("div",{tabIndex:0,id:"no-blur",className:e,onKeyDown:this.handleInput,ref:t=>t&&t.focus(),"data-lm-suppress-shortcuts":"true"},d.createElement("p",{className:this.state.selected&&"replace"===this.props.newOrReplace?"jp-Shortcuts-InputText jp-mod-selected-InputText":""===this.state.value?"jp-Shortcuts-InputText jp-mod-waiting-InputText":"jp-Shortcuts-InputText"},""===this.state.value?t.__("press keys"):this.state.value)),d.createElement("button",{className:this.state.isFunctional?this.state.isAvailable?"jp-Shortcuts-Submit":"jp-Shortcuts-Submit jp-mod-conflict-Submit":"jp-Shortcuts-Submit jp-mod-defunc-Submit",id:"no-blur",disabled:!this.state.isAvailable||!this.state.isFunctional,onClick:()=>{"new"===this.props.newOrReplace?(this.handleUpdate(),this.setState({value:"",keys:[],currentChain:""}),this.props.toggleInput()):this.state.selected?(this.props.toggleInput(),this.setState({value:"",userInput:""}),this.props.clearConflicts()):this.handleReplace()}},this.state.isAvailable?d.createElement(y.eQ.react,null):d.createElement(y.mb.react,null)),!this.state.isAvailable&&d.createElement("button",{hidden:!0,id:"overwrite",onClick:()=>{this.handleOverwrite(),this.props.clearConflicts(),this.props.toggleInput()}},t.__("Overwrite")))}}!function(t){t[t.Left=0]="Left",t[t.Right=1]="Right"}(r||(r={}));class b extends d.Component{constructor(t){var e;super(t),this.toggleInputNew=()=>{this.setState({displayNewInput:!this.state.displayNewInput})},this.toggleInputReplaceLeft=()=>{this.setState({displayReplaceInputLeft:!this.state.displayReplaceInputLeft})},this.toggleInputReplaceRight=()=>{this.setState({displayReplaceInputRight:!this.state.displayReplaceInputRight})},this.addCommandIfNeeded=(t,e)=>{const s=this.props.shortcut.commandName+"_"+this.props.shortcut.selector;this.props.external.hasCommand(t.commandId+s)||this.props.external.addCommand(t.commandId+s,{label:t.label,caption:t.caption,execute:e})},this.handleRightClick=t=>{this.addCommandIfNeeded(this._commands.shortcutEdit,(()=>this.toggleInputReplaceLeft())),this.addCommandIfNeeded(this._commands.shortcutEditLeft,(()=>this.toggleInputReplaceLeft())),this.addCommandIfNeeded(this._commands.shortcutEditRight,(()=>this.toggleInputReplaceRight())),this.addCommandIfNeeded(this._commands.shortcutAddNew,(()=>this.toggleInputNew())),this.addCommandIfNeeded(this._commands.shortcutAddAnother,(()=>this.toggleInputNew())),this.addCommandIfNeeded(this._commands.shortcutReset,(()=>this.props.resetShortcut(this.props.shortcut)));const e=this.props.shortcut.commandName+"_"+this.props.shortcut.selector;this.setState({numShortcuts:Object.keys(this.props.shortcut.keys).filter((t=>""!==this.props.shortcut.keys[t][0])).length},(()=>{let s=[];s=2==this.state.numShortcuts?s.concat([this._commands.shortcutEditLeft.commandId+e,this._commands.shortcutEditRight.commandId+e]):1==this.state.numShortcuts?s.concat([this._commands.shortcutEdit.commandId+e,this._commands.shortcutAddAnother.commandId+e]):s.concat([this._commands.shortcutAddNew.commandId+e]),"Custom"===this.props.shortcut.source&&(s=s.concat([this._commands.shortcutReset.commandId+e])),this.props.contextMenu(t,s)}))},this.toSymbols=t=>t.split(" ").reduce(((t,e)=>"Ctrl"===e?(t+" ⌃").trim():"Alt"===e?(t+" ⌥").trim():"Shift"===e?(t+" ⇧").trim():"Accel"===e&&u.t4.IS_MAC?(t+" ⌘").trim():"Accel"===e?(t+" ⌃").trim():(t+" "+e).trim()),""),this._commands={shortcutEditLeft:{commandId:"shortcutui:EditLeft",label:(e=t.external.translator.load("jupyterlab")).__("Edit First"),caption:e.__("Edit existing shortcut")},shortcutEditRight:{commandId:"shortcutui:EditRight",label:e.__("Edit Second"),caption:e.__("Edit existing shortcut")},shortcutEdit:{commandId:"shortcutui:Edit",label:e.__("Edit"),caption:e.__("Edit existing shortcut")},shortcutAddNew:{commandId:"shortcutui:AddNew",label:e.__("Add"),caption:e.__("Add new shortcut")},shortcutAddAnother:{commandId:"shortcutui:AddAnother",label:e.__("Add"),caption:e.__("Add another shortcut")},shortcutReset:{commandId:"shortcutui:Reset",label:e.__("Reset"),caption:e.__("Reset shortcut back to default")}},this.state={displayNewInput:!1,displayReplaceInputLeft:!1,displayReplaceInputRight:!1,numShortcuts:Object.keys(this.props.shortcut.keys).filter((t=>""!==this.props.shortcut.keys[t][0])).length}}getErrorRow(){const t=this.props.external.translator.load("jupyterlab");return d.createElement("div",{className:"jp-Shortcuts-Row"},d.createElement("div",{className:"jp-Shortcuts-ConflictContainer"},d.createElement("div",{className:"jp-Shortcuts-ErrorMessage"},t.__("Shortcut already in use by %1. Overwrite it?",this.props.shortcut.takenBy.takenByLabel)),d.createElement("div",{className:"jp-Shortcuts-ErrorButton"},d.createElement("button",null,t.__("Cancel")),d.createElement("button",{id:"no-blur",onClick:()=>{var t;null===(t=document.getElementById("overwrite"))||void 0===t||t.click()}},t.__("Overwrite")))))}getCategoryCell(){return d.createElement("div",{className:"jp-Shortcuts-Cell"},this.props.shortcut.category)}getLabelCell(){return d.createElement("div",{className:"jp-Shortcuts-Cell"},d.createElement("div",{className:"jp-label"},this.props.shortcut.label))}getResetShortCutLink(){const t=this.props.external.translator.load("jupyterlab");return d.createElement("a",{className:"jp-Shortcuts-Reset",onClick:()=>this.props.resetShortcut(this.props.shortcut)},t.__("Reset"))}getSourceCell(){return d.createElement("div",{className:"jp-Shortcuts-Cell"},d.createElement("div",{className:"jp-Shortcuts-SourceCell"},this.props.shortcut.source),"Custom"===this.props.shortcut.source&&this.getResetShortCutLink())}getOptionalSelectorCell(){return this.props.showSelectors?d.createElement("div",{className:"jp-Shortcuts-Cell"},d.createElement("div",{className:"jp-selector"},this.props.shortcut.selector)):null}getClassNameForShortCuts(t){const e=["jp-Shortcuts-ShortcutCell"];switch(t.length){case 1:e.push("jp-Shortcuts-SingleCell");break;case 0:e.push("jp-Shortcuts-EmptyCell")}return e.join(" ")}getToggleInputReplaceMethod(t){switch(t){case r.Left:return this.toggleInputReplaceLeft;case r.Right:return this.toggleInputReplaceRight}}getDisplayReplaceInput(t){switch(t){case r.Left:return this.state.displayReplaceInputLeft;case r.Right:return this.state.displayReplaceInputRight}}getOrDiplayIfNeeded(t){const e=this.props.external.translator.load("jupyterlab");return d.createElement("div",{className:2==t.length||this.state.displayNewInput?"jp-Shortcuts-OrTwo":"jp-Shortcuts-Or",id:2==t.length?"secondor":this.state.displayReplaceInputLeft?"noor":"or"},e.__("or"))}getShortCutAsInput(t,e){return d.createElement(k,{handleUpdate:this.props.handleUpdate,deleteShortcut:this.props.deleteShortcut,toggleInput:this.getToggleInputReplaceMethod(e),shortcut:this.props.shortcut,shortcutId:t,toSymbols:this.toSymbols,keyBindingsUsed:this.props.keyBindingsUsed,sortConflict:this.props.sortConflict,clearConflicts:this.props.clearConflicts,displayInput:this.getDisplayReplaceInput(e),newOrReplace:"replace",placeholder:this.toSymbols(this.props.shortcut.keys[t].join(", ")),translator:this.props.external.translator})}getShortCutForDisplayOnly(t){return this.props.shortcut.keys[t].map(((e,s)=>d.createElement("div",{className:"jp-Shortcuts-ShortcutKeysContainer",key:s},d.createElement("div",{className:"jp-Shortcuts-ShortcutKeys"},this.toSymbols(e)),s+1<this.props.shortcut.keys[t].length?d.createElement("div",{className:"jp-Shortcuts-Comma"},","):null)))}isLocationBeingEdited(t){return t===r.Left&&this.state.displayReplaceInputLeft||t===r.Right&&this.state.displayReplaceInputRight}getLocationFromIndex(t){return 0===t?r.Left:r.Right}getDivForKey(t,e,s){const o=this.getLocationFromIndex(t);return d.createElement("div",{className:"jp-Shortcuts-ShortcutContainer",key:this.props.shortcut.id+"_"+t,onClick:this.getToggleInputReplaceMethod(o)},this.isLocationBeingEdited(o)?this.getShortCutAsInput(e,o):this.getShortCutForDisplayOnly(e),o===r.Left&&this.getOrDiplayIfNeeded(s))}getAddLink(){const t=this.props.external.translator.load("jupyterlab");return d.createElement("a",{className:this.state.displayNewInput?"":"jp-Shortcuts-Plus",onClick:()=>{this.toggleInputNew(),this.props.clearConflicts()},id:"add-link"},t.__("Add"))}getInputBoxWhenToggled(){return this.state.displayNewInput?d.createElement(k,{handleUpdate:this.props.handleUpdate,deleteShortcut:this.props.deleteShortcut,toggleInput:this.toggleInputNew,shortcut:this.props.shortcut,shortcutId:"",toSymbols:this.toSymbols,keyBindingsUsed:this.props.keyBindingsUsed,sortConflict:this.props.sortConflict,clearConflicts:this.props.clearConflicts,displayInput:this.state.displayNewInput,newOrReplace:"new",placeholder:"",translator:this.props.external.translator}):d.createElement("div",null)}getShortCutsCell(t){return d.createElement("div",{className:"jp-Shortcuts-Cell"},d.createElement("div",{className:this.getClassNameForShortCuts(t)},t.map(((e,s)=>this.getDivForKey(s,e,t))),1===t.length&&!this.state.displayNewInput&&!this.state.displayReplaceInputLeft&&this.getAddLink(),0===t.length&&!this.state.displayNewInput&&this.getAddLink(),this.getInputBoxWhenToggled()))}render(){const t=Object.keys(this.props.shortcut.keys).filter((t=>""!==this.props.shortcut.keys[t][0]));return"error_row"===this.props.shortcut.id?this.getErrorRow():d.createElement("div",{className:"jp-Shortcuts-Row",onContextMenu:t=>{t.persist(),this.handleRightClick(t)}},this.getCategoryCell(),this.getLabelCell(),this.getShortCutsCell(t),this.getSourceCell(),this.getOptionalSelectorCell())}}class I extends d.Component{render(){return d.createElement("div",{className:"jp-Shortcuts-ShortcutListContainer",style:{height:this.props.height-115+"px"},id:"shortcutListContainer"},d.createElement("div",{className:"jp-Shortcuts-ShortcutList"},this.props.shortcuts.map((t=>d.createElement(b,{key:t.commandName+"_"+t.selector,resetShortcut:this.props.resetShortcut,shortcut:t,handleUpdate:this.props.handleUpdate,deleteShortcut:this.props.deleteShortcut,showSelectors:this.props.showSelectors,keyBindingsUsed:this.props.keyBindingsUsed,sortConflict:this.props.sortConflict,clearConflicts:this.props.clearConflicts,contextMenu:this.props.contextMenu,external:this.props.external})))))}}var w,_=s(69768);class E extends d.Component{render(){return d.createElement("div",{className:this.props.title.toLowerCase()===this.props.active?"jp-Shortcuts-Header jp-Shortcuts-CurrentHeader":"jp-Shortcuts-Header",onClick:()=>this.props.updateSort(this.props.title.toLowerCase())},this.props.title,d.createElement(y.EN.react,{className:"jp-Shortcuts-SortButton jp-ShortcutTitleItem-sortButton"}))}}function v(t){return d.createElement("div",{className:"jp-Shortcuts-Symbols"},d.createElement("table",null,d.createElement("tbody",null,d.createElement("tr",null,d.createElement("td",null,d.createElement("kbd",null,"Cmd")),d.createElement("td",null,"⌘"),d.createElement("td",null,d.createElement("kbd",null,"Ctrl")),d.createElement("td",null,"⌃")),d.createElement("tr",null,d.createElement("td",null,d.createElement("kbd",null,"Alt")),d.createElement("td",null,"⌥"),d.createElement("td",null,d.createElement("kbd",null,"Shift")),d.createElement("td",null,"⇧")))))}function j(t){const e=t.translator.load("jupyterlab");return d.createElement("div",{className:"jp-Shortcuts-AdvancedOptions"},d.createElement("a",{className:"jp-Shortcuts-AdvancedOptionsLink",onClick:()=>t.toggleSelectors()},t.showSelectors?e.__("Hide Selectors"):e.__("Show Selectors")),d.createElement("a",{className:"jp-Shortcuts-AdvancedOptionsLink",onClick:()=>t.resetShortcuts()},e.__("Reset All")))}!function(t){t.showSelectors="shortcutui:showSelectors",t.resetAll="shortcutui:resetAll"}(w||(w={}));class x extends d.Component{constructor(t){super(t),this.addMenuCommands(),this.menu=this.props.external.createMenu(),this.menu.addItem({command:w.showSelectors}),this.menu.addItem({command:w.resetAll})}addMenuCommands(){const t=this.props.external.translator.load("jupyterlab");this.props.external.hasCommand(w.showSelectors)||this.props.external.addCommand(w.showSelectors,{label:t.__("Toggle Selectors"),caption:t.__("Toggle command selectors"),execute:()=>{this.props.toggleSelectors()}}),this.props.external.hasCommand(w.resetAll)||this.props.external.addCommand(w.resetAll,{label:t.__("Reset All"),caption:t.__("Reset all shortcuts"),execute:()=>{this.props.resetShortcuts()}})}getShortCutTitleItem(t){return d.createElement("div",{className:"jp-Shortcuts-Cell"},d.createElement(E,{title:t,updateSort:this.props.updateSort,active:this.props.currentSort}))}render(){const t=this.props.external.translator.load("jupyterlab");return d.createElement("div",{className:"jp-Shortcuts-Top"},d.createElement("div",{className:"jp-Shortcuts-TopNav"},d.createElement(v,null),d.createElement(_.B,{className:"jp-Shortcuts-Search","aria-label":t.__("Search shortcuts"),type:"text",onChange:t=>this.props.updateSearchQuery(t),placeholder:t.__("Search…"),rightIcon:"ui-components:search"}),d.createElement(j,{toggleSelectors:this.props.toggleSelectors,showSelectors:this.props.showSelectors,resetShortcuts:this.props.resetShortcuts,menu:this.menu,translator:this.props.external.translator})),d.createElement("div",{className:"jp-Shortcuts-HeaderRowContainer"},d.createElement("div",{className:"jp-Shortcuts-HeaderRow"},this.getShortCutTitleItem(t.__("Category")),this.getShortCutTitleItem(t.__("Command")),d.createElement("div",{className:"jp-Shortcuts-Cell"},d.createElement("div",{className:"title-div"},t.__("Shortcut"))),this.getShortCutTitleItem(t.__("Source")),this.props.showSelectors&&this.getShortCutTitleItem(t.__("Selectors")))))}}function N(t,e){const s=t.category.toLowerCase(),r=`${s} ${t.label.toLowerCase()}`;let o=1/0,a=null;const i=/\b\w/g;for(;;){const t=i.exec(r);if(!t)break;const s=m.kf.matchSumOfDeltas(r,e,t.index);if(!s)break;s&&s.score<=o&&(o=s.score,a=s.indices)}if(!a||o===1/0)return null;const n=s.length+1,c=m.RO.lowerBound(a,n,((t,e)=>t-e)),l=a.slice(0,c),h=a.slice(c);for(let t=0,e=h.length;t<e;++t)h[t]-=n;return 0===l.length?{matchType:0,categoryIndices:null,labelIndices:h,score:o,item:t}:0===h.length?{matchType:1,categoryIndices:l,labelIndices:null,score:o,item:t}:{matchType:2,categoryIndices:l,labelIndices:h,score:o,item:t}}class A extends d.Component{constructor(t){super(t),this.updateSearchQuery=t=>{this.setState({searchQuery:t.target.value},(()=>this.setState({filteredShortcutList:this._searchFilterShortcuts(this.state.shortcutList)},(()=>{this.sortShortcuts()}))))},this.resetShortcuts=async()=>{const t=await this.props.external.getAllShortCutSettings();for(const e of Object.keys(t.user))await this.props.external.removeShortCut(e);await this._refreshShortcutList()},this.handleUpdate=async(t,e)=>{const s=await this.props.external.getAllShortCutSettings(),r=s.user.shortcuts,o=[];let a=!1;for(let s of r)s.command===t.commandName&&s.selector===t.selector?(o.push({command:s.command,selector:s.selector,keys:e}),a=!0):o.push(s);a||o.push({command:t.commandName,selector:t.selector,keys:e}),await s.set("shortcuts",o),await this._refreshShortcutList()},this.deleteShortcut=async(t,e)=>{await this.handleUpdate(t,[""]),await this._refreshShortcutList()},this.resetShortcut=async t=>{const e=await this.props.external.getAllShortCutSettings(),s=e.user.shortcuts,r=[];for(let e of s)e.command===t.commandName&&e.selector===t.selector||r.push(e);await e.set("shortcuts",r),await this._refreshShortcutList()},this.toggleSelectors=()=>{this.setState({showSelectors:!this.state.showSelectors})},this.updateSort=t=>{t!==this.state.currentSort&&this.setState({currentSort:t},this.sortShortcuts)},this.sortConflict=(t,e)=>{const s=this.state.filteredShortcutList;if(0===s.filter((t=>"error_row"===t.id)).length){const r=new f;r.takenBy=e,r.id="error_row",s.splice(s.indexOf(t)+1,0,r),r.hasConflict=!0,this.setState({filteredShortcutList:s})}},this.clearConflicts=()=>{const t=this.state.filteredShortcutList.filter((t=>"error_row"!==t.id));t.forEach((t=>{t.hasConflict=!1})),this.setState({filteredShortcutList:t})},this.contextMenu=(t,e)=>{t.persist(),this.setState({contextMenu:this.props.external.createMenu()},(()=>{t.preventDefault();for(let t of e)this.state.contextMenu.addItem({command:t});this.state.contextMenu.open(t.clientX,t.clientY)}))},this.state={shortcutList:{},filteredShortcutList:new Array,shortcutsFetched:!1,searchQuery:"",showSelectors:!1,currentSort:"category",keyBindingsUsed:{},contextMenu:this.props.external.createMenu()}}componentDidMount(){this._refreshShortcutList()}async _refreshShortcutList(){const t=await this.props.external.getAllShortCutSettings(),e=function(t,e){const s=e.composite.shortcuts;let r={};return s.forEach((e=>{let s=e.command+"_"+e.selector;if(-1!==Object.keys(r).indexOf(s)){let t=r[s].numberOfShortcuts;r[s].keys[t]=e.keys,r[s].numberOfShortcuts++}else{let o=new g;o.commandName=e.command;let a=t.getLabel(e.command);const i=e.command.split(":");a||(a=i.length>1?i[1]:"(Command label missing)"),o.label=a,o.category=i[0],o.keys[0]=e.keys,o.selector=e.selector,o.source="Default",o.id=s,o.numberOfShortcuts=1,r[s]=o}})),e.user.shortcuts.forEach((t=>{const e=t.command+"_"+t.selector;r[e]&&(r[e].source="Custom")})),r}(this.props.external,t);this.setState({shortcutList:e,filteredShortcutList:this._searchFilterShortcuts(e),shortcutsFetched:!0},(()=>{let t=function(t){let e={};return Object.keys(t).forEach((s=>{Object.keys(t[s].keys).forEach((r=>{const o=new C(t[s]);o.takenByKey=r,e[t[s].keys[r].join(" ")+"_"+t[s].selector]=o}))})),e}(e);this.setState({keyBindingsUsed:t}),this.sortShortcuts()}))}_searchFilterShortcuts(t){return function(t,e){e=e.replace(/\s+/g,"").toLowerCase();let s=[],r=Object.keys(t);for(let o=0,a=r.length;o<a;++o){let a=t[r[o]];if(!e){s.push({matchType:3,categoryIndices:null,labelIndices:null,score:0,item:a});continue}let i=N(a,e);i&&s.push(i)}return s}(t,this.state.searchQuery).map((t=>t.item))}sortShortcuts(){const t=this.state.filteredShortcutList;let e=this.state.currentSort;"command"===e&&(e="label"),""!==e&&t.sort(((t,s)=>{const r=t.get(e),o=s.get(e);return r<o?-1:r>o?1:t.label<s.label?-1:t.label>s.label?1:0})),this.setState({filteredShortcutList:t})}render(){return this.state.shortcutsFetched?d.createElement("div",{className:"jp-Shortcuts-ShortcutUI",id:"jp-shortcutui"},d.createElement(x,{updateSearchQuery:this.updateSearchQuery,resetShortcuts:this.resetShortcuts,toggleSelectors:this.toggleSelectors,showSelectors:this.state.showSelectors,updateSort:this.updateSort,currentSort:this.state.currentSort,width:this.props.width,external:this.props.external}),d.createElement(I,{shortcuts:this.state.filteredShortcutList,resetShortcut:this.resetShortcut,handleUpdate:this.handleUpdate,deleteShortcut:this.deleteShortcut,showSelectors:this.state.showSelectors,keyBindingsUsed:this.state.keyBindingsUsed,sortConflict:this.sortConflict,clearConflicts:this.clearConflicts,height:this.props.height,contextMenu:this.contextMenu,external:this.props.external})):null}}const R="@jupyterlab/shortcuts-extension:shortcuts";function L(t,e,s){const{commands:r}=e;return{translator:s,getAllShortCutSettings:()=>t.load(R,!0),removeShortCut:e=>t.remove(R,e),createMenu:()=>new p.v2({commands:r}),hasCommand:t=>r.hasCommand(t),addCommand:(t,e)=>r.addCommand(t,e),getLabel:t=>r.label(t)}}const O={id:R,description:"Adds the keyboard shortcuts editor.",requires:[o.O],optional:[i.gv,n.C],activate:async(t,e,s,r)=>{const o=null!=s?s:i.Sr,n=o.load("jupyterlab"),{commands:h}=t;let p,m,S={};if(r){const s={fieldRenderer:s=>(t=>d.createElement(A,{external:t.external,height:1e3,width:1e3}))({external:L(e,t,o),...s})};r.addRenderer(`${O.id}.shortcuts`,s)}function y(s){const r=t.commands.listCommands().join("\n");m||(m=l.JSONExt.deepCopy(s.properties.shortcuts.default)),S={},s.properties.shortcuts.default=Object.keys(e.plugins).map((t=>{const s=e.plugins[t].schema["jupyter.lab.shortcuts"]||[];return S[t]=s,s})).concat([m]).reduce(((t,e)=>u.t4.IS_MAC?t.concat(e):t.concat(e.filter((t=>!t.keys.some((t=>{const{cmd:e}=c.H.parseKeystroke(t);return e})))))),[]).sort(((t,e)=>t.command.localeCompare(e.command))),s.properties.shortcuts.description=n.__('Note: To disable a system default shortcut,\ncopy it to User Preferences and add the\n"disabled" key, for example:\n{\n    "command": "application:activate-next-tab",\n    "keys": [\n        "Ctrl Shift ]"\n    ],\n    "selector": "body",\n    "disabled": true\n}\n\nList of commands followed by keyboard shortcuts:\n%1\n\nList of keyboard shortcuts:',r)}e.pluginChanged.connect((async(t,s)=>{if(s!==O.id){const t=S[s],r=e.plugins[s].schema["jupyter.lab.shortcuts"]||[];void 0!==t&&l.JSONExt.deepEqual(t,r)||(p=null,e.plugins[O.id].schema.properties.shortcuts.default=m,await e.load(O.id,!0))}})),e.transform(O.id,{compose:t=>{var e,s,r,o;p||(p=l.JSONExt.deepCopy(t.schema),y(p));const i=null!==(r=null===(s=null===(e=p.properties)||void 0===e?void 0:e.shortcuts)||void 0===s?void 0:s.default)&&void 0!==r?r:[],n={shortcuts:null!==(o=t.data.user.shortcuts)&&void 0!==o?o:[]},c={shortcuts:a.tC.reconcileShortcuts(i,n.shortcuts)};return t.data={composite:c,user:n},t},fetch:t=>(p||(p=l.JSONExt.deepCopy(t.schema),y(p)),{data:t.data,id:t.id,raw:t.raw,schema:p,version:t.version})});try{p=null;const t=await e.load(O.id);U.loadShortcuts(h,t.composite),t.changed.connect((()=>{U.loadShortcuts(h,t.composite)}))}catch(t){console.error(`Loading ${O.id} failed.`,t)}},autoStart:!0},B=O;var U;!function(t){let e;t.loadShortcuts=function(t,s){var r;const o=null!==(r=null==s?void 0:s.shortcuts)&&void 0!==r?r:[];e&&e.dispose(),e=o.reduce(((e,s)=>{const r=function(t){if(!t||"object"!=typeof t)return;const{isArray:e}=Array;return"command"in t&&"keys"in t&&"selector"in t&&e(t.keys)?t:void 0}(s);return r&&e.add(t.addKeyBinding(r)),e}),new h.DisposableSet)}}(U||(U={}))},56276:(t,e,s)=>{s.d(e,{C:()=>o,E:()=>a});var r=s(47963);const o=new r.Token("@jupyterlab/ui-components:IFormRendererRegistry","A service for settings form renderer registration."),a=new r.Token("@jupyterlab/ui-components:ILabIconManager","A service to register and request icons.")}}]);