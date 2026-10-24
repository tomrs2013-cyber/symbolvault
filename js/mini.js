/* Páginas de conteúdo: grelhas de símbolos com cópia ao clicar */
(function(){
"use strict";
var $=function(s){return document.querySelector(s)};
var toast=document.createElement("div");toast.id="toast";toast.setAttribute("role","status");toast.setAttribute("aria-live","polite");document.body.appendChild(toast);
function mostrar(m){toast.textContent=m;toast.classList.add("on");clearTimeout(mostrar.t);mostrar.t=setTimeout(function(){toast.classList.remove("on")},1600)}
async function copiar(t){try{await navigator.clipboard.writeText(t);return true}catch(e){var a=document.createElement("textarea");a.value=t;a.style.cssText="position:fixed;opacity:0";document.body.appendChild(a);a.select();var ok=false;try{ok=document.execCommand("copy")}catch(_){}a.remove();return ok}}
function cat(id){var c=SV_CATS.find(function(x){return x.id===id});return c?c.s:[]}
var nick=$("#nickIn");
function base(){var v=nick&&nick.value.trim();return v&&/[A-Za-z0-9]/.test(v)?v:"Gamer"}
var FONTES={
  cat:function(a){return cat(a)},
  catn:function(a){var p=a.split(":");return cat(p[0]).slice(0,+p[1])},
  tryhard:function(){return TRYHARD},
  tryleet:function(){return TRYHARD.filter(function(x){return /^[A-Za-z0-9_]+$/.test(x)})},
  presets:function(){var n=base();return PRESETS.map(function(p){return aplicar(p,n)})},
  leetpresets:function(){var n=base();return PRESETS.filter(function(p){return !/[^A-Za-z0-9_{}nLT]/.test(p)}).map(function(p){return aplicar(p,n)})},
  fancy:function(){var n=base();return ESTILOS.map(function(e){return e.f(n)})}
};
function render(g){
  var spec=g.dataset.src.split("|"),out=[];
  spec.forEach(function(sp){var i=sp.indexOf(":"),k=i<0?sp:sp.slice(0,i),a=i<0?"":sp.slice(i+1);if(FONTES[k])out=out.concat(FONTES[k](a))});
  g.innerHTML="";var f=document.createDocumentFragment();
  out.forEach(function(s){var b=document.createElement("button");b.type="button";b.className="sym";b.textContent=s;b.dataset.s=s;b.setAttribute("aria-label","Copiar "+s);f.appendChild(b)});
  g.appendChild(f);
}
var grids=document.querySelectorAll("[data-src]");
grids.forEach(render);
if(nick){var t;nick.addEventListener("input",function(){clearTimeout(t);t=setTimeout(function(){grids.forEach(function(g){if(/presets|fancy/.test(g.dataset.src))render(g)})},120)})}
document.addEventListener("click",async function(e){
  var b=e.target.closest&&e.target.closest(".sym");if(!b||!b.dataset.s)return;
  var ok=await copiar(b.dataset.s);mostrar(ok?"Copiado: "+(Array.from(b.dataset.s).length>24?Array.from(b.dataset.s).slice(0,24).join("")+"…":b.dataset.s):"Não foi possível copiar");
  b.classList.remove("pop");void b.offsetWidth;b.classList.add("pop");
});
})();
