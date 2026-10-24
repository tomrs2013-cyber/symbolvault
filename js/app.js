(function(){
"use strict";
const $=s=>document.querySelector(s);
const el=(t,c,x)=>{const e=document.createElement(t);if(c)e.className=c;if(x!=null)e.textContent=x;return e};
const nome=$("#nome"),busca=$("#busca"),toast=$("#toast"),info=$("#info");
const LS={get(k,d){try{return JSON.parse(localStorage.getItem(k))??d}catch(e){return d}},set(k,v){try{localStorage.setItem(k,JSON.stringify(v))}catch(e){}}};
let recentes=LS.get("sv_rec",[]),favs=LS.get("sv_fav",[]);
const reduce=matchMedia("(prefers-reduced-motion: reduce)").matches;

/* ---------- utilitários ---------- */
const norm=s=>s.toLowerCase().normalize("NFD").replace(/[\u0300-\u036f]/g,"");
const hex=c=>"U+"+c.codePointAt(0).toString(16).toUpperCase().padStart(4,"0");
const len=s=>Array.from(s).length;
const baseNome=()=>{const v=nome.value.trim();return v&&/[A-Za-z0-9]/.test(v)?v:"Gamer"};

/* ---------- compatibilidade (heurística indicativa) ---------- */
function compatChar(c){
  const cp=c.codePointAt(0);
  const letraBasica=/^[A-Za-z0-9 _.\-]$/.test(c)||(cp>=0xC0&&cp<=0x24F&&/\p{L}/u.test(c));
  if(letraBasica)return{epic:1,roblox:1,discord:1,steam:1};
  const raro=cp>=0x1D000||(cp>=0x1F000)||(cp>=0x2800&&cp<=0x28FF&&false);
  return{epic:0,roblox:0,discord:1,steam:raro&&cp>=0x1F000?0:1};
}
function compat(s){
  const r={epic:1,roblox:1,discord:1,steam:1};
  for(const c of s){const x=compatChar(c);for(const k in r)r[k]=r[k]&&x[k]}
  return r;
}
const JOGOS={epic:"Epic/Fortnite",roblox:"Roblox",discord:"Discord",steam:"Steam"};
function tagsHTML(s,box){
  box.innerHTML="";const r=compat(s);
  for(const k in JOGOS){const t=el("span","tag "+(r[k]?"ok":"maybe"),JOGOS[k]+": "+(r[k]?"provável":"pode não funcionar"));box.appendChild(t)}
}

/* ---------- feedback ---------- */
function mostrar(m){toast.textContent=m;toast.classList.add("on");clearTimeout(mostrar.t);mostrar.t=setTimeout(()=>toast.classList.remove("on"),1700)}
async function copiar(t){
  try{await navigator.clipboard.writeText(t);return true}catch(e){
    const a=document.createElement("textarea");a.value=t;a.style.cssText="position:fixed;opacity:0";document.body.appendChild(a);a.select();
    let ok=false;try{ok=document.execCommand("copy")}catch(_){}a.remove();return ok}
}
const fx=$("#fx"),ctx=fx.getContext("2d");let parts=[],anim=false;
function confete(x,y){
  if(reduce)return;
  if(fx.width!==innerWidth||fx.height!==innerHeight){fx.width=innerWidth;fx.height=innerHeight}fx.classList.add("on");
  const cores=["#8b5cf6","#22d3ee","#f472b6","#fbbf24","#34d399"];
  for(let i=0;i<22;i++){const a=Math.random()*Math.PI*2,v=2+Math.random()*4;parts.push({x,y,vx:Math.cos(a)*v,vy:Math.sin(a)*v-2,l:1,c:cores[i%5],s:3+Math.random()*3})}
  if(!anim){anim=true;requestAnimationFrame(passo)}
}
function passo(){
  ctx.clearRect(0,0,fx.width,fx.height);
  parts=parts.filter(p=>p.l>0);
  parts.forEach(p=>{p.x+=p.vx;p.y+=p.vy;p.vy+=.18;p.l-=.022;ctx.globalAlpha=Math.max(p.l,0);ctx.fillStyle=p.c;ctx.fillRect(p.x,p.y,p.s,p.s)});
  if(parts.length)requestAnimationFrame(passo);else{anim=false;ctx.clearRect(0,0,fx.width,fx.height);fx.classList.remove("on")}
}
function ripple(b,ev){
  const r=b.getBoundingClientRect(),d=Math.max(r.width,r.height),s=el("span","ripple");
  s.style.cssText=`width:${d}px;height:${d}px;left:${(ev&&ev.clientX?ev.clientX-r.left:r.width/2)-d/2}px;top:${(ev&&ev.clientY?ev.clientY-r.top:r.height/2)-d/2}px`;
  b.appendChild(s);setTimeout(()=>s.remove(),650);
  b.classList.remove("pop");void b.offsetWidth;b.classList.add("pop");
}
function efeito(b,ev){
  if(!b)return;ripple(b,ev);const r=b.getBoundingClientRect();
  confete(ev&&ev.clientX?ev.clientX:r.left+r.width/2,ev&&ev.clientY?ev.clientY:r.top+r.height/2);
}

/* ---------- estado do nick ---------- */
function atualizarNome(){
  const v=nome.value;
  $("#contagem").textContent=len(v)+" caracteres";
  $("#previewBig").textContent=v||"Nick";
  $("#miniNick").hidden=!v;$("#miniTxt").textContent=v;document.body.classList.toggle("has-nick",!!v);
  tagsHTML(v||"a",$("#compatNome"));
  clearTimeout(atualizarNome.t);atualizarNome.t=setTimeout(()=>{desenharPresets();desenharFancy()},120);
}
function guardarRec(s){recentes=[s,...recentes.filter(x=>x!==s)].slice(0,30);LS.set("sv_rec",recentes);desenharLista("#recentes",recentes,"#recentes-box")}
async function usarTexto(txt,b,ev){
  const ok=await copiar(txt);
  mostrar(ok?"Copiado: "+(len(txt)>24?Array.from(txt).slice(0,24).join("")+"…":txt):"Não foi possível copiar – seleciona manualmente");
  efeito(b,ev);guardarRec(txt);
}
async function usarSimbolo(s,b,ev){
  const partes=s.split(" ");
  const envolve=b&&b.dataset.wrap&&partes.length===2;
  if(envolve){
    const res=partes[0]+baseNome()+partes[1];
    if($("#modoNome").checked){nome.value=partes[0]+(nome.value||"")+partes[1];atualizarNome()}
    return usarTexto(res,b,ev);
  }
  if($("#modoNome").checked){nome.value+=s;atualizarNome()}
  usarTexto(s,b,ev);
}

/* ---------- células ---------- */
function celula(s,opts={}){
  const b=el("button","sym");
  b.type="button";b.dataset.s=s;
  if(opts.wrap&&s.includes(" ")){b.dataset.wrap="1";b.textContent=s.replace(" "," … ")}else b.textContent=s;
  b.setAttribute("aria-label","Copiar "+s);
  if(opts.copyOnly)b.dataset.copy="1";
  else if(favs.includes(s))b.classList.add("isfav");
  return b;
}
function desenharLista(sel,arr,boxSel){
  const g=$(sel);g.innerHTML="";const frag=document.createDocumentFragment();
  arr.forEach(s=>frag.appendChild(celula(s,{wrap:false})));g.appendChild(frag);
  $(boxSel).hidden=!arr.length;
}
function toggleFav(s){
  const on=!favs.includes(s);
  favs=on?[s,...favs]:favs.filter(x=>x!==s);
  LS.set("sv_fav",favs);
  document.querySelectorAll(".sym").forEach(b=>{if(b.dataset.s===s&&!b.dataset.copy)b.classList.toggle("isfav",on)});
  desenharLista("#favoritos",favs,"#favoritos-box");
  favBtnEstado(s);
  mostrar(on?"♥ Adicionado aos favoritos":"Removido dos favoritos");
}
/* botão de favorito único, posicionado sobre o símbolo em hover */
const favBtn=el("button",null,"♥");favBtn.id="favBtn";favBtn.type="button";document.body.appendChild(favBtn);
function favBtnEstado(s){const on=favs.includes(s);favBtn.setAttribute("aria-pressed",on);favBtn.setAttribute("aria-label",(on?"Remover dos favoritos: ":"Adicionar aos favoritos: ")+s)}
function favBtnMostrar(b){
  if(b.dataset.copy){favBtn.classList.remove("on");return}
  const r=b.getBoundingClientRect();favBtn.style.left=(r.right-26)+"px";favBtn.style.top=(r.top+2)+"px";
  favBtn.dataset.f=b.dataset.s;favBtnEstado(b.dataset.s);favBtn.classList.add("on");
}
favBtn.addEventListener("click",()=>toggleFav(favBtn.dataset.f));
addEventListener("scroll",()=>favBtn.classList.remove("on"),{passive:true});

/* ---------- info (hover / foco / toque longo) ---------- */
function mostrarInfo(s,b){
  const cps=Array.from(s);let nomeU=SV_NAMES[s];
  if(!nomeU)nomeU=cps.length>1?cps.length+" caracteres":"—";
  const cod=cps.length>6?cps.slice(0,6).map(hex).join(" ")+" …":cps.map(hex).join(" ");
  info.innerHTML="";
  const big=el("div","big",s.replace(" "," … "));info.appendChild(big);
  const l=el("div");l.innerHTML="<code></code> · <span></span>";l.firstChild.textContent=cod;l.lastChild.textContent=nomeU.toLowerCase();info.appendChild(l);
  const t=el("div","tags");tagsHTML(s,t);info.appendChild(t);
  info.classList.remove("touch");
  info.classList.add("on");
}
function infoToque(s){
  mostrarInfo(s);info.classList.add("touch");
  const f=el("button","btn peq favt",favs.includes(s)?"♥ Remover dos favoritos":"♡ Adicionar aos favoritos");f.type="button";
  f.addEventListener("click",()=>{toggleFav(s);esconderInfo()});info.appendChild(f);
}
function esconderInfo(){info.classList.remove("on")}
let lp=null,lpFired=false;
document.addEventListener("pointerover",e=>{const b=e.target.closest&&e.target.closest(".sym");if(b&&e.pointerType==="mouse"&&b.dataset.s){mostrarInfo(b.dataset.s,b);favBtnMostrar(b)}});
document.addEventListener("pointerout",e=>{const b=e.target.closest&&e.target.closest(".sym");if(b&&e.pointerType==="mouse"){esconderInfo();if(!(e.relatedTarget&&e.relatedTarget.id==="favBtn"))favBtn.classList.remove("on")}});
favBtn.addEventListener("pointerleave",()=>favBtn.classList.remove("on"));
document.addEventListener("focusin",e=>{const b=e.target.closest&&e.target.closest(".sym");if(b&&b.dataset.s)mostrarInfo(b.dataset.s,b)});
document.addEventListener("focusout",e=>{if(e.target.closest&&e.target.closest(".sym"))esconderInfo()});
document.addEventListener("pointerdown",e=>{
  const b=e.target.closest&&e.target.closest(".sym");lpFired=false;
  if(b&&e.pointerType!=="mouse"&&b.dataset.s){lp=setTimeout(()=>{lpFired=true;infoToque(b.dataset.s);clearTimeout(esconderInfo.t);esconderInfo.t=setTimeout(esconderInfo,5000)},450)}
});
["pointerup","pointercancel","pointermove"].forEach(t=>document.addEventListener(t,()=>{clearTimeout(lp)}));
document.addEventListener("contextmenu",e=>{if(e.target.closest&&e.target.closest(".sym")&&lpFired)e.preventDefault()});

/* ---------- cliques (delegação) ---------- */
document.addEventListener("click",e=>{
  const b=e.target.closest&&e.target.closest(".sym");
  if(!b)return;
  if(lpFired){lpFired=false;return}
  if(b.dataset.copy)usarTexto(b.dataset.s,b,e);else usarSimbolo(b.dataset.s,b,e);
});

/* ---------- predefinições ---------- */
function desenharPresets(){
  const n=baseNome(),frag=document.createDocumentFragment(),g=$("#presets");g.innerHTML="";
  PRESETS.forEach(p=>frag.appendChild(celula(aplicar(p,n),{copyOnly:true})));g.appendChild(frag);
  const g2=$("#tryhardProntos");if(!g2.children.length){const f2=document.createDocumentFragment();TRYHARD.forEach(t=>f2.appendChild(celula(t,{copyOnly:true})));g2.appendChild(f2)}
}
/* ---------- aleatório ---------- */
const PAL=["Ruthless","Sweat","Clutch","Headshot","Demon","Elite","Slayer","Reaper","N0Mercy","MLG","Tryhard","Sombra","Lobo","Ninja","Dragão","Fénix","Trovão","Falcão","Titã","Fantasma","Rei","Samurai","Viking","Cobra","Raio","Gelo","Fogo","Alpha","Omega","Nova","Vortex","Pixel","Turbo","Zeus","Hunter","Sniper","Rogue","Storm","Blaze","Shadow","Phantom","Cyber","Neon","Reaper","Wolf","Hawk","Ghost","Titan","Comet","Astro","Nitro","Glitch","Boss","Lenda","Mestre","Guerreiro","Caçador","Tubarão","Aranha"];
const DEC=["★彡 | 彡★","꧁ | ꧂","༺ | ༻","【 | 】","『 | 』","✦ | ✦","⚔ | ⚔","☠ | ☠","♛ | ♛","✧ | ✧","ミ | ミ","« | »","✪ | ✪","𓆩 | 𓆪","⚝ | ⚝","❖ | ❖","☬ | ☬","⛧ | ⛧","≪ | ≫","-=≡ | ≡=-"];
const pick=a=>a[Math.floor(Math.random()*a.length)];
function gerarUm(){
  const w=pick(PAL)+(Math.random()<.4?pick(PAL):"")+(Math.random()<.35?Math.floor(Math.random()*99):"");
  const st=Math.random()<.55?pick(ESTILOS.slice(0,20)):null;
  const t=st?st.f(w):w;const[a,b]=pick(DEC).split(" | ");
  return Math.random()<.85?a+" "+t+" "+b:t+" "+pick(["ツ","★","☠","♛","⚡","✦"]);
}
function gerar(){
  const g=$("#aleatorios");g.innerHTML="";
  for(let i=0;i<12;i++)g.appendChild(celula(gerarUm(),{copyOnly:true}));
}
/* ---------- fancy ---------- */
function desenharFancy(){
  const g=$("#fancyGrid");g.innerHTML="";const t=baseNome();
  ESTILOS.forEach(e=>{const c=celula(e.f(t),{copyOnly:true});c.title=e.n;c.setAttribute("aria-label","Copiar estilo "+e.n+": "+e.f(t));g.appendChild(c)});
  $("#fancyN").textContent="("+ESTILOS.length+" estilos)";
}

/* ---------- categorias ---------- */
const filtroCompat=$("#filtroCompat");
function simbolosVisiveis(c,q){
  let arr=c.s;const qn=norm(q);
  if(q){
    const catMatch=norm(c.t+" "+c.k).includes(qn);
    if(!catMatch){
      const u=q.toLowerCase().replace(/^u\+?/,"");const isHex=/^[0-9a-f]{2,6}$/.test(u)&&/^u/i.test(q);
      arr=arr.filter(s=>s.includes(q)||(SV_NAMES[s]&&SV_NAMES[s].toLowerCase().includes(q.toLowerCase()))||(isHex&&hex(s).toLowerCase().includes(u)));
    }
  }
  const fc=filtroCompat.value;
  if(fc)arr=arr.filter(s=>compat(s)[fc]);
  return arr;
}
function desenhar(){
  const g=$("#grelha");g.innerHTML="";const q=busca.value.trim();let total=0;
  const chips=$("#chips");
  chips.innerHTML="";
  SV_CATS.forEach(c=>{
    const arr=simbolosVisiveis(c,q);if(!arr.length)return;total+=arr.length;
    const s=el("section","cat");s.id="cat-"+c.id;s.dataset.n=arr.length;s.dataset.l=(c.id==="kaomoji"||c.id==="combos")?"1":"";
    const h=el("h3");h.innerHTML='<span class="ic" aria-hidden="true"></span><span></span><small></small>';
    h.children[0].textContent=c.icon;h.children[1].textContent=c.t;h.children[2].textContent="("+arr.length+")";
    s.appendChild(h);
    const gr=el("div","grid"+(c.id==="kaomoji"||c.id==="combos"||c.id==="bandeiras"&&false?" largo":""));
    const frag=document.createDocumentFragment();
    arr.forEach(x=>frag.appendChild(celula(x,{wrap:c.id==="combos"})));
    gr.appendChild(frag);s.appendChild(gr);g.appendChild(s);
    const a=el("a",null,c.icon+" "+c.t+" ");a.href="#cat-"+c.id;a.appendChild(el("small",null,arr.length));chips.appendChild(a);
  });
  calibrar();
  [["builder","🛠","Construtor"],["predefinicoes","😈","Tryhard"],["gerador","🎲","Gerador"],["fancy","🔤","Estilos"],["faq","❓","FAQ"]].forEach(([id,ic,t])=>{const a=el("a",null,ic+" "+t);a.href="#"+id;chips.appendChild(a)});
  $("#vazio").hidden=total>0;
  observar();
}
function calibrar(){
  const W=$("#grelha").clientWidth||innerWidth-28,sz=parseFloat(getComputedStyle(document.documentElement).getPropertyValue("--sz"))||26;
  document.querySelectorAll("#grelha .cat").forEach(c=>{
    const largo=c.dataset.l==="1",minW=largo?190:sz*2.1,cols=Math.max(1,Math.floor((W+7)/(minW+7))),rowH=(largo?52:sz*2)+7;
    c.style.setProperty("--ch",(34+10+Math.ceil(c.dataset.n/cols)*rowH-7)+"px");
  });
}
let rz;addEventListener("resize",()=>{clearTimeout(rz);rz=setTimeout(calibrar,150)},{passive:true});
let io;
function observar(){
  if(io)io.disconnect();
  if(!("IntersectionObserver" in window))return;
  io=new IntersectionObserver(es=>{es.forEach(en=>{if(en.isIntersecting){if(0)0;
    document.querySelectorAll("#chips a").forEach(a=>a.classList.toggle("on",a.getAttribute("href")==="#"+en.target.id));
    const on=document.querySelector("#chips a.on"),ch=$("#chips");if(on)ch.scrollLeft=on.offsetLeft-ch.clientWidth/2+on.offsetWidth/2;
  }})},{rootMargin:"-140px 0px -70% 0px"});
  document.querySelectorAll(".cat,#builder,#predefinicoes,#gerador,#fancy,#faq").forEach(s=>io.observe(s));
}

/* ---------- ações ---------- */
$("#copiarNome").addEventListener("click",async e=>{if(!nome.value)return mostrar("O nick está vazio");const ok=await copiar(nome.value);mostrar(ok?"Nick copiado!":"Não foi possível copiar");if(ok){efeito(e.currentTarget,e);guardarRec(nome.value)}});
$("#miniCopiar").addEventListener("click",e=>$("#copiarNome").click());
$("#miniLimpar").addEventListener("click",()=>{nome.value="";atualizarNome()});
$("#limparNome").addEventListener("click",()=>{nome.value="";atualizarNome();nome.focus()});
$("#desfazer").addEventListener("click",()=>{nome.value=Array.from(nome.value).slice(0,-1).join("");atualizarNome();nome.focus()});
$("#limparRec").addEventListener("click",()=>{recentes=[];LS.set("sv_rec",[]);desenharLista("#recentes",recentes,"#recentes-box")});
$("#limparFav").addEventListener("click",()=>{favs=[];LS.set("sv_fav",[]);document.querySelectorAll(".sym.isfav").forEach(f=>f.classList.remove("isfav"));desenharLista("#favoritos",favs,"#favoritos-box")});
$("#gerar").addEventListener("click",gerar);
$("#heroRandom").addEventListener("click",e=>{const s=gerarUm();nome.value=s;atualizarNome();gerar();copiar(s).then(ok=>mostrar(ok?"Nick copiado: "+s:"Nick gerado: "+s));efeito(e.currentTarget,e)});
nome.addEventListener("input",atualizarNome);
$("#tam").addEventListener("input",e=>{document.documentElement.style.setProperty("--sz",e.target.value+"px");LS.set("sv_tam",e.target.value);calibrar()});
let dt;busca.addEventListener("input",()=>{clearTimeout(dt);dt=setTimeout(desenhar,150)});
filtroCompat.addEventListener("change",desenhar);
function tema(t){document.documentElement.dataset.theme=t;LS.set("sv_tema",t);document.querySelector('meta[name=theme-color]').content=t==="dark"?"#07060f":"#f4f3ff"}
$("#tema").addEventListener("click",()=>tema(document.documentElement.dataset.theme==="dark"?"light":"dark"));
$("#ajuda").addEventListener("click",()=>$("#dlg").showModal&&$("#dlg").showModal());
document.addEventListener("keydown",e=>{
  const tag=(e.target.tagName||"").toLowerCase(),typing=tag==="input"||tag==="textarea"||tag==="select";
  if(e.key==="Escape"){if(document.activeElement===busca||busca.value){busca.value="";desenhar();busca.blur()}return}
  if(typing||e.ctrlKey||e.metaKey||e.altKey)return;
  const k=e.key.toLowerCase();
  if(k==="/"){e.preventDefault();busca.focus()}
  else if(k==="n"){e.preventDefault();nome.focus()}
  else if(k==="c"){$("#copiarNome").click()}
  else if(k==="r"){gerar();mostrar("🎲 Novos nicks gerados")}
  else if(k==="t"){$("#tema").click()}
  else if(k==="?"){$("#ajuda").click()}
  else if(k==="f"){const b=document.activeElement;if(b&&b.classList.contains("sym")&&!b.dataset.copy)toggleFav(b.dataset.s)}
});

/* ---------- init ---------- */
(function(){
  const t=LS.get("sv_tema","dark");tema(t);
  const z=LS.get("sv_tam",26);$("#tam").value=z;document.documentElement.style.setProperty("--sz",z+"px");
  const uniq=new Set();SV_CATS.forEach(c=>c.s.forEach(s=>uniq.add(s)));
  const st=$("#stats");
  [[uniq.size.toLocaleString("pt-PT"),"símbolos únicos"],[SV_CATS.length,"categorias"],[ESTILOS.length,"estilos de letra"],[PRESETS.length+TRYHARD.length,"nicks tryhard"]].forEach(([n,t])=>{const li=el("li");li.appendChild(el("b",null,n));li.appendChild(el("span",null,t));st.appendChild(li)});
  window.__sv={total:uniq.size};
  atualizarNome();desenharPresets();desenharFancy();gerar();desenhar();
  desenharLista("#recentes",recentes,"#recentes-box");desenharLista("#favoritos",favs,"#favoritos-box");
})();
})();
