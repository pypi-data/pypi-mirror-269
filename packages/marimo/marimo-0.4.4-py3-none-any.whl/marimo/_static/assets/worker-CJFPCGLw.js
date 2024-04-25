var ye=Object.defineProperty;var pe=(m,f,g)=>f in m?ye(m,f,{enumerable:!0,configurable:!0,writable:!0,value:g}):m[f]=g;var p=(m,f,g)=>(pe(m,typeof f!="symbol"?f+"":f,g),g);(function(){"use strict";function m(e){return e.FS}const f="notebook.py";async function g(e){const{pyodide:t,filename:n,code:s}=e,a=m(t),d="/marimo";await a.mkdir(d),await a.mount(t.FS.filesystems.IDBFS,{root:"."},d),await T(t,!0),a.chdir(d);const M=u=>{try{return a.readFile(u,{encoding:"utf8"})}catch{return null}};if(n&&n!==f){const u=M(n);if(u)return{content:u,filename:n}}return a.writeFile(f,s),{content:s,filename:f}}function T(e,t){return new Promise((n,s)=>{m(e).syncfs(t,a=>{if(a){s(a);return}n()})})}const v={debug:(...e)=>{},log:(...e)=>{console.log(...e)},warn:(...e)=>{console.warn(...e)},error:(...e)=>{console.error(...e)}};function J(){return typeof window<"u"&&window.Logger||v}const I=J();function x(e,t){if(!e)throw new Error(t)}function L(e){return e?e==="local"?"http://localhost:8000/dist/marimo-0.4.2-py3-none-any.whl":e==="latest"?"marimo":`marimo==${e}`:"marimo >= 0.3.0"}class W{constructor(){p(this,"pyodide",null)}get requirePyodide(){return x(this.pyodide,"Pyodide not loaded"),this.pyodide}async bootstrap(t){const n=await this.loadPyoideAndPackages(),{version:s}=t;return s.includes("dev")&&await this.installDevMarimo(n,s),await this.installMarimoAndDeps(n,s),n}async loadPyoideAndPackages(){if(!loadPyodide)throw new Error("loadPyodide is not defined");const t=await loadPyodide({packages:["micropip","docutils","Pygments","jedi","pyodide-http"],indexURL:"https://cdn.jsdelivr.net/pyodide/v0.25.0/full/"});return this.pyodide=t,t}async installDevMarimo(t,n){await t.runPythonAsync(`
      import micropip

      await micropip.install(
        [
          "${L(n)}",
        ],
        deps=False,
        index_urls="https://test.pypi.org/pypi/{package_name}/json"
        );
      `)}async installMarimoAndDeps(t,n){await t.runPythonAsync(`
      import micropip

      await micropip.install(
        [
          "${L(n)}",
          "markdown",
          "pymdown-extensions",
        ],
        deps=False,
        );
      `)}mountFilesystem(t){return g({pyodide:this.requirePyodide,...t})}async startSession(t){const{filename:n,content:s}=await this.mountFilesystem({code:t.code,filename:t.filename});return self.messenger={callback:t.onMessage},self.query_params=t.queryParameters,self.user_config=t.userConfig,await this.requirePyodide.loadPackagesFromImports(s,{messageCallback:I.log,errorCallback:I.error}),await this.requirePyodide.runPythonAsync(`
      print("[py] Starting marimo...")
      import asyncio
      import js
      from marimo._pyodide.pyodide_session import create_session, instantiate

      assert js.messenger, "messenger is not defined"
      assert js.query_params, "query_params is not defined"

      session, bridge = create_session(
        filename="${n}",
        query_params=js.query_params.to_py(),
        message_callback=js.messenger.callback,
        user_config=js.user_config.to_py(),
      )
      instantiate(session)
      asyncio.create_task(session.start())

      bridge`)}}class K{constructor(){p(this,"promise");p(this,"resolve");p(this,"reject");this.promise=new Promise((t,n)=>{this.reject=n,this.resolve=t})}}class X{constructor(t){p(this,"buffer");p(this,"started",!1);p(this,"push",t=>{this.started?this.onMessage(t):this.buffer.push(t)});p(this,"start",()=>{this.started=!0,this.buffer.forEach(t=>this.onMessage(t)),this.buffer=[]});this.onMessage=t,this.buffer=[]}}function A(e){if(!e)return"Unknown error";if(e instanceof Error)return Q(e.message);try{return JSON.stringify(e)}catch{return String(e)}}function Q(e){try{const t=JSON.parse(e);if(!t)return e;if(typeof t=="object"&&"detail"in t&&typeof t.detail=="string")return t.detail}catch{}return e}function me(e){return e}const V=1e10,G=1e3;function S(e,t){const n=e.map(s=>`"${s}"`).join(", ");return new Error(`This RPC instance cannot ${t} because the transport did not provide one or more of these methods: ${n}`)}function Y(e={}){let t={};function n(r){t=r}let s={};function a(r){var o;s.unregisterHandler&&s.unregisterHandler(),s=r,(o=s.registerHandler)==null||o.call(s,fe)}let d;function M(r){if(typeof r=="function"){d=r;return}d=(o,c)=>{const i=r[o];if(i)return i(c);const l=r._;if(!l)throw new Error(`The requested method has no handler: ${o}`);return l(o,c)}}const{maxRequestTime:u=G}=e;e.transport&&a(e.transport),e.requestHandler&&M(e.requestHandler),e._debugHooks&&n(e._debugHooks);let w=0;function F(){return w<=V?++w:w=0}const R=new Map,b=new Map;function k(r,...o){const c=o[0];return new Promise((i,l)=>{var E;if(!s.send)throw S(["send"],"make requests");const y=F(),P={type:"request",id:y,method:r,params:c};R.set(y,{resolve:i,reject:l}),u!==1/0&&b.set(y,setTimeout(()=>{b.delete(y),l(new Error("RPC request timed out."))},u)),(E=t.onSend)==null||E.call(t,P),s.send(P)})}const N=new Proxy(k,{get:(r,o,c)=>o in r?Reflect.get(r,o,c):i=>k(o,i)}),O=N;function B(r,...o){var l;const c=o[0];if(!s.send)throw S(["send"],"send messages");const i={type:"message",id:r,payload:c};(l=t.onSend)==null||l.call(t,i),s.send(i)}const U=new Proxy(B,{get:(r,o,c)=>o in r?Reflect.get(r,o,c):i=>B(o,i)}),z=U,h=new Map,C=new Set;function le(r,o){var c;if(!s.registerHandler)throw S(["registerHandler"],"register message listeners");if(r==="*"){C.add(o);return}h.has(r)||h.set(r,new Set),(c=h.get(r))==null||c.add(o)}function ue(r,o){var c,i;if(r==="*"){C.delete(o);return}(c=h.get(r))==null||c.delete(o),((i=h.get(r))==null?void 0:i.size)===0&&h.delete(r)}async function fe(r){var o,c;if((o=t.onReceive)==null||o.call(t,r),!("type"in r))throw new Error("Message does not contain a type.");if(r.type==="request"){if(!s.send||!d)throw S(["send","requestHandler"],"handle requests");const{id:i,method:l,params:y}=r;let P;try{P={type:"response",id:i,success:!0,payload:await d(l,y)}}catch(E){if(!(E instanceof Error))throw E;P={type:"response",id:i,success:!1,error:E.message}}(c=t.onSend)==null||c.call(t,P),s.send(P);return}if(r.type==="response"){const i=b.get(r.id);i!=null&&clearTimeout(i);const{resolve:l,reject:y}=R.get(r.id)??{};r.success?l==null||l(r.payload):y==null||y(new Error(r.error));return}if(r.type==="message"){for(const l of C)l(r.id,r.payload);const i=h.get(r.id);if(!i)return;for(const l of i)l(r.payload);return}throw new Error(`Unexpected RPC message type: ${r.type}`)}return{setTransport:a,setRequestHandler:M,request:N,requestProxy:O,send:U,sendProxy:z,addMessageListener:le,removeMessageListener:ue,proxy:{send:z,request:O},_setDebugHooks:n}}function Z(e){return Y(e)}const D="[transport-id]";function ee(e,t){const{transportId:n}=t;return n!=null?{[D]:n,data:e}:e}function te(e,t){const{transportId:n,filter:s}=t,a=s==null?void 0:s();if(n!=null&&a!=null)throw new Error("Cannot use both `transportId` and `filter` at the same time");let d=e;if(n){if(e[D]!==n)return[!0];d=e.data}return a===!1?[!0]:[!1,d]}function re(e,t={}){const{transportId:n,filter:s,remotePort:a}=t,d=e,M=a??e;let u;return{send(w){M.postMessage(ee(w,{transportId:n}))},registerHandler(w){u=F=>{const R=F.data,[b,k]=te(R,{transportId:n,filter:()=>s==null?void 0:s(F)});b||w(k)},d.addEventListener("message",u)},unregisterHandler(){u&&d.removeEventListener("message",u)}}}function ne(e){return re(self,e)}const se="marimo-transport";async function oe(){await import("https://cdn.jsdelivr.net/pyodide/v0.25.0/full/pyodide.js");try{const e=de(),t=await ie(e);self.controller=t,self.pyodide=await t.bootstrap({version:e})}catch(e){console.error("Error bootstrapping",e),q.send.initializedError({error:A(e)})}}async function ie(e){try{return await import(`/wasm/controller.js?version=${e}`)}catch{return new W}}const _=oe(),j=new X(e=>{q.send.kernelMessage({message:e})}),H=new K;let $=!1;const ae={startSession:async e=>{if(await _,$){I.warn("Session already started");return}$=!0;try{x(self.controller,"Controller not loaded");const t=await self.controller.startSession({code:e.code,filename:e.filename,queryParameters:e.queryParameters,userConfig:e.userConfig,onMessage:j.push});H.resolve(t),q.send.initialized({})}catch(t){q.send.initializedError({error:A(t)})}},loadPackages:async e=>{await _,await self.pyodide.loadPackagesFromImports(e,{messageCallback:console.log,errorCallback:console.error})},readFile:async e=>(await _,self.pyodide.FS.readFile(e,{encoding:"utf8"})),setInterruptBuffer:async e=>{await _,self.pyodide.setInterruptBuffer(e)},bridge:async e=>{await _;const{functionName:t,payload:n}=e;t==="format"&&await self.pyodide.runPythonAsync(`
        import micropip

        try:
          import black
        except ModuleNotFoundError:
          await micropip.install("black")
        `);const s=await H.promise,a=n==null?null:typeof n=="string"?n:JSON.stringify(n),d=a==null?await s[t]():await s[t](a);return ce.has(t)&&T(self.pyodide,!1),typeof d=="string"?JSON.parse(d):d}},q=Z({transport:ne({transportId:se}),requestHandler:ae});q.send("ready",{}),q.addMessageListener("consumerReady",async()=>{await _,j.start()});const ce=new Set(["save","save_app_config","rename_file","create_file_or_directory","delete_file_or_directory","move_file_or_directory","update_file"]);function de(){return self.name}})();
