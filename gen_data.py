import json,re,subprocess,unicodedata as U
D='/workspace/simbolos-gamer/'
# curated data from old files (kept in tools/ copy)
import os
if not os.path.exists('old_data.js'):
    open('old_data.js','w',encoding='utf8').write(open(D+'js/data.js',encoding='utf8').read())
    open('old_app.js','w',encoding='utf8').write(open(D+'js/app.js',encoding='utf8').read())
old=subprocess.check_output(['node','-e','eval(require("fs").readFileSync("old_data.js","utf8")+";console.log(JSON.stringify({c:CATEGORIAS,e:ESTILOS}))")'],encoding='utf8')
old=json.loads(old)
kao=json.loads(re.search(r'const lista=(\[.*?\]);',open('old_app.js',encoding='utf8').read(),re.S).group(1))
def rng(*rs,skip_cat=('Cn','Cc','Cs','Co','Mn','Zs','Cf','Me','Mc')):
    out=[]
    for a,b in rs:
        for cp in range(a,b+1):
            c=chr(cp)
            if U.category(c) in skip_cat: continue
            out.append(c)
    return out
cur={c[0]:(c[1],c[2].split(),c[3]) for c in old['c']}
cats=[]
def add(id,t,icon,k,s):
    seen=[];[seen.append(x) for x in s if x not in seen]
    cats.append(dict(id=id,t=t,icon=icon,k=k,s=seen))
def C(id,icon): 
    t,s,k=cur[id];add(id,t,icon,k,s)
gaming="🎮 🕹 👾 🎯 🏆 🥇 🎖 🏅 ⚔ 🛡 🏹 🔫 💣 🧨 💥 🔥 ⚡ 🚀 🛸 🪐 🌌 🤖 👽 💀 ☠ 👑 💎 🧿 🎲 ♟ 🃏 🎰 🎧 🎤 🔊 📡 🔮 🧬 ⚙ 🛠 🗡 🪓 🪄 🐉 🦅 🐺 🦁 🐯 🦈 🐍 🦂 🕷 🦇 🔰 ⚜ ☢ ☣ ⚛ ✪ ➳ ꧁ ꧂ ༺ ༻ ᴳᴳ ᴱᶻ 𝔾𝔾 ᵍᵍ 🅶🅶 ㉿ ツ 彡 ミ 乂 ๖ۣۜ ᵛᵃᶰᵍᵘᵃʳᵈ ۞ ꗥ ༒ ☬ ✠ ⚑ ✞ ⛧ 〄 ⌬ ⏣ ⟁ ⛨ ⚝ 🅿 🅥 ♠ ♦ ♣ ♥".split()
add("gaming","Gaming","🎮","jogos gamer controlo troféu gg",gaming)
C("estrelas","★");C("coracoes","♥");C("coroas","♛");C("armas","⚔");C("caveiras","☠")
add("alien","Alien e Ocultismo","👽","alien ocultismo runas alquimia astrologia zodíaco misterioso",
 rng((0x16A0,0x16F0))+rng((0x1F700,0x1F773))+rng((0x2648,0x2653))+list("☿♀♁♂♃♄♅♆♇☉☽☾☊☋☌☍♈♉♊♋♌♍♎♏♐♑♒♓⛎⛢⛤⛥⛦⛧☥☦☧☨☩☫☬☭☸☯☮⚕⚚⚛⚜⚝⚶⚷⚸⚹⚺👁🔮🧿🕉☸✡🔯🛐𓂀𓁿𓃠𓆣ꙮ"))
add("flores","Flores e Natureza","🌸","flor natureza folha planta animal árvore",
 list("✿❀❁❃❊❋✾✽✼✻❄❅❆☘🌸🌺🌻🌹🌷🌼🌱🌿🍀🍁🍂🍃🌲🌳🌴🌵🌾💐🍄🌍🌙☀⭐🌈🔥💧🌊🦋🐝🐞🐾🦄🐉🐺🦊🐱🐶🐼🐨🦁🐯🦅🕊🦉🐧🐬🐋🦈🐙🦑🐢🐍🦎🦖")+rng((0x2740,0x274B)))
add("musica","Música","🎵","música nota som clave",
 rng((0x2669,0x266F),(0x1D100,0x1D126))+list("🎵🎶🎼🎤🎧🎷🎸🎹🎺🎻🥁🔔🔊📻〰〜♬♫♪♩𝄞𝄢𝄪𝄫"))
add("tempo","Meteorologia e Tempo","⛈","meteorologia chuva sol nuvem neve tempo relógio",
 list("☀☁☂☃☄★☆☼☽☾⛅⛈⛄⛱⛆❄❅❆⚡☔🌈🌤🌥🌦🌧🌨🌩🌪🌫🌬🌀🌙🌛🌜🌞🌝🌑🌒🌓🌔🌕🌖🌗🌘💧💦🌊⌛⏳⌚⏰⏱⏲🕐🕑🕒🕓🕔🕕🕖🕗🕘🕙🕚🕛")+rng((0x2600,0x2603)))
