# Publicar o SymbolVault (symbolvault.net)

Site 100 % estático (HTML + CSS + JS, sem build). Funciona em GitHub Pages, Netlify, Cloudflare Pages, etc.

> ⚠ **Domínio:** o endereço escolhido é **symbolvault.net**, mas **a disponibilidade não foi verificada** e **o domínio tem de ser registado por ti** num registador (por exemplo Namecheap, Porkbun, Cloudflare, GoDaddy…). Se `symbolvault.net` já estiver ocupado, escolhe outro e faz «Localizar e substituir» de `https://symbolvault.net` por `https://O-TEU-DOMINIO` em todos os ficheiros (ver tabela abaixo).

## 1. Marcadores a substituir antes de publicar

| Onde | Marcador | Substituir por |
|---|---|---|
| `js/config.js` → `ADSENSE_CLIENT` | `ca-pub-XXXXXXXXXXXXXXXX` | O teu ID de editor AdSense (`ca-pub-` + 16 dígitos). Enquanto for marcador, **não é carregado nenhum anúncio**. |
| `js/config.js` → `SLOTS` (`topo`, `meio`, `fundo`) | `XXXXXXXXXX` | IDs (10 dígitos) dos blocos de anúncio responsivos criados no AdSense. Sem ID válido o espaço fica oculto. |
| `ads.txt` | `pub-XXXXXXXXXXXXXXXX` | O teu ID `pub-…` e remove o `#` da linha |
| `contacto.html`, `privacidade.html` | `O_TEU_EMAIL@EXEMPLO.COM` | O teu email real de contacto |
| `termos.html`, `privacidade.html` | `[NOME DO EDITOR / DENOMINAÇÃO SOCIAL]` | O teu nome ou empresa (NIF, morada se aplicável) |
| Todos os `.html`, `sitemap.xml`, `robots.txt`, `js/config.js` | `https://symbolvault.net` | Só se mudares de domínio |

Os marcadores aparecem destacados a amarelo nas páginas. Depois de editar, procura `XXXX`, `EXEMPLO` e `[NOME` para garantir que não ficou nenhum.

Se alterares `js/data.js`/`js/nicks.js`/`css/style.css`, o ficheiro único `SymbolVault.html` (cópia autónoma da página principal) tem de ser regenerado; as outras páginas usam os ficheiros da pasta.

## 2. Publicar no GitHub Pages
1. Cria uma conta em github.com e um repositório novo (por exemplo `symbolvault`), público.
2. Carrega **todo o conteúdo da pasta** `simbolos-gamer` (`index.html`, `css/`, `js/`, `*.html`, `sitemap.xml`, `robots.txt`, `ads.txt`, …) para a raiz do repositório (ou `git init`, `git add .`, `git commit`, `git remote add origin …`, `git push -u origin main`).
3. No repositório: **Settings → Pages → Build and deployment → Source: Deploy from a branch**, branch `main`, pasta `/ (root)` → **Save**.
4. Aguarda 1–2 minutos: o site fica em `https://UTILIZADOR.github.io/REPOSITORIO/`.
5. Cria um ficheiro vazio `.nojekyll` na raiz (evita processamento Jekyll desnecessário).
6. A página `404.html` é usada automaticamente pelo GitHub Pages **quando o site está na raiz de um domínio** (ver passo 3). Num endereço `utilizador.github.io/repositorio/` os caminhos absolutos do 404 (`/css/style.css`) não funcionam, e isso deixa de acontecer com domínio próprio.

**Alternativa Netlify:** arrasta a pasta para app.netlify.com/drop (ou liga o repositório; *build command* vazio, *publish directory* `.`). O `404.html` é reconhecido automaticamente.

## 3. Domínio próprio (symbolvault.net)
1. Regista o domínio num registador (por tua conta; a disponibilidade tem de ser confirmada).
2. No GitHub: **Settings → Pages → Custom domain** → `symbolvault.net` → Save (cria o ficheiro `CNAME`).
3. No DNS do registador:
   - Registos **A** para `@` (apex): `185.199.108.153`, `185.199.109.153`, `185.199.110.153`, `185.199.111.153`
   - Registo **CNAME** para `www` → `UTILIZADOR.github.io`
   (confirma os IPs atuais na documentação do GitHub Pages).
