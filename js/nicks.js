/* Funções e listas partilhadas (estilos de letra, leetspeak, modelos de nick tryhard) */
function estilizar(txt,e){
  const U=Array.from(e[1]),L=Array.from(e[2]),D=e[3]?Array.from(e[3]):null;
  return Array.from(txt).map(c=>{
    if(c>="A"&&c<="Z")return U[c.charCodeAt(0)-65]||c;
    if(c>="a"&&c<="z")return L[c.charCodeAt(0)-97]||c;
    if(D&&c>="0"&&c<="9")return D[+c]||c;
    return c}).join("");
}
const ESTILOS=SV_STYLES.map(e=>({n:e[0],f:t=>estilizar(t,e)}));
SV_COMBINING.forEach(([n,m])=>ESTILOS.push({n,f:t=>Array.from(t).map(c=>c===" "?c:c+m).join("")}));
const LEET={a:"4",e:"3",i:"1",o:"0",s:"5",t:"7",A:"4",E:"3",I:"1",O:"0",S:"5",T:"7"};
const TRY={A:"Д",B:"ß",C:"Ҫ",D:"Đ",E:"Σ",F:"Ғ",G:"Ϛ",H:"Н",I:"Ї",J:"Ј",K:"Қ",L:"Ł",M:"Ϻ",N:"И",O:"Ө",P:"Ҏ",Q:"Ǫ",R:"Я",S:"Ƨ",T:"Ҭ",U:"Ц",V:"Ѵ",W:"Ш",X:"Ҳ",Y:"У",Z:"Ƶ"};
const leet=t=>Array.from(t).map(c=>LEET[c]||c).join("");
const tryg=t=>Array.from(t.toUpperCase()).map(c=>TRY[c]||c).join("");
const est=n=>ESTILOS.find(e=>e.n===n);
const FANCY={B:"Negrito serifa",G:"Gótico negrito",K:"Versaletes",C:"Cursivo negrito",D:"Duplo traço",Q:"Largo (fullwidth)"};
function aplicar(tpl,n){
  const sem=n.replace(/\s+/g,"_");
  return tpl.replace(/\{([nLTUBGKCDQ])\}/g,(m,k)=>{
    if(k==="n")return sem;if(k==="L")return leet(sem);if(k==="T")return tryg(sem);if(k==="U")return sem.toUpperCase();
    const e=est(FANCY[k]);return e?e.f(sem):sem});
}
/* Modelos aplicados ao nick: {n} nick, {L} leetspeak, {T} glifos tryhard, {U} maiúsculas, {B}{G}{K}{C}{D}{Q} fontes */
const PRESETS=["꧁༺ xX_{n}_Xx ༻꧂","彡{n}彡","☠ {L} ☠","TTV_{n}","TTV_{L}","{n}_TTV","xX_{n}_Xx","Xx{L}xX","MLG_{n}","{n}_MLG","MLG_{L}","Ruthless_{n}","{n}_Ruthless","Sweat_{n}","{n}_Sweat","Clutch_{n}","{n}_Clutch","Headshot_{n}","{n}_HeadShot","Demon_{n}","{n}_Demon","Elite_{n}","{n}_Elite","N0_Mercy_{n}","{n}_N0Mercy","{T}","⚔ {T} ⚔","☬{T}☬","xX{T}Xx","TTV_{T}","✞ {U} ✞","乂{U}乂","ミ★{L}★彡","⛧{K}⛧","༒{G}༒","▄︻デ{n}══━一","𓆩{B}𓆪","⚡{D}⚡","『☠』{L}","【ᴛᴛᴠ】{n}","[ELITE] {n}","[MLG] {n}","[TTV] {n}","{n}_420","{L}_420","1_TAP_{n}","{n} ✪ ᴳᴳ","{n}ツ","{n}〄","★{L}★","༺ {L} ༻","꧁{T}꧂","彡{T}彡","☠ {B} ☠","⌈{n}⌋","{C} ☠","ᴰᵉᵐᵒⁿ {n}","Sw3at_{L}","Cl7tch_{n}","Hdsht_{L}","D3m0n_{n}","3L1T3_{n}","R7thl3ss_{n}","{Q}"];
const TRYHARD=["ҬЯУНДЯD","꧁༺ xX_Slayer_Xx ༻꧂","彡Reaper彡","☠ N0Mercy ☠","Ŧ1LT3D","TTV_Sw3at","MLG_Cl7tch","R7thl3ss","Headshot_God","☠ D3m0n ☠","彡3L1T3彡","꧁Sw34tL0rd꧂","ҬЯУНДЯD_TTV","Cl7tch_K1ng","xX_N0Scope_Xx","N0_M3rcy_TTV","ᴴᴱᴬᴰˢᴴᴼᵀ","𝕽𝖚𝖙𝖍𝖑𝖊𝖘𝖘","⚔ 𝕯𝖊𝖒𝖔𝖓 ⚔","𝔼𝕝𝕚𝕥𝕖","✞ ҬЯУНДЯD ✞","▄︻デ H34DSH0T ══━一","𝓢𝔀𝓮𝓪𝓽_𝓛𝓸𝓻𝓭","༺ D3M0N_S1ay3r ༻","乂 Cl7tch 乂","꧁ Ƶ3R0_Mercy ꧂","TTV_ҬЯУНДЯD","Ɗ3ɱ0ŋ_Ҟ1ŋg","MLG_Pr0","⚡ 𝗦𝗪𝗘𝗔𝗧 ⚡","彡RUTHLESS彡","[ELITE] Sl4y3r","N0_L1F3_TTV","1_T4P_K1LL","Ghost_H34DSH0T","ᴍʟɢ_ᴘʀᴏ","☠ ŦЯУНДЯD ☠","꧁ Sn1p3r_TTV ꧂","ミ★ Ruthl3ss ★彡","〄 Cl7tch_G0d 〄"];