add("matematica","Matemática","∑","matemática operadores conjuntos lógica",rng((0x2200,0x22FF),(0x27C0,0x27EF),(0x2A00,0x2A2F))+list("±×÷√∛∜∞πΣΩ∂∆∇≠≤≥≈≡½⅓¼¾"))
add("moeda","Moeda e Dinheiro","€","moeda dinheiro euro dólar libra",rng((0x20A0,0x20C0))+list("$¢£¤¥€₿฿₽₹₩₪₫₱₴₦₡💰💵💶💷💴💳🪙"))
add("caixas","Caixas e Blocos","▦","caixas blocos desenho bordas pixel",rng((0x2500,0x259F)))
add("braille","Braille","⠿","braille pontos",rng((0x2800,0x28FF)))
C("setas","➤")
add("setas2","Setas Extra","⇶","setas suplementares",rng((0x2190,0x21FF),(0x27F0,0x27FF),(0x2900,0x297F),(0x2B00,0x2B11),(0x2B30,0x2B4F),(0x2B60,0x2B73)))
add("formas","Formas","◆","formas geometria",cur["formas"][1]+rng((0x25A0,0x25FF)))
C("linhas","═");C("parenteses","【");C("numeros","①");C("letras","Ω")
add("dingbats","Dingbats","✂","dingbats ornamentos",rng((0x2700,0x27BF)))
add("tecnicos","Técnicos","⌘","técnicos teclado interface",rng((0x2300,0x23FF)))
add("diversos2","Símbolos Variados","☯","variados símbolos",rng((0x2600,0x26FF)))
add("cartas","Cartas, Xadrez e Dados","♠","cartas xadrez dados dominó mahjong",rng((0x2654,0x265F),(0x2680,0x2685),(0x1F030,0x1F093),(0x1F0A0,0x1F0F5),(0x1F000,0x1F02B)))
add("latino","Latim Estilizado","Ɛ","acentos letras latinas estendidas",rng((0x00C0,0x00FF),(0x0100,0x017F),(0x0180,0x024F),(0x1D00,0x1D2B),(0x2C60,0x2C7F),(0xA720,0xA7FF)))
add("grego","Grego e Cirílico","Ω","grego cirílico",rng((0x0391,0x03C9),(0x0400,0x04FF)))
add("japones","Katakana e Hiragana","ツ","japonês katakana hiragana chinês cjk",rng((0x3041,0x3096),(0x30A1,0x30FA),(0x3105,0x312F),(0x3200,0x321E),(0x3300,0x3357)))
add("sobrescrito","Pequenos (sobrescrito/subscrito)","ᵃ","superior inferior pequeno",rng((0x2070,0x209C),(0x1D2C,0x1D6A),(0x1D43,0x1D61)))
add("kaomoji","Kaomoji","(ʘ‿ʘ)","kaomoji cara emoticon",kao)
flags=["PT","BR","AO","MV" if False else "MZ","CV","ES","FR","GB","US","DE","IT","NL","BE","CH","IE","CA","MX","AR","CL","CO","PE","JP","KR","CN","IN","AU","NZ","SE","NO","FI","DK","PL","TR","GR","UA","ZA","EU","UN"]
fl=["".join(chr(0x1F1E6+ord(x)-65) for x in f) for f in flags]
add("bandeiras","Bandeiras (países)","🏁","bandeira país região regional",fl+list("🏁🚩🎌🏴🏳"))
combos="""★彡 彡★|꧁ ꧂|༺ ༻|【 】|『 』|「 」|•°•|•.¸¸.•|✧･ﾟ: *|*:･ﾟ✧|☆*:.｡.|.｡.:*☆|✦ ✦|⚔ ⚔|☠ ☠|♛ ♛|▁▂▃▄▅▆▇█|░▒▓█|▀▄▀▄▀▄|⋆⭒˚｡⋆|𓆩 𓆪|ミ★ ★彡|«• •»|≪ ≫|⟦ ⟧|⟪ ⟫|-=≡ ≡=-|✿ ✿|❖ ❖|◥◣ ◢◤|▄︻デ══━一|(っ◔◡◔)っ|ᕙ( )ᕗ|ᕦ( )ᕤ|♪♫ ♫♪|⌜ ⌟|❝ ❞|⊹ ⊹|⋆ ⋆|۞ ۞|☬ ☬|⛧ ⛧|𖤐 𖤐|▌│█║▌║▌║ ║▌║▌║█│▌|✪ ✪|༒ ༒|𝕏|☆彡|[ ]|〔 〕|‹ ›|⸢ ⸥|╰☆☆ ☆☆╮|▓▒░ ░▒▓|⟬ ⟭|⚝ ⚝|❂ ❂|᚛ ᚜|♦ ♦|✠ ✠|◤ ◢|⫷ ⫸|⌈ ⌋|⎡ ⎦""".split("|")
combos=[c.replace(" "," ") for c in combos]
cats.append(dict(id="combos",t="Combos e Molduras",icon="✧",k="combos molduras prefixo sufixo decoração",s=combos))
names={}
for c in cats:
    for s in c['s']:
        if len(s)==1:
            try:names[s]=U.name(s)
            except ValueError:pass
        elif all(0x1F1E6<=ord(x)<=0x1F1FF for x in s) and len(s)==2:
            names[s]="Bandeira "+"".join(chr(ord(x)-0x1F1E6+65) for x in s)
uniq=set(s for c in cats for s in c['s'])
est=old['e']
extra=[("Riscado","\u0336"),("Sublinhado","\u0332"),("Sublinhado duplo","\u0333"),("Com pontos","\u0307"),("Com barra","\u0338")]
out="/* gerado por tools/gen.py */\nconst SV_CATS="+json.dumps(cats,ensure_ascii=False,separators=(',',':'))+";\nconst SV_NAMES="+json.dumps(names,ensure_ascii=False,separators=(',',':'))+";\nconst SV_STYLES="+json.dumps(est,ensure_ascii=False,separators=(',',':'))+";\nconst SV_COMBINING="+json.dumps(extra,ensure_ascii=False)+";\n"
open(D+'js/data.js','w',encoding='utf8').write(out)
print(len(uniq),len(out),[(c['id'],len(c['s'])) for c in cats])
