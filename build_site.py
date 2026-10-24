import json,html,re
D='/workspace/simbolos-gamer/'
SITE='https://symbolvault.net'
DATE='2026-10-18'
NAV=[('index.html','Início'),('simbolos-nick-fortnite.html','Fortnite/Epic'),('simbolos-discord.html','Discord'),('nicks-tryhard.html','Tryhard'),('letras-estilizadas.html','Letras'),('kaomoji.html','Kaomoji')]
def url(p): return SITE+'/' if p=='index.html' else SITE+'/'+p
def footer():
    return '''<footer>
<nav class="foot-links" aria-label="Rodapé"><a href="sobre.html">Sobre</a><a href="privacidade.html">Política de Privacidade</a><a href="termos.html">Termos de Utilização</a><a href="contacto.html">Contacto</a><button type="button" data-cookie-settings>Gerir cookies</button></nav>
<strong>SymbolVault</strong> · Feito para gamers 🎮 · Projeto independente, sem ligação a qualquer editora de jogos. Todas as marcas pertencem aos respetivos donos.<br>© 2026 SymbolVault · <a href="#topo">Voltar ao topo ↑</a>
</footer>'''
def ad(slot): return f'<div class="ad-slot" data-slot="{slot}" aria-label="Publicidade"></div>'
def head(title,desc,path,extra_ld=None,noindex=False):
    ld=[{"@type":"WebPage","name":title,"url":url(path),"description":desc,"inLanguage":"pt-PT","isPartOf":{"@type":"WebSite","name":"SymbolVault","url":SITE+"/"}}]
    if path!='index.html':
        ld.append({"@type":"BreadcrumbList","itemListElement":[{"@type":"ListItem","position":1,"name":"SymbolVault","item":SITE+"/"},{"@type":"ListItem","position":2,"name":title.split(' – ')[0],"item":url(path)}]})
    if extra_ld: ld+=extra_ld
    j=json.dumps({"@context":"https://schema.org","@graph":ld},ensure_ascii=False)
    t=html.escape(title);d=html.escape(desc)
    return f'''<!DOCTYPE html>
<html lang="pt-PT" data-theme="dark">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{t}</title>
<meta name="description" content="{d}">
<link rel="canonical" href="{url(path)}">
<meta name="robots" content="{'noindex,follow' if noindex else 'index,follow,max-image-preview:large'}">
<meta name="theme-color" content="#07060f">
<meta property="og:type" content="website"><meta property="og:site_name" content="SymbolVault"><meta property="og:locale" content="pt_PT">
<meta property="og:title" content="{t}"><meta property="og:description" content="{d}"><meta property="og:url" content="{url(path)}">
<meta name="twitter:card" content="summary">
<link rel="icon" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 64 64'%3E%3Crect width='64' height='64' rx='14' fill='%2307060f'/%3E%3Ctext x='32' y='45' font-size='38' text-anchor='middle' fill='%2300e5ff'%3E%E2%9C%A6%3C/text%3E%3C/svg%3E">
<script type="application/ld+json">{j}</script>
<link rel="stylesheet" href="css/style.css">
</head>'''
def top(path):
    links=''.join(f'<a href="{h}"{" aria-current=\"page\"" if h==path else ""}>{t}</a>' for h,t in NAV)
    return f'''<body>
<a class="skip" href="#conteudo">Saltar para o conteúdo</a>
<div class="bg" aria-hidden="true"></div>
<header class="page-head" id="topo"><div class="bar-row"><a class="brand" href="index.html" aria-label="SymbolVault – início"><span class="logo" aria-hidden="true">✦</span><span>Symbol<b>Vault</b></span></a><nav class="top-nav" aria-label="Principal">{links}</nav></div></header>
<main class="pagina" id="conteudo">'''
def end(scripts):
    return f'''</main>
{footer()}
{scripts}
<script src="js/config.js"></script>
<script src="js/consent.js"></script>
</body>
</html>
'''
def faq_ld(items):
    return [{"@type":"FAQPage","mainEntity":[{"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":re.sub('<[^>]+>','',a)}} for q,a in items]}]
def faq_html(items):
    return '<h2>Perguntas frequentes</h2>'+''.join(f'<details><summary>{q}</summary><p>{a}</p></details>' for q,a in items)
