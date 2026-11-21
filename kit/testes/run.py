#!/usr/bin/env python3
"""Testes do checar_ui.py. Sem rede e sem instalar nada: python3 kit/testes/run.py"""
import contextlib
import io
import json
import sys
import tempfile
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(RAIZ / "kit"))
import checar_ui as c  # noqa: E402

CSS_PADRAO = ":root{--radius: 0.625rem;--primary: oklch(0.205 0 0);}"
CSS_MARCA = ":root{--radius: 0.25rem;--primary: oklch(0.42 0.09 195);}"
falhas, total = [], 0


def projeto(arquivos: dict) -> Path:
    raiz = Path(tempfile.mkdtemp(prefix="ui-kit-"))
    for nome, conteudo in arquivos.items():
        p = raiz / nome
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(conteudo, encoding="utf-8")
    return raiz


def regras(arquivos: dict) -> list:
    return sorted(a["regra"] for a in c.analisar(projeto(arquivos))["achados"])


def rodar(*args):
    saida = io.StringIO()
    with contextlib.redirect_stdout(saida), contextlib.redirect_stderr(io.StringIO()):
        codigo = c.main([str(a) for a in args])
    return codigo, saida.getvalue()


def confere(nome, obtido, esperado):
    global total
    total += 1
    if obtido != esperado:
        falhas.append(f"{nome}: esperado {esperado!r}, veio {obtido!r}")


PKG = lambda *d: json.dumps({"dependencies": {x: "1" for x in d}})  # noqa: E731

# Exemplo completo
antes = c.analisar(RAIZ / "exemplo/antes")
confere("antes: regras", sorted(a["regra"] for a in antes["achados"]), [
    "clique-sem-teclado", "comando-sem-teclado", "cor-padrao", "fonte-padrao",
    "gaveta-sem-arrasto", "muitos-destaques", "raio-padrao", "toast-a-mao"])
confere("depois: limpo", c.analisar(RAIZ / "exemplo/depois")["total"], 0)

# Identidade
confere("tema padrão", regras({"a.css": CSS_PADRAO}), ["cor-padrao", "raio-padrao"])
confere("tema da marca", regras({"a.css": CSS_MARCA}), [])
confere("css sem tema não é shadcn", regras({"a.css": "body{color:red}"}), [])
confere("cinza sem matiz", regras({"a.css": ":root{--radius:1rem;--primary: oklch(0.12 0 0);}"}), ["cor-padrao"])
FONTE = 'import { Inter } from "next/font/google";'
confere("fonte padrão com tema", regras({"a.css": CSS_MARCA, "l.tsx": FONTE}), ["fonte-padrao"])
confere("fonte padrão sem tema não acusa", regras({"l.tsx": FONTE}), [])
confere("fonte própria", regras({"a.css": CSS_MARCA, "l.tsx": 'import { Fraunces, Inter } from "next/font/google";'}), [])

# Toast
TOAST = "const [t, setToasts] = useState([]);"
confere("toast à mão", regras({"a.tsx": TOAST}), ["toast-a-mao"])
confere("toast com sonner", regras({"a.tsx": TOAST, "package.json": PKG("sonner")}), [])
confere("só importar não acusa", regras({"a.tsx": 'import ToastContainer from "./t";\n<ToastContainer />'}), [])

# Gaveta
GAVETA = "export function MenuDrawer(){ return null }"
confere("gaveta sem arrasto", regras({"a.tsx": GAVETA}), ["gaveta-sem-arrasto"])
confere("gaveta com arrasto", regras({"a.tsx": GAVETA + " <div onPointerDown={f} />"}), [])
confere("fechar gaveta não é gaveta", regras({"a.tsx": "const closeDrawer = () => setOpen(false)"}), [])
confere("gaveta do daisyUI", regras({"a.tsx": '<div className="drawer" />', "package.json": PKG("daisyui")}), [])
confere("gaveta com vaul", regras({"a.tsx": GAVETA, "package.json": PKG("vaul")}), [])

# Comando
CMD = "function CommandPalette(){ return null }"
confere("comando sem setas", regras({"a.tsx": CMD}), ["comando-sem-teclado"])
confere("comando com setas", regras({"a.tsx": CMD + " if (e.key === 'ArrowDown') f()"}), [])
confere("comando com Headless UI", regras({"a.tsx": CMD, "package.json": PKG("@headlessui/react")}), [])
confere("comando com cmdk", regras({"a.tsx": CMD, "package.json": PKG("cmdk")}), [])
confere("só usar não acusa", regras({"a.tsx": "<CommandPalette />"}), [])

