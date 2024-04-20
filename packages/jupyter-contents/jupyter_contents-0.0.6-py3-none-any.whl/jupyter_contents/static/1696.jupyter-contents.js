"use strict";(self.webpackChunk_datalayer_jupyter_contents=self.webpackChunk_datalayer_jupyter_contents||[]).push([[1696],{31696:(e,t,n)=>{function r(e){for(var t={},n=e.split(" "),r=0;r<n.length;++r)t[n[r]]=!0;return t}n.r(t),n.d(t,{ecl:()=>v});var a,o=r("abs acos allnodes ascii asin asstring atan atan2 ave case choose choosen choosesets clustersize combine correlation cos cosh count covariance cron dataset dedup define denormalize distribute distributed distribution ebcdic enth error evaluate event eventextra eventname exists exp failcode failmessage fetch fromunicode getisvalid global graph group hash hash32 hash64 hashcrc hashmd5 having if index intformat isvalid iterate join keyunicode length library limit ln local log loop map matched matchlength matchposition matchtext matchunicode max merge mergejoin min nolocal nonempty normalize parse pipe power preload process project pull random range rank ranked realformat recordof regexfind regexreplace regroup rejected rollup round roundup row rowdiff sample set sin sinh sizeof soapcall sort sorted sqrt stepped stored sum table tan tanh thisnode topn tounicode transfer trim truncate typeof ungroup unicodeorder variance which workunit xmldecode xmlencode xmltext xmlunicode"),i=r("apply assert build buildindex evaluate fail keydiff keypatch loadxml nothor notify output parallel sequential soapcall wait"),l=r("__compressed__ all and any as atmost before beginc++ best between case const counter csv descend encrypt end endc++ endmacro except exclusive expire export extend false few first flat from full function group header heading hole ifblock import in interface joined keep keyed last left limit load local locale lookup macro many maxcount maxlength min skew module named nocase noroot noscan nosort not of only opt or outer overwrite packed partition penalty physicallength pipe quote record relationship repeat return right scan self separator service shared skew skip sql store terminator thor threshold token transform trim true type unicodeorder unsorted validate virtual whole wild within xml xpath"),s=r("ascii big_endian boolean data decimal ebcdic integer pattern qstring real record rule set of string token udecimal unicode unsigned varstring varunicode"),u=r("checkpoint deprecated failcode failmessage failure global independent onwarning persist priority recovery stored success wait when"),c=r("catch class do else finally for if switch try while"),p=r("true false null"),d={"#":function(e,t){return!!t.startOfLine&&(e.skipToEnd(),"meta")}},m=/[+\-*&%=<>!?|\/]/;function f(e,t){var n,r=e.next();if(d[r]){var y=d[r](e,t);if(!1!==y)return y}if('"'==r||"'"==r)return t.tokenize=(n=r,function(e,t){for(var r,a=!1,o=!1;null!=(r=e.next());){if(r==n&&!a){o=!0;break}a=!a&&"\\"==r}return!o&&a||(t.tokenize=f),"string"}),t.tokenize(e,t);if(/[\[\]{}\(\),;\:\.]/.test(r))return a=r,null;if(/\d/.test(r))return e.eatWhile(/[\w\.]/),"number";if("/"==r){if(e.eat("*"))return t.tokenize=h,h(e,t);if(e.eat("/"))return e.skipToEnd(),"comment"}if(m.test(r))return e.eatWhile(m),"operator";e.eatWhile(/[\w\$_]/);var g=e.current().toLowerCase();if(o.propertyIsEnumerable(g))return c.propertyIsEnumerable(g)&&(a="newstatement"),"keyword";if(i.propertyIsEnumerable(g))return c.propertyIsEnumerable(g)&&(a="newstatement"),"variable";if(l.propertyIsEnumerable(g))return c.propertyIsEnumerable(g)&&(a="newstatement"),"modifier";if(s.propertyIsEnumerable(g))return c.propertyIsEnumerable(g)&&(a="newstatement"),"type";if(u.propertyIsEnumerable(g))return c.propertyIsEnumerable(g)&&(a="newstatement"),"builtin";for(var b=g.length-1;b>=0&&(!isNaN(g[b])||"_"==g[b]);)--b;if(b>0){var v=g.substr(0,b+1);if(s.propertyIsEnumerable(v))return c.propertyIsEnumerable(v)&&(a="newstatement"),"type"}return p.propertyIsEnumerable(g)?"atom":null}function h(e,t){for(var n,r=!1;n=e.next();){if("/"==n&&r){t.tokenize=f;break}r="*"==n}return"comment"}function y(e,t,n,r,a){this.indented=e,this.column=t,this.type=n,this.align=r,this.prev=a}function g(e,t,n){return e.context=new y(e.indented,t,n,null,e.context)}function b(e){var t=e.context.type;return")"!=t&&"]"!=t&&"}"!=t||(e.indented=e.context.indented),e.context=e.context.prev}const v={name:"ecl",startState:function(e){return{tokenize:null,context:new y(-e,0,"top",!1),indented:0,startOfLine:!0}},token:function(e,t){var n=t.context;if(e.sol()&&(null==n.align&&(n.align=!1),t.indented=e.indentation(),t.startOfLine=!0),e.eatSpace())return null;a=null;var r=(t.tokenize||f)(e,t);if("comment"==r||"meta"==r)return r;if(null==n.align&&(n.align=!0),";"!=a&&":"!=a||"statement"!=n.type)if("{"==a)g(t,e.column(),"}");else if("["==a)g(t,e.column(),"]");else if("("==a)g(t,e.column(),")");else if("}"==a){for(;"statement"==n.type;)n=b(t);for("}"==n.type&&(n=b(t));"statement"==n.type;)n=b(t)}else a==n.type?b(t):("}"==n.type||"top"==n.type||"statement"==n.type&&"newstatement"==a)&&g(t,e.column(),"statement");else b(t);return t.startOfLine=!1,r},indent:function(e,t,n){if(e.tokenize!=f&&null!=e.tokenize)return 0;var r=e.context,a=t&&t.charAt(0);"statement"==r.type&&"}"==a&&(r=r.prev);var o=a==r.type;return"statement"==r.type?r.indented+("{"==a?0:n.unit):r.align?r.column+(o?0:1):r.indented+(o?0:n.unit)},languageData:{indentOnInput:/^\s*[{}]$/}}}}]);