RELATED=lambda cur:'<h2>Mais guias</h2><div class="guias">'+''.join(f'<a href="{h}"><b>{t}</b><span>{d}</span></a>' for h,t,d in GUIDES if h!=cur)+'<a href="index.html"><b>Todos os símbolos</b><span>Mais de 4500 símbolos para copiar</span></a></div>'
GUIDES=[
('simbolos-nick-fortnite.html','Símbolos para Fortnite/Epic','O que costuma ser aceite e o que testar'),
('simbolos-discord.html','Símbolos para Discord','Nomes de ecrã, alcunhas e estado'),
('nicks-tryhard.html','Nicks tryhard','Leetspeak, TTV, MLG e molduras'),
('letras-estilizadas.html','Letras estilizadas','Gótico, negrito, cursivo e mais'),
('kaomoji.html','Kaomoji','Caras japonesas para copiar'),
]
CTA='<p><a class="btn pri cta-tool" href="index.html">Ver todos os 4500+ símbolos →</a></p>'
def landing(path,title,desc,h1,intro,sections,faq,scripts_extra='',nickbox=False):
    body=head(title,desc,path,faq_ld(faq))+top(path)
    body+=f'<nav class="crumbs" aria-label="Breadcrumb"><a href="index.html">SymbolVault</a> › {html.escape(h1)}</nav>'
    body+=ad('topo')
    body+=f'<article class="prose"><h1>{h1}</h1>{intro}'
    if nickbox:
        body+='<div class="nick-in"><label for="nickIn"><strong>O teu nick base:</strong></label><input id="nickIn" type="text" maxlength="30" placeholder="Escreve o teu nick (ex.: Tomas)" autocomplete="off"></div>'
    for sec in sections: body+=sec
    body+=CTA+faq_html(faq)+RELATED(path)+'</article>'+ad('fundo')
    body+=end('<script src="js/data.js"></script>\n<script src="js/nicks.js"></script>\n<script src="js/mini.js"></script>')
    open(D+path,'w',encoding='utf8').write(body)
def grid(src,cls=''): return f'<div class="grid{cls} compacto" data-src="{src}"></div>'
H2=lambda t:f'<h2>{t}</h2>'

# ---- páginas de conteúdo ----
landing('simbolos-nick-fortnite.html','Símbolos para nick Fortnite e Epic Games – o que funciona | SymbolVault',
 'Guia de símbolos e caracteres para nicks no Fortnite e Epic Games: o que costuma ser aceite, o que é recusado, letras acentuadas e nicks com leetspeak para copiar e testar.',
 'Símbolos para nick Fortnite e Epic Games',
 '<p>Queres um nome diferente no Fortnite? A <strong>Epic Games</strong> é bastante restritiva com os caracteres permitidos no nome de ecrã, e as regras podem mudar sem aviso. Por isso, esta página separa o que tem <em>mais probabilidade</em> de ser aceite do que costuma ser recusado. <strong>Nada aqui é garantido: testa sempre o nome na conta antes de o escolheres.</strong></p>',
 [H2('Letras acentuadas e latinas (mais prováveis)')+'<p>Letras como á, ç, ñ, ø ou ü fazem parte do alfabeto latino estendido e, em geral, têm mais hipóteses de passar nos filtros do que símbolos decorativos. Clica para copiar.</p>'+grid('catn:latino:64'),
  H2('Nicks com leetspeak (só letras, números e _)')+'<p>O leetspeak troca letras por números parecidos (A→4, E→3, I→1, O→0, S→5, T→7). Como usa apenas caracteres comuns, é a forma mais segura de dar um toque «tryhard» ao nome.</p>'+grid('tryleet'),
  H2('Símbolos para testar (podem ser recusados)')+'<p>Estrelas, coroas e molduras ficam bem, mas é frequente a Epic Games rejeitá-los ou removê-los. Experimenta um de cada vez; se a conta recusar, tenta outro.</p>'+grid('catn:estrelas:30|catn:coroas:20|catn:armas:20|catn:caveiras:20'),
  H2('Dicas para escolher o nick')+'<ul><li>Mantém o nome curto e fácil de ler: nomes muito carregados de símbolos são difíceis de procurar pelos amigos.</li><li>Evita nomes ofensivos ou que imitem outras pessoas: podem ser removidos.</li><li>Se o símbolo for recusado no nome de utilizador, experimenta usá-lo noutras plataformas (por exemplo, Discord) onde há mais liberdade.</li><li>Guarda os teus favoritos no SymbolVault para os reencontrares depressa.</li></ul>'],
 [('A Epic Games aceita símbolos no nome?','Aceita apenas alguns caracteres e as regras podem mudar. Letras e números comuns são o mais seguro; muitos símbolos decorativos são recusados. Testa sempre.'),
  ('Porque é que o símbolo aparece como quadrado?','O tipo de letra do jogo pode não incluir esse carácter. Experimenta outro símbolo da mesma categoria.'),
  ('Posso mudar o nome de ecrã quando quiser?','A Epic Games impõe limites de tempo entre alterações. Consulta a ajuda oficial da Epic para as regras atuais.')])

