import { c as Xn, a as Yn, g as Hn } from "./module-2c3384e6.js";
const Ot = /* @__PURE__ */ new Set(), Zn = Xn({
  deregister: ({ call: e }) => (t) => e("deregister", { port: t }, [t]),
  encode: ({ call: e }) => async (t, n) => {
    const r = await e("encode", { encoderId: t, timeslice: n });
    return Ot.delete(t), r;
  },
  instantiate: ({ call: e }) => async (t, n) => {
    const r = Yn(Ot), o = await e("instantiate", { encoderId: r, mimeType: t, sampleRate: n });
    return { encoderId: r, port: o };
  },
  register: ({ call: e }) => (t) => e("register", { port: t }, [t])
}), Kn = (e) => {
  const t = new Worker(e);
  return Zn(t);
}, Qn = `(()=>{var e={455:function(e,t){!function(e){"use strict";var t=function(e){return function(t){var r=e(t);return t.add(r),r}},r=function(e){return function(t,r){return e.set(t,r),r}},n=void 0===Number.MAX_SAFE_INTEGER?9007199254740991:Number.MAX_SAFE_INTEGER,o=536870912,s=2*o,a=function(e,t){return function(r){var a=t.get(r),i=void 0===a?r.size:a<s?a+1:0;if(!r.has(i))return e(r,i);if(r.size<o){for(;r.has(i);)i=Math.floor(Math.random()*s);return e(r,i)}if(r.size>n)throw new Error("Congratulations, you created a collection of unique numbers which uses all available integers!");for(;r.has(i);)i=Math.floor(Math.random()*n);return e(r,i)}},i=new WeakMap,c=r(i),l=a(c,i),d=t(l);e.addUniqueNumber=d,e.generateUniqueNumber=l}(t)}},t={};function r(n){var o=t[n];if(void 0!==o)return o.exports;var s=t[n]={exports:{}};return e[n].call(s.exports,s,s.exports,r),s.exports}(()=>{"use strict";var e=r(455);const t=new WeakMap,n=new WeakMap,o=(r=>{const o=(s=r,{...s,connect:e=>{let{call:r}=e;return async()=>{const{port1:e,port2:n}=new MessageChannel,o=await r("connect",{port:e},[e]);return t.set(n,o),n}},disconnect:e=>{let{call:r}=e;return async e=>{const n=t.get(e);if(void 0===n)throw new Error("The given port is not connected.");await r("disconnect",{portId:n})}},isSupported:e=>{let{call:t}=e;return()=>t("isSupported")}});var s;return t=>{const r=(e=>{if(n.has(e))return n.get(e);const t=new Map;return n.set(e,t),t})(t);t.addEventListener("message",(e=>{let{data:t}=e;const{id:n}=t;if(null!==n&&r.has(n)){const{reject:e,resolve:o}=r.get(n);r.delete(n),void 0===t.error?o(t.result):e(new Error(t.error.message))}})),(e=>"function"==typeof e.start)(t)&&t.start();const s=function(n){let o=arguments.length>1&&void 0!==arguments[1]?arguments[1]:null,s=arguments.length>2&&void 0!==arguments[2]?arguments[2]:[];return new Promise(((a,i)=>{const c=(0,e.generateUniqueNumber)(r);r.set(c,{reject:i,resolve:a}),null===o?t.postMessage({id:c,method:n},s):t.postMessage({id:c,method:n,params:o},s)}))},a=function(e,r){let n=arguments.length>2&&void 0!==arguments[2]?arguments[2]:[];t.postMessage({id:null,method:e,params:r},n)};let i={};for(const[e,t]of Object.entries(o))i={...i,[e]:t({call:s,notify:a})};return{...i}}})({characterize:e=>{let{call:t}=e;return()=>t("characterize")},encode:e=>{let{call:t}=e;return(e,r)=>t("encode",{recordingId:e,timeslice:r})},record:e=>{let{call:t}=e;return async(e,r,n)=>{await t("record",{recordingId:e,sampleRate:r,typedArrays:n},n.map((e=>{let{buffer:t}=e;return t})))}}}),s=-32603,a=-32602,i=-32601,c=(e,t)=>Object.assign(new Error(e),{status:t}),l=e=>c('The handler of the method called "'.concat(e,'" returned an unexpected result.'),s),d=(e,t)=>async r=>{let{data:{id:n,method:o,params:a}}=r;const d=t[o];try{if(void 0===d)throw(e=>c('The requested method called "'.concat(e,'" is not supported.'),i))(o);const t=void 0===a?d():d(a);if(void 0===t)throw(e=>c('The handler of the method called "'.concat(e,'" returned no required result.'),s))(o);const r=t instanceof Promise?await t:t;if(null===n){if(void 0!==r.result)throw l(o)}else{if(void 0===r.result)throw l(o);const{result:t,transferables:s=[]}=r;e.postMessage({id:n,result:t},s)}}catch(t){const{message:r,status:o=-32603}=t;e.postMessage({error:{code:o,message:r},id:n})}},u=new Map,h=(t,r,n)=>({...r,connect:n=>{let{port:o}=n;o.start();const s=t(o,r),a=(0,e.generateUniqueNumber)(u);return u.set(a,(()=>{s(),o.close(),u.delete(a)})),{result:a}},disconnect:e=>{let{portId:t}=e;const r=u.get(t);if(void 0===r)throw(e=>c('The specified parameter called "portId" with the given value "'.concat(e,'" does not identify a port connected to this worker.'),a))(t);return r(),{result:null}},isSupported:async()=>{if(await new Promise((e=>{const t=new ArrayBuffer(0),{port1:r,port2:n}=new MessageChannel;r.onmessage=t=>{let{data:r}=t;return e(null!==r)},n.postMessage(t,[t])}))){const e=n();return{result:e instanceof Promise?await e:e}}return{result:!1}}}),f=function(e,t){const r=h(f,t,arguments.length>2&&void 0!==arguments[2]?arguments[2]:()=>!0),n=d(e,r);return e.addEventListener("message",n),()=>e.removeEventListener("message",n)},p=e=>{e.onmessage=null,e.close()},w=new Map,m=new WeakMap,g=((e,t)=>r=>{const n=t.get(r);if(void 0===n)throw new Error("There is no encoder stored which wraps this port.");e.delete(n),t.delete(r)})(w,m),v=new Map,y=(e=>t=>{const r=e.get(t);if(void 0===r)throw new Error("There was no instance of an encoder stored with the given id.");return r})(v),M=((e,t)=>r=>{const n=t(r);return e.delete(r),n})(v,y),E=((e,t)=>r=>{const[n,o,s,a]=t(r);return s?new Promise((t=>{o.onmessage=s=>{let{data:i}=s;0===i.length?(e(o),t(n.encode(r,null))):n.record(r,a,i)}})):n.encode(r,null)})(p,M),b=(e=>t=>{for(const[r,n]of Array.from(e.values()))if(r.test(t))return n;throw new Error("There is no encoder registered which could handle the given mimeType.")})(w),T=((e,t,r)=>(n,o,s)=>{if(t.has(n))throw new Error('There is already an encoder registered with an id called "'.concat(n,'".'));const a=r(o),{port1:i,port2:c}=new MessageChannel,l=[a,i,!0,s];return t.set(n,l),i.onmessage=t=>{let{data:r}=t;0===r.length?(e(i),l[2]=!1):a.record(n,s,r.map((e=>"number"==typeof e?new Float32Array(e):e)))},c})(p,v,b),I=((e,t,r)=>async n=>{const o=r(n),s=await o.characterize(),a=s.toString();if(e.has(a)||t.has(n))throw new Error("There is already an encoder stored which handles exactly the same mime types.");return e.set(a,[s,o]),t.set(n,a),s})(w,m,o),A=(e=>(t,r)=>{const[n]=e(t);return n.encode(t,r)})(y);f(self,{deregister:async e=>{let{port:t}=e;return{result:g(t)}},encode:async e=>{let{encoderId:t,timeslice:r}=e;const n=null===r?await E(t):await A(t,r);return{result:n,transferables:n}},instantiate:e=>{let{encoderId:t,mimeType:r,sampleRate:n}=e;const o=T(t,r,n);return{result:o,transferables:[o]}},register:async e=>{let{port:t}=e;return{result:await I(t)}}})})()})();`, Jn = new Blob([Qn], { type: "application/javascript; charset=utf-8" }), Yt = URL.createObjectURL(Jn), xe = Kn(Yt), er = xe.deregister, Se = xe.encode, Ht = xe.instantiate, tr = xe.register;
URL.revokeObjectURL(Yt);
const nr = (e) => (t, n) => {
  if (e === null)
    throw new Error("A native BlobEvent could not be created.");
  return new e(t, n);
}, rr = (e, t) => (n, r, o) => {
  const s = [];
  let a = r, c = 0;
  for (; c < n.byteLength; )
    if (a === null) {
      const i = t(n, c);
      if (i === null)
        break;
      const { length: u, type: d } = i;
      a = d, c += u;
    } else {
      const i = e(n, c, a, o);
      if (i === null)
        break;
      const { content: u, length: d } = i;
      a = null, c += d, u !== null && s.push(u);
    }
  return { contents: s, currentElementType: a, offset: c };
}, or = (e, t) => class {
  constructor(r = null) {
    this._listeners = /* @__PURE__ */ new WeakMap(), this._nativeEventTarget = r === null ? e() : r;
  }
  addEventListener(r, o, s) {
    if (o !== null) {
      let a = this._listeners.get(o);
      a === void 0 && (a = t(this, o), typeof o == "function" && this._listeners.set(o, a)), this._nativeEventTarget.addEventListener(r, a, s);
    }
  }
  dispatchEvent(r) {
    return this._nativeEventTarget.dispatchEvent(r);
  }
  removeEventListener(r, o, s) {
    const a = o === null ? void 0 : this._listeners.get(o);
    this._nativeEventTarget.removeEventListener(r, a === void 0 ? null : a, s);
  }
}, sr = (e) => () => {
  if (e === null)
    throw new Error("A native EventTarget could not be created.");
  return e.document.createElement("p");
}, ar = (e = "") => {
  try {
    return new DOMException(e, "InvalidModificationError");
  } catch (t) {
    return t.code = 13, t.message = e, t.name = "InvalidModificationError", t;
  }
}, ir = () => {
  try {
    return new DOMException("", "InvalidStateError");
  } catch (e) {
    return e.code = 11, e.name = "InvalidStateError", e;
  }
}, cr = (e) => {
  if (e !== null && // Bug #14: Before v14.1 Safari did not support the BlobEvent.
  e.BlobEvent !== void 0 && e.MediaStream !== void 0 && /*
   * Bug #10: An early experimental implemenation in Safari v14 did not provide the isTypeSupported() function.
   *
   * Bug #17: Safari up to v14.1.2 throttled the processing on hidden tabs if there was no active audio output. This is not tested
   * here but should be covered by the following test, too.
   */
  (e.MediaRecorder === void 0 || e.MediaRecorder.isTypeSupported !== void 0)) {
    if (e.MediaRecorder === void 0)
      return Promise.resolve(!0);
    const t = e.document.createElement("canvas"), n = t.getContext("2d");
    if (n === null || typeof t.captureStream != "function")
      return Promise.resolve(!1);
    const r = t.captureStream();
    return Promise.all([
      /*
       * Bug #5: Up until v70 Firefox did emit a blob of type video/webm when asked to encode a MediaStream with a video track into an
       * audio codec.
       */
      new Promise((o) => {
        const s = "audio/webm";
        try {
          const a = new e.MediaRecorder(r, { mimeType: s });
          a.addEventListener("dataavailable", ({ data: c }) => o(c.type === s)), a.start(), setTimeout(() => a.stop(), 10);
        } catch (a) {
          o(a.name === "NotSupportedError");
        }
      }),
      /*
       * Bug #1 & #2: Up until v83 Firefox fired an error event with an UnknownError when adding or removing a track.
       *
       * Bug #3 & #4: Up until v112 Chrome dispatched an error event without any error.
       *
       * Bug #6: Up until v113 Chrome emitted a blob without any data when asked to encode a MediaStream with a video track as audio.
       * This is not directly tested here as it can only be tested by recording something for a short time. It got fixed at the same
       * time as #7 and #8.
       *
       * Bug #7 & #8: Up until v113 Chrome dispatched the dataavailable and stop events before it dispatched the error event.
       */
      new Promise((o) => {
        const s = new e.MediaRecorder(r);
        let a = !1, c = !1;
        s.addEventListener("dataavailable", () => a = !0), s.addEventListener("error", (i) => {
          o(!a && !c && "error" in i && i.error !== null && typeof i.error == "object" && "name" in i.error && i.error.name !== "UnknownError");
        }), s.addEventListener("stop", () => c = !0), s.start(), n.fillRect(0, 0, 1, 1), r.removeTrack(r.getVideoTracks()[0]);
      })
    ]).then((o) => o.every((s) => s));
  }
  return Promise.resolve(!1);
}, ur = (e, t, n, r, o, s, a) => class extends s {
  constructor(i, u = {}) {
    const { mimeType: d } = u;
    if (a !== null && // Bug #10: Safari does not yet implement the isTypeSupported() method.
    (d === void 0 || a.isTypeSupported !== void 0 && a.isTypeSupported(d))) {
      const l = e(a, i, u);
      super(l), this._internalMediaRecorder = l;
    } else if (d !== void 0 && o.some((l) => l.test(d)))
      super(), a !== null && a.isTypeSupported !== void 0 && a.isTypeSupported("audio/webm;codecs=pcm") ? this._internalMediaRecorder = r(this, a, i, d) : this._internalMediaRecorder = n(this, i, d);
    else
      throw a !== null && e(a, i, u), t();
    this._ondataavailable = null, this._onerror = null, this._onpause = null, this._onresume = null, this._onstart = null, this._onstop = null;
  }
  get mimeType() {
    return this._internalMediaRecorder.mimeType;
  }
  get ondataavailable() {
    return this._ondataavailable === null ? this._ondataavailable : this._ondataavailable[0];
  }
  set ondataavailable(i) {
    if (this._ondataavailable !== null && this.removeEventListener("dataavailable", this._ondataavailable[1]), typeof i == "function") {
      const u = i.bind(this);
      this.addEventListener("dataavailable", u), this._ondataavailable = [i, u];
    } else
      this._ondataavailable = null;
  }
  get onerror() {
    return this._onerror === null ? this._onerror : this._onerror[0];
  }
  set onerror(i) {
    if (this._onerror !== null && this.removeEventListener("error", this._onerror[1]), typeof i == "function") {
      const u = i.bind(this);
      this.addEventListener("error", u), this._onerror = [i, u];
    } else
      this._onerror = null;
  }
  get onpause() {
    return this._onpause === null ? this._onpause : this._onpause[0];
  }
  set onpause(i) {
    if (this._onpause !== null && this.removeEventListener("pause", this._onpause[1]), typeof i == "function") {
      const u = i.bind(this);
      this.addEventListener("pause", u), this._onpause = [i, u];
    } else
      this._onpause = null;
  }
  get onresume() {
    return this._onresume === null ? this._onresume : this._onresume[0];
  }
  set onresume(i) {
    if (this._onresume !== null && this.removeEventListener("resume", this._onresume[1]), typeof i == "function") {
      const u = i.bind(this);
      this.addEventListener("resume", u), this._onresume = [i, u];
    } else
      this._onresume = null;
  }
  get onstart() {
    return this._onstart === null ? this._onstart : this._onstart[0];
  }
  set onstart(i) {
    if (this._onstart !== null && this.removeEventListener("start", this._onstart[1]), typeof i == "function") {
      const u = i.bind(this);
      this.addEventListener("start", u), this._onstart = [i, u];
    } else
      this._onstart = null;
  }
  get onstop() {
    return this._onstop === null ? this._onstop : this._onstop[0];
  }
  set onstop(i) {
    if (this._onstop !== null && this.removeEventListener("stop", this._onstop[1]), typeof i == "function") {
      const u = i.bind(this);
      this.addEventListener("stop", u), this._onstop = [i, u];
    } else
      this._onstop = null;
  }
  get state() {
    return this._internalMediaRecorder.state;
  }
  pause() {
    return this._internalMediaRecorder.pause();
  }
  resume() {
    return this._internalMediaRecorder.resume();
  }
  start(i) {
    return this._internalMediaRecorder.start(i);
  }
  stop() {
    return this._internalMediaRecorder.stop();
  }
  static isTypeSupported(i) {
    return a !== null && // Bug #10: Safari does not yet implement the isTypeSupported() method.
    a.isTypeSupported !== void 0 && a.isTypeSupported(i) || o.some((u) => u.test(i));
  }
}, lr = (e) => e !== null && e.BlobEvent !== void 0 ? e.BlobEvent : null, dr = (e) => e === null || e.MediaRecorder === void 0 ? null : e.MediaRecorder, fr = (e) => (t, n, r) => {
  const o = /* @__PURE__ */ new Map(), s = /* @__PURE__ */ new WeakMap(), a = /* @__PURE__ */ new WeakMap(), c = [], i = new t(n, r), u = /* @__PURE__ */ new WeakMap();
  return i.addEventListener("stop", ({ isTrusted: d }) => {
    d && setTimeout(() => c.shift());
  }), i.addEventListener = /* @__PURE__ */ ((d) => (l, g, w) => {
    let p = g;
    if (typeof g == "function")
      if (l === "dataavailable") {
        const f = [];
        p = (m) => {
          const [[h, A] = [!1, !1]] = c;
          h && !A ? f.push(m) : g.call(i, m);
        }, o.set(g, f), s.set(g, p);
      } else
        l === "error" ? (p = (f) => {
          f instanceof ErrorEvent ? g.call(i, f) : g.call(i, new ErrorEvent("error", { error: f.error }));
        }, a.set(g, p)) : l === "stop" && (p = (f) => {
          for (const [m, h] of o.entries())
            if (h.length > 0) {
              const [A] = h;
              h.length > 1 && Object.defineProperty(A, "data", {
                value: new Blob(h.map(({ data: _ }) => _), { type: A.data.type })
              }), h.length = 0, m.call(i, A);
            }
          g.call(i, f);
        }, u.set(g, p));
    return d.call(i, l, p, w);
  })(i.addEventListener), i.removeEventListener = /* @__PURE__ */ ((d) => (l, g, w) => {
    let p = g;
    if (typeof g == "function") {
      if (l === "dataavailable") {
        o.delete(g);
        const f = s.get(g);
        f !== void 0 && (p = f);
      } else if (l === "error") {
        const f = a.get(g);
        f !== void 0 && (p = f);
      } else if (l === "stop") {
        const f = u.get(g);
        f !== void 0 && (p = f);
      }
    }
    return d.call(i, l, p, w);
  })(i.removeEventListener), i.start = /* @__PURE__ */ ((d) => (l) => {
    if (r.mimeType !== void 0 && r.mimeType.startsWith("audio/") && n.getVideoTracks().length > 0)
      throw e();
    return i.state === "inactive" && c.push([l !== void 0, !0]), l === void 0 ? d.call(i) : d.call(i, l);
  })(i.start), i.stop = /* @__PURE__ */ ((d) => () => {
    i.state !== "inactive" && (c[0][1] = !1), d.call(i);
  })(i.stop), i;
}, et = () => {
  try {
    return new DOMException("", "NotSupportedError");
  } catch (e) {
    return e.code = 9, e.name = "NotSupportedError", e;
  }
}, hr = (e) => (t, n, r, o = 2) => {
  const s = e(t, n);
  if (s === null)
    return s;
  const { length: a, value: c } = s;
  if (r === "master")
    return { content: null, length: a };
  if (n + a + c > t.byteLength)
    return null;
  if (r === "binary") {
    const i = (c / Float32Array.BYTES_PER_ELEMENT - 1) / o, u = Array.from({ length: o }, () => new Float32Array(i));
    for (let d = 0; d < i; d += 1) {
      const l = d * o + 1;
      for (let g = 0; g < o; g += 1)
        u[g][d] = t.getFloat32(n + a + (l + g) * Float32Array.BYTES_PER_ELEMENT, !0);
    }
    return { content: u, length: a + c };
  }
  return { content: null, length: a + c };
}, pr = (e) => (t, n) => {
  const r = e(t, n);
  if (r === null)
    return r;
  const { length: o, value: s } = r;
  return s === 35 ? { length: o, type: "binary" } : s === 46 || s === 97 || s === 88713574 || s === 106212971 || s === 139690087 || s === 172351395 || s === 256095861 ? { length: o, type: "master" } : { length: o, type: "unknown" };
}, mr = (e) => (t, n) => {
  const r = e(t, n);
  if (r === null)
    return r;
  const o = n + Math.floor((r - 1) / 8);
  if (o + r > t.byteLength)
    return null;
  let a = t.getUint8(o) & (1 << 8 - r % 8) - 1;
  for (let c = 1; c < r; c += 1)
    a = (a << 8) + t.getUint8(o + c);
  return { length: r, value: a };
}, kt = Symbol.observable || "@@observable";
function gr(e) {
  return Symbol.observable || (typeof e == "function" && e.prototype && e.prototype[Symbol.observable] ? (e.prototype[kt] = e.prototype[Symbol.observable], delete e.prototype[Symbol.observable]) : (e[kt] = e[Symbol.observable], delete e[Symbol.observable])), e;
}
const Ne = () => {
}, It = (e) => {
  throw e;
};
function wr(e) {
  return e ? e.next && e.error && e.complete ? e : {
    complete: (e.complete ?? Ne).bind(e),
    error: (e.error ?? It).bind(e),
    next: (e.next ?? Ne).bind(e)
  } : {
    complete: Ne,
    error: It,
    next: Ne
  };
}
const vr = (e) => (t, n, r) => e((o) => {
  const s = (a) => o.next(a);
  return t.addEventListener(n, s, r), () => t.removeEventListener(n, s, r);
}), _r = (e, t) => {
  const n = () => {
  }, r = (o) => typeof o[0] == "function";
  return (o) => {
    const s = (...a) => {
      const c = o(r(a) ? t({ next: a[0] }) : t(...a));
      return c !== void 0 ? c : n;
    };
    return s[Symbol.observable] = () => ({
      subscribe: (...a) => ({ unsubscribe: s(...a) })
    }), e(s);
  };
}, yr = _r(gr, wr), Zt = vr(yr), Er = (e, t, n) => async (r) => {
  const o = new e([n], { type: "application/javascript; charset=utf-8" }), s = t.createObjectURL(o);
  try {
    await r(s);
  } finally {
    t.revokeObjectURL(s);
  }
}, br = (e) => ({ data: t }) => {
  const { id: n } = t;
  if (n !== null) {
    const r = e.get(n);
    if (r !== void 0) {
      const { reject: o, resolve: s } = r;
      e.delete(n), t.error === void 0 ? s(t.result) : o(new Error(t.error.message));
    }
  }
}, Ar = (e) => (t, n) => (r, o = []) => new Promise((s, a) => {
  const c = e(t);
  t.set(c, { reject: a, resolve: s }), n.postMessage({ id: c, ...r }, o);
}), Cr = (e, t, n, r) => (o, s, a = {}) => {
  const c = new o(s, "recorder-audio-worklet-processor", {
    ...a,
    channelCountMode: "explicit",
    numberOfInputs: 1,
    numberOfOutputs: 0
  }), i = /* @__PURE__ */ new Map(), u = t(i, c.port), d = n(c.port, "message")(e(i));
  c.port.start();
  let l = "inactive";
  return Object.defineProperties(c, {
    pause: {
      get() {
        return async () => (r(["recording"], l), l = "paused", u({
          method: "pause"
        }));
      }
    },
    port: {
      get() {
        throw new Error("The port of a RecorderAudioWorkletNode can't be accessed.");
      }
    },
    record: {
      get() {
        return async (g) => (r(["inactive"], l), l = "recording", u({
          method: "record",
          params: { encoderPort: g }
        }, [g]));
      }
    },
    resume: {
      get() {
        return async () => (r(["paused"], l), l = "recording", u({
          method: "resume"
        }));
      }
    },
    stop: {
      get() {
        return async () => {
          r(["paused", "recording"], l), l = "stopped";
          try {
            await u({ method: "stop" });
          } finally {
            d();
          }
        };
      }
    }
  }), c;
}, Tr = (e, t) => {
  if (!e.includes(t))
    throw new Error(`Expected the state to be ${e.map((n) => `"${n}"`).join(" or ")} but it was "${t}".`);
}, Mr = '(()=>{"use strict";class e extends AudioWorkletProcessor{constructor(){super(),this._encoderPort=null,this._numberOfChannels=0,this._state="inactive",this.port.onmessage=e=>{let{data:t}=e;"pause"===t.method?"active"===this._state||"recording"===this._state?(this._state="paused",this._sendAcknowledgement(t.id)):this._sendUnexpectedStateError(t.id):"record"===t.method?"inactive"===this._state?(this._encoderPort=t.params.encoderPort,this._state="active",this._sendAcknowledgement(t.id)):this._sendUnexpectedStateError(t.id):"resume"===t.method?"paused"===this._state?(this._state="active",this._sendAcknowledgement(t.id)):this._sendUnexpectedStateError(t.id):"stop"===t.method?"active"!==this._state&&"paused"!==this._state&&"recording"!==this._state||null===this._encoderPort?this._sendUnexpectedStateError(t.id):(this._stop(this._encoderPort),this._sendAcknowledgement(t.id)):"number"==typeof t.id&&this.port.postMessage({error:{code:-32601,message:"The requested method is not supported."},id:t.id})}}process(e){let[t]=e;if("inactive"===this._state||"paused"===this._state)return!0;if("active"===this._state){if(void 0===t)throw new Error("No channelData was received for the first input.");if(0===t.length)return!0;this._state="recording"}if("recording"===this._state&&null!==this._encoderPort){if(void 0===t)throw new Error("No channelData was received for the first input.");return 0===t.length?this._encoderPort.postMessage(Array.from({length:this._numberOfChannels},(()=>128))):(this._encoderPort.postMessage(t,t.map((e=>{let{buffer:t}=e;return t}))),this._numberOfChannels=t.length),!0}return!1}_sendAcknowledgement(e){this.port.postMessage({id:e,result:null})}_sendUnexpectedStateError(e){this.port.postMessage({error:{code:-32603,message:"The internal state does not allow to process the given message."},id:e})}_stop(e){e.postMessage([]),e.close(),this._encoderPort=null,this._state="stopped"}}e.parameterDescriptors=[],registerProcessor("recorder-audio-worklet-processor",e)})();', Nr = Er(Blob, URL, Mr), Or = Cr(br, Ar(Hn), Zt, Tr), St = (e, t, n) => ({ endTime: t, insertTime: n, type: "exponentialRampToValue", value: e }), Rt = (e, t, n) => ({ endTime: t, insertTime: n, type: "linearRampToValue", value: e }), tt = (e, t) => ({ startTime: t, type: "setValue", value: e }), Kt = (e, t, n) => ({ duration: n, startTime: t, type: "setValueCurve", values: e }), Qt = (e, t, { startTime: n, target: r, timeConstant: o }) => r + (t - r) * Math.exp((n - e) / o), me = (e) => e.type === "exponentialRampToValue", Re = (e) => e.type === "linearRampToValue", re = (e) => me(e) || Re(e), dt = (e) => e.type === "setValue", J = (e) => e.type === "setValueCurve", Le = (e, t, n, r) => {
  const o = e[t];
  return o === void 0 ? r : re(o) || dt(o) ? o.value : J(o) ? o.values[o.values.length - 1] : Qt(n, Le(e, t - 1, o.startTime, r), o);
}, Lt = (e, t, n, r, o) => n === void 0 ? [r.insertTime, o] : re(n) ? [n.endTime, n.value] : dt(n) ? [n.startTime, n.value] : J(n) ? [
  n.startTime + n.duration,
  n.values[n.values.length - 1]
] : [
  n.startTime,
  Le(e, t - 1, n.startTime, o)
], nt = (e) => e.type === "cancelAndHold", rt = (e) => e.type === "cancelScheduledValues", ne = (e) => nt(e) || rt(e) ? e.cancelTime : me(e) || Re(e) ? e.endTime : e.startTime, Pt = (e, t, n, { endTime: r, value: o }) => n === o ? o : 0 < n && 0 < o || n < 0 && o < 0 ? n * (o / n) ** ((e - t) / (r - t)) : 0, Bt = (e, t, n, { endTime: r, value: o }) => n + (e - t) / (r - t) * (o - n), kr = (e, t) => {
  const n = Math.floor(t), r = Math.ceil(t);
  return n === r ? e[n] : (1 - (t - n)) * e[n] + (1 - (r - t)) * e[r];
}, Ir = (e, { duration: t, startTime: n, values: r }) => {
  const o = (e - n) / t * (r.length - 1);
  return kr(r, o);
}, Oe = (e) => e.type === "setTarget";
class Sr {
  constructor(t) {
    this._automationEvents = [], this._currenTime = 0, this._defaultValue = t;
  }
  [Symbol.iterator]() {
    return this._automationEvents[Symbol.iterator]();
  }
  add(t) {
    const n = ne(t);
    if (nt(t) || rt(t)) {
      const r = this._automationEvents.findIndex((s) => rt(t) && J(s) ? s.startTime + s.duration >= n : ne(s) >= n), o = this._automationEvents[r];
      if (r !== -1 && (this._automationEvents = this._automationEvents.slice(0, r)), nt(t)) {
        const s = this._automationEvents[this._automationEvents.length - 1];
        if (o !== void 0 && re(o)) {
          if (s !== void 0 && Oe(s))
            throw new Error("The internal list is malformed.");
          const a = s === void 0 ? o.insertTime : J(s) ? s.startTime + s.duration : ne(s), c = s === void 0 ? this._defaultValue : J(s) ? s.values[s.values.length - 1] : s.value, i = me(o) ? Pt(n, a, c, o) : Bt(n, a, c, o), u = me(o) ? St(i, n, this._currenTime) : Rt(i, n, this._currenTime);
          this._automationEvents.push(u);
        }
        if (s !== void 0 && Oe(s) && this._automationEvents.push(tt(this.getValue(n), n)), s !== void 0 && J(s) && s.startTime + s.duration > n) {
          const a = n - s.startTime, c = (s.values.length - 1) / s.duration, i = Math.max(2, 1 + Math.ceil(a * c)), u = a / (i - 1) * c, d = s.values.slice(0, i);
          if (u < 1)
            for (let l = 1; l < i; l += 1) {
              const g = u * l % 1;
              d[l] = s.values[l - 1] * (1 - g) + s.values[l] * g;
            }
          this._automationEvents[this._automationEvents.length - 1] = Kt(d, s.startTime, a);
        }
      }
    } else {
      const r = this._automationEvents.findIndex((a) => ne(a) > n), o = r === -1 ? this._automationEvents[this._automationEvents.length - 1] : this._automationEvents[r - 1];
      if (o !== void 0 && J(o) && ne(o) + o.duration > n)
        return !1;
      const s = me(t) ? St(t.value, t.endTime, this._currenTime) : Re(t) ? Rt(t.value, n, this._currenTime) : t;
      if (r === -1)
        this._automationEvents.push(s);
      else {
        if (J(t) && n + t.duration > ne(this._automationEvents[r]))
          return !1;
        this._automationEvents.splice(r, 0, s);
      }
    }
    return !0;
  }
  flush(t) {
    const n = this._automationEvents.findIndex((r) => ne(r) > t);
    if (n > 1) {
      const r = this._automationEvents.slice(n - 1), o = r[0];
      Oe(o) && r.unshift(tt(Le(this._automationEvents, n - 2, o.startTime, this._defaultValue), o.startTime)), this._automationEvents = r;
    }
  }
  getValue(t) {
    if (this._automationEvents.length === 0)
      return this._defaultValue;
    const n = this._automationEvents.findIndex((a) => ne(a) > t), r = this._automationEvents[n], o = (n === -1 ? this._automationEvents.length : n) - 1, s = this._automationEvents[o];
    if (s !== void 0 && Oe(s) && (r === void 0 || !re(r) || r.insertTime > t))
      return Qt(t, Le(this._automationEvents, o - 1, s.startTime, this._defaultValue), s);
    if (s !== void 0 && dt(s) && (r === void 0 || !re(r)))
      return s.value;
    if (s !== void 0 && J(s) && (r === void 0 || !re(r) || s.startTime + s.duration > t))
      return t < s.startTime + s.duration ? Ir(t, s) : s.values[s.values.length - 1];
    if (s !== void 0 && re(s) && (r === void 0 || !re(r)))
      return s.value;
    if (r !== void 0 && me(r)) {
      const [a, c] = Lt(this._automationEvents, o, s, r, this._defaultValue);
      return Pt(t, a, c, r);
    }
    if (r !== void 0 && Re(r)) {
      const [a, c] = Lt(this._automationEvents, o, s, r, this._defaultValue);
      return Bt(t, a, c, r);
    }
    return this._defaultValue;
  }
}
const Rr = (e) => ({ cancelTime: e, type: "cancelAndHold" }), Lr = (e) => ({ cancelTime: e, type: "cancelScheduledValues" }), Pr = (e, t) => ({ endTime: t, type: "exponentialRampToValue", value: e }), Br = (e, t) => ({ endTime: t, type: "linearRampToValue", value: e }), Ur = (e, t, n) => ({ startTime: t, target: e, timeConstant: n, type: "setTarget" }), Dr = () => new DOMException("", "AbortError"), Wr = (e) => (t, n, [r, o, s], a) => {
  e(t[o], [n, r, s], (c) => c[0] === n && c[1] === r, a);
}, Vr = (e) => (t, n, r) => {
  const o = [];
  for (let s = 0; s < r.numberOfInputs; s += 1)
    o.push(/* @__PURE__ */ new Set());
  e.set(t, {
    activeInputs: o,
    outputs: /* @__PURE__ */ new Set(),
    passiveInputs: /* @__PURE__ */ new WeakMap(),
    renderer: n
  });
}, xr = (e) => (t, n) => {
  e.set(t, { activeInputs: /* @__PURE__ */ new Set(), passiveInputs: /* @__PURE__ */ new WeakMap(), renderer: n });
}, ge = /* @__PURE__ */ new WeakSet(), Jt = /* @__PURE__ */ new WeakMap(), en = /* @__PURE__ */ new WeakMap(), tn = /* @__PURE__ */ new WeakMap(), nn = /* @__PURE__ */ new WeakMap(), rn = /* @__PURE__ */ new WeakMap(), on = /* @__PURE__ */ new WeakMap(), ot = /* @__PURE__ */ new WeakMap(), st = /* @__PURE__ */ new WeakMap(), at = /* @__PURE__ */ new WeakMap(), sn = {
  construct() {
    return sn;
  }
}, Fr = (e) => {
  try {
    const t = new Proxy(e, sn);
    new t();
  } catch {
    return !1;
  }
  return !0;
}, Ut = /^import(?:(?:[\s]+[\w]+|(?:[\s]+[\w]+[\s]*,)?[\s]*\{[\s]*[\w]+(?:[\s]+as[\s]+[\w]+)?(?:[\s]*,[\s]*[\w]+(?:[\s]+as[\s]+[\w]+)?)*[\s]*}|(?:[\s]+[\w]+[\s]*,)?[\s]*\*[\s]+as[\s]+[\w]+)[\s]+from)?(?:[\s]*)("([^"\\]|\\.)+"|'([^'\\]|\\.)+')(?:[\s]*);?/, Dt = (e, t) => {
  const n = [];
  let r = e.replace(/^[\s]+/, ""), o = r.match(Ut);
  for (; o !== null; ) {
    const s = o[1].slice(1, -1), a = o[0].replace(/([\s]+)?;?$/, "").replace(s, new URL(s, t).toString());
    n.push(a), r = r.slice(o[0].length).replace(/^[\s]+/, ""), o = r.match(Ut);
  }
  return [n.join(";"), r];
}, Wt = (e) => {
  if (e !== void 0 && !Array.isArray(e))
    throw new TypeError("The parameterDescriptors property of given value for processorCtor is not an array.");
}, Vt = (e) => {
  if (!Fr(e))
    throw new TypeError("The given value for processorCtor should be a constructor.");
  if (e.prototype === null || typeof e.prototype != "object")
    throw new TypeError("The given value for processorCtor should have a prototype.");
}, jr = (e, t, n, r, o, s, a, c, i, u, d, l, g) => {
  let w = 0;
  return (p, f, m = { credentials: "omit" }) => {
    const h = d.get(p);
    if (h !== void 0 && h.has(f))
      return Promise.resolve();
    const A = u.get(p);
    if (A !== void 0) {
      const E = A.get(f);
      if (E !== void 0)
        return E;
    }
    const _ = s(p), T = _.audioWorklet === void 0 ? o(f).then(([E, b]) => {
      const [y, v] = Dt(E, b), M = `${y};((a,b)=>{(a[b]=a[b]||[]).push((AudioWorkletProcessor,global,registerProcessor,sampleRate,self,window)=>{${v}
})})(window,'_AWGS')`;
      return n(M);
    }).then(() => {
      const E = g._AWGS.pop();
      if (E === void 0)
        throw new SyntaxError();
      r(_.currentTime, _.sampleRate, () => E(class {
      }, void 0, (b, y) => {
        if (b.trim() === "")
          throw t();
        const v = st.get(_);
        if (v !== void 0) {
          if (v.has(b))
            throw t();
          Vt(y), Wt(y.parameterDescriptors), v.set(b, y);
        } else
          Vt(y), Wt(y.parameterDescriptors), st.set(_, /* @__PURE__ */ new Map([[b, y]]));
      }, _.sampleRate, void 0, void 0));
    }) : Promise.all([
      o(f),
      Promise.resolve(e(l, l))
    ]).then(([[E, b], y]) => {
      const v = w + 1;
      w = v;
      const [M, S] = Dt(E, b), B = `${M};((AudioWorkletProcessor,registerProcessor)=>{${S}
})(${y ? "AudioWorkletProcessor" : "class extends AudioWorkletProcessor {__b=new WeakSet();constructor(){super();(p=>p.postMessage=(q=>(m,t)=>q.call(p,m,t?t.filter(u=>!this.__b.has(u)):t))(p.postMessage))(this.port)}}"},(n,p)=>registerProcessor(n,class extends p{${y ? "" : "__c = (a) => a.forEach(e=>this.__b.add(e.buffer));"}process(i,o,p){${y ? "" : "i.forEach(this.__c);o.forEach(this.__c);this.__c(Object.values(p));"}return super.process(i.map(j=>j.some(k=>k.length===0)?[]:j),o,p)}}));registerProcessor('__sac${v}',class extends AudioWorkletProcessor{process(){return !1}})`, D = new Blob([B], { type: "application/javascript; charset=utf-8" }), I = URL.createObjectURL(D);
      return _.audioWorklet.addModule(I, m).then(() => {
        if (c(_))
          return _;
        const U = a(_);
        return U.audioWorklet.addModule(I, m).then(() => U);
      }).then((U) => {
        if (i === null)
          throw new SyntaxError();
        try {
          new i(U, `__sac${v}`);
        } catch {
          throw new SyntaxError();
        }
      }).finally(() => URL.revokeObjectURL(I));
    });
    return A === void 0 ? u.set(p, /* @__PURE__ */ new Map([[f, T]])) : A.set(f, T), T.then(() => {
      const E = d.get(p);
      E === void 0 ? d.set(p, /* @__PURE__ */ new Set([f])) : E.add(f);
    }).finally(() => {
      const E = u.get(p);
      E !== void 0 && E.delete(f);
    }), T;
  };
}, K = (e, t) => {
  const n = e.get(t);
  if (n === void 0)
    throw new Error("A value with the given key could not be found.");
  return n;
}, Fe = (e, t) => {
  const n = Array.from(e).filter(t);
  if (n.length > 1)
    throw Error("More than one element was found.");
  if (n.length === 0)
    throw Error("No element was found.");
  const [r] = n;
  return e.delete(r), r;
}, an = (e, t, n, r) => {
  const o = K(e, t), s = Fe(o, (a) => a[0] === n && a[1] === r);
  return o.size === 0 && e.delete(t), s;
}, be = (e) => K(on, e), Pe = (e) => {
  if (ge.has(e))
    throw new Error("The AudioNode is already stored.");
  ge.add(e), be(e).forEach((t) => t(!0));
}, cn = (e) => "port" in e, ft = (e) => {
  if (!ge.has(e))
    throw new Error("The AudioNode is not stored.");
  ge.delete(e), be(e).forEach((t) => t(!1));
}, it = (e, t) => {
  !cn(e) && t.every((n) => n.size === 0) && ft(e);
}, Gr = (e, t, n, r, o, s, a, c, i, u, d, l, g) => {
  const w = /* @__PURE__ */ new WeakMap();
  return (p, f, m, h, A) => {
    const { activeInputs: _, passiveInputs: T } = s(f), { outputs: E } = s(p), b = c(p), y = (v) => {
      const M = i(f), S = i(p);
      if (v) {
        const N = an(T, p, m, h);
        e(_, p, N, !1), !A && !l(p) && n(S, M, m, h), g(f) && Pe(f);
      } else {
        const N = r(_, p, m, h);
        t(T, h, N, !1), !A && !l(p) && o(S, M, m, h);
        const L = a(f);
        if (L === 0)
          d(f) && it(f, _);
        else {
          const P = w.get(f);
          P !== void 0 && clearTimeout(P), w.set(f, setTimeout(() => {
            d(f) && it(f, _);
          }, L * 1e3));
        }
      }
    };
    return u(E, [f, m, h], (v) => v[0] === f && v[1] === m && v[2] === h, !0) ? (b.add(y), d(p) ? e(_, p, [m, h, y], !0) : t(T, h, [p, m, y], !0), !0) : !1;
  };
}, $r = (e) => (t, n, [r, o, s], a) => {
  const c = t.get(r);
  c === void 0 ? t.set(r, /* @__PURE__ */ new Set([[o, n, s]])) : e(c, [o, n, s], (i) => i[0] === o && i[1] === n, a);
}, qr = (e) => (t, n) => {
  const r = e(t, {
    channelCount: 1,
    channelCountMode: "explicit",
    channelInterpretation: "discrete",
    gain: 0
  });
  n.connect(r).connect(t.destination);
  const o = () => {
    n.removeEventListener("ended", o), n.disconnect(r), r.disconnect();
  };
  n.addEventListener("ended", o);
}, zr = (e) => (t, n) => {
  e(t).add(n);
}, un = (e, t) => e.context === t, xt = (e) => {
  try {
    e.copyToChannel(new Float32Array(1), 0, -1);
  } catch {
    return !1;
  }
  return !0;
}, ue = () => new DOMException("", "IndexSizeError"), Xr = (e) => {
  e.getChannelData = /* @__PURE__ */ ((t) => (n) => {
    try {
      return t.call(e, n);
    } catch (r) {
      throw r.code === 12 ? ue() : r;
    }
  })(e.getChannelData);
}, Yr = {
  numberOfChannels: 1
}, Hr = (e, t, n, r, o, s, a, c) => {
  let i = null;
  return class ln {
    constructor(d) {
      if (o === null)
        throw new Error("Missing the native OfflineAudioContext constructor.");
      const { length: l, numberOfChannels: g, sampleRate: w } = { ...Yr, ...d };
      i === null && (i = new o(1, 1, 44100));
      const p = r !== null && t(s, s) ? new r({ length: l, numberOfChannels: g, sampleRate: w }) : i.createBuffer(g, l, w);
      if (p.numberOfChannels === 0)
        throw n();
      return typeof p.copyFromChannel != "function" ? (a(p), Xr(p)) : t(xt, () => xt(p)) || c(p), e.add(p), p;
    }
    static [Symbol.hasInstance](d) {
      return d !== null && typeof d == "object" && Object.getPrototypeOf(d) === ln.prototype || e.has(d);
    }
  };
}, je = -34028234663852886e22, ht = -je, ae = (e) => ge.has(e), Zr = {
  buffer: null,
  channelCount: 2,
  channelCountMode: "max",
  channelInterpretation: "speakers",
  // Bug #149: Safari does not yet support the detune AudioParam.
  loop: !1,
  loopEnd: 0,
  loopStart: 0,
  playbackRate: 1
}, Kr = (e, t, n, r, o, s, a, c) => class extends e {
  constructor(u, d) {
    const l = s(u), g = { ...Zr, ...d }, w = o(l, g), p = a(l), f = p ? t() : null;
    super(u, !1, w, f), this._audioBufferSourceNodeRenderer = f, this._isBufferNullified = !1, this._isBufferSet = g.buffer !== null, this._nativeAudioBufferSourceNode = w, this._onended = null, this._playbackRate = n(this, p, w.playbackRate, ht, je);
  }
  get buffer() {
    return this._isBufferNullified ? null : this._nativeAudioBufferSourceNode.buffer;
  }
  set buffer(u) {
    if (this._nativeAudioBufferSourceNode.buffer = u, u !== null) {
      if (this._isBufferSet)
        throw r();
      this._isBufferSet = !0;
    }
  }
  get loop() {
    return this._nativeAudioBufferSourceNode.loop;
  }
  set loop(u) {
    this._nativeAudioBufferSourceNode.loop = u;
  }
  get loopEnd() {
    return this._nativeAudioBufferSourceNode.loopEnd;
  }
  set loopEnd(u) {
    this._nativeAudioBufferSourceNode.loopEnd = u;
  }
  get loopStart() {
    return this._nativeAudioBufferSourceNode.loopStart;
  }
  set loopStart(u) {
    this._nativeAudioBufferSourceNode.loopStart = u;
  }
  get onended() {
    return this._onended;
  }
  set onended(u) {
    const d = typeof u == "function" ? c(this, u) : null;
    this._nativeAudioBufferSourceNode.onended = d;
    const l = this._nativeAudioBufferSourceNode.onended;
    this._onended = l !== null && l === d ? u : l;
  }
  get playbackRate() {
    return this._playbackRate;
  }
  start(u = 0, d = 0, l) {
    if (this._nativeAudioBufferSourceNode.start(u, d, l), this._audioBufferSourceNodeRenderer !== null && (this._audioBufferSourceNodeRenderer.start = l === void 0 ? [u, d] : [u, d, l]), this.context.state !== "closed") {
      Pe(this);
      const g = () => {
        this._nativeAudioBufferSourceNode.removeEventListener("ended", g), ae(this) && ft(this);
      };
      this._nativeAudioBufferSourceNode.addEventListener("ended", g);
    }
  }
  stop(u = 0) {
    this._nativeAudioBufferSourceNode.stop(u), this._audioBufferSourceNodeRenderer !== null && (this._audioBufferSourceNodeRenderer.stop = u);
  }
}, Qr = (e, t, n, r, o) => () => {
  const s = /* @__PURE__ */ new WeakMap();
  let a = null, c = null;
  const i = async (u, d) => {
    let l = n(u);
    const g = un(l, d);
    if (!g) {
      const w = {
        buffer: l.buffer,
        channelCount: l.channelCount,
        channelCountMode: l.channelCountMode,
        channelInterpretation: l.channelInterpretation,
        // Bug #149: Safari does not yet support the detune AudioParam.
        loop: l.loop,
        loopEnd: l.loopEnd,
        loopStart: l.loopStart,
        playbackRate: l.playbackRate.value
      };
      l = t(d, w), a !== null && l.start(...a), c !== null && l.stop(c);
    }
    return s.set(d, l), g ? await e(d, u.playbackRate, l.playbackRate) : await r(d, u.playbackRate, l.playbackRate), await o(u, d, l), l;
  };
  return {
    set start(u) {
      a = u;
    },
    set stop(u) {
      c = u;
    },
    render(u, d) {
      const l = s.get(d);
      return l !== void 0 ? Promise.resolve(l) : i(u, d);
    }
  };
}, Jr = (e) => "playbackRate" in e, eo = (e) => "frequency" in e && "gain" in e, to = (e) => "offset" in e, no = (e) => !("frequency" in e) && "gain" in e, ro = (e) => "detune" in e && "frequency" in e, oo = (e) => "pan" in e, z = (e) => K(Jt, e), Ae = (e) => K(tn, e), ct = (e, t) => {
  const { activeInputs: n } = z(e);
  n.forEach((o) => o.forEach(([s]) => {
    t.includes(e) || ct(s, [...t, e]);
  }));
  const r = Jr(e) ? [
    // Bug #149: Safari does not yet support the detune AudioParam.
    e.playbackRate
  ] : cn(e) ? Array.from(e.parameters.values()) : eo(e) ? [e.Q, e.detune, e.frequency, e.gain] : to(e) ? [e.offset] : no(e) ? [e.gain] : ro(e) ? [e.detune, e.frequency] : oo(e) ? [e.pan] : [];
  for (const o of r) {
    const s = Ae(o);
    s !== void 0 && s.activeInputs.forEach(([a]) => ct(a, t));
  }
  ae(e) && ft(e);
}, so = (e) => {
  ct(e.destination, []);
}, ao = (e) => e === void 0 || typeof e == "number" || typeof e == "string" && (e === "balanced" || e === "interactive" || e === "playback"), io = (e, t, n, r, o, s, a, c) => class extends e {
  constructor(u, d) {
    const l = s(u), g = a(l), w = o(l, d, g), p = g ? t(c) : null;
    super(u, !1, w, p), this._isNodeOfNativeOfflineAudioContext = g, this._nativeAudioDestinationNode = w;
  }
  get channelCount() {
    return this._nativeAudioDestinationNode.channelCount;
  }
  set channelCount(u) {
    if (this._isNodeOfNativeOfflineAudioContext)
      throw r();
    if (u > this._nativeAudioDestinationNode.maxChannelCount)
      throw n();
    this._nativeAudioDestinationNode.channelCount = u;
  }
  get channelCountMode() {
    return this._nativeAudioDestinationNode.channelCountMode;
  }
  set channelCountMode(u) {
    if (this._isNodeOfNativeOfflineAudioContext)
      throw r();
    this._nativeAudioDestinationNode.channelCountMode = u;
  }
  get maxChannelCount() {
    return this._nativeAudioDestinationNode.maxChannelCount;
  }
}, co = (e) => {
  const t = /* @__PURE__ */ new WeakMap(), n = async (r, o) => {
    const s = o.destination;
    return t.set(o, s), await e(r, o, s), s;
  };
  return {
    render(r, o) {
      const s = t.get(o);
      return s !== void 0 ? Promise.resolve(s) : n(r, o);
    }
  };
}, uo = (e, t, n, r, o, s, a, c) => (i, u) => {
  const d = u.listener, l = () => {
    const E = new Float32Array(1), b = t(u, {
      channelCount: 1,
      channelCountMode: "explicit",
      channelInterpretation: "speakers",
      numberOfInputs: 9
    }), y = a(u);
    let v = !1, M = [0, 0, -1, 0, 1, 0], S = [0, 0, 0];
    const N = () => {
      if (v)
        return;
      v = !0;
      const D = r(u, 256, 9, 0);
      D.onaudioprocess = ({ inputBuffer: I }) => {
        const U = [
          s(I, E, 0),
          s(I, E, 1),
          s(I, E, 2),
          s(I, E, 3),
          s(I, E, 4),
          s(I, E, 5)
        ];
        U.some((O, R) => O !== M[R]) && (d.setOrientation(...U), M = U);
        const V = [
          s(I, E, 6),
          s(I, E, 7),
          s(I, E, 8)
        ];
        V.some((O, R) => O !== S[R]) && (d.setPosition(...V), S = V);
      }, b.connect(D);
    }, L = (D) => (I) => {
      I !== M[D] && (M[D] = I, d.setOrientation(...M));
    }, P = (D) => (I) => {
      I !== S[D] && (S[D] = I, d.setPosition(...S));
    }, B = (D, I, U) => {
      const V = n(u, {
        channelCount: 1,
        channelCountMode: "explicit",
        channelInterpretation: "discrete",
        offset: I
      });
      V.connect(b, 0, D), V.start(), Object.defineProperty(V.offset, "defaultValue", {
        get() {
          return I;
        }
      });
      const O = e({ context: i }, y, V.offset, ht, je);
      return c(O, "value", (R) => () => R.call(O), (R) => (x) => {
        try {
          R.call(O, x);
        } catch ($) {
          if ($.code !== 9)
            throw $;
        }
        N(), y && U(x);
      }), O.cancelAndHoldAtTime = /* @__PURE__ */ ((R) => y ? () => {
        throw o();
      } : (...x) => {
        const $ = R.apply(O, x);
        return N(), $;
      })(O.cancelAndHoldAtTime), O.cancelScheduledValues = /* @__PURE__ */ ((R) => y ? () => {
        throw o();
      } : (...x) => {
        const $ = R.apply(O, x);
        return N(), $;
      })(O.cancelScheduledValues), O.exponentialRampToValueAtTime = /* @__PURE__ */ ((R) => y ? () => {
        throw o();
      } : (...x) => {
        const $ = R.apply(O, x);
        return N(), $;
      })(O.exponentialRampToValueAtTime), O.linearRampToValueAtTime = /* @__PURE__ */ ((R) => y ? () => {
        throw o();
      } : (...x) => {
        const $ = R.apply(O, x);
        return N(), $;
      })(O.linearRampToValueAtTime), O.setTargetAtTime = /* @__PURE__ */ ((R) => y ? () => {
        throw o();
      } : (...x) => {
        const $ = R.apply(O, x);
        return N(), $;
      })(O.setTargetAtTime), O.setValueAtTime = /* @__PURE__ */ ((R) => y ? () => {
        throw o();
      } : (...x) => {
        const $ = R.apply(O, x);
        return N(), $;
      })(O.setValueAtTime), O.setValueCurveAtTime = /* @__PURE__ */ ((R) => y ? () => {
        throw o();
      } : (...x) => {
        const $ = R.apply(O, x);
        return N(), $;
      })(O.setValueCurveAtTime), O;
    };
    return {
      forwardX: B(0, 0, L(0)),
      forwardY: B(1, 0, L(1)),
      forwardZ: B(2, -1, L(2)),
      positionX: B(6, 0, P(0)),
      positionY: B(7, 0, P(1)),
      positionZ: B(8, 0, P(2)),
      upX: B(3, 0, L(3)),
      upY: B(4, 1, L(4)),
      upZ: B(5, 0, L(5))
    };
  }, { forwardX: g, forwardY: w, forwardZ: p, positionX: f, positionY: m, positionZ: h, upX: A, upY: _, upZ: T } = d.forwardX === void 0 ? l() : d;
  return {
    get forwardX() {
      return g;
    },
    get forwardY() {
      return w;
    },
    get forwardZ() {
      return p;
    },
    get positionX() {
      return f;
    },
    get positionY() {
      return m;
    },
    get positionZ() {
      return h;
    },
    get upX() {
      return A;
    },
    get upY() {
      return _;
    },
    get upZ() {
      return T;
    }
  };
}, Be = (e) => "context" in e, Ce = (e) => Be(e[0]), le = (e, t, n, r) => {
  for (const o of e)
    if (n(o)) {
      if (r)
        return !1;
      throw Error("The set contains at least one similar element.");
    }
  return e.add(t), !0;
}, Ft = (e, t, [n, r], o) => {
  le(e, [t, n, r], (s) => s[0] === t && s[1] === n, o);
}, jt = (e, [t, n, r], o) => {
  const s = e.get(t);
  s === void 0 ? e.set(t, /* @__PURE__ */ new Set([[n, r]])) : le(s, [n, r], (a) => a[0] === n, o);
}, dn = (e) => "inputs" in e, ut = (e, t, n, r) => {
  if (dn(t)) {
    const o = t.inputs[r];
    return e.connect(o, n, 0), [o, n, 0];
  }
  return e.connect(t, n, r), [t, n, r];
}, fn = (e, t, n) => {
  for (const r of e)
    if (r[0] === t && r[1] === n)
      return e.delete(r), r;
  return null;
}, lo = (e, t, n) => Fe(e, (r) => r[0] === t && r[1] === n), hn = (e, t) => {
  if (!be(e).delete(t))
    throw new Error("Missing the expected event listener.");
}, pn = (e, t, n) => {
  const r = K(e, t), o = Fe(r, (s) => s[0] === n);
  return r.size === 0 && e.delete(t), o;
}, lt = (e, t, n, r) => {
  dn(t) ? e.disconnect(t.inputs[r], n, 0) : e.disconnect(t, n, r);
}, H = (e) => K(en, e), ye = (e) => K(nn, e), ie = (e) => ot.has(e), Ie = (e) => !ge.has(e), Gt = (e, t) => new Promise((n) => {
  if (t !== null)
    n(!0);
  else {
    const r = e.createScriptProcessor(256, 1, 1), o = e.createGain(), s = e.createBuffer(1, 2, 44100), a = s.getChannelData(0);
    a[0] = 1, a[1] = 1;
    const c = e.createBufferSource();
    c.buffer = s, c.loop = !0, c.connect(r).connect(e.destination), c.connect(o), c.disconnect(o), r.onaudioprocess = (i) => {
      const u = i.inputBuffer.getChannelData(0);
      Array.prototype.some.call(u, (d) => d === 1) ? n(!0) : n(!1), c.stop(), r.onaudioprocess = null, c.disconnect(r), r.disconnect(e.destination);
    }, c.start();
  }
}), Qe = (e, t) => {
  const n = /* @__PURE__ */ new Map();
  for (const r of e)
    for (const o of r) {
      const s = n.get(o);
      n.set(o, s === void 0 ? 1 : s + 1);
    }
  n.forEach((r, o) => t(o, r));
}, Ue = (e) => "context" in e, fo = (e) => {
  const t = /* @__PURE__ */ new Map();
  e.connect = /* @__PURE__ */ ((n) => (r, o = 0, s = 0) => {
    const a = Ue(r) ? n(r, o, s) : n(r, o), c = t.get(r);
    return c === void 0 ? t.set(r, [{ input: s, output: o }]) : c.every((i) => i.input !== s || i.output !== o) && c.push({ input: s, output: o }), a;
  })(e.connect.bind(e)), e.disconnect = /* @__PURE__ */ ((n) => (r, o, s) => {
    if (n.apply(e), r === void 0)
      t.clear();
    else if (typeof r == "number")
      for (const [a, c] of t) {
        const i = c.filter((u) => u.output !== r);
        i.length === 0 ? t.delete(a) : t.set(a, i);
      }
    else if (t.has(r))
      if (o === void 0)
        t.delete(r);
      else {
        const a = t.get(r);
        if (a !== void 0) {
          const c = a.filter((i) => i.output !== o && (i.input !== s || s === void 0));
          c.length === 0 ? t.delete(r) : t.set(r, c);
        }
      }
    for (const [a, c] of t)
      c.forEach((i) => {
        Ue(a) ? e.connect(a, i.output, i.input) : e.connect(a, i.output);
      });
  })(e.disconnect);
}, ho = (e, t, n, r) => {
  const { activeInputs: o, passiveInputs: s } = Ae(t), { outputs: a } = z(e), c = be(e), i = (u) => {
    const d = H(e), l = ye(t);
    if (u) {
      const g = pn(s, e, n);
      Ft(o, e, g, !1), !r && !ie(e) && d.connect(l, n);
    } else {
      const g = lo(o, e, n);
      jt(s, g, !1), !r && !ie(e) && d.disconnect(l, n);
    }
  };
  return le(a, [t, n], (u) => u[0] === t && u[1] === n, !0) ? (c.add(i), ae(e) ? Ft(o, e, [n, i], !0) : jt(s, [e, n, i], !0), !0) : !1;
}, po = (e, t, n, r) => {
  const { activeInputs: o, passiveInputs: s } = z(t), a = fn(o[r], e, n);
  return a === null ? [an(s, e, n, r)[2], !1] : [a[2], !0];
}, mo = (e, t, n) => {
  const { activeInputs: r, passiveInputs: o } = Ae(t), s = fn(r, e, n);
  return s === null ? [pn(o, e, n)[1], !1] : [s[2], !0];
}, pt = (e, t, n, r, o) => {
  const [s, a] = po(e, n, r, o);
  if (s !== null && (hn(e, s), a && !t && !ie(e) && lt(H(e), H(n), r, o)), ae(n)) {
    const { activeInputs: c } = z(n);
    it(n, c);
  }
}, mt = (e, t, n, r) => {
  const [o, s] = mo(e, n, r);
  o !== null && (hn(e, o), s && !t && !ie(e) && H(e).disconnect(ye(n), r));
}, go = (e, t) => {
  const n = z(e), r = [];
  for (const o of n.outputs)
    Ce(o) ? pt(e, t, ...o) : mt(e, t, ...o), r.push(o[0]);
  return n.outputs.clear(), r;
}, wo = (e, t, n) => {
  const r = z(e), o = [];
  for (const s of r.outputs)
    s[1] === n && (Ce(s) ? pt(e, t, ...s) : mt(e, t, ...s), o.push(s[0]), r.outputs.delete(s));
  return o;
}, vo = (e, t, n, r, o) => {
  const s = z(e);
  return Array.from(s.outputs).filter((a) => a[0] === n && (r === void 0 || a[1] === r) && (o === void 0 || a[2] === o)).map((a) => (Ce(a) ? pt(e, t, ...a) : mt(e, t, ...a), s.outputs.delete(a), a[0]));
}, _o = (e, t, n, r, o, s, a, c, i, u, d, l, g, w, p, f) => class extends u {
  constructor(h, A, _, T) {
    super(_), this._context = h, this._nativeAudioNode = _;
    const E = d(h);
    l(E) && n(Gt, () => Gt(E, f)) !== !0 && fo(_), en.set(this, _), on.set(this, /* @__PURE__ */ new Set()), h.state !== "closed" && A && Pe(this), e(this, T, _);
  }
  get channelCount() {
    return this._nativeAudioNode.channelCount;
  }
  set channelCount(h) {
    this._nativeAudioNode.channelCount = h;
  }
  get channelCountMode() {
    return this._nativeAudioNode.channelCountMode;
  }
  set channelCountMode(h) {
    this._nativeAudioNode.channelCountMode = h;
  }
  get channelInterpretation() {
    return this._nativeAudioNode.channelInterpretation;
  }
  set channelInterpretation(h) {
    this._nativeAudioNode.channelInterpretation = h;
  }
  get context() {
    return this._context;
  }
  get numberOfInputs() {
    return this._nativeAudioNode.numberOfInputs;
  }
  get numberOfOutputs() {
    return this._nativeAudioNode.numberOfOutputs;
  }
  // tslint:disable-next-line:invalid-void
  connect(h, A = 0, _ = 0) {
    if (A < 0 || A >= this._nativeAudioNode.numberOfOutputs)
      throw o();
    const T = d(this._context), E = p(T);
    if (g(h) || w(h))
      throw s();
    if (Be(h)) {
      const v = H(h);
      try {
        const S = ut(this._nativeAudioNode, v, A, _), N = Ie(this);
        (E || N) && this._nativeAudioNode.disconnect(...S), this.context.state !== "closed" && !N && Ie(h) && Pe(h);
      } catch (S) {
        throw S.code === 12 ? s() : S;
      }
      if (t(this, h, A, _, E)) {
        const S = i([this], h);
        Qe(S, r(E));
      }
      return h;
    }
    const b = ye(h);
    if (b.name === "playbackRate" && b.maxValue === 1024)
      throw a();
    try {
      this._nativeAudioNode.connect(b, A), (E || Ie(this)) && this._nativeAudioNode.disconnect(b, A);
    } catch (v) {
      throw v.code === 12 ? s() : v;
    }
    if (ho(this, h, A, E)) {
      const v = i([this], h);
      Qe(v, r(E));
    }
  }
  disconnect(h, A, _) {
    let T;
    const E = d(this._context), b = p(E);
    if (h === void 0)
      T = go(this, b);
    else if (typeof h == "number") {
      if (h < 0 || h >= this.numberOfOutputs)
        throw o();
      T = wo(this, b, h);
    } else {
      if (A !== void 0 && (A < 0 || A >= this.numberOfOutputs) || Be(h) && _ !== void 0 && (_ < 0 || _ >= h.numberOfInputs))
        throw o();
      if (T = vo(this, b, h, A, _), T.length === 0)
        throw s();
    }
    for (const y of T) {
      const v = i([this], y);
      Qe(v, c);
    }
  }
}, yo = (e, t, n, r, o, s, a, c, i, u, d, l, g) => (w, p, f, m = null, h = null) => {
  const A = f.value, _ = new Sr(A), T = p ? r(_) : null, E = {
    get defaultValue() {
      return A;
    },
    get maxValue() {
      return m === null ? f.maxValue : m;
    },
    get minValue() {
      return h === null ? f.minValue : h;
    },
    get value() {
      return f.value;
    },
    set value(b) {
      f.value = b, E.setValueAtTime(b, w.context.currentTime);
    },
    cancelAndHoldAtTime(b) {
      if (typeof f.cancelAndHoldAtTime == "function")
        T === null && _.flush(w.context.currentTime), _.add(o(b)), f.cancelAndHoldAtTime(b);
      else {
        const y = Array.from(_).pop();
        T === null && _.flush(w.context.currentTime), _.add(o(b));
        const v = Array.from(_).pop();
        f.cancelScheduledValues(b), y !== v && v !== void 0 && (v.type === "exponentialRampToValue" ? f.exponentialRampToValueAtTime(v.value, v.endTime) : v.type === "linearRampToValue" ? f.linearRampToValueAtTime(v.value, v.endTime) : v.type === "setValue" ? f.setValueAtTime(v.value, v.startTime) : v.type === "setValueCurve" && f.setValueCurveAtTime(v.values, v.startTime, v.duration));
      }
      return E;
    },
    cancelScheduledValues(b) {
      return T === null && _.flush(w.context.currentTime), _.add(s(b)), f.cancelScheduledValues(b), E;
    },
    exponentialRampToValueAtTime(b, y) {
      if (b === 0)
        throw new RangeError();
      if (!Number.isFinite(y) || y < 0)
        throw new RangeError();
      const v = w.context.currentTime;
      return T === null && _.flush(v), Array.from(_).length === 0 && (_.add(u(A, v)), f.setValueAtTime(A, v)), _.add(a(b, y)), f.exponentialRampToValueAtTime(b, y), E;
    },
    linearRampToValueAtTime(b, y) {
      const v = w.context.currentTime;
      return T === null && _.flush(v), Array.from(_).length === 0 && (_.add(u(A, v)), f.setValueAtTime(A, v)), _.add(c(b, y)), f.linearRampToValueAtTime(b, y), E;
    },
    setTargetAtTime(b, y, v) {
      return T === null && _.flush(w.context.currentTime), _.add(i(b, y, v)), f.setTargetAtTime(b, y, v), E;
    },
    setValueAtTime(b, y) {
      return T === null && _.flush(w.context.currentTime), _.add(u(b, y)), f.setValueAtTime(b, y), E;
    },
    setValueCurveAtTime(b, y, v) {
      const M = b instanceof Float32Array ? b : new Float32Array(b);
      if (l !== null && l.name === "webkitAudioContext") {
        const S = y + v, N = w.context.sampleRate, L = Math.ceil(y * N), P = Math.floor(S * N), B = P - L, D = new Float32Array(B);
        for (let U = 0; U < B; U += 1) {
          const V = (M.length - 1) / v * ((L + U) / N - y), O = Math.floor(V), R = Math.ceil(V);
          D[U] = O === R ? M[O] : (1 - (V - O)) * M[O] + (1 - (R - V)) * M[R];
        }
        T === null && _.flush(w.context.currentTime), _.add(d(D, y, v)), f.setValueCurveAtTime(D, y, v);
        const I = P / N;
        I < S && g(E, D[D.length - 1], I), g(E, M[M.length - 1], S);
      } else
        T === null && _.flush(w.context.currentTime), _.add(d(M, y, v)), f.setValueCurveAtTime(M, y, v);
      return E;
    }
  };
  return n.set(E, f), t.set(E, w), e(E, T), E;
}, Eo = (e) => ({
  replay(t) {
    for (const n of e)
      if (n.type === "exponentialRampToValue") {
        const { endTime: r, value: o } = n;
        t.exponentialRampToValueAtTime(o, r);
      } else if (n.type === "linearRampToValue") {
        const { endTime: r, value: o } = n;
        t.linearRampToValueAtTime(o, r);
      } else if (n.type === "setTarget") {
        const { startTime: r, target: o, timeConstant: s } = n;
        t.setTargetAtTime(o, r, s);
      } else if (n.type === "setValue") {
        const { startTime: r, value: o } = n;
        t.setValueAtTime(o, r);
      } else if (n.type === "setValueCurve") {
        const { duration: r, startTime: o, values: s } = n;
        t.setValueCurveAtTime(s, o, r);
      } else
        throw new Error("Can't apply an unknown automation.");
  }
});
class mn {
  constructor(t) {
    this._map = new Map(t);
  }
  get size() {
    return this._map.size;
  }
  entries() {
    return this._map.entries();
  }
  forEach(t, n = null) {
    return this._map.forEach((r, o) => t.call(n, r, o, this));
  }
  get(t) {
    return this._map.get(t);
  }
  has(t) {
    return this._map.has(t);
  }
  keys() {
    return this._map.keys();
  }
  values() {
    return this._map.values();
  }
}
const bo = {
  channelCount: 2,
  // Bug #61: The channelCountMode should be 'max' according to the spec but is set to 'explicit' to achieve consistent behavior.
  channelCountMode: "explicit",
  channelInterpretation: "speakers",
  numberOfInputs: 1,
  numberOfOutputs: 1,
  parameterData: {},
  processorOptions: {}
}, Ao = (e, t, n, r, o, s, a, c, i, u, d, l, g, w) => class extends t {
  constructor(f, m, h) {
    var A;
    const _ = c(f), T = i(_), E = d({ ...bo, ...h });
    g(E);
    const b = st.get(_), y = b == null ? void 0 : b.get(m), v = T || _.state !== "closed" ? _ : (A = a(_)) !== null && A !== void 0 ? A : _, M = o(v, T ? null : f.baseLatency, u, m, y, E), S = T ? r(m, E, y) : null;
    super(f, !0, M, S);
    const N = [];
    M.parameters.forEach((P, B) => {
      const D = n(this, T, P);
      N.push([B, D]);
    }), this._nativeAudioWorkletNode = M, this._onprocessorerror = null, this._parameters = new mn(N), T && e(_, this);
    const { activeInputs: L } = s(this);
    l(M, L);
  }
  get onprocessorerror() {
    return this._onprocessorerror;
  }
  set onprocessorerror(f) {
    const m = typeof f == "function" ? w(this, f) : null;
    this._nativeAudioWorkletNode.onprocessorerror = m;
    const h = this._nativeAudioWorkletNode.onprocessorerror;
    this._onprocessorerror = h !== null && h === m ? f : h;
  }
  get parameters() {
    return this._parameters === null ? this._nativeAudioWorkletNode.parameters : this._parameters;
  }
  get port() {
    return this._nativeAudioWorkletNode.port;
  }
};
function De(e, t, n, r, o) {
  if (typeof e.copyFromChannel == "function")
    t[n].byteLength === 0 && (t[n] = new Float32Array(128)), e.copyFromChannel(t[n], r, o);
  else {
    const s = e.getChannelData(r);
    if (t[n].byteLength === 0)
      t[n] = s.slice(o, o + 128);
    else {
      const a = new Float32Array(s.buffer, o * Float32Array.BYTES_PER_ELEMENT, 128);
      t[n].set(a);
    }
  }
}
const gn = (e, t, n, r, o) => {
  typeof e.copyToChannel == "function" ? t[n].byteLength !== 0 && e.copyToChannel(t[n], r, o) : t[n].byteLength !== 0 && e.getChannelData(r).set(t[n], o);
}, We = (e, t) => {
  const n = [];
  for (let r = 0; r < e; r += 1) {
    const o = [], s = typeof t == "number" ? t : t[r];
    for (let a = 0; a < s; a += 1)
      o.push(new Float32Array(128));
    n.push(o);
  }
  return n;
}, Co = (e, t) => {
  const n = K(at, e), r = H(t);
  return K(n, r);
}, To = async (e, t, n, r, o, s, a) => {
  const c = t === null ? Math.ceil(e.context.length / 128) * 128 : t.length, i = r.channelCount * r.numberOfInputs, u = o.reduce((m, h) => m + h, 0), d = u === 0 ? null : n.createBuffer(u, c, n.sampleRate);
  if (s === void 0)
    throw new Error("Missing the processor constructor.");
  const l = z(e), g = await Co(n, e), w = We(r.numberOfInputs, r.channelCount), p = We(r.numberOfOutputs, o), f = Array.from(e.parameters.keys()).reduce((m, h) => ({ ...m, [h]: new Float32Array(128) }), {});
  for (let m = 0; m < c; m += 128) {
    if (r.numberOfInputs > 0 && t !== null)
      for (let h = 0; h < r.numberOfInputs; h += 1)
        for (let A = 0; A < r.channelCount; A += 1)
          De(t, w[h], A, A, m);
    s.parameterDescriptors !== void 0 && t !== null && s.parameterDescriptors.forEach(({ name: h }, A) => {
      De(t, f, h, i + A, m);
    });
    for (let h = 0; h < r.numberOfInputs; h += 1)
      for (let A = 0; A < o[h]; A += 1)
        p[h][A].byteLength === 0 && (p[h][A] = new Float32Array(128));
    try {
      const h = w.map((_, T) => l.activeInputs[T].size === 0 ? [] : _), A = a(m / n.sampleRate, n.sampleRate, () => g.process(h, p, f));
      if (d !== null)
        for (let _ = 0, T = 0; _ < r.numberOfOutputs; _ += 1) {
          for (let E = 0; E < o[_]; E += 1)
            gn(d, p[_], E, T + E, m);
          T += o[_];
        }
      if (!A)
        break;
    } catch (h) {
      e.dispatchEvent(new ErrorEvent("processorerror", {
        colno: h.colno,
        filename: h.filename,
        lineno: h.lineno,
        message: h.message
      }));
      break;
    }
  }
  return d;
}, Mo = (e, t, n, r, o, s, a, c, i, u, d, l, g, w, p, f) => (m, h, A) => {
  const _ = /* @__PURE__ */ new WeakMap();
  let T = null;
  const E = async (b, y) => {
    let v = d(b), M = null;
    const S = un(v, y), N = Array.isArray(h.outputChannelCount) ? h.outputChannelCount : Array.from(h.outputChannelCount);
    if (l === null) {
      const L = N.reduce((I, U) => I + U, 0), P = o(y, {
        channelCount: Math.max(1, L),
        channelCountMode: "explicit",
        channelInterpretation: "discrete",
        numberOfOutputs: Math.max(1, L)
      }), B = [];
      for (let I = 0; I < b.numberOfOutputs; I += 1)
        B.push(r(y, {
          channelCount: 1,
          channelCountMode: "explicit",
          channelInterpretation: "speakers",
          numberOfInputs: N[I]
        }));
      const D = a(y, {
        channelCount: h.channelCount,
        channelCountMode: h.channelCountMode,
        channelInterpretation: h.channelInterpretation,
        gain: 1
      });
      D.connect = t.bind(null, B), D.disconnect = i.bind(null, B), M = [P, B, D];
    } else
      S || (v = new l(y, m));
    if (_.set(y, M === null ? v : M[2]), M !== null) {
      if (T === null) {
        if (A === void 0)
          throw new Error("Missing the processor constructor.");
        if (g === null)
          throw new Error("Missing the native OfflineAudioContext constructor.");
        const U = b.channelCount * b.numberOfInputs, V = A.parameterDescriptors === void 0 ? 0 : A.parameterDescriptors.length, O = U + V;
        T = To(b, O === 0 ? null : await (async () => {
          const x = new g(
            O,
            // Ceil the length to the next full render quantum.
            // Bug #17: Safari does not yet expose the length.
            Math.ceil(b.context.length / 128) * 128,
            y.sampleRate
          ), $ = [], fe = [];
          for (let j = 0; j < h.numberOfInputs; j += 1)
            $.push(a(x, {
              channelCount: h.channelCount,
              channelCountMode: h.channelCountMode,
              channelInterpretation: h.channelInterpretation,
              gain: 1
            })), fe.push(o(x, {
              channelCount: h.channelCount,
              channelCountMode: "explicit",
              channelInterpretation: "discrete",
              numberOfOutputs: h.channelCount
            }));
          const he = await Promise.all(Array.from(b.parameters.values()).map(async (j) => {
            const X = s(x, {
              channelCount: 1,
              channelCountMode: "explicit",
              channelInterpretation: "discrete",
              offset: j.value
            });
            return await w(x, j, X.offset), X;
          })), pe = r(x, {
            channelCount: 1,
            channelCountMode: "explicit",
            channelInterpretation: "speakers",
            numberOfInputs: Math.max(1, U + V)
          });
          for (let j = 0; j < h.numberOfInputs; j += 1) {
            $[j].connect(fe[j]);
            for (let X = 0; X < h.channelCount; X += 1)
              fe[j].connect(pe, X, j * h.channelCount + X);
          }
          for (const [j, X] of he.entries())
            X.connect(pe, 0, U + j), X.start(0);
          return pe.connect(x.destination), await Promise.all($.map((j) => p(b, x, j))), f(x);
        })(), y, h, N, A, u);
      }
      const L = await T, P = n(y, {
        buffer: null,
        channelCount: 2,
        channelCountMode: "max",
        channelInterpretation: "speakers",
        loop: !1,
        loopEnd: 0,
        loopStart: 0,
        playbackRate: 1
      }), [B, D, I] = M;
      L !== null && (P.buffer = L, P.start(0)), P.connect(B);
      for (let U = 0, V = 0; U < b.numberOfOutputs; U += 1) {
        const O = D[U];
        for (let R = 0; R < N[U]; R += 1)
          B.connect(O, V + R, R);
        V += N[U];
      }
      return I;
    }
    if (S)
      for (const [L, P] of b.parameters.entries())
        await e(
          y,
          P,
          // @todo The definition that TypeScript uses of the AudioParamMap is lacking many methods.
          v.parameters.get(L)
        );
    else
      for (const [L, P] of b.parameters.entries())
        await w(
          y,
          P,
          // @todo The definition that TypeScript uses of the AudioParamMap is lacking many methods.
          v.parameters.get(L)
        );
    return await p(b, y, v), v;
  };
  return {
    render(b, y) {
      c(y, b);
      const v = _.get(y);
      return v !== void 0 ? Promise.resolve(v) : E(b, y);
    }
  };
}, No = (e, t) => (n, r) => {
  const o = t.get(n);
  if (o !== void 0)
    return o;
  const s = e.get(n);
  if (s !== void 0)
    return s;
  try {
    const a = r();
    return a instanceof Promise ? (e.set(n, a), a.catch(() => !1).then((c) => (e.delete(n), t.set(n, c), c))) : (t.set(n, a), a);
  } catch {
    return t.set(n, !1), !1;
  }
}, Oo = (e) => (t, n, r) => e(n, t, r), ko = (e) => (t, n, r = 0, o = 0) => {
  const s = t[r];
  if (s === void 0)
    throw e();
  return Ue(n) ? s.connect(n, 0, o) : s.connect(n, 0);
}, Io = (e) => (t) => (e[0] = t, e[0]), So = (e, t, n, r, o, s, a, c) => (i, u) => {
  const d = t.get(i);
  if (d === void 0)
    throw new Error("Missing the expected cycle count.");
  const l = s(i.context), g = c(l);
  if (d === u) {
    if (t.delete(i), !g && a(i)) {
      const w = r(i), { outputs: p } = n(i);
      for (const f of p)
        if (Ce(f)) {
          const m = r(f[0]);
          e(w, m, f[1], f[2]);
        } else {
          const m = o(f[0]);
          w.connect(m, f[1]);
        }
    }
  } else
    t.set(i, d - u);
}, Ro = (e) => (t, n, r, o) => e(t[o], (s) => s[0] === n && s[1] === r), Lo = (e) => (t, n) => {
  e(t).delete(n);
}, Po = (e) => "delayTime" in e, Bo = (e, t, n) => function r(o, s) {
  const a = Be(s) ? s : n(e, s);
  if (Po(a))
    return [];
  if (o[0] === a)
    return [o];
  if (o.includes(a))
    return [];
  const { outputs: c } = t(a);
  return Array.from(c).map((i) => r([...o, a], i[0])).reduce((i, u) => i.concat(u), []);
}, ke = (e, t, n) => {
  const r = t[n];
  if (r === void 0)
    throw e();
  return r;
}, Uo = (e) => (t, n = void 0, r = void 0, o = 0) => n === void 0 ? t.forEach((s) => s.disconnect()) : typeof n == "number" ? ke(e, t, n).disconnect() : Ue(n) ? r === void 0 ? t.forEach((s) => s.disconnect(n)) : o === void 0 ? ke(e, t, r).disconnect(n, 0) : ke(e, t, r).disconnect(n, 0, o) : r === void 0 ? t.forEach((s) => s.disconnect(n)) : ke(e, t, r).disconnect(n, 0), Do = (e) => (t) => new Promise((n, r) => {
  if (e === null) {
    r(new SyntaxError());
    return;
  }
  const o = e.document.head;
  if (o === null)
    r(new SyntaxError());
  else {
    const s = e.document.createElement("script"), a = new Blob([t], { type: "application/javascript" }), c = URL.createObjectURL(a), i = e.onerror, u = () => {
      e.onerror = i, URL.revokeObjectURL(c);
    };
    e.onerror = (d, l, g, w, p) => {
      if (l === c || l === e.location.href && g === 1 && w === 1)
        return u(), r(p), !1;
      if (i !== null)
        return i(d, l, g, w, p);
    }, s.onerror = () => {
      u(), r(new SyntaxError());
    }, s.onload = () => {
      u(), n();
    }, s.src = c, s.type = "module", o.appendChild(s);
  }
}), Wo = (e) => class {
  constructor(n) {
    this._nativeEventTarget = n, this._listeners = /* @__PURE__ */ new WeakMap();
  }
  addEventListener(n, r, o) {
    if (r !== null) {
      let s = this._listeners.get(r);
      s === void 0 && (s = e(this, r), typeof r == "function" && this._listeners.set(r, s)), this._nativeEventTarget.addEventListener(n, s, o);
    }
  }
  dispatchEvent(n) {
    return this._nativeEventTarget.dispatchEvent(n);
  }
  removeEventListener(n, r, o) {
    const s = r === null ? void 0 : this._listeners.get(r);
    this._nativeEventTarget.removeEventListener(n, s === void 0 ? null : s, o);
  }
}, Vo = (e) => (t, n, r) => {
  Object.defineProperties(e, {
    currentFrame: {
      configurable: !0,
      get() {
        return Math.round(t * n);
      }
    },
    currentTime: {
      configurable: !0,
      get() {
        return t;
      }
    }
  });
  try {
    return r();
  } finally {
    e !== null && (delete e.currentFrame, delete e.currentTime);
  }
}, xo = (e) => async (t) => {
  try {
    const n = await fetch(t);
    if (n.ok)
      return [await n.text(), n.url];
  } catch {
  }
  throw e();
}, Fo = (e, t) => (n) => t(e, n), jo = (e) => (t) => {
  const n = e(t);
  if (n.renderer === null)
    throw new Error("Missing the renderer of the given AudioNode in the audio graph.");
  return n.renderer;
}, Go = (e) => (t) => {
  var n;
  return (n = e.get(t)) !== null && n !== void 0 ? n : 0;
}, $o = (e) => (t) => {
  const n = e(t);
  if (n.renderer === null)
    throw new Error("Missing the renderer of the given AudioParam in the audio graph.");
  return n.renderer;
}, qo = (e) => (t) => e.get(t), Z = () => new DOMException("", "InvalidStateError"), zo = (e) => (t) => {
  const n = e.get(t);
  if (n === void 0)
    throw Z();
  return n;
}, Xo = (e, t) => (n) => {
  let r = e.get(n);
  if (r !== void 0)
    return r;
  if (t === null)
    throw new Error("Missing the native OfflineAudioContext constructor.");
  return r = new t(1, 1, 44100), e.set(n, r), r;
}, Yo = (e) => (t) => {
  const n = e.get(t);
  if (n === void 0)
    throw new Error("The context has no set of AudioWorkletNodes.");
  return n;
}, Ho = () => new DOMException("", "InvalidAccessError"), Zo = (e, t, n, r, o, s) => (a) => (c, i) => {
  const u = e.get(c);
  if (u === void 0) {
    if (!a && s(c)) {
      const d = r(c), { outputs: l } = n(c);
      for (const g of l)
        if (Ce(g)) {
          const w = r(g[0]);
          t(d, w, g[1], g[2]);
        } else {
          const w = o(g[0]);
          d.disconnect(w, g[1]);
        }
    }
    e.set(c, i);
  } else
    e.set(c, u + i);
}, Ko = (e) => (t) => e !== null && t instanceof e, Qo = (e) => (t) => e !== null && typeof e.AudioNode == "function" && t instanceof e.AudioNode, Jo = (e) => (t) => e !== null && typeof e.AudioParam == "function" && t instanceof e.AudioParam, es = (e) => (t) => e !== null && t instanceof e, ts = (e) => e !== null && e.isSecureContext, ns = (e, t, n, r) => class extends e {
  constructor(s, a) {
    const c = n(s), i = t(c, a);
    if (r(c))
      throw new TypeError();
    super(s, !0, i, null), this._nativeMediaStreamAudioSourceNode = i;
  }
  get mediaStream() {
    return this._nativeMediaStreamAudioSourceNode.mediaStream;
  }
}, rs = (e, t, n, r, o) => class extends r {
  constructor(a = {}) {
    if (o === null)
      throw new Error("Missing the native AudioContext constructor.");
    let c;
    try {
      c = new o(a);
    } catch (d) {
      throw d.code === 12 && d.message === "sampleRate is not in range" ? t() : d;
    }
    if (c === null)
      throw n();
    if (!ao(a.latencyHint))
      throw new TypeError(`The provided value '${a.latencyHint}' is not a valid enum value of type AudioContextLatencyCategory.`);
    if (a.sampleRate !== void 0 && c.sampleRate !== a.sampleRate)
      throw t();
    super(c, 2);
    const { latencyHint: i } = a, { sampleRate: u } = c;
    if (this._baseLatency = typeof c.baseLatency == "number" ? c.baseLatency : i === "balanced" ? 512 / u : i === "interactive" || i === void 0 ? 256 / u : i === "playback" ? 1024 / u : (
      /*
       * @todo The min (256) and max (16384) values are taken from the allowed bufferSize values of a
       * ScriptProcessorNode.
       */
      Math.max(2, Math.min(128, Math.round(i * u / 128))) * 128 / u
    ), this._nativeAudioContext = c, o.name === "webkitAudioContext" ? (this._nativeGainNode = c.createGain(), this._nativeOscillatorNode = c.createOscillator(), this._nativeGainNode.gain.value = 1e-37, this._nativeOscillatorNode.connect(this._nativeGainNode).connect(c.destination), this._nativeOscillatorNode.start()) : (this._nativeGainNode = null, this._nativeOscillatorNode = null), this._state = null, c.state === "running") {
      this._state = "suspended";
      const d = () => {
        this._state === "suspended" && (this._state = null), c.removeEventListener("statechange", d);
      };
      c.addEventListener("statechange", d);
    }
  }
  get baseLatency() {
    return this._baseLatency;
  }
  get state() {
    return this._state !== null ? this._state : this._nativeAudioContext.state;
  }
  close() {
    return this.state === "closed" ? this._nativeAudioContext.close().then(() => {
      throw e();
    }) : (this._state === "suspended" && (this._state = null), this._nativeAudioContext.close().then(() => {
      this._nativeGainNode !== null && this._nativeOscillatorNode !== null && (this._nativeOscillatorNode.stop(), this._nativeGainNode.disconnect(), this._nativeOscillatorNode.disconnect()), so(this);
    }));
  }
  resume() {
    return this._state === "suspended" ? new Promise((a, c) => {
      const i = () => {
        this._nativeAudioContext.removeEventListener("statechange", i), this._nativeAudioContext.state === "running" ? a() : this.resume().then(a, c);
      };
      this._nativeAudioContext.addEventListener("statechange", i);
    }) : this._nativeAudioContext.resume().catch((a) => {
      throw a === void 0 || a.code === 15 ? e() : a;
    });
  }
  suspend() {
    return this._nativeAudioContext.suspend().catch((a) => {
      throw a === void 0 ? e() : a;
    });
  }
}, os = (e, t, n, r, o, s) => class extends n {
  constructor(c, i) {
    super(c), this._nativeContext = c, rn.set(this, c), r(c) && o.set(c, /* @__PURE__ */ new Set()), this._destination = new e(this, i), this._listener = t(this, c), this._onstatechange = null;
  }
  get currentTime() {
    return this._nativeContext.currentTime;
  }
  get destination() {
    return this._destination;
  }
  get listener() {
    return this._listener;
  }
  get onstatechange() {
    return this._onstatechange;
  }
  set onstatechange(c) {
    const i = typeof c == "function" ? s(this, c) : null;
    this._nativeContext.onstatechange = i;
    const u = this._nativeContext.onstatechange;
    this._onstatechange = u !== null && u === i ? c : u;
  }
  get sampleRate() {
    return this._nativeContext.sampleRate;
  }
  get state() {
    return this._nativeContext.state;
  }
}, $t = (e) => {
  const t = new Uint32Array([1179011410, 40, 1163280727, 544501094, 16, 131073, 44100, 176400, 1048580, 1635017060, 4, 0]);
  try {
    const n = e.decodeAudioData(t.buffer, () => {
    });
    return n === void 0 ? !1 : (n.catch(() => {
    }), !0);
  } catch {
  }
  return !1;
}, ss = (e, t) => (n, r, o) => {
  const s = /* @__PURE__ */ new Set();
  return n.connect = /* @__PURE__ */ ((a) => (c, i = 0, u = 0) => {
    const d = s.size === 0;
    if (t(c))
      return a.call(n, c, i, u), e(s, [c, i, u], (l) => l[0] === c && l[1] === i && l[2] === u, !0), d && r(), c;
    a.call(n, c, i), e(s, [c, i], (l) => l[0] === c && l[1] === i, !0), d && r();
  })(n.connect), n.disconnect = /* @__PURE__ */ ((a) => (c, i, u) => {
    const d = s.size > 0;
    if (c === void 0)
      a.apply(n), s.clear();
    else if (typeof c == "number") {
      a.call(n, c);
      for (const g of s)
        g[1] === c && s.delete(g);
    } else {
      t(c) ? a.call(n, c, i, u) : a.call(n, c, i);
      for (const g of s)
        g[0] === c && (i === void 0 || g[1] === i) && (u === void 0 || g[2] === u) && s.delete(g);
    }
    const l = s.size === 0;
    d && l && o();
  })(n.disconnect), n;
}, se = (e, t, n) => {
  const r = t[n];
  r !== void 0 && r !== e[n] && (e[n] = r);
}, Te = (e, t) => {
  se(e, t, "channelCount"), se(e, t, "channelCountMode"), se(e, t, "channelInterpretation");
}, as = (e) => e === null ? null : e.hasOwnProperty("AudioBuffer") ? e.AudioBuffer : null, gt = (e, t, n) => {
  const r = t[n];
  r !== void 0 && r !== e[n].value && (e[n].value = r);
}, is = (e) => {
  e.start = /* @__PURE__ */ ((t) => {
    let n = !1;
    return (r = 0, o = 0, s) => {
      if (n)
        throw Z();
      t.call(e, r, o, s), n = !0;
    };
  })(e.start);
}, wn = (e) => {
  e.start = /* @__PURE__ */ ((t) => (n = 0, r = 0, o) => {
    if (typeof o == "number" && o < 0 || r < 0 || n < 0)
      throw new RangeError("The parameters can't be negative.");
    t.call(e, n, r, o);
  })(e.start);
}, vn = (e) => {
  e.stop = /* @__PURE__ */ ((t) => (n = 0) => {
    if (n < 0)
      throw new RangeError("The parameter can't be negative.");
    t.call(e, n);
  })(e.stop);
}, cs = (e, t, n, r, o, s, a, c, i, u, d) => (l, g) => {
  const w = l.createBufferSource();
  return Te(w, g), gt(w, g, "playbackRate"), se(w, g, "buffer"), se(w, g, "loop"), se(w, g, "loopEnd"), se(w, g, "loopStart"), t(n, () => n(l)) || is(w), t(r, () => r(l)) || i(w), t(o, () => o(l)) || u(w, l), t(s, () => s(l)) || wn(w), t(a, () => a(l)) || d(w, l), t(c, () => c(l)) || vn(w), e(l, w), w;
}, us = (e) => e === null ? null : e.hasOwnProperty("AudioContext") ? e.AudioContext : e.hasOwnProperty("webkitAudioContext") ? e.webkitAudioContext : null, ls = (e, t) => (n, r, o) => {
  const s = n.destination;
  if (s.channelCount !== r)
    try {
      s.channelCount = r;
    } catch {
    }
  o && s.channelCountMode !== "explicit" && (s.channelCountMode = "explicit"), s.maxChannelCount === 0 && Object.defineProperty(s, "maxChannelCount", {
    value: r
  });
  const a = e(n, {
    channelCount: r,
    channelCountMode: s.channelCountMode,
    channelInterpretation: s.channelInterpretation,
    gain: 1
  });
  return t(a, "channelCount", (c) => () => c.call(a), (c) => (i) => {
    c.call(a, i);
    try {
      s.channelCount = i;
    } catch (u) {
      if (i > s.maxChannelCount)
        throw u;
    }
  }), t(a, "channelCountMode", (c) => () => c.call(a), (c) => (i) => {
    c.call(a, i), s.channelCountMode = i;
  }), t(a, "channelInterpretation", (c) => () => c.call(a), (c) => (i) => {
    c.call(a, i), s.channelInterpretation = i;
  }), Object.defineProperty(a, "maxChannelCount", {
    get: () => s.maxChannelCount
  }), a.connect(s), a;
}, ds = (e) => e === null ? null : e.hasOwnProperty("AudioWorkletNode") ? e.AudioWorkletNode : null, fs = (e) => {
  const { port1: t } = new MessageChannel();
  try {
    t.postMessage(e);
  } finally {
    t.close();
  }
}, hs = (e, t, n, r, o) => (s, a, c, i, u, d) => {
  if (c !== null)
    try {
      const l = new c(s, i, d), g = /* @__PURE__ */ new Map();
      let w = null;
      if (Object.defineProperties(l, {
        /*
         * Bug #61: Overwriting the property accessors for channelCount and channelCountMode is necessary as long as some
         * browsers have no native implementation to achieve a consistent behavior.
         */
        channelCount: {
          get: () => d.channelCount,
          set: () => {
            throw e();
          }
        },
        channelCountMode: {
          get: () => "explicit",
          set: () => {
            throw e();
          }
        },
        // Bug #156: Chrome and Edge do not yet fire an ErrorEvent.
        onprocessorerror: {
          get: () => w,
          set: (p) => {
            typeof w == "function" && l.removeEventListener("processorerror", w), w = typeof p == "function" ? p : null, typeof w == "function" && l.addEventListener("processorerror", w);
          }
        }
      }), l.addEventListener = /* @__PURE__ */ ((p) => (...f) => {
        if (f[0] === "processorerror") {
          const m = typeof f[1] == "function" ? f[1] : typeof f[1] == "object" && f[1] !== null && typeof f[1].handleEvent == "function" ? f[1].handleEvent : null;
          if (m !== null) {
            const h = g.get(f[1]);
            h !== void 0 ? f[1] = h : (f[1] = (A) => {
              A.type === "error" ? (Object.defineProperties(A, {
                type: { value: "processorerror" }
              }), m(A)) : m(new ErrorEvent(f[0], { ...A }));
            }, g.set(m, f[1]));
          }
        }
        return p.call(l, "error", f[1], f[2]), p.call(l, ...f);
      })(l.addEventListener), l.removeEventListener = /* @__PURE__ */ ((p) => (...f) => {
        if (f[0] === "processorerror") {
          const m = g.get(f[1]);
          m !== void 0 && (g.delete(f[1]), f[1] = m);
        }
        return p.call(l, "error", f[1], f[2]), p.call(l, f[0], f[1], f[2]);
      })(l.removeEventListener), d.numberOfOutputs !== 0) {
        const p = n(s, {
          channelCount: 1,
          channelCountMode: "explicit",
          channelInterpretation: "discrete",
          gain: 0
        });
        return l.connect(p).connect(s.destination), o(l, () => p.disconnect(), () => p.connect(s.destination));
      }
      return l;
    } catch (l) {
      throw l.code === 11 ? r() : l;
    }
  if (u === void 0)
    throw r();
  return fs(d), t(s, a, u, d);
}, ps = (e, t) => e === null ? 512 : Math.max(512, Math.min(16384, Math.pow(2, Math.round(Math.log2(e * t))))), ms = (e) => new Promise((t, n) => {
  const { port1: r, port2: o } = new MessageChannel();
  r.onmessage = ({ data: s }) => {
    r.close(), o.close(), t(s);
  }, r.onmessageerror = ({ data: s }) => {
    r.close(), o.close(), n(s);
  }, o.postMessage(e);
}), gs = async (e, t) => {
  const n = await ms(t);
  return new e(n);
}, ws = (e, t, n, r) => {
  let o = at.get(e);
  o === void 0 && (o = /* @__PURE__ */ new WeakMap(), at.set(e, o));
  const s = gs(n, r);
  return o.set(t, s), s;
}, vs = (e, t, n, r, o, s, a, c, i, u, d, l, g) => (w, p, f, m) => {
  if (m.numberOfInputs === 0 && m.numberOfOutputs === 0)
    throw i();
  const h = Array.isArray(m.outputChannelCount) ? m.outputChannelCount : Array.from(m.outputChannelCount);
  if (h.some((C) => C < 1))
    throw i();
  if (h.length !== m.numberOfOutputs)
    throw t();
  if (m.channelCountMode !== "explicit")
    throw i();
  const A = m.channelCount * m.numberOfInputs, _ = h.reduce((C, k) => C + k, 0), T = f.parameterDescriptors === void 0 ? 0 : f.parameterDescriptors.length;
  if (A + T > 6 || _ > 6)
    throw i();
  const E = new MessageChannel(), b = [], y = [];
  for (let C = 0; C < m.numberOfInputs; C += 1)
    b.push(a(w, {
      channelCount: m.channelCount,
      channelCountMode: m.channelCountMode,
      channelInterpretation: m.channelInterpretation,
      gain: 1
    })), y.push(o(w, {
      channelCount: m.channelCount,
      channelCountMode: "explicit",
      channelInterpretation: "discrete",
      numberOfOutputs: m.channelCount
    }));
  const v = [];
  if (f.parameterDescriptors !== void 0)
    for (const { defaultValue: C, maxValue: k, minValue: q, name: F } of f.parameterDescriptors) {
      const W = s(w, {
        channelCount: 1,
        channelCountMode: "explicit",
        channelInterpretation: "discrete",
        offset: m.parameterData[F] !== void 0 ? m.parameterData[F] : C === void 0 ? 0 : C
      });
      Object.defineProperties(W.offset, {
        defaultValue: {
          get: () => C === void 0 ? 0 : C
        },
        maxValue: {
          get: () => k === void 0 ? ht : k
        },
        minValue: {
          get: () => q === void 0 ? je : q
        }
      }), v.push(W);
    }
  const M = r(w, {
    channelCount: 1,
    channelCountMode: "explicit",
    channelInterpretation: "speakers",
    numberOfInputs: Math.max(1, A + T)
  }), S = ps(p, w.sampleRate), N = c(
    w,
    S,
    A + T,
    // Bug #87: Only Firefox will fire an AudioProcessingEvent if there is no connected output.
    Math.max(1, _)
  ), L = o(w, {
    channelCount: Math.max(1, _),
    channelCountMode: "explicit",
    channelInterpretation: "discrete",
    numberOfOutputs: Math.max(1, _)
  }), P = [];
  for (let C = 0; C < m.numberOfOutputs; C += 1)
    P.push(r(w, {
      channelCount: 1,
      channelCountMode: "explicit",
      channelInterpretation: "speakers",
      numberOfInputs: h[C]
    }));
  for (let C = 0; C < m.numberOfInputs; C += 1) {
    b[C].connect(y[C]);
    for (let k = 0; k < m.channelCount; k += 1)
      y[C].connect(M, k, C * m.channelCount + k);
  }
  const B = new mn(f.parameterDescriptors === void 0 ? [] : f.parameterDescriptors.map(({ name: C }, k) => {
    const q = v[k];
    return q.connect(M, 0, A + k), q.start(0), [C, q.offset];
  }));
  M.connect(N);
  let D = m.channelInterpretation, I = null;
  const U = m.numberOfOutputs === 0 ? [N] : P, V = {
    get bufferSize() {
      return S;
    },
    get channelCount() {
      return m.channelCount;
    },
    set channelCount(C) {
      throw n();
    },
    get channelCountMode() {
      return m.channelCountMode;
    },
    set channelCountMode(C) {
      throw n();
    },
    get channelInterpretation() {
      return D;
    },
    set channelInterpretation(C) {
      for (const k of b)
        k.channelInterpretation = C;
      D = C;
    },
    get context() {
      return N.context;
    },
    get inputs() {
      return b;
    },
    get numberOfInputs() {
      return m.numberOfInputs;
    },
    get numberOfOutputs() {
      return m.numberOfOutputs;
    },
    get onprocessorerror() {
      return I;
    },
    set onprocessorerror(C) {
      typeof I == "function" && V.removeEventListener("processorerror", I), I = typeof C == "function" ? C : null, typeof I == "function" && V.addEventListener("processorerror", I);
    },
    get parameters() {
      return B;
    },
    get port() {
      return E.port2;
    },
    addEventListener(...C) {
      return N.addEventListener(C[0], C[1], C[2]);
    },
    connect: e.bind(null, U),
    disconnect: u.bind(null, U),
    dispatchEvent(...C) {
      return N.dispatchEvent(C[0]);
    },
    removeEventListener(...C) {
      return N.removeEventListener(C[0], C[1], C[2]);
    }
  }, O = /* @__PURE__ */ new Map();
  E.port1.addEventListener = /* @__PURE__ */ ((C) => (...k) => {
    if (k[0] === "message") {
      const q = typeof k[1] == "function" ? k[1] : typeof k[1] == "object" && k[1] !== null && typeof k[1].handleEvent == "function" ? k[1].handleEvent : null;
      if (q !== null) {
        const F = O.get(k[1]);
        F !== void 0 ? k[1] = F : (k[1] = (W) => {
          d(w.currentTime, w.sampleRate, () => q(W));
        }, O.set(q, k[1]));
      }
    }
    return C.call(E.port1, k[0], k[1], k[2]);
  })(E.port1.addEventListener), E.port1.removeEventListener = /* @__PURE__ */ ((C) => (...k) => {
    if (k[0] === "message") {
      const q = O.get(k[1]);
      q !== void 0 && (O.delete(k[1]), k[1] = q);
    }
    return C.call(E.port1, k[0], k[1], k[2]);
  })(E.port1.removeEventListener);
  let R = null;
  Object.defineProperty(E.port1, "onmessage", {
    get: () => R,
    set: (C) => {
      typeof R == "function" && E.port1.removeEventListener("message", R), R = typeof C == "function" ? C : null, typeof R == "function" && (E.port1.addEventListener("message", R), E.port1.start());
    }
  }), f.prototype.port = E.port1;
  let x = null;
  ws(w, V, f, m).then((C) => x = C);
  const fe = We(m.numberOfInputs, m.channelCount), he = We(m.numberOfOutputs, h), pe = f.parameterDescriptors === void 0 ? [] : f.parameterDescriptors.reduce((C, { name: k }) => ({ ...C, [k]: new Float32Array(128) }), {});
  let j = !0;
  const X = () => {
    m.numberOfOutputs > 0 && N.disconnect(L);
    for (let C = 0, k = 0; C < m.numberOfOutputs; C += 1) {
      const q = P[C];
      for (let F = 0; F < h[C]; F += 1)
        L.disconnect(q, k + F, F);
      k += h[C];
    }
  }, Me = /* @__PURE__ */ new Map();
  N.onaudioprocess = ({ inputBuffer: C, outputBuffer: k }) => {
    if (x !== null) {
      const q = l(V);
      for (let F = 0; F < S; F += 128) {
        for (let W = 0; W < m.numberOfInputs; W += 1)
          for (let G = 0; G < m.channelCount; G += 1)
            De(C, fe[W], G, G, F);
        f.parameterDescriptors !== void 0 && f.parameterDescriptors.forEach(({ name: W }, G) => {
          De(C, pe, W, A + G, F);
        });
        for (let W = 0; W < m.numberOfInputs; W += 1)
          for (let G = 0; G < h[W]; G += 1)
            he[W][G].byteLength === 0 && (he[W][G] = new Float32Array(128));
        try {
          const W = fe.map((Y, te) => {
            if (q[te].size > 0)
              return Me.set(te, S / 128), Y;
            const Ke = Me.get(te);
            return Ke === void 0 ? [] : (Y.every((qn) => qn.every((zn) => zn === 0)) && (Ke === 1 ? Me.delete(te) : Me.set(te, Ke - 1)), Y);
          });
          j = d(w.currentTime + F / w.sampleRate, w.sampleRate, () => x.process(W, he, pe));
          for (let Y = 0, te = 0; Y < m.numberOfOutputs; Y += 1) {
            for (let _e = 0; _e < h[Y]; _e += 1)
              gn(k, he[Y], _e, te + _e, F);
            te += h[Y];
          }
        } catch (W) {
          j = !1, V.dispatchEvent(new ErrorEvent("processorerror", {
            colno: W.colno,
            filename: W.filename,
            lineno: W.lineno,
            message: W.message
          }));
        }
        if (!j) {
          for (let W = 0; W < m.numberOfInputs; W += 1) {
            b[W].disconnect(y[W]);
            for (let G = 0; G < m.channelCount; G += 1)
              y[F].disconnect(M, G, W * m.channelCount + G);
          }
          if (f.parameterDescriptors !== void 0) {
            const W = f.parameterDescriptors.length;
            for (let G = 0; G < W; G += 1) {
              const Y = v[G];
              Y.disconnect(M, 0, A + G), Y.stop();
            }
          }
          M.disconnect(N), N.onaudioprocess = null, He ? X() : Nt();
          break;
        }
      }
    }
  };
  let He = !1;
  const Ze = a(w, {
    channelCount: 1,
    channelCountMode: "explicit",
    channelInterpretation: "discrete",
    gain: 0
  }), Mt = () => N.connect(Ze).connect(w.destination), Nt = () => {
    N.disconnect(Ze), Ze.disconnect();
  }, Gn = () => {
    if (j) {
      Nt(), m.numberOfOutputs > 0 && N.connect(L);
      for (let C = 0, k = 0; C < m.numberOfOutputs; C += 1) {
        const q = P[C];
        for (let F = 0; F < h[C]; F += 1)
          L.connect(q, k + F, F);
        k += h[C];
      }
    }
    He = !0;
  }, $n = () => {
    j && (Mt(), X()), He = !1;
  };
  return Mt(), g(V, Gn, $n);
}, _s = (e, t) => (n, r) => {
  const o = n.createChannelMerger(r.numberOfInputs);
  return e !== null && e.name === "webkitAudioContext" && t(n, o), Te(o, r), o;
}, ys = (e) => {
  const t = e.numberOfOutputs;
  Object.defineProperty(e, "channelCount", {
    get: () => t,
    set: (n) => {
      if (n !== t)
        throw Z();
    }
  }), Object.defineProperty(e, "channelCountMode", {
    get: () => "explicit",
    set: (n) => {
      if (n !== "explicit")
        throw Z();
    }
  }), Object.defineProperty(e, "channelInterpretation", {
    get: () => "discrete",
    set: (n) => {
      if (n !== "discrete")
        throw Z();
    }
  });
}, _n = (e, t) => {
  const n = e.createChannelSplitter(t.numberOfOutputs);
  return Te(n, t), ys(n), n;
}, Es = (e, t, n, r, o) => (s, a) => {
  if (s.createConstantSource === void 0)
    return n(s, a);
  const c = s.createConstantSource();
  return Te(c, a), gt(c, a, "offset"), t(r, () => r(s)) || wn(c), t(o, () => o(s)) || vn(c), e(s, c), c;
}, yn = (e, t) => (e.connect = t.connect.bind(t), e.disconnect = t.disconnect.bind(t), e), bs = (e, t, n, r) => (o, { offset: s, ...a }) => {
  const c = o.createBuffer(1, 2, 44100), i = t(o, {
    buffer: null,
    channelCount: 2,
    channelCountMode: "max",
    channelInterpretation: "speakers",
    loop: !1,
    loopEnd: 0,
    loopStart: 0,
    playbackRate: 1
  }), u = n(o, { ...a, gain: s }), d = c.getChannelData(0);
  d[0] = 1, d[1] = 1, i.buffer = c, i.loop = !0;
  const l = {
    get bufferSize() {
    },
    get channelCount() {
      return u.channelCount;
    },
    set channelCount(p) {
      u.channelCount = p;
    },
    get channelCountMode() {
      return u.channelCountMode;
    },
    set channelCountMode(p) {
      u.channelCountMode = p;
    },
    get channelInterpretation() {
      return u.channelInterpretation;
    },
    set channelInterpretation(p) {
      u.channelInterpretation = p;
    },
    get context() {
      return u.context;
    },
    get inputs() {
      return [];
    },
    get numberOfInputs() {
      return i.numberOfInputs;
    },
    get numberOfOutputs() {
      return u.numberOfOutputs;
    },
    get offset() {
      return u.gain;
    },
    get onended() {
      return i.onended;
    },
    set onended(p) {
      i.onended = p;
    },
    addEventListener(...p) {
      return i.addEventListener(p[0], p[1], p[2]);
    },
    dispatchEvent(...p) {
      return i.dispatchEvent(p[0]);
    },
    removeEventListener(...p) {
      return i.removeEventListener(p[0], p[1], p[2]);
    },
    start(p = 0) {
      i.start.call(i, p);
    },
    stop(p = 0) {
      i.stop.call(i, p);
    }
  }, g = () => i.connect(u), w = () => i.disconnect(u);
  return e(o, i), r(yn(l, u), g, w);
}, oe = (e, t) => {
  const n = e.createGain();
  return Te(n, t), gt(n, t, "gain"), n;
}, As = (e, { mediaStream: t }) => {
  const n = t.getAudioTracks();
  n.sort((s, a) => s.id < a.id ? -1 : s.id > a.id ? 1 : 0);
  const r = n.slice(0, 1), o = e.createMediaStreamSource(new MediaStream(r));
  return Object.defineProperty(o, "mediaStream", { value: t }), o;
}, Cs = (e) => e === null ? null : e.hasOwnProperty("OfflineAudioContext") ? e.OfflineAudioContext : e.hasOwnProperty("webkitOfflineAudioContext") ? e.webkitOfflineAudioContext : null, wt = (e, t, n, r) => e.createScriptProcessor(t, n, r), de = () => new DOMException("", "NotSupportedError"), Ts = (e, t) => (n, r, o) => (e(r).replay(o), t(r, n, o)), Ms = (e, t, n) => async (r, o, s) => {
  const a = e(r);
  await Promise.all(a.activeInputs.map((c, i) => Array.from(c).map(async ([u, d]) => {
    const g = await t(u).render(u, o), w = r.context.destination;
    !n(u) && (r !== w || !n(r)) && g.connect(s, d, i);
  })).reduce((c, i) => [...c, ...i], []));
}, Ns = (e, t, n) => async (r, o, s) => {
  const a = t(r);
  await Promise.all(Array.from(a.activeInputs).map(async ([c, i]) => {
    const d = await e(c).render(c, o);
    n(c) || d.connect(s, i);
  }));
}, Os = (e, t, n, r) => (o) => e($t, () => $t(o)) ? Promise.resolve(e(r, r)).then((s) => {
  if (!s) {
    const a = n(o, 512, 0, 1);
    o.oncomplete = () => {
      a.onaudioprocess = null, a.disconnect();
    }, a.onaudioprocess = () => o.currentTime, a.connect(o.destination);
  }
  return o.startRendering();
}) : new Promise((s) => {
  const a = t(o, {
    channelCount: 1,
    channelCountMode: "explicit",
    channelInterpretation: "discrete",
    gain: 0
  });
  o.oncomplete = (c) => {
    a.disconnect(), s(c.renderedBuffer);
  }, a.connect(o.destination), o.startRendering();
}), ks = (e) => (t, n) => {
  e.set(t, n);
}, Is = (e) => () => {
  if (e === null)
    return !1;
  try {
    new e({ length: 1, sampleRate: 44100 });
  } catch {
    return !1;
  }
  return !0;
}, Ss = (e, t) => async () => {
  if (e === null)
    return !0;
  if (t === null)
    return !1;
  const n = new Blob(['class A extends AudioWorkletProcessor{process(i){this.port.postMessage(i,[i[0][0].buffer])}}registerProcessor("a",A)'], {
    type: "application/javascript; charset=utf-8"
  }), r = new t(1, 128, 44100), o = URL.createObjectURL(n);
  let s = !1, a = !1;
  try {
    await r.audioWorklet.addModule(o);
    const c = new e(r, "a", { numberOfOutputs: 0 }), i = r.createOscillator();
    c.port.onmessage = () => s = !0, c.onprocessorerror = () => a = !0, i.connect(c), i.start(0), await r.startRendering(), await new Promise((u) => setTimeout(u));
  } catch {
  } finally {
    URL.revokeObjectURL(o);
  }
  return s && !a;
}, Rs = (e, t) => () => {
  if (t === null)
    return Promise.resolve(!1);
  const n = new t(1, 1, 44100), r = e(n, {
    channelCount: 1,
    channelCountMode: "explicit",
    channelInterpretation: "discrete",
    gain: 0
  });
  return new Promise((o) => {
    n.oncomplete = () => {
      r.disconnect(), o(n.currentTime !== 0);
    }, n.startRendering();
  });
}, Ls = () => new DOMException("", "UnknownError"), Ps = () => typeof window > "u" ? null : window, Bs = (e, t) => (n) => {
  n.copyFromChannel = (r, o, s = 0) => {
    const a = e(s), c = e(o);
    if (c >= n.numberOfChannels)
      throw t();
    const i = n.length, u = n.getChannelData(c), d = r.length;
    for (let l = a < 0 ? -a : 0; l + a < i && l < d; l += 1)
      r[l] = u[l + a];
  }, n.copyToChannel = (r, o, s = 0) => {
    const a = e(s), c = e(o);
    if (c >= n.numberOfChannels)
      throw t();
    const i = n.length, u = n.getChannelData(c), d = r.length;
    for (let l = a < 0 ? -a : 0; l + a < i && l < d; l += 1)
      u[l + a] = r[l];
  };
}, Us = (e) => (t) => {
  t.copyFromChannel = /* @__PURE__ */ ((n) => (r, o, s = 0) => {
    const a = e(s), c = e(o);
    if (a < t.length)
      return n.call(t, r, c, a);
  })(t.copyFromChannel), t.copyToChannel = /* @__PURE__ */ ((n) => (r, o, s = 0) => {
    const a = e(s), c = e(o);
    if (a < t.length)
      return n.call(t, r, c, a);
  })(t.copyToChannel);
}, Ds = (e) => (t, n) => {
  const r = n.createBuffer(1, 1, 44100);
  t.buffer === null && (t.buffer = r), e(t, "buffer", (o) => () => {
    const s = o.call(t);
    return s === r ? null : s;
  }, (o) => (s) => o.call(t, s === null ? r : s));
}, Ws = (e, t) => (n, r) => {
  r.channelCount = 1, r.channelCountMode = "explicit", Object.defineProperty(r, "channelCount", {
    get: () => 1,
    set: () => {
      throw e();
    }
  }), Object.defineProperty(r, "channelCountMode", {
    get: () => "explicit",
    set: () => {
      throw e();
    }
  });
  const o = n.createBufferSource();
  t(r, () => {
    const c = r.numberOfInputs;
    for (let i = 0; i < c; i += 1)
      o.connect(r, 0, i);
  }, () => o.disconnect(r));
}, Vs = (e, t, n) => e.copyFromChannel === void 0 ? e.getChannelData(n)[0] : (e.copyFromChannel(t, n), t[0]), vt = (e, t, n, r) => {
  let o = e;
  for (; !o.hasOwnProperty(t); )
    o = Object.getPrototypeOf(o);
  const { get: s, set: a } = Object.getOwnPropertyDescriptor(o, t);
  Object.defineProperty(e, t, { get: n(s), set: r(a) });
}, xs = (e) => ({
  ...e,
  outputChannelCount: e.outputChannelCount !== void 0 ? e.outputChannelCount : e.numberOfInputs === 1 && e.numberOfOutputs === 1 ? (
    /*
     * Bug #61: This should be the computedNumberOfChannels, but unfortunately that is almost impossible to fake. That's why
     * the channelCountMode is required to be 'explicit' as long as there is not a native implementation in every browser. That
     * makes sure the computedNumberOfChannels is equivilant to the channelCount which makes it much easier to compute.
     */
    [e.channelCount]
  ) : Array.from({ length: e.numberOfOutputs }, () => 1)
}), En = (e, t, n) => {
  try {
    e.setValueAtTime(t, n);
  } catch (r) {
    if (r.code !== 9)
      throw r;
    En(e, t, n + 1e-7);
  }
}, Fs = (e) => {
  const t = e.createBufferSource();
  t.start();
  try {
    t.start();
  } catch {
    return !0;
  }
  return !1;
}, js = (e) => {
  const t = e.createBufferSource(), n = e.createBuffer(1, 1, 44100);
  t.buffer = n;
  try {
    t.start(0, 1);
  } catch {
    return !1;
  }
  return !0;
}, Gs = (e) => {
  const t = e.createBufferSource();
  t.start();
  try {
    t.stop();
  } catch {
    return !1;
  }
  return !0;
}, bn = (e) => {
  const t = e.createOscillator();
  try {
    t.start(-1);
  } catch (n) {
    return n instanceof RangeError;
  }
  return !1;
}, $s = (e) => {
  const t = e.createBuffer(1, 1, 44100), n = e.createBufferSource();
  n.buffer = t, n.start(), n.stop();
  try {
    return n.stop(), !0;
  } catch {
    return !1;
  }
}, An = (e) => {
  const t = e.createOscillator();
  try {
    t.stop(-1);
  } catch (n) {
    return n instanceof RangeError;
  }
  return !1;
}, qs = (e) => {
  const { port1: t, port2: n } = new MessageChannel();
  try {
    t.postMessage(e);
  } finally {
    t.close(), n.close();
  }
}, zs = (e) => {
  e.start = /* @__PURE__ */ ((t) => (n = 0, r = 0, o) => {
    const s = e.buffer, a = s === null ? r : Math.min(s.duration, r);
    s !== null && a > s.duration - 0.5 / e.context.sampleRate ? t.call(e, n, 0, 0) : t.call(e, n, a, o);
  })(e.start);
}, Xs = (e, t) => {
  const n = t.createGain();
  e.connect(n);
  const r = /* @__PURE__ */ ((o) => () => {
    o.call(e, n), e.removeEventListener("ended", r);
  })(e.disconnect);
  e.addEventListener("ended", r), yn(e, n), e.stop = /* @__PURE__ */ ((o) => {
    let s = !1;
    return (a = 0) => {
      if (s)
        try {
          o.call(e, a);
        } catch {
          n.gain.setValueAtTime(0, a);
        }
      else
        o.call(e, a), s = !0;
    };
  })(e.stop);
}, Ge = (e, t) => (n) => {
  const r = { value: e };
  return Object.defineProperties(n, {
    currentTarget: r,
    target: r
  }), typeof t == "function" ? t.call(e, n) : t.handleEvent.call(e, n);
}, Ys = Wr(le), Hs = $r(le), Zs = Ro(Fe), Ks = /* @__PURE__ */ new WeakMap(), Qs = Go(Ks), we = No(/* @__PURE__ */ new Map(), /* @__PURE__ */ new WeakMap()), Q = Ps(), Cn = jo(z), _t = Ms(z, Cn, ie), ce = zo(rn), ve = Cs(Q), ee = es(ve), Tn = /* @__PURE__ */ new WeakMap(), Mn = Wo(Ge), $e = us(Q), Js = Ko($e), Nn = Qo(Q), ea = Jo(Q), Ee = ds(Q), qe = _o(Vr(Jt), Gr(Ys, Hs, ut, Zs, lt, z, Qs, be, H, le, ae, ie, Ie), we, Zo(ot, lt, z, H, ye, ae), ue, Ho, de, So(ut, ot, z, H, ye, ce, ae, ee), Bo(Tn, z, K), Mn, ce, Js, Nn, ea, ee, Ee), ta = /* @__PURE__ */ new WeakSet(), qt = as(Q), On = Io(new Uint32Array(1)), na = Bs(On, ue), ra = Us(On), oa = Hr(ta, we, de, qt, ve, Is(qt), na, ra), yt = qr(oe), kn = Ns(Cn, Ae, ie), In = Oo(kn), ze = cs(yt, we, Fs, js, Gs, bn, $s, An, zs, Ds(vt), Xs), Sn = Ts($o(Ae), kn), sa = Qr(In, ze, H, Sn, _t), Et = yo(xr(tn), Tn, nn, Eo, Rr, Lr, Pr, Br, Ur, tt, Kt, $e, En), aa = Kr(qe, sa, Et, Z, ze, ce, ee, Ge), ia = io(qe, co, ue, Z, ls(oe, vt), ce, ee, _t), Xe = ss(le, Nn), ca = Ws(Z, Xe), bt = _s($e, ca), ua = bs(yt, ze, oe, Xe), At = Es(yt, we, ua, bn, An), la = Os(we, oe, wt, Rs(oe, ve)), da = uo(Et, bt, At, wt, de, Vs, ee, vt), Rn = /* @__PURE__ */ new WeakMap(), fa = os(ia, da, Mn, ee, Rn, Ge), Ln = ts(Q), Ct = Vo(Q), Pn = /* @__PURE__ */ new WeakMap(), ha = Xo(Pn, ve), zt = Ln ? jr(
  we,
  de,
  Do(Q),
  Ct,
  xo(Dr),
  ce,
  ha,
  ee,
  Ee,
  /* @__PURE__ */ new WeakMap(),
  /* @__PURE__ */ new WeakMap(),
  Ss(Ee, ve),
  // @todo window is guaranteed to be defined because isSecureContext checks that as well.
  Q
) : void 0, pa = ns(qe, As, ce, ee), Bn = Yo(Rn), ma = zr(Bn), Un = ko(ue), ga = Lo(Bn), Dn = Uo(ue), Wn = /* @__PURE__ */ new WeakMap(), wa = Fo(Wn, K), va = vs(Un, ue, Z, bt, _n, At, oe, wt, de, Dn, Ct, wa, Xe), _a = hs(Z, va, oe, de, Xe), ya = Mo(In, Un, ze, bt, _n, At, oe, ga, Dn, Ct, H, Ee, ve, Sn, _t, la), Ea = qo(Pn), ba = ks(Wn), Xt = Ln ? Ao(ma, qe, Et, ya, _a, z, Ea, ce, ee, Ee, xs, ba, qs, Ge) : void 0, Aa = rs(Z, de, Ls, fa, $e), Vn = "Missing AudioWorklet support. Maybe this is not running in a secure context.", Ca = async (e, t, n, r, o) => {
  const { encoderId: s, port: a } = await Ht(o, t.sampleRate);
  if (Xt === void 0)
    throw new Error(Vn);
  const c = new aa(t, { buffer: e }), i = new pa(t, { mediaStream: r }), u = Or(Xt, t, { channelCount: n });
  return { audioBufferSourceNode: c, encoderId: s, mediaStreamAudioSourceNode: i, port: a, recorderAudioWorkletNode: u };
}, Ta = (e, t, n, r) => (o, s, a) => {
  var c;
  const i = (c = s.getAudioTracks()[0]) === null || c === void 0 ? void 0 : c.getSettings().sampleRate, u = new Aa({ latencyHint: "playback", sampleRate: i }), d = Math.max(1024, Math.ceil(u.baseLatency * u.sampleRate)), l = new oa({ length: d, sampleRate: u.sampleRate }), g = [], w = Nr((v) => {
    if (zt === void 0)
      throw new Error(Vn);
    return zt(u, v);
  });
  let p = null, f = null, m = null, h = null, A = !0;
  const _ = (v) => {
    o.dispatchEvent(e("dataavailable", { data: new Blob(v, { type: a }) }));
  }, T = async (v, M) => {
    const S = await Se(v, M);
    m === null ? g.push(...S) : (_(S), h = T(v, M));
  }, E = () => (A = !0, u.resume()), b = () => {
    m !== null && (p !== null && (s.removeEventListener("addtrack", p), s.removeEventListener("removetrack", p)), f !== null && clearTimeout(f), m.then(async ({ encoderId: v, mediaStreamAudioSourceNode: M, recorderAudioWorkletNode: S }) => {
      h !== null && (h.catch(() => {
      }), h = null), await S.stop(), M.disconnect(S);
      const N = await Se(v, null);
      m === null && await y(), _([...g, ...N]), g.length = 0, o.dispatchEvent(new Event("stop"));
    }), m = null);
  }, y = () => (A = !1, u.suspend());
  return y(), {
    get mimeType() {
      return a;
    },
    get state() {
      return m === null ? "inactive" : A ? "recording" : "paused";
    },
    pause() {
      if (m === null)
        throw n();
      A && (y(), o.dispatchEvent(new Event("pause")));
    },
    resume() {
      if (m === null)
        throw n();
      A || (E(), o.dispatchEvent(new Event("resume")));
    },
    start(v) {
      var M;
      if (m !== null)
        throw n();
      if (s.getVideoTracks().length > 0)
        throw r();
      o.dispatchEvent(new Event("start"));
      const S = s.getAudioTracks(), N = S.length === 0 ? 2 : (M = S[0].getSettings().channelCount) !== null && M !== void 0 ? M : 2;
      m = Promise.all([
        E(),
        w.then(() => Ca(l, u, N, s, a))
      ]).then(async ([, { audioBufferSourceNode: P, encoderId: B, mediaStreamAudioSourceNode: D, port: I, recorderAudioWorkletNode: U }]) => (D.connect(U), await new Promise((V) => {
        P.onended = V, P.connect(U), P.start(u.currentTime + d / u.sampleRate);
      }), P.disconnect(U), await U.record(I), v !== void 0 && (h = T(B, v)), { encoderId: B, mediaStreamAudioSourceNode: D, recorderAudioWorkletNode: U }));
      const L = s.getTracks();
      p = () => {
        b(), o.dispatchEvent(new ErrorEvent("error", { error: t() }));
      }, s.addEventListener("addtrack", p), s.addEventListener("removetrack", p), f = setInterval(() => {
        const P = s.getTracks();
        (P.length !== L.length || P.some((B, D) => B !== L[D])) && p !== null && p();
      }, 1e3);
    },
    stop: b
  };
};
class Je {
  constructor(t, n = 0, r) {
    if (n < 0 || r !== void 0 && r < 0)
      throw new RangeError();
    const o = t.reduce((d, l) => d + l.byteLength, 0);
    if (n > o || r !== void 0 && n + r > o)
      throw new RangeError();
    const s = [], a = r === void 0 ? o - n : r, c = [];
    let i = 0, u = n;
    for (const d of t)
      if (c.length === 0)
        if (d.byteLength > u) {
          i = d.byteLength - u;
          const l = i > a ? a : i;
          s.push(new DataView(d, u, l)), c.push(d);
        } else
          u -= d.byteLength;
      else if (i < a) {
        i += d.byteLength;
        const l = i > a ? d.byteLength - i + a : d.byteLength;
        s.push(new DataView(d, 0, l)), c.push(d);
      }
    this._buffers = c, this._byteLength = a, this._byteOffset = u, this._dataViews = s, this._internalBuffer = new DataView(new ArrayBuffer(8));
  }
  get buffers() {
    return this._buffers;
  }
  get byteLength() {
    return this._byteLength;
  }
  get byteOffset() {
    return this._byteOffset;
  }
  getFloat32(t, n) {
    return this._internalBuffer.setUint8(0, this.getUint8(t + 0)), this._internalBuffer.setUint8(1, this.getUint8(t + 1)), this._internalBuffer.setUint8(2, this.getUint8(t + 2)), this._internalBuffer.setUint8(3, this.getUint8(t + 3)), this._internalBuffer.getFloat32(0, n);
  }
  getFloat64(t, n) {
    return this._internalBuffer.setUint8(0, this.getUint8(t + 0)), this._internalBuffer.setUint8(1, this.getUint8(t + 1)), this._internalBuffer.setUint8(2, this.getUint8(t + 2)), this._internalBuffer.setUint8(3, this.getUint8(t + 3)), this._internalBuffer.setUint8(4, this.getUint8(t + 4)), this._internalBuffer.setUint8(5, this.getUint8(t + 5)), this._internalBuffer.setUint8(6, this.getUint8(t + 6)), this._internalBuffer.setUint8(7, this.getUint8(t + 7)), this._internalBuffer.getFloat64(0, n);
  }
  getInt16(t, n) {
    return this._internalBuffer.setUint8(0, this.getUint8(t + 0)), this._internalBuffer.setUint8(1, this.getUint8(t + 1)), this._internalBuffer.getInt16(0, n);
  }
  getInt32(t, n) {
    return this._internalBuffer.setUint8(0, this.getUint8(t + 0)), this._internalBuffer.setUint8(1, this.getUint8(t + 1)), this._internalBuffer.setUint8(2, this.getUint8(t + 2)), this._internalBuffer.setUint8(3, this.getUint8(t + 3)), this._internalBuffer.getInt32(0, n);
  }
  getInt8(t) {
    const [n, r] = this._findDataViewWithOffset(t);
    return n.getInt8(t - r);
  }
  getUint16(t, n) {
    return this._internalBuffer.setUint8(0, this.getUint8(t + 0)), this._internalBuffer.setUint8(1, this.getUint8(t + 1)), this._internalBuffer.getUint16(0, n);
  }
  getUint32(t, n) {
    return this._internalBuffer.setUint8(0, this.getUint8(t + 0)), this._internalBuffer.setUint8(1, this.getUint8(t + 1)), this._internalBuffer.setUint8(2, this.getUint8(t + 2)), this._internalBuffer.setUint8(3, this.getUint8(t + 3)), this._internalBuffer.getUint32(0, n);
  }
  getUint8(t) {
    const [n, r] = this._findDataViewWithOffset(t);
    return n.getUint8(t - r);
  }
  setFloat32(t, n, r) {
    this._internalBuffer.setFloat32(0, n, r), this.setUint8(t, this._internalBuffer.getUint8(0)), this.setUint8(t + 1, this._internalBuffer.getUint8(1)), this.setUint8(t + 2, this._internalBuffer.getUint8(2)), this.setUint8(t + 3, this._internalBuffer.getUint8(3));
  }
  setFloat64(t, n, r) {
    this._internalBuffer.setFloat64(0, n, r), this.setUint8(t, this._internalBuffer.getUint8(0)), this.setUint8(t + 1, this._internalBuffer.getUint8(1)), this.setUint8(t + 2, this._internalBuffer.getUint8(2)), this.setUint8(t + 3, this._internalBuffer.getUint8(3)), this.setUint8(t + 4, this._internalBuffer.getUint8(4)), this.setUint8(t + 5, this._internalBuffer.getUint8(5)), this.setUint8(t + 6, this._internalBuffer.getUint8(6)), this.setUint8(t + 7, this._internalBuffer.getUint8(7));
  }
  setInt16(t, n, r) {
    this._internalBuffer.setInt16(0, n, r), this.setUint8(t, this._internalBuffer.getUint8(0)), this.setUint8(t + 1, this._internalBuffer.getUint8(1));
  }
  setInt32(t, n, r) {
    this._internalBuffer.setInt32(0, n, r), this.setUint8(t, this._internalBuffer.getUint8(0)), this.setUint8(t + 1, this._internalBuffer.getUint8(1)), this.setUint8(t + 2, this._internalBuffer.getUint8(2)), this.setUint8(t + 3, this._internalBuffer.getUint8(3));
  }
  setInt8(t, n) {
    const [r, o] = this._findDataViewWithOffset(t);
    r.setInt8(t - o, n);
  }
  setUint16(t, n, r) {
    this._internalBuffer.setUint16(0, n, r), this.setUint8(t, this._internalBuffer.getUint8(0)), this.setUint8(t + 1, this._internalBuffer.getUint8(1));
  }
  setUint32(t, n, r) {
    this._internalBuffer.setUint32(0, n, r), this.setUint8(t, this._internalBuffer.getUint8(0)), this.setUint8(t + 1, this._internalBuffer.getUint8(1)), this.setUint8(t + 2, this._internalBuffer.getUint8(2)), this.setUint8(t + 3, this._internalBuffer.getUint8(3));
  }
  setUint8(t, n) {
    const [r, o] = this._findDataViewWithOffset(t);
    r.setUint8(t - o, n);
  }
  _findDataViewWithOffset(t) {
    let n = 0;
    for (const r of this._dataViews) {
      const o = n + r.byteLength;
      if (t >= n && t < o)
        return [r, n];
      n = o;
    }
    throw new RangeError();
  }
}
const Ma = (e, t, n) => (r, o, s, a) => {
  const c = [], i = new o(s, { mimeType: "audio/webm;codecs=pcm" });
  let u = null, d = () => {
  };
  const l = (p) => {
    r.dispatchEvent(e("dataavailable", { data: new Blob(p, { type: a }) }));
  }, g = async (p, f) => {
    const m = await Se(p, f);
    i.state === "inactive" ? c.push(...m) : (l(m), u = g(p, f));
  }, w = () => {
    i.state !== "inactive" && (u !== null && (u.catch(() => {
    }), u = null), d(), d = () => {
    }, i.stop());
  };
  return i.addEventListener("error", (p) => {
    w(), r.dispatchEvent(new ErrorEvent("error", {
      error: p.error
    }));
  }), i.addEventListener("pause", () => r.dispatchEvent(new Event("pause"))), i.addEventListener("resume", () => r.dispatchEvent(new Event("resume"))), i.addEventListener("start", () => r.dispatchEvent(new Event("start"))), {
    get mimeType() {
      return a;
    },
    get state() {
      return i.state;
    },
    pause() {
      return i.pause();
    },
    resume() {
      return i.resume();
    },
    start(p) {
      const [f] = s.getAudioTracks();
      if (f !== void 0 && i.state === "inactive") {
        const { channelCount: m, sampleRate: h } = f.getSettings();
        if (m === void 0)
          throw new Error("The channelCount is not defined.");
        if (h === void 0)
          throw new Error("The sampleRate is not defined.");
        let A = !1, _ = !1, T = 0, E = Ht(a, h);
        d = () => {
          _ = !0;
        };
        const b = Zt(i, "dataavailable")(({ data: y }) => {
          T += 1;
          const v = y.arrayBuffer();
          E = E.then(async ({ dataView: M = null, elementType: S = null, encoderId: N, port: L }) => {
            const P = await v;
            T -= 1;
            const B = M === null ? new Je([P]) : new Je([...M.buffers, P], M.byteOffset);
            if (!A && i.state === "recording" && !_) {
              const O = n(B, 0);
              if (O === null)
                return { dataView: B, elementType: S, encoderId: N, port: L };
              const { value: R } = O;
              if (R !== 172351395)
                return { dataView: M, elementType: S, encoderId: N, port: L };
              A = !0;
            }
            const { currentElementType: D, offset: I, contents: U } = t(B, S, m), V = I < B.byteLength ? new Je(B.buffers, B.byteOffset + I) : null;
            return U.forEach((O) => L.postMessage(O, O.map(({ buffer: R }) => R))), T === 0 && (i.state === "inactive" || _) && (Se(N, null).then((O) => {
              l([...c, ...O]), c.length = 0, r.dispatchEvent(new Event("stop"));
            }), L.postMessage([]), L.close(), b()), { dataView: V, elementType: D, encoderId: N, port: L };
          });
        });
        p !== void 0 && E.then(({ encoderId: y }) => u = g(y, p));
      }
      i.start(100);
    },
    stop: w
  };
}, Na = () => typeof window > "u" ? null : window, xn = (e, t) => {
  if (t >= e.byteLength)
    return null;
  const n = e.getUint8(t);
  if (n > 127)
    return 1;
  if (n > 63)
    return 2;
  if (n > 31)
    return 3;
  if (n > 15)
    return 4;
  if (n > 7)
    return 5;
  if (n > 3)
    return 6;
  if (n > 1)
    return 7;
  if (n > 0)
    return 8;
  const r = xn(e, t + 1);
  return r === null ? null : r + 8;
}, Oa = (e, t) => (n) => {
  const r = { value: e };
  return Object.defineProperties(n, {
    currentTarget: r,
    target: r
  }), typeof t == "function" ? t.call(e, n) : t.handleEvent.call(e, n);
}, Ve = [], Ye = Na(), ka = lr(Ye), Fn = nr(ka), Ia = Ta(Fn, ar, ir, et), Tt = mr(xn), Sa = hr(Tt), Ra = pr(Tt), La = rr(Sa, Ra), Pa = Ma(Fn, La, Tt), Ba = sr(Ye), Ua = dr(Ye), Ha = ur(fr(et), et, Ia, Pa, Ve, or(Ba, Oa), Ua), jn = /* @__PURE__ */ new WeakMap(), Za = async (e) => {
  await er(e);
  const t = jn.get(e);
  if (t !== void 0) {
    const n = Ve.indexOf(t);
    Ve.splice(n, 1);
  }
}, Ka = () => cr(Ye), Qa = async (e) => {
  const t = await tr(e);
  Ve.push(t), jn.set(e, t);
};
export {
  Ha as MediaRecorder,
  Za as deregister,
  Ka as isSupported,
  Qa as register
};
