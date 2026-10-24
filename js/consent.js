/* Consentimento de cookies (estilo RGPD) + carregamento condicional do Google AdSense */
(function(){
"use strict";
var C=window.SV_CONFIG||{},KEY="sv_consent",loaded=false;
function get(){try{return JSON.parse(localStorage.getItem(KEY))}catch(e){return null}}
function set(ads){try{localStorage.setItem(KEY,JSON.stringify({v:1,ads:!!ads,ts:Date.now()}))}catch(e){}}
function adsConfigurados(){return /^ca-pub-\d{16}$/.test(C.ADSENSE_CLIENT||"")}
function montarSlots(){
  var n=0;
  document.querySelectorAll(".ad-slot").forEach(function(s){
    var id=C.SLOTS&&C.SLOTS[s.dataset.slot];
    if(!/^\d{10}$/.test(id||"")||s.dataset.ready)return;
    var ins=document.createElement("ins");ins.className="adsbygoogle";ins.style.display="block";
    ins.setAttribute("data-ad-client",C.ADSENSE_CLIENT);ins.setAttribute("data-ad-slot",id);
    ins.setAttribute("data-ad-format","auto");ins.setAttribute("data-full-width-responsive","true");
    s.appendChild(ins);s.classList.add("on");s.dataset.ready="1";n++;
    try{(window.adsbygoogle=window.adsbygoogle||[]).push({})}catch(e){}
  });
  return n;
}
function carregarAnuncios(){
  if(loaded||!adsConfigurados())return;loaded=true;
  var sc=document.createElement("script");sc.async=true;sc.crossOrigin="anonymous";
  sc.src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client="+encodeURIComponent(C.ADSENSE_CLIENT);
  document.head.appendChild(sc);montarSlots();
}
var banner;
function fechar(){if(banner){banner.remove();banner=null}}
function abrir(){
  if(banner)return;
  banner=document.createElement("div");banner.id="cookie-banner";banner.setAttribute("role","dialog");banner.setAttribute("aria-label","Consentimento de cookies");
  banner.innerHTML='<p><strong>🍪 Privacidade e cookies</strong><br>O SymbolVault guarda no teu browser (localStorage) as tuas preferências, favoritos e símbolos recentes. Com o teu consentimento, parceiros como o Google AdSense podem usar cookies para mostrar anúncios. Podes mudar de ideias a qualquer momento em «Gerir cookies». <a href="privacidade.html">Política de Privacidade</a></p><div class="cb-btns"><button type="button" class="btn" id="cb-no">Recusar</button><button type="button" class="btn pri" id="cb-yes">Aceitar anúncios</button></div>';
  document.body.appendChild(banner);
  banner.querySelector("#cb-yes").addEventListener("click",function(){var antes=get();set(true);fechar();carregarAnuncios()});
  banner.querySelector("#cb-no").addEventListener("click",function(){var antes=get();set(false);fechar();if(antes&&antes.ads)location.reload()});
}
document.addEventListener("click",function(e){var b=e.target.closest&&e.target.closest("[data-cookie-settings]");if(b){e.preventDefault();abrir()}});
function init(){var c=get();if(!c)abrir();else if(c.ads)carregarAnuncios()}
if(document.readyState==="loading")document.addEventListener("DOMContentLoaded",init);else init();
})();