landing('simbolos-discord.html','Símbolos para Discord: nomes, alcunhas e estado | SymbolVault',
 'Copia símbolos, molduras e letras estilizadas para o teu nome de ecrã, alcunha de servidor e estado do Discord. Guia com dicas e listas prontas a usar.',
 'Símbolos para Discord: nome de ecrã, alcunha e estado',
 '<p>O <strong>Discord</strong> é das plataformas mais flexíveis para personalizar o nome. O <em>nome de utilizador</em> segue regras mais rígidas (letras minúsculas, números, sublinhado e ponto), mas o <em>nome de ecrã</em> e a <em>alcunha por servidor</em> costumam aceitar muitos símbolos, letras estilizadas e emojis. As alcunhas têm um limite de 32 caracteres. Mesmo assim, alguns servidores têm regras próprias (por exemplo, exigir nomes legíveis), por isso respeita-as.</p>',
 [H2('Estrelas e brilhos')+grid('cat:estrelas'),
  H2('Corações')+grid('cat:coracoes'),
  H2('Coroas e realeza')+grid('cat:coroas'),
  H2('Caveiras e visual sombrio')+grid('cat:caveiras'),
  H2('Setas e molduras')+grid('catn:setas:60|cat:combos'),
  H2('Como usar')+'<ol><li>Clica no símbolo para o copiar.</li><li>No Discord, abre as <strong>Definições do utilizador</strong> (ou a alcunha do servidor).</li><li>Cola no campo do nome (Ctrl+V / Cmd+V) e guarda.</li></ol><p>Dica: combina uma moldura (por exemplo, ꧁ nome ꧂) com um símbolo no fim, mas evita exagerar, porque nomes muito longos ficam cortados na lista de membros.</p>'],
 [('Qual é o limite de caracteres da alcunha no Discord?','As alcunhas de servidor podem ter até 32 caracteres, e alguns símbolos contam como mais do que um.'),
  ('As letras estilizadas funcionam no Discord?','Normalmente sim, mas leitores de ecrã e a pesquisa por nome podem ter dificuldade. Usa com moderação.'),
  ('Posso usar estes símbolos no estado?','Em geral sim. O estado personalizado aceita texto Unicode e emojis.')])

landing('nicks-tryhard.html','Nicks tryhard para jogos: ideias, leetspeak, TTV e MLG | SymbolVault',
 'Gerador e ideias de nicks tryhard: leetspeak, prefixos TTV e MLG, molduras e glifos como ҬЯУНДЯD. Escreve o teu nick e copia o resultado.',
 'Nicks tryhard: ideias e gerador para o teu nick',
 '<p>Um nick <strong>tryhard</strong> mistura símbolos, letras trocadas por números (leetspeak) e palavras como <em>Sweat</em>, <em>Clutch</em>, <em>Ruthless</em>, <em>Headshot</em> ou <em>Elite</em> para passar uma imagem competitiva. Escreve o teu nick abaixo e vê dezenas de variações prontas a copiar.</p>',
 [H2('Os teus modelos tryhard')+grid('presets'),
  H2('Nicks tryhard prontos')+grid('tryhard'),
  H2('Como montar um bom nick tryhard')+'<ul><li><strong>Leetspeak:</strong> troca A→4, E→3, I→1, O→0, S→5, T→7. Não exageres, ou ninguém o consegue ler.</li><li><strong>Prefixos e sufixos:</strong> TTV_ é usado por quem faz streams na Twitch; MLG vem do circuito competitivo de Call of Duty.</li><li><strong>Molduras:</strong> 彡nick彡 ou ꧁nick꧂ dão destaque visual, mas nem todos os jogos as aceitam.</li><li><strong>Glifos parecidos:</strong> letras cirílicas e latinas estendidas (Я, Д, Ҭ) imitam o alfabeto, mas podem ser recusadas ou aparecer como quadrados.</li></ul><p>Cada jogo tem as suas regras de nomes: na dúvida, usa a versão só com letras, números e sublinhado.</p>'],
 [('O que significa TTV no nick?','TTV é a abreviatura de «Twitch TV» e indica que a pessoa transmite na Twitch. Só o uses se for verdade.'),
  ('O que é leetspeak?','É uma forma de escrever que troca letras por números ou símbolos parecidos, por exemplo «elite» → «3l1t3».'),
  ('Estes nicks funcionam em todos os jogos?','Não. As versões só com letras, números e sublinhado têm mais probabilidade de serem aceites; molduras e glifos podem ser recusados.')],nickbox=True)