4. Aguarda a propagação DNS (minutos a horas) e ativa **Enforce HTTPS** em Settings → Pages.
5. No Netlify: *Domain management → Add custom domain* e segue as instruções DNS.

## 4. Google Search Console
1. Vai a search.google.com/search-console → **Adicionar propriedade**.
2. Escolhe **Domínio** (`symbolvault.net`) e adiciona o registo TXT pedido ao DNS; ou **Prefixo do URL** (`https://symbolvault.net/`) com ficheiro HTML/meta tag.
3. Em **Sitemaps**, submete `https://symbolvault.net/sitemap.xml`.
4. Usa a **Inspeção de URL** para pedir indexação da página inicial e dos guias.
5. A indexação pode demorar dias ou semanas. Conteúdo útil e ligações de outros sites ajudam.

## 5. Google AdSense
**Antes de pedir:** o site deve estar online no domínio próprio, com conteúdo original e útil, e ter Sobre, Contacto, Privacidade e Termos (já incluídos). Sites com pouco conteúdo ou sem tráfego podem ser recusados; acrescenta guias úteis e espera algum tráfego.
1. Cria conta em adsense.google.com e adiciona o site `symbolvault.net`.
2. Coloca o teu ID em `js/config.js` (`ADSENSE_CLIENT`). Nota: o script só carrega **depois de o visitante aceitar** o aviso de cookies; se a verificação do AdSense exigir o código no `<head>`, segue o método alternativo que a Google indicar (ficheiro `ads.txt` ou meta tag).
3. Publica o `ads.txt` na raiz com o teu ID (a linha `google.com, pub-…, DIRECT, f08c47fec0942fa0`).
4. Aguarda a revisão (de dias a semanas).
5. Depois da aprovação, cria 3 blocos **responsivos** (display) e coloca os IDs em `SLOTS` (`topo`, `meio`, `fundo`). Os espaços reservam altura mínima para não causar saltos na página e nunca ficam dentro da grelha de símbolos.
6. Atenção às regras do programa: não cliques nos teus anúncios, não peças cliques e não coloques anúncios em excesso.

### ⚠ Consentimento no Espaço Económico Europeu / Reino Unido / Suíça
Para servir anúncios a utilizadores nestas regiões, a Google exige uma **plataforma de gestão de consentimento (CMP) certificada pela Google e compatível com o TCF da IAB**. O aviso de cookies incluído é simples (consentimento antes de carregar o script) e **pode não ser suficiente** para cumprir esse requisito. Recomendado: ativa a mensagem gratuita **Google Funding Choices / «Privacidade e mensagens»** no AdSense (ou outra CMP certificada) e, nesse caso, mantém ou ajusta o aviso incluído para não haver dois avisos duplicados. Não é aconselhamento jurídico: confirma com um profissional se necessário.

## 6. Verificações finais
- Abre o site em separador anónimo: o aviso de cookies aparece; antes de aceitar, o separador **Rede** do browser **não** deve mostrar pedidos a `googlesyndication.com`.
- «Gerir cookies» no rodapé volta a abrir o aviso.
- Testa em telemóvel e confirma que os anúncios não ficam sobre os símbolos.
- Valida `https://symbolvault.net/sitemap.xml`, `/robots.txt` e `/ads.txt`.
- Testa os dados estruturados em search.google.com/test/rich-results.

## Estrutura de ficheiros
`index.html` (página principal), 5 guias (`simbolos-nick-fortnite.html`, `simbolos-discord.html`, `nicks-tryhard.html`, `letras-estilizadas.html`, `kaomoji.html`), `sobre.html`, `privacidade.html`, `termos.html`, `contacto.html`, `404.html`, `sitemap.xml`, `robots.txt`, `ads.txt`, `css/style.css`, `js/` (`config.js`, `consent.js`, `data.js`, `nicks.js`, `app.js`, `mini.js`), `gen_data.py` (gera `js/data.js`).