# Clique
confere("div clicável", regras({"a.tsx": "<div onClick={() => abrir()}>x</div>"}), ["clique-sem-teclado"])
confere("div com role e foco", regras({"a.tsx": '<div role="button" tabIndex={0} onClick={f}>x</div>'}), [])
confere("role sem foco", regras({"a.tsx": '<div role="button" onClick={f}>x</div>'}), ["clique-sem-teclado"])
confere("tabIndex -1", regras({"a.tsx": "<div tabIndex={-1} onClick={f}>x</div>"}), ["clique-sem-teclado"])
for nome, tag in {"motion.div": "<motion.div onClick={f} />", "parágrafo": "<p onClick={f}>x</p>",
                  "linha de tabela": "<tr onClick={f}></tr>", "imagem": "<img onClick={f} />",
                  "link sem href": "<a onClick={f}>x</a>"}.items():
    confere(f"clique em {nome}", regras({"a.tsx": tag}), ["clique-sem-teclado"])
confere("Vue @click", regras({"a.vue": '<div @click="f">x</div>'}), ["clique-sem-teclado"])
confere("Vue v-on:click", regras({"a.vue": '<div v-on:click="f">x</div>'}), ["clique-sem-teclado"])
confere("área auxiliar aria-hidden", regras({"a.tsx": '<div aria-hidden="true" onClick={f} />'}), [])
confere("link com href", regras({"a.tsx": '<a href="/x" onClick={f}>x</a>'}), [])
confere("motion.button", regras({"a.tsx": "<motion.button onClick={f} />"}), [])
confere("comentário não conta", regras({"a.tsx": "{/* <div onClick={f}>x</div> */}\n// <div onClick={f}>"}), [])
confere("seta e maior que dentro do clique", regras({
    "a.tsx": '<div onClick={() => { if (a > b) go() }} role="button" tabIndex={0}>x</div>'}), [])
confere("arquivo de teste ignorado", regras({"a.test.tsx": "<div onClick={f}>x</div>", "b.tsx": "<b />"}), [])
tres = c.analisar(projeto({"a.tsx": "<div onClick={f} />\n\n<div onClick={f} />\n<p onClick={f} />"}))["achados"][0]
confere("todas as linhas aparecem", "linhas 1, 3, 4" in tres["alerta"], True)
confere("stopPropagation", regras({"a.tsx": "<div onClick={(e) => e.stopPropagation()}>x</div>"}), [])
confere("stopPropagation com ação", regras({"a.tsx": "<div onClick={(e) => { e.stopPropagation(); salvar(); }}>x</div>"}), ["clique-sem-teclado"])
confere("motion.a sem href", regras({"a.tsx": "<motion.a onClick={f}>x</motion.a>"}), ["clique-sem-teclado"])
confere("motion.a com href", regras({"a.tsx": '<motion.a href="/x" onClick={f}>x</motion.a>'}), [])
confere("fundo de janela sem foco precisa conferir", regras({"a.tsx": '<div className="fixed inset-0" onClick={f} />'}), ["clique-sem-teclado"])
confere("props espalhadas", regras({"a.tsx": "<div {...attrs} onClick={f}>x</div>"}), [])
confere("botão de verdade", regras({"a.tsx": "<button onClick={f}>x</button>"}), [])
confere("peça copiada ignorada", regras({"components/ui/x.tsx": "<div onClick={f}>x</div>"}), [])

confere("overlay não oculta botão sem foco", regras({"a.tsx": '<div className="overlay-card" onClick={f}>x</div>'}), ["clique-sem-teclado"])
confere("backdrop não oculta botão sem foco", regras({"a.tsx": '<div className="backdrop" onClick={f}>x</div>'}), ["clique-sem-teclado"])
confere("HTML tabindex numérico", regras({"a.html": '<div tabindex=0 onclick="f()" onkeydown="f()">x</div>'}), [])
confere("HTML tabindex negativo", regras({"a.html": '<div tabindex=-1 onclick="f()">x</div>'}), ["clique-sem-teclado"])

# Excesso
DOIS = "<Meteors /><Marquee />"
confere("dois efeitos", regras({"app/page.tsx": DOIS}), ["muitos-destaques"])
confere("um efeito", regras({"app/page.tsx": "<Meteors />"}), [])
confere("componente e classe do mesmo efeito", regras({"app/page.tsx": '<Meteors className="animate-meteor" />'}), [])
confere("fora de página não conta", regras({"components/a.tsx": DOIS}), [])
confere("efeito no componente importado", regras({
    "app/page.tsx": 'import H from "../c/h";\n<Meteors /><H />', "c/h.tsx": "<Marquee />"}), ["muitos-destaques"])