landing('letras-estilizadas.html','Letras estilizadas (fancy text): gótico, negrito, cursivo | SymbolVault',
 'Gerador de letras estilizadas em Unicode: gótico, negrito, cursivo, círculos, duplo traço e mais de 20 estilos. Escreve o texto e copia.',
 'Letras estilizadas: gerador de fancy text',
 '<p>As <strong>letras estilizadas</strong> não são tipos de letra: são caracteres Unicode diferentes que parecem versões decoradas do alfabeto (por exemplo 𝕲𝖔́𝖙𝖎𝖈𝖔 ou 𝓒𝓾𝓻𝓼𝓲𝓿𝓸). Por isso podes colá-las em muitos sítios sem instalar nada. Escreve o texto abaixo e copia o estilo que preferires.</p>',
 [H2('Os teus estilos')+grid('fancy'),
  H2('Quando usar (e quando evitar)')+'<ul><li>Funcionam bem em redes sociais, biografias e nomes de ecrã que aceitam Unicode.</li><li>Muitos jogos recusam-nas em nomes de utilizador. Testa antes.</li><li>Leitores de ecrã podem ler cada letra como «letra matemática em negrito», o que prejudica a acessibilidade.</li><li>O texto em estilos Unicode não é encontrado pela pesquisa normal.</li><li>Os acentos portugueses (á, ç, ã) normalmente não têm versão estilizada e ficam como letra normal ou aparecem partidos.</li></ul>'],
 [('As letras estilizadas são tipos de letra?','Não. São caracteres Unicode distintos, por isso funcionam onde o texto Unicode é aceite.'),
  ('Porque é que algumas letras aparecem como quadrados?','O dispositivo ou a aplicação não tem esse carácter no tipo de letra. Experimenta outro estilo.'),
  ('Posso usar estas letras no nome do jogo?','Depende do jogo. Muitos aceitam apenas letras e números comuns, por isso testa sempre.')],nickbox=True)

landing('kaomoji.html','Kaomoji para copiar e colar: caras japonesas (ʘ‿ʘ) | SymbolVault',
 'Lista de kaomoji para copiar e colar: caras japonesas feitas com símbolos como (ʘ‿ʘ), ʕ•ᴥ•ʔ e ¯\\_(ツ)_/¯. Úteis para chat, Discord e redes sociais.',
 'Kaomoji: caras japonesas para copiar e colar',
 '<p>Os <strong>kaomoji</strong> (顔文字, «letras de cara») são expressões feitas com caracteres de texto. Ao contrário dos emojis, são várias letras e símbolos juntos, por isso funcionam em qualquer sítio que aceite Unicode. São populares no chat dos jogos, no Discord e nas redes sociais. Clica para copiar.</p>',
 [H2('Kaomoji populares')+grid('cat:kaomoji',' largo'),
  H2('Dicas')+'<ul><li>Cola o kaomoji no fim da mensagem para dar tom, por exemplo «GG ¯\\_(ツ)_/¯».</li><li>Alguns jogos limitam o chat a caracteres básicos e mostram quadrados nos símbolos especiais.</li><li>Em nomes de utilizador, os kaomoji raramente são aceites.</li></ul>'],
 [('O que significa kaomoji?','É uma palavra japonesa que significa «letras de cara»: expressões feitas só com texto.'),
  ('Kaomoji e emoji são a mesma coisa?','Não. Os emojis são imagens padronizadas; os kaomoji são combinações de caracteres.'),
  ('Funcionam nos jogos?','Depende do jogo e do tipo de letra do chat. Experimenta num amigo ou em modo privado.')])

