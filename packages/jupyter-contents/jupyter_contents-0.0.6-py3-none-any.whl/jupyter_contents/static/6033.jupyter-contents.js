"use strict";(self.webpackChunk_datalayer_jupyter_contents=self.webpackChunk_datalayer_jupyter_contents||[]).push([[6033],{6033:(e,t,n)=>{function r(e){for(var t={},n=e.split(","),r=0;r<n.length;++r){var i=n[r].toUpperCase(),o=n[r].charAt(0).toUpperCase()+n[r].slice(1);t[n[r]]=!0,t[i]=!0,t[o]=!0}return t}function i(e){return e.eatWhile(/[\w\$_]/),"meta"}n.r(t),n.d(t,{vhdl:()=>y});var o,a=r("null"),l={"`":i,$:i},u=r("abs,access,after,alias,all,and,architecture,array,assert,attribute,begin,block,body,buffer,bus,case,component,configuration,constant,disconnect,downto,else,elsif,end,end block,end case,end component,end for,end generate,end if,end loop,end process,end record,end units,entity,exit,file,for,function,generate,generic,generic map,group,guarded,if,impure,in,inertial,inout,is,label,library,linkage,literal,loop,map,mod,nand,new,next,nor,null,of,on,open,or,others,out,package,package body,port,port map,postponed,procedure,process,pure,range,record,register,reject,rem,report,return,rol,ror,select,severity,signal,sla,sll,sra,srl,subtype,then,to,transport,type,unaffected,units,until,use,variable,wait,when,while,with,xnor,xor"),s=r("architecture,entity,begin,case,port,else,elsif,end,for,function,if"),c=/[&|~><!\)\(*#%@+\/=?\:;}{,\.\^\-\[\]]/;function p(e,t){var n,r=e.next();if(l[r]){var i=l[r](e,t);if(!1!==i)return i}if('"'==r)return t.tokenize=(n=r,function(e,t){for(var r,i=!1,o=!1;null!=(r=e.next());){if(r==n&&!i){o=!0;break}i=!i&&"--"==r}return(o||!i&&!0)&&(t.tokenize=p),"string.special"}),t.tokenize(e,t);if("'"==r)return t.tokenize=function(e){return function(t,n){for(var r,i=!1,o=!1;null!=(r=t.next());){if(r==e&&!i){o=!0;break}i=!i&&"--"==r}return(o||!i&&!0)&&(n.tokenize=p),"string"}}(r),t.tokenize(e,t);if(/[\[\]{}\(\),;\:\.]/.test(r))return o=r,null;if(/[\d']/.test(r))return e.eatWhile(/[\w\.']/),"number";if("-"==r&&e.eat("-"))return e.skipToEnd(),"comment";if(c.test(r))return e.eatWhile(c),"operator";e.eatWhile(/[\w\$_]/);var f=e.current();return u.propertyIsEnumerable(f.toLowerCase())?(s.propertyIsEnumerable(f)&&(o="newstatement"),"keyword"):a.propertyIsEnumerable(f)?"atom":"variable"}function f(e,t,n,r,i){this.indented=e,this.column=t,this.type=n,this.align=r,this.prev=i}function d(e,t,n){return e.context=new f(e.indented,t,n,null,e.context)}function m(e){var t=e.context.type;return")"!=t&&"]"!=t&&"}"!=t||(e.indented=e.context.indented),e.context=e.context.prev}const y={name:"vhdl",startState:function(e){return{tokenize:null,context:new f(-e,0,"top",!1),indented:0,startOfLine:!0}},token:function(e,t){var n=t.context;if(e.sol()&&(null==n.align&&(n.align=!1),t.indented=e.indentation(),t.startOfLine=!0),e.eatSpace())return null;o=null;var r=(t.tokenize||p)(e,t);if("comment"==r||"meta"==r)return r;if(null==n.align&&(n.align=!0),";"!=o&&":"!=o||"statement"!=n.type)if("{"==o)d(t,e.column(),"}");else if("["==o)d(t,e.column(),"]");else if("("==o)d(t,e.column(),")");else if("}"==o){for(;"statement"==n.type;)n=m(t);for("}"==n.type&&(n=m(t));"statement"==n.type;)n=m(t)}else o==n.type?m(t):("}"==n.type||"top"==n.type||"statement"==n.type&&"newstatement"==o)&&d(t,e.column(),"statement");else m(t);return t.startOfLine=!1,r},indent:function(e,t,n){if(e.tokenize!=p&&null!=e.tokenize)return 0;var r=t&&t.charAt(0),i=e.context,o=r==i.type;return"statement"==i.type?i.indented+("{"==r?0:n.unit):i.align?i.column+(o?0:1):i.indented+(o?0:n.unit)},languageData:{indentOnInput:/^\s*[{}]$/,commentTokens:{line:"--"}}}}}]);