"use strict";(self.webpackChunk_datalayer_jupyter_contents=self.webpackChunk_datalayer_jupyter_contents||[]).push([[4484],{27167:(e,t,n)=>{n.r(t),n.d(t,{KERNEL_SETTINGS_SCHEMA:()=>f,default:()=>v});var l,s,o=n(1865),i=n(51954),r=n(92154),a=n(44406),h=n.n(a),c=n(97930);new c.Token("@jupyterlite/contents:IContents"),function(e){e.JSON="application/json",e.PLAIN_TEXT="text/plain",e.OCTET_STREAM="octet/stream"}(l||(l={})),function(e){const t=JSON.parse(o.PageConfig.getOption("fileTypes")||"{}");e.getType=function(e,n=null){e=e.toLowerCase();for(const n of Object.values(t))for(const t of n.extensions||[])if(t===e&&n.mimeTypes&&n.mimeTypes.length)return n.mimeTypes[0];return h().getType(e)||n||l.OCTET_STREAM},e.hasFormat=function(e,n){e=e.toLowerCase();for(const l of Object.values(t))if(l.fileFormat===n)for(const t of l.extensions||[])if(t===e)return!0;return!1}}(s||(s={}));const p=new c.Token("@jupyterlite/contents:IBroadcastChannelWrapper"),d=n.p+"schema/kernel.v0.schema.json";var f=n.t(d);const y=`data:image/svg+xml;base64,${btoa('<?xml version="1.0" encoding="UTF-8"?>\n<svg width="182" height="182" data-name="Layer 1" version="1.1" viewBox="0 0 182 182" xmlns="http://www.w3.org/2000/svg">\n <defs>\n  <style>.cls-1 {\n        fill: #fff;\n      }\n\n      .cls-2 {\n        fill: #654ff0;\n      }</style>\n </defs>\n <rect width="182" height="182" fill="#fff" stop-color="#000000" style="paint-order:stroke fill markers"/>\n <rect class="cls-1" x="107" y="125" width="50" height="32"/>\n <path class="cls-2" d="m135.18 97c0-0.13-0.01-7.24-0.02-7.37h27.51v71.33h-71.34v-71.33h27.51c0 0.13-0.02 7.24-0.02 7.37m32.59 56.33h4.9l-7.43-25.25h-7.45l-6.12 25.25h4.75l1.24-5.62h8.49l1.61 5.62zm-26.03 0h4.69l6.02-25.25h-4.63l-3.69 17.4h-0.06l-3.5-17.4h-4.42l-3.9 17.19h-0.06l-3.23-17.19h-4.72l5.44 25.25h4.78l3.75-17.19h0.06zm18.89-19.03h1.99l2.37 9.27h-6.42z"/>\n <path d="m89 49.66c0 10.6-8.8 20-20 20h-40v20h-10v-70h50c10.7 0 19.7 8.9 20 20zm-10-10c0-5.5-4.5-10-10-10h-40v30h40c5.5 0 10-4.5 10-10z"/>\n <path d="m132 67.66v22h-10v-22l-30-33v-15h10v10.9l25 27.5 25-27.5v-10.9h10v15z"/>\n</svg>\n')}`,u="@jupyterlite/pyodide-kernel-extension:kernel",v=[{id:u,autoStart:!0,requires:[r.qP],optional:[i.f,p],activate:(e,t,l,s)=>{const i=JSON.parse(o.PageConfig.getOption("litePluginSettings")||"{}")[u]||{},r=i.pyodideUrl||"https://cdn.jsdelivr.net/pyodide/v0.25.0/full/pyodide.js",a=o.URLExt.parse(r).href,h=i.pipliteWheelUrl?o.URLExt.parse(i.pipliteWheelUrl).href:void 0,c=(i.pipliteUrls||[]).map((e=>o.URLExt.parse(e).href)),p=!!i.disablePyPIFallback;t.register({spec:{name:"python",display_name:"Python (Pyodide)",language:"python",argv:[],resources:{"logo-32x32":y,"logo-64x64":y}},create:async e=>{const{PyodideKernel:t}=await Promise.all([n.e(3353),n.e(5726)]).then(n.bind(n,99878)),o=!(!(null==l?void 0:l.enabled)||!(null==s?void 0:s.enabled));return o?console.info("Pyodide contents will be synced with Jupyter Contents"):console.warn("Pyodide contents will NOT be synced with Jupyter Contents"),new t({...e,pyodideUrl:a,pipliteWheelUrl:h,pipliteUrls:c,disablePyPIFallback:p,mountDrive:o})}})}}]}}]);