# ---- páginas institucionais ----
def inst(path,title,desc,h1,content,noindex=False):
    b=head(title,desc,path,None,noindex)+top(path)+f'<nav class="crumbs" aria-label="Breadcrumb"><a href="index.html">SymbolVault</a> › {html.escape(h1)}</nav><article class="prose"><h1>{h1}</h1>{content}</article>'+end('')
    open(D+path,'w',encoding='utf8').write(b)
PH=lambda t:f'<span class="placeholder">{t}</span>'
inst('sobre.html','Sobre o SymbolVault','O SymbolVault é um site gratuito para copiar símbolos, letras estilizadas e nicks para jogos. Saiba quem somos e como funciona.','Sobre o SymbolVault',
'''<p>O <strong>SymbolVault</strong> é um site gratuito, em português europeu, que reúne milhares de símbolos Unicode, letras estilizadas, kaomoji e ideias de nicks para personalizares o teu nome em jogos, no Discord, na Steam e nas redes sociais.</p>
<h2>Como funciona</h2><p>Clicas num símbolo, ele é copiado para a área de transferência e colas onde quiseres. Também podes montar o teu nick com o construtor, gerar nomes aleatórios e guardar favoritos. Tudo corre no teu browser: não precisas de criar conta.</p>
<h2>Compatibilidade honesta</h2><p>Cada jogo tem as suas regras para nomes. Por exemplo, a Epic Games e o Roblox restringem muitos caracteres. As etiquetas de compatibilidade do site são indicativas e sem garantias: testa sempre o símbolo no jogo.</p>
<h2>Independência</h2><p>O SymbolVault é um projeto independente e não tem qualquer ligação à Epic Games, Fortnite, Roblox, Valve, Discord ou outras empresas. Os nomes de marcas são mencionados apenas para descrever compatibilidade e pertencem aos respetivos donos.</p>
<h2>Financiamento</h2><p>O site é gratuito e poderá mostrar publicidade (por exemplo, Google AdSense), apenas se aceitares os cookies de publicidade. Consulta a <a href="privacidade.html">Política de Privacidade</a>.</p>
<h2>Contacto</h2><p>Sugestões de símbolos ou erros? Vê a página de <a href="contacto.html">contacto</a>.</p>''')
inst('contacto.html','Contacto – SymbolVault','Contacta o SymbolVault: sugestões de símbolos, correções, questões de privacidade e pedidos de remoção.','Contacto',
f'''<p class="aviso" role="note"><strong>⚠ Para o editor do site:</strong> substitui o email abaixo ({PH('O_TEU_EMAIL@EXEMPLO.COM')}) por um endereço real antes de publicar (ver PUBLICAR.md).</p>
<p>Para sugestões, correções, questões de privacidade ou pedidos relacionados com os teus dados, escreve para: {PH('O_TEU_EMAIL@EXEMPLO.COM')}</p>
<h2>O que podes enviar</h2><ul><li>Sugestões de novos símbolos ou categorias.</li><li>Avisos de símbolos que não funcionam num jogo (indica o jogo e o símbolo).</li><li>Pedidos de acesso, retificação ou apagamento de dados pessoais (ver <a href="privacidade.html">Política de Privacidade</a>).</li><li>Questões legais ou de direitos de autor.</li></ul>
<p>Respondemos assim que possível. Não pedimos nem guardamos dados pessoais para além do necessário para responder.</p>''')
inst('termos.html','Termos de Utilização – SymbolVault','Termos e condições de utilização do site SymbolVault.','Termos de Utilização',
f'''<p><em>Última atualização: 18 de outubro de 2026.</em></p>
<p class="aviso" role="note"><strong>⚠ Para o editor do site:</strong> este texto é um modelo. Revê-o e adapta-o à tua situação (e, se necessário, com apoio jurídico) antes de publicar. Substitui {PH('[NOME DO EDITOR / DENOMINAÇÃO SOCIAL]')}.</p>
<h2>1. Aceitação</h2><p>Ao utilizar o site symbolvault.net («SymbolVault»), propriedade de {PH('[NOME DO EDITOR]')}, aceitas estes termos. Se não concordares, não uses o site.</p>
<h2>2. Serviço</h2><p>O SymbolVault disponibiliza gratuitamente símbolos Unicode, letras estilizadas e ferramentas para os copiares e usares. O serviço é fornecido «tal como está», sem garantias de disponibilidade, exatidão ou adequação a um fim específico.</p>
<h2>3. Compatibilidade e responsabilidade</h2><p>Os símbolos podem ser recusados ou apresentados de forma diferente por jogos, plataformas e dispositivos. As etiquetas de compatibilidade são indicativas. Não nos responsabilizamos por contas, nomes rejeitados, suspensões ou outras consequências do uso dos símbolos em serviços de terceiros; cumpre sempre as regras de cada serviço.</p>
<h2>4. Utilização aceitável</h2><p>Não podes usar o site para fins ilegais, para assediar ou impersonar terceiros, nem para tentar prejudicar o seu funcionamento (por exemplo, extração automática abusiva).</p>
<h2>5. Propriedade intelectual</h2><p>Os símbolos Unicode são caracteres de uso comum. O design, os textos e o código do site pertencem ao editor, salvo indicação em contrário. Marcas de terceiros pertencem aos respetivos titulares; o SymbolVault não tem qualquer ligação a esses titulares.</p>
<h2>6. Publicidade e ligações</h2><p>O site pode mostrar publicidade de terceiros e ligações externas, sobre as quais não temos controlo. Ver a <a href="privacidade.html">Política de Privacidade</a>.</p>
<h2>7. Limitação de responsabilidade</h2><p>Na máxima medida permitida por lei, o editor não responde por danos indiretos decorrentes do uso do site. Nada nestes termos exclui direitos que a lei portuguesa reconhece aos consumidores.</p>
<h2>8. Alterações</h2><p>Podemos atualizar estes termos; a data acima indica a última versão. A utilização continuada implica aceitação.</p>
<h2>9. Lei aplicável</h2><p>Estes termos regem-se pela lei portuguesa. Para litígios de consumo, podes recorrer às entidades de resolução alternativa de litígios e à plataforma europeia de RLL.</p>
<h2>10. Contacto</h2><p>Ver <a href="contacto.html">Contacto</a>.</p>''')
inst('privacidade.html','Política de Privacidade e Cookies – SymbolVault','Como o SymbolVault trata dados pessoais, cookies, localStorage e publicidade (Google AdSense), em conformidade com o RGPD.','Política de Privacidade e Cookies',
f'''<p><em>Última atualização: 18 de outubro de 2026.</em></p>
<p class="aviso" role="note"><strong>⚠ Para o editor do site:</strong> este texto é um modelo informativo e não constitui aconselhamento jurídico. Preenche os campos assinalados e revê-o antes de publicar.</p>
<h2>1. Responsável pelo tratamento</h2><p>{PH('[NOME DO EDITOR / DENOMINAÇÃO SOCIAL]')}, contacto: {PH('O_TEU_EMAIL@EXEMPLO.COM')}. Site: symbolvault.net.</p>
<h2>2. Que dados tratamos</h2><ul>
<li><strong>Não há contas nem formulários</strong> no SymbolVault: não pedimos nome, email nem outros dados para usares o site.</li>
<li><strong>Dados técnicos de alojamento:</strong> o fornecedor de alojamento (por exemplo, GitHub Pages ou Netlify) pode registar o teu endereço IP e dados do pedido (páginas, data/hora, browser) para segurança e funcionamento. Estes registos são tratados por esse fornecedor, segundo as suas políticas.</li>
<li><strong>Contacto:</strong> se nos escreveres, usamos o teu email e a mensagem apenas para responder.</li></ul>
<h2>3. localStorage (armazenamento local)</h2><p>Para o site funcionar como esperas, guardamos <strong>no teu próprio browser</strong> (localStorage) — nada disto é enviado para os nossos servidores:</p>
<ul><li><code>sv_fav</code>: os teus símbolos favoritos;</li><li><code>sv_rec</code>: símbolos copiados recentemente;</li><li><code>sv_tema</code> e <code>sv_tam</code>: tema claro/escuro e tamanho dos símbolos;</li><li><code>sv_consent</code>: a tua escolha sobre cookies de publicidade (e a data).</li></ul>
<p>Podes apagar estes dados a qualquer momento nas definições do browser («limpar dados do site»), ou com os botões «Limpar» do site.</p>
<h2>4. Cookies e publicidade (Google AdSense)</h2>
<p>O SymbolVault pode apresentar publicidade através do <strong>Google AdSense</strong>. <strong>Só carregamos o script de anúncios depois de aceitares</strong> no aviso de cookies. Se recusares, não é carregado nenhum cookie de publicidade nem script do Google AdSense.</p>
<p>Se aceitares, a Google e os seus parceiros podem usar cookies e identificadores semelhantes para mostrar e medir anúncios, limitar repetições, prevenir fraude e, consoante as tuas definições, personalizar anúncios. A Google atua como responsável pelo tratamento desses dados. Mais informação: <a href="https://policies.google.com/technologies/partner-sites" rel="noopener" target="_blank">como a Google usa dados de sites parceiros</a>, <a href="https://policies.google.com/technologies/ads" rel="noopener" target="_blank">publicidade da Google</a> e <a href="https://adssettings.google.com" rel="noopener" target="_blank">definições de anúncios</a>.</p>
<h2>5. Fundamento jurídico</h2><p>Para cookies e anúncios, o fundamento é o teu <strong>consentimento</strong> (art. 6.º, n.º 1, al. a) do RGPD e lei aplicável sobre comunicações eletrónicas). Para o armazenamento local estritamente necessário às funcionalidades que pedes (favoritos, tema), o fundamento é o interesse legítimo em prestar o serviço solicitado. Para responder a mensagens, é o interesse legítimo/execução de diligências pré-contratuais a pedido do titular.</p>
<h2>6. Gerir ou retirar o consentimento</h2><p>Podes alterar a tua escolha a qualquer momento em <button type="button" class="btn peq" data-cookie-settings>Gerir cookies</button> (também disponível no rodapé de todas as páginas). Retirar o consentimento não afeta a licitude do tratamento anterior. Podes também apagar cookies nas definições do browser.</p>
<h2>7. Conservação</h2><p>O localStorage permanece no teu dispositivo até o apagares. Os cookies de terceiros têm a duração definida por esses terceiros. Mensagens de contacto são guardadas apenas pelo tempo necessário para responder.</p>
<h2>8. Os teus direitos</h2><p>Nos termos do RGPD, tens direito de acesso, retificação, apagamento, limitação, portabilidade e oposição, bem como de retirar o consentimento e de apresentar reclamação à autoridade de controlo: a <a href="https://www.cnpd.pt" rel="noopener" target="_blank">Comissão Nacional de Proteção de Dados (CNPD)</a>. Para exercer direitos, contacta-nos através da página de <a href="contacto.html">contacto</a>.</p>
<h2>9. Transferências internacionais</h2><p>Os fornecedores referidos (alojamento e Google) podem tratar dados fora do Espaço Económico Europeu, com as garantias previstas por lei (por exemplo, cláusulas contratuais-tipo ou decisões de adequação).</p>
<h2>10. Menores</h2><p>O site não se dirige especificamente a crianças. Se tens menos de 16 anos, pede autorização aos teus pais ou tutor antes de aceitares cookies de publicidade.</p>
<h2>11. Alterações</h2><p>Podemos atualizar esta política; a data no topo indica a versão atual.</p>''')