confere("ícone não é efeito", regras({
    "app/page.tsx": 'import { Sparkles, Globe } from "lucide-react";\n<Sparkles /><Globe />'}), [])
confere("ícone reexportado", regras({
    "app/page.tsx": 'import { Sparkles, Globe } from "./icones";\n<Sparkles /><Globe />'}), [])
confere("efeito ambíguo de biblioteca", regras({
    "app/page.tsx": 'import { Sparkles } from "@/components/ui/sparkles";\n<Sparkles /><Meteors />'}), ["muitos-destaques"])
confere("App do Vite é página", regras({"src/App.tsx": "<Marquee /><Meteors />"}), ["muitos-destaques"])

# Cor, fonte e monorepo
TEMA = ":root{--radius:1rem;--primary: %s;}"
for valor in ("0 0% 20%", "#333333", "#333", "240 5.9% 10%", "oklch(0.21 0.006 285.885)"):
    confere(f"cor neutra {valor}", regras({"a.css": TEMA % valor}), ["cor-padrao"])
for valor in ("#0f766e", "195 80% 30%", "oklch(0.42 0.09 195)"):
    confere(f"cor de marca {valor}", regras({"a.css": TEMA % valor}), [])
confere("Inter pelo fontsource", regras({"a.css": CSS_MARCA, "m.tsx": 'import "@fontsource/inter";'}), ["fonte-padrao"])
confere("Inter no CSS", regras({"a.css": CSS_MARCA + "body{font-family: Inter, sans-serif}"}), ["fonte-padrao"])
confere("fonte própria no CSS", regras({"a.css": CSS_MARCA + "body{font-family: Fraunces, serif}"}), [])
confere("um app não silencia o outro", regras({
    "apps/a/package.json": PKG("sonner"), "apps/a/x.tsx": TOAST,
    "apps/b/package.json": PKG("react"), "apps/b/x.tsx": TOAST}), ["toast-a-mao"])
confere("dependência da raiz vale para todos", regras({"package.json": PKG("sonner"), "apps/b/x.tsx": TOAST}), [])
confere("cópia do kit dentro do projeto", regras({
    "ui-sem-cara-de-ia/kit/checar_ui.py": "", "ui-sem-cara-de-ia/exemplo/x.tsx": TOAST, "b.tsx": "<b />"}), [])

# Pastas e linha de comando
confere("node_modules ignorado", regras({"node_modules/x/a.tsx": TOAST, "dist/a.tsx": TOAST}), [])
confere("pasta inexistente", rodar("/nao/existe/mesmo")[0], 2)
confere("pasta vazia não é aprovação", rodar(projeto({}))[0], 2)
confere("só PHP não é aprovação", rodar(projeto({"index.php": "<?php"}))[0], 2)
confere("raiz do kit é recusada", rodar(RAIZ)[0], 2)
limpo = projeto({"a.css": CSS_MARCA, "a.tsx": "<b />"})
confere("saída 0 sem sinais", rodar(limpo)[0], 0)
codigo, texto = rodar(RAIZ / "exemplo/antes", "--json")
confere("saída 1 com sinais", codigo, 1)
confere("json válido", json.loads(texto)["total"], antes["total"])
codigo, texto = rodar(RAIZ / "exemplo/antes", "--pedido")
confere("pedido manda conferir", "pode ser falso" in texto and "Sonner" in texto, True)
confere("pedido sem sinais", "não há correção" in rodar(limpo, "--pedido")[1], True)
copia = (RAIZ / "exemplo/antes/app/page.tsx").read_text(encoding="utf-8")
c.analisar(RAIZ / "exemplo/antes")
confere("não altera o projeto", (RAIZ / "exemplo/antes/app/page.tsx").read_text(encoding="utf-8"), copia)

