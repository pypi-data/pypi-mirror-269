!function(){"use strict";var e,t,n,r,o,u,i,c,f,a={},l={};function d(e){var t=l[e];if(void 0!==t)return t.exports;var n=l[e]={id:e,loaded:!1,exports:{}},r=!0;try{a[e](n,n.exports,d),r=!1}finally{r&&delete l[e]}return n.loaded=!0,n.exports}d.m=a,e=[],d.O=function(t,n,r,o){if(n){o=o||0;for(var u=e.length;u>0&&e[u-1][2]>o;u--)e[u]=e[u-1];e[u]=[n,r,o];return}for(var i=1/0,u=0;u<e.length;u++){for(var n=e[u][0],r=e[u][1],o=e[u][2],c=!0,f=0;f<n.length;f++)i>=o&&Object.keys(d.O).every(function(e){return d.O[e](n[f])})?n.splice(f--,1):(c=!1,o<i&&(i=o));if(c){e.splice(u--,1);var a=r();void 0!==a&&(t=a)}}return t},d.n=function(e){var t=e&&e.__esModule?function(){return e.default}:function(){return e};return d.d(t,{a:t}),t},n=Object.getPrototypeOf?function(e){return Object.getPrototypeOf(e)}:function(e){return e.__proto__},d.t=function(e,r){if(1&r&&(e=this(e)),8&r||"object"==typeof e&&e&&(4&r&&e.__esModule||16&r&&"function"==typeof e.then))return e;var o=Object.create(null);d.r(o);var u={};t=t||[null,n({}),n([]),n(n)];for(var i=2&r&&e;"object"==typeof i&&!~t.indexOf(i);i=n(i))Object.getOwnPropertyNames(i).forEach(function(t){u[t]=function(){return e[t]}});return u.default=function(){return e},d.d(o,u),o},d.d=function(e,t){for(var n in t)d.o(t,n)&&!d.o(e,n)&&Object.defineProperty(e,n,{enumerable:!0,get:t[n]})},d.f={},d.e=function(e){return Promise.all(Object.keys(d.f).reduce(function(t,n){return d.f[n](e,t),t},[]))},d.u=function(e){},d.miniCssF=function(e){return"static/css/dc347b0d22ffde5d.css"},d.g=function(){if("object"==typeof globalThis)return globalThis;try{return this||Function("return this")()}catch(e){if("object"==typeof window)return window}}(),d.o=function(e,t){return Object.prototype.hasOwnProperty.call(e,t)},r={},o="_N_E:",d.l=function(e,t,n,u){if(r[e]){r[e].push(t);return}if(void 0!==n)for(var i,c,f=document.getElementsByTagName("script"),a=0;a<f.length;a++){var l=f[a];if(l.getAttribute("src")==e||l.getAttribute("data-webpack")==o+n){i=l;break}}i||(c=!0,(i=document.createElement("script")).charset="utf-8",i.timeout=120,d.nc&&i.setAttribute("nonce",d.nc),i.setAttribute("data-webpack",o+n),i.src=d.tu(e)),r[e]=[t];var s=function(t,n){i.onerror=i.onload=null,clearTimeout(p);var o=r[e];if(delete r[e],i.parentNode&&i.parentNode.removeChild(i),o&&o.forEach(function(e){return e(n)}),t)return t(n)},p=setTimeout(s.bind(null,void 0,{type:"timeout",target:i}),12e4);i.onerror=s.bind(null,i.onerror),i.onload=s.bind(null,i.onload),c&&document.head.appendChild(i)},d.r=function(e){"undefined"!=typeof Symbol&&Symbol.toStringTag&&Object.defineProperty(e,Symbol.toStringTag,{value:"Module"}),Object.defineProperty(e,"__esModule",{value:!0})},d.nmd=function(e){return e.paths=[],e.children||(e.children=[]),e},d.tt=function(){return void 0===u&&(u={createScriptURL:function(e){return e}},"undefined"!=typeof trustedTypes&&trustedTypes.createPolicy&&(u=trustedTypes.createPolicy("nextjs#bundler",u))),u},d.tu=function(e){return d.tt().createScriptURL(e)},d.p="/ui/_next/",i={272:0},d.f.j=function(e,t){var n=d.o(i,e)?i[e]:void 0;if(0!==n){if(n)t.push(n[2]);else if(272!=e){var r=new Promise(function(t,r){n=i[e]=[t,r]});t.push(n[2]=r);var o=d.p+d.u(e),u=Error();d.l(o,function(t){if(d.o(i,e)&&(0!==(n=i[e])&&(i[e]=void 0),n)){var r=t&&("load"===t.type?"missing":t.type),o=t&&t.target&&t.target.src;u.message="Loading chunk "+e+" failed.\n("+r+": "+o+")",u.name="ChunkLoadError",u.type=r,u.request=o,n[1](u)}},"chunk-"+e,e)}else i[e]=0}},d.O.j=function(e){return 0===i[e]},c=function(e,t){var n,r,o=t[0],u=t[1],c=t[2],f=0;if(o.some(function(e){return 0!==i[e]})){for(n in u)d.o(u,n)&&(d.m[n]=u[n]);if(c)var a=c(d)}for(e&&e(t);f<o.length;f++)r=o[f],d.o(i,r)&&i[r]&&i[r][0](),i[r]=0;return d.O(a)},(f=self.webpackChunk_N_E=self.webpackChunk_N_E||[]).forEach(c.bind(null,0)),f.push=c.bind(null,f.push.bind(f))}();