# ---- 404 ----
b=head('Página não encontrada – SymbolVault','A página que procuras não existe. Volta ao SymbolVault e copia símbolos para o teu nick.','404.html',None,True).replace('<link rel="stylesheet" href="css/style.css">','<link rel="stylesheet" href="/css/style.css">')
b+='<body><div class="bg" aria-hidden="true"></div><main class="pagina" id="conteudo" style="text-align:center;padding-top:60px"><article class="prose"><h1>404 – Página não encontrada</h1><p>Esta página não existe ou foi movida. ✦</p><p><a class="btn pri" href="/">Voltar ao SymbolVault</a></p><div class="guias">'+''.join(f'<a href="/{h}"><b>{t}</b><span>{d}</span></a>' for h,t,d in GUIDES)+'</div></article></main>'+footer().replace('href="sobre','href="/sobre').replace('href="privacidade','href="/privacidade').replace('href="termos','href="/termos').replace('href="contacto','href="/contacto')+'<script src="/js/config.js"></script><script src="/js/consent.js"></script></body></html>\n'
b=b.replace('privacidade.html">Política','privacidade.html">Política')
open(D+'404.html','w',encoding='utf8').write(b)

# ---- sitemap, robots, ads.txt ----
pages=['index.html']+[g[0] for g in GUIDES]+['sobre.html','contacto.html','privacidade.html','termos.html']
pr={'index.html':'1.0'}
sm='<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'+''.join(f'  <url><loc>{url(p)}</loc><lastmod>{DATE}</lastmod><changefreq>{"weekly" if p=="index.html" else "monthly"}</changefreq><priority>{pr.get(p,"0.8" if p in [g[0] for g in GUIDES] else "0.3")}</priority></url>\n' for p in pages)+'</urlset>\n'
open(D+'sitemap.xml','w',encoding='utf8').write(sm)
open(D+'robots.txt','w').write(f'User-agent: *\nAllow: /\n\nSitemap: {SITE}/sitemap.xml\n')
open(D+'ads.txt','w').write('# SUBSTITUIR depois da aprovação do AdSense: troca pub-XXXXXXXXXXXXXXXX pelo teu ID de editor e remove o "#" da linha abaixo.\n# google.com, pub-XXXXXXXXXXXXXXXX, DIRECT, f08c47fec0942fa0\n')