# Cobertura: nunca aprovar o que não foi lido
confere("só .js não é tela", rodar(projeto({"app.js": "x"}))[0], 2)
confere("PHP com .js não é aprovação", rodar(projeto({"index.php": "<div onclick>", "a/app.js": "x"}))[0], 2)
confere("EJS com server.js não é aprovação", rodar(projeto({"server.js": "x", "views/i.ejs": "<div>"}))[0], 2)
misto = projeto({"a.html": "<b>x</b>", "b.php": "<div>"})
confere("tela não lida é avisada", "não foram lidos" in rodar(misto)[1], True)
confere("HTML em public é lido", regras({"public/index.html": "<div onclick='f()'>x</div>"}), ["clique-sem-teclado"])
confere("JS em public é ignorado", regras({"public/a.js": TOAST, "b.tsx": "<b />"}), [])
confere("accept com barra e asterisco", regras({"a.tsx": '<input accept="image/*" />\n<div onClick={go}>x</div>\n{/* fim */}'}), ["clique-sem-teclado"])
confere("url com duas barras", regras({"a.tsx": '<a href="https://x.y" />\n<div onClick={go}>x</div>'}), ["clique-sem-teclado"])
confere("gaveta com nome simples", regras({"a.tsx": "function Drawer(){ return null }"}), ["gaveta-sem-arrasto"])
confere("BottomSheet com nome simples", regras({"a.tsx": "function BottomSheet(){ return null }"}), ["gaveta-sem-arrasto"])
confere("SweetAlert2 não é aviso à mão", regras({"a.tsx": "const Toast = Swal.mixin({})", "package.json": PKG("sweetalert2")}), [])
confere("Bootstrap por link", regras({"a.html": '<link href="bootstrap.min.css"><div class="toast"></div>'}), [])
confere("atalho de busca não é menu", regras({"a.tsx": "if (e.metaKey && e.key === 'k') foco()"}), [])
html = c.analisar(projeto({"a.html": '<div class="toast"></div>'}))
confere("HTML puro não recebe Sonner", "Sonner" in c.texto_pedido(html), False)
vue = c.analisar(projeto({"a.vue": '<div class="toast"></div>', "package.json": PKG("vue")}))
confere("Vue recebe a peça de Vue", "vue-sonner" in c.texto_pedido(vue), True)
confere("fonte local é da marca", regras({"a.css": CSS_MARCA, "l.tsx": FONTE + '\nimport f from "next/font/local";'}), [])
confere("fonte da marca em outro CSS", regras({"a.css": CSS_MARCA, "b.css": "h1{font-family:'Playfair Display',serif}", "l.tsx": FONTE}), [])
confere("tema em dois arquivos", regras({"a.css": ":root{--primary: oklch(0.205 0 0);}", "b.css": ":root{--radius: 0.5rem;}"}), ["cor-padrao", "raio-padrao"])

grande = "<div onclick='f()'>x</div><img src='data:image/png;base64," + "A" * 450000 + "'>"
confere("tela com imagem embutida é lida", regras({"a.html": grande}), ["clique-sem-teclado"])
confere("cor em hsl()", regras({"a.css": TEMA % "hsl(240 5.9% 10%)"}), ["cor-padrao"])
for pasta in (".output/public", ".venv/x", "venv/x", ".claude/worktrees/a"):
    confere(f"pasta {pasta} ignorada", regras({pasta + "/a.html": "<div onclick='f()'>x</div>", "b.tsx": "<b />"}), [])
pai = projeto({"package.json": PKG("sonner"), "src/a.tsx": TOAST})
confere("package.json acima de src", c.analisar(pai / "src")["total"], 0)

confere("Inter Variable", regras({"a.css": CSS_MARCA + "body{font-family:'Inter Variable',sans-serif}"}), ["fonte-padrao"])
confere("fontsource no CSS", regras({"a.css": CSS_MARCA + '@import "@fontsource/inter";', "a.tsx": "<b />"}), ["fonte-padrao"])
confere("estado showToast", regras({"a.tsx": "const [showToast, setShowToast] = useState(false)"}), ["toast-a-mao"])
confere("estado toastMessage", regras({"a.tsx": "const [toastMessage, setToastMessage] = useState('')"}), ["toast-a-mao"])
confere("pedido avisa tela não lida", "não foram lidos" in rodar(misto, "--pedido")[1], True)
confere("React em .js é tela", rodar(projeto({"app/page.js": "export default () => <main>x</main>"}))[0], 0)
confere("App.js é página", regras({"src/App.js": "export default () => (<div><Marquee /><Meteors /></div>)"}), ["muitos-destaques"])
confere("avisa identidade não avaliada", "não foram avaliados" in rodar(projeto({"a.html": "<b>x</b>"}))[1], True)

for f in falhas:
    print("FALHOU", f)
print(f"{total - len(falhas)}/{total} testes passaram")
sys.exit(1 if falhas else 0)