# ---- index ----
h=open(D+'index.html',encoding='utf8').read()
if 'rel="canonical"' not in h:
    ldfaq=[("Como uso um símbolo no meu nick?","Clica no símbolo para o copiar e cola-o no campo do nome no jogo. Também podes juntar vários no construtor de nick."),("Porque é que o meu jogo não aceita um símbolo?","Muitos jogos só permitem letras, números e alguns sinais. A Epic Games e o Roblox, por exemplo, são restritivos. Testa sempre."),("O que significam as etiquetas de compatibilidade?","São uma estimativa baseada no tipo de carácter e não uma garantia."),("Os meus favoritos ficam guardados?","Sim, apenas no teu browser (localStorage).")]
    new=head('SymbolVault – 4500+ símbolos, letras estilizadas e nicks tryhard para jogos','SymbolVault: mais de 4500 símbolos, kaomoji, letras estilizadas e nicks tryhard para copiar e colar em jogos, Discord, Steam e redes sociais. Gerador de nicks, favoritos e compatibilidade.','index.html',[{"@type":"WebApplication","name":"SymbolVault","url":SITE+"/","inLanguage":"pt-PT","applicationCategory":"UtilitiesApplication","operatingSystem":"Web","offers":{"@type":"Offer","price":"0","priceCurrency":"EUR"}}]+faq_ld(ldfaq))
    new=new.replace('<link rel="stylesheet" href="css/style.css">\n</head>','<meta name="keywords" content="símbolos para nick, símbolos gamer, letras estilizadas, kaomoji, nicks tryhard, copiar e colar">\n<link rel="stylesheet" href="css/style.css">\n</head>')
    # keep body of old index
    body=h[h.index('<body>'):]
    h=new+'\n'+body
    h=h.replace('<html lang="pt-PT" data-theme="dark">','<html lang="pt-PT" data-theme="dark">')
    h=h.replace('<section id="simbolos" tabindex="-1" aria-label="Todos os símbolos">','<section id="simbolos" tabindex="-1" aria-label="Todos os símbolos">'.replace('<section','<section'),1)
    h=h.replace('<section class="painel" id="favoritos-box"',ad('topo')+'\n<section class="painel" id="favoritos-box"',1)
    h=h.replace('<div class="tools-title">',ad('meio')+'\n<div class="tools-title">',1)
    guias='<section class="painel" id="guias" aria-labelledby="h-guias"><h2 id="h-guias">📚 Guias úteis</h2><div class="guias">'+''.join(f'<a href="{a}"><b>{t}</b><span>{d}</span></a>' for a,t,d in GUIDES)+'</div></section>\n'
    h=h.replace('<section class="painel faq"',guias+'<section class="painel faq"',1)
    h=h.replace('</main>','</main>\n'+ad('fundo'),1)
    a=h.index('<footer>');b2=h.index('</footer>')+9
    h=h[:a]+footer()+h[b2:]
    h=h.replace('<script src="js/data.js"></script>','<script src="js/config.js"></script>\n<script src="js/data.js"></script>',1)
    h=h.replace('<script src="js/app.js"></script>','<script src="js/app.js"></script>\n<script src="js/consent.js"></script>',1)
    open(D+'index.html','w',encoding='utf8').write(h)
print('ok')
