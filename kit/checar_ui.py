#!/usr/bin/env python3
"""checar_ui.py: aponta onde a interface de um projeto entrega que foi feita no automático.

Só lê arquivos. Não instala nada, não usa rede e não altera o projeto.
Uso:  python3 kit/checar_ui.py <pasta> [--json] [--pedido]
Saída: 0 = nenhum alerta · 1 = há alertas · 2 = erro de uso ou nada que ele saiba ler.

Cada achado é um ALERTA para conferir, não uma sentença: a regra lê texto, não vê a tela.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

VERSAO = "1.0.4"

PASTAS_IGNORADAS = {
    "node_modules", ".next", ".nuxt", ".svelte-kit", ".turbo", ".git", ".vercel",
    "dist", "build", "out", "coverage", "vendor", "__pycache__", "venv", "env", "site-packages",
}
EXT_CODIGO = {".tsx", ".jsx", ".ts", ".js", ".vue", ".svelte", ".html", ".astro", ".mdx"}
# Arquivos que desenham tela. Só .js ou .ts não prova que a interface foi lida.
EXT_TELA = {".tsx", ".jsx", ".vue", ".svelte", ".html", ".astro", ".mdx"}
# Telas em tecnologias que o verificador não entende: ele avisa em vez de aprovar.
EXT_TELA_NAO_LIDA = {".php", ".ejs", ".erb", ".hbs", ".handlebars", ".pug", ".twig", ".cshtml", ".razor",
                     ".jinja", ".jinja2", ".j2", ".liquid", ".njk", ".mustache"}
EXT_CSS = {".css", ".scss"}
TAMANHO_MAX = 400_000      # código comum acima disso costuma ser pacote gerado
TAMANHO_MAX_TELA = 5_000_000  # tela grande costuma ter imagem embutida, que é removida antes da leitura
RE_BASE64 = re.compile(r"data:[\w/+.-]+;base64,[A-Za-z0-9+/=]+")
RE_TESTE = re.compile(r"\.(test|spec|stories)\.\w+$|(^|/)(__tests__|__mocks__|tests?|e2e|cypress|playwright)/")

# Valores lidos no repositório oficial do shadcn/ui em 18/11/2026.
RAIOS_PADRAO = {"0.625rem", "0.5rem"}
PRIMARIAS_PADRAO = {"222.2 47.4% 11.2%", "240 5.9% 10%", "24 9.8% 10%", "220.9 39.3% 11%", "0 0% 9%"}
FONTES_PADRAO = {"geist", "geist sans", "geist mono", "inter"}
FONTES_GENERICAS = {"var", "inherit", "initial", "system", "system ui", "ui sans serif", "ui serif", "ui monospace",
                    "sans serif", "serif", "monospace", "apple system", "blinkmacsystemfont", "arial", "helvetica"}

LIBS_TOAST = {"sonner", "vue-sonner", "svelte-sonner", "react-hot-toast", "react-toastify", "@radix-ui/react-toast",
              "@base-ui-components/react", "@base-ui/react", "notistack", "@mantine/notifications",
              "@chakra-ui/react", "@mui/material", "antd", "@heroui/react", "@nextui-org/react", "daisyui",
              "sweetalert2", "bootstrap", "react-bootstrap", "vue-toastification", "vuetify", "element-plus",
              "primereact", "primevue", "flowbite", "flowbite-react", "notyf", "toastify-js", "izitoast",
              "quasar", "@nuxt/ui", "@ark-ui/react"}
LIBS_DRAWER = {"vaul", "vaul-vue", "vaul-svelte", "@mui/material", "antd", "@chakra-ui/react",
               "@heroui/react", "@nextui-org/react", "daisyui", "bootstrap", "react-bootstrap", "vuetify",
               "element-plus", "primereact", "primevue", "flowbite", "flowbite-react", "quasar", "@nuxt/ui"}
LIBS_COMANDO = {"cmdk", "cmdk-sv", "vue-command-palette", "kbar", "ninja-keys", "@headlessui/react", "@heroui/react"}
# Biblioteca sugerida conforme a tecnologia do projeto. Sem tecnologia conhecida, o pedido não crava um nome.
PECAS = {
    "toast": {"react": "Sonner", "vue": "vue-sonner", "svelte": "svelte-sonner"},
    "gaveta": {"react": "Vaul", "vue": "vaul-vue", "svelte": "vaul-svelte"},
    "comando": {"react": "cmdk", "vue": "vue-command-palette", "svelte": "cmdk-sv"},
}

EFEITOS = (
    "Marquee Meteors BorderBeam Particles ShimmerButton Spotlight BackgroundBeams AuroraText "
    "AuroraBackground Sparkles SparklesCore RetroGrid AnimatedBeam NeonGradientCard Confetti "
    "WavyBackground BackgroundGradient Vortex Lamp LampContainer HeroParallax InfiniteMovingCards "
    "TextGenerateEffect TypewriterEffect CardContainer Globe DotPattern FlickeringGrid Ripple "
    "MagicCard ShineBorder Boxes GlowingEffect"
).split()
# Estes nomes também são ícones comuns: só contam se vierem claramente de um componente de efeito.
AMBIGUOS = {"Sparkles", "Globe", "Boxes", "Lamp", "Ripple", "Confetti"}
FAMILIAS = {"meteors": "meteor", "auroratext": "aurora", "aurorabackground": "aurora"}

RE_EFEITO = re.compile(r"<(" + "|".join(EFEITOS) + r")\b")
RE_ANIMA = re.compile(r"\banimate-(marquee|aurora|meteor|spotlight)\b")
RE_PKG_ICONE = re.compile(r"lucide|react-icons|heroicons|tabler/icons|phosphor|radix-ui/react-icons|(^|/)ic[oô]n")
RE_FONTE_EFEITO = re.compile(r"magicui|magic-ui|aceternity|efeito|effect|sparkles|confetti|globe|ripple|lamp|boxes|components/ui")
RE_IMPORT_NOMES = re.compile(r"import\s+(?:([\w$]+)\s*,?\s*)?(?:\{([^}]*)\})?\s*from\s*[\"']([^\"']+)[\"']")
RE_IMPORT = re.compile(r"""(?:from\s+|import\s+)["']((?:\.{1,2}/|@/|~/)[^"']+)["']""")

# Procuram onde a peça é CRIADA, não onde ela só é importada, usada ou fechada.
RE_TOAST = re.compile(r"\bconst\s*\[\s*\w+\s*,\s*set\w*Toast\w*\s*\]|\b(?:function|const)\s+(?:showToast|addToast|ToastContainer|Toast)\b"
                      r"|class(?:Name)?=[\"'][^\"']*\btoast\b")
RE_DRAWER = re.compile(r"\b(?:function|const|class)\s+(?:[A-Z]\w*)?(?:Drawer|BottomSheet)\b|class(?:Name)?=[\"'][^\"']*\b(?:drawer|bottom-sheet)\b")
RE_ARRASTO = re.compile(r"onPointerDown|onTouchStart|onPointerMove|onTouchMove|useDrag|\bdrag=|pointerdown|touchstart")
RE_COMANDO = re.compile(r"\b(?:function|const|class)\s+[A-Z]\w*Command(?:Menu|Palette)\b|\b(?:function|const|class)\s+Command(?:Menu|Palette)\b"
                        r"|class(?:Name)?=[\"'][^\"']*\bcommand-(?:menu|palette)\b")
RE_SETAS = re.compile(r"ArrowDown")

RE_TAG_CLIQUE = re.compile(r"<(div|span|p|li|tr|td|img|section|article|header|footer|main|aside|h[1-6]|a|motion\.(?!button\b)\w+)(?=[\s>/])")
RE_TEM_CLIQUE = re.compile(r"(?:\bon[Cc]lick\s*=|@click\b|\bv-on:click\b|\bon:click\b)")
# Clique que só impede a propagação não é uma ação: serve para o clique não vazar para o elemento de fora.
RE_SO_PROPAGACAO = re.compile(r"on[Cc]lick\s*=\s*\{\s*\(?\s*\w*\s*(?::\s*[\w.<>]+\s*)?\)?\s*=>\s*\{?\s*\w+\.stopPropagation\(\)\s*;?\s*\}?\s*\}"
                              r"|@click\.stop(?!\s*=)|v-on:click\.stop(?!\s*=)")
RE_JSX = re.compile(r"(?:return\s*\(?|=>\s*\(?)\s*<[A-Za-z>]")
RE_TABINDEX = re.compile(r"\btab[Ii]ndex\s*=\s*(?:\{\s*(?!-)|[\"']\s*(?!-)|\d+(?=[\s>/]))")


def achado(grupo, regra, arquivo, linha, alerta, pedido):
    return {"grupo": grupo, "regra": regra, "arquivo": arquivo, "linha": linha, "alerta": alerta, "pedido": pedido}


def familia(nome: str) -> str:
    """Meteors e animate-meteor são o mesmo efeito: contam uma vez."""
    chave = nome.lower().removeprefix("animate-")
    return FAMILIAS.get(chave, chave)


def grande_demais(p: Path) -> bool:
    try:
        return p.stat().st_size > (TAMANHO_MAX_TELA if p.suffix in EXT_TELA else TAMANHO_MAX)
    except OSError:
        return True


def ler(p: Path) -> str:
    if grande_demais(p):
        return ""
    try:
        return RE_BASE64.sub("data:", p.read_text(encoding="utf-8", errors="ignore"))
    except OSError:
        return ""


# Textos entre aspas vêm primeiro: accept="image/*" não é começo de comentário.
RE_TEXTO_OU_COMENTARIO = re.compile(
    r"\"(?:[^\"\\\n]|\\.)*\"|'(?:[^'\\\n]|\\.)*'|`(?:[^`\\]|\\.)*`"
    r"|(?P<c>/\*.*?\*/|<!--.*?-->|(?<![:\\])//[^\n]*)", re.S)


def _branco(m: re.Match) -> str:
    return re.sub(r"[^\n]", " ", m.group(0)) if m.group("c") else m.group(0)


def sem_comentarios(t: str) -> str:
    """Troca comentários por espaços, mantém os textos e o número de cada linha."""
    return RE_TEXTO_OU_COMENTARIO.sub(_branco, t)


def tecnologia(deps: set) -> str:
    if deps & {"react", "next", "preact", "@remix-run/react"}:
        return "react"
    if deps & {"vue", "nuxt"}:
        return "vue"
    if deps & {"svelte", "@sveltejs/kit"}:
        return "svelte"
    return ""


def pedido_peca(tipo: str, deps: set, com_lib: str, sem_lib: str) -> str:
    nome = PECAS[tipo].get(tecnologia(deps))
    return com_lib.format(nome) if nome else sem_lib


def eh_copia_do_kit(pasta: Path) -> bool:
    return (pasta / "kit" / "checar_ui.py").is_file()


def varrer(raiz: Path):
    pilha = [raiz]
    while pilha:
        atual = pilha.pop()
        if eh_copia_do_kit(atual):
            continue
        try:
            itens = sorted(atual.iterdir())
        except OSError:
            continue
        for item in itens:
            if item.is_symlink():
                continue
            if item.is_dir():
                # Pastas com ponto são de ferramentas: caches, ambientes e cópias de trabalho.
                if item.name not in PASTAS_IGNORADAS and not item.name.startswith("."):
                    pilha.append(item)
            elif item.is_file():
                yield item


def linha_de(texto: str, pos: int) -> int:
    return texto.count("\n", 0, pos) + 1


def mapa_dependencias(arquivos) -> dict:
    mapa = {}
    for p in arquivos:
        if p.name != "package.json":
            continue
        try:
            dados = json.loads(ler(p) or "{}")
        except ValueError:
            continue
        deps = set()
        for chave in ("dependencies", "devDependencies", "peerDependencies"):
            valor = dados.get(chave)
            if isinstance(valor, dict):
                deps.update(valor)
        mapa[p.parent] = deps
    return mapa


def deps_de(p: Path, raiz: Path, mapa: dict) -> set:
    """Só valem o package.json da pasta do arquivo e os acima dela: um app não silencia o outro."""
    deps, atual = set(), p.parent
    while True:
        deps |= mapa.get(atual, set())
        if atual == raiz or atual.parent == atual:
            break
        atual = atual.parent
    # Quem aponta para src/ ainda tem o package.json logo acima.
    for acima in list(raiz.resolve().parents)[:3]:
        arq = acima / "package.json"
        if arq.is_file():
            deps |= mapa_dependencias([arq]).get(acima, set())
            break
    return deps


def eh_peca_copiada(rel: str) -> bool:
    """components/ui é onde o shadcn copia as peças: não é código feito à mão pelo projeto."""
    return "components/ui/" in rel or "/ui/src/components/" in rel


def cor_neutra(valor: str) -> bool:
    v = " ".join(valor.split()).lower()
    m = re.fullmatch(r"hsla?\((.*)\)", v)
    if m:
        v = " ".join(m.group(1).replace(",", " ").split("/")[0].split())
    if v in PRIMARIAS_PADRAO:
        return True
    m = re.fullmatch(r"oklch\(\s*[\d.]+%?\s+([\d.]+)\s+[\d.]+\s*(?:/.*)?\)", v)
    if m:
        return float(m.group(1)) < 0.02
    m = re.fullmatch(r"(?:hsla?\()?\s*[\d.]+(?:deg)?[ ,]+([\d.]+)%[ ,]+[\d.]+%\s*\)?", v)
    if m:
        return float(m.group(1)) == 0
    m = re.fullmatch(r"#([0-9a-f]{3}|[0-9a-f]{6})", v)
    if m:
        h = m.group(1)
        h = "".join(c * 2 for c in h) if len(h) == 3 else h
        rgb = [int(h[i:i + 2], 16) for i in (0, 2, 4)]
        return max(rgb) - min(rgb) <= 8
    return False


def nome_fonte(texto: str) -> str:
    nome = re.sub(r"[_\-]+", " ", texto.strip().strip("'\"")).strip().lower()
    return re.sub(r"\s+variable$", "", nome)


def checar_identidade(raiz, arquivos, codigo, mapa):
    saida = []
    css = [(p, sem_comentarios(ler(p))) for p in arquivos if p.suffix in EXT_CSS]
    temas = [(p, t) for p, t in css if re.search(r"--(?:primary|radius)\s*:", t)]
    # O tema pode estar dividido em mais de um arquivo.
    if not (any(re.search(r"--primary\s*:", t) for _, t in temas) and any(re.search(r"--radius\s*:", t) for _, t in temas)):
        return saida
    for p, t in temas:
        rel = p.relative_to(raiz).as_posix()
        m = re.search(r"--radius\s*:\s*([^;]+);", t)
        if m and m.group(1).strip() in RAIOS_PADRAO:
            saida.append(achado("identidade", "raio-padrao", rel, linha_de(t, m.start()),
                                f"Cantos no valor que vem de fábrica ({m.group(1).strip()}).",
                                "Defina o raio dos cantos a partir da minha marca e aplique em todas as peças."))
        m = re.search(r"--primary\s*:\s*([^;]+);", t)
        if m and cor_neutra(m.group(1)):
            valor = " ".join(m.group(1).split())
            saida.append(achado("identidade", "cor-padrao", rel, linha_de(t, m.start()),
                                f"Cor principal sem identidade: preto ou cinza de fábrica ({valor}).",
                                "Troque a cor principal pela cor da minha marca e confira o contraste."))
    fontes, onde = set(), None

    def anota(nome, p, t, pos):
        nonlocal onde
        n = nome_fonte(nome)
        if n and n not in FONTES_GENERICAS and not n.startswith("var"):
            fontes.add(n)
            if n in FONTES_PADRAO and onde is None:
                onde = (p.relative_to(raiz).as_posix(), linha_de(t, pos))

    for p, t in codigo:
        for m in re.finditer(r"import\s*\{([^}]+)\}\s*from\s*[\"']next/font/google[\"']", t):
            for n in m.group(1).split(","):
                if n.strip():
                    anota(n.split(" as ")[0], p, t, m.start())
        for m in re.finditer(r"[\"']@fontsource(?:-variable)?/([\w-]+)", t):
            anota(m.group(1), p, t, m.start())
        if re.search(r"[\"']next/font/local[\"']", t):
            fontes.add("fonte local")
    for p, t in css:
        for m in re.finditer(r"[\"']@fontsource(?:-variable)?/([\w-]+)", t):
            anota(m.group(1), p, t, m.start())
        for m in re.finditer(r"(?:font-family|--font-sans|--font-heading|--font-display)\s*:\s*([^;,}]+)", t):
            anota(m.group(1), p, t, m.start())
    if fontes and fontes <= FONTES_PADRAO and onde:
        saida.append(achado("identidade", "fonte-padrao", onde[0], onde[1],
                            "Só as fontes que quase todo projeto gerado usa (" + ", ".join(sorted(fontes)) + ").",
                            "Escolha uma fonte de títulos com a personalidade da minha marca."))
    return saida


def fim_da_tag(t: str, inicio: int) -> int:
    """Acha o > que fecha a tag, ignorando o que está dentro de {} e de aspas."""
    aspas, chaves = None, 0
    for i in range(inicio, min(len(t), inicio + 4000)):
        c = t[i]
        if aspas:
            if c == aspas and t[i - 1] != "\\":
                aspas = None
        elif c in "\"'`":
            aspas = c
        elif c == "{":
            chaves += 1
        elif c == "}":
            chaves = max(0, chaves - 1)
        elif c == ">" and chaves == 0 and t[i - 1] != "=":
            return i + 1
    return -1


def cliques_sem_teclado(t: str) -> list:
    linhas = []
    for m in RE_TAG_CLIQUE.finditer(t):
        fim = fim_da_tag(t, m.end())
        if fim < 0:
            continue
        tag = t[m.start():fim]
        if not RE_TEM_CLIQUE.search(tag):
            continue
        if m.group(1) in ("a", "motion.a") and re.search(r"\b(?:href|to)\s*=", tag):
            continue
        if RE_SO_PROPAGACAO.search(tag) or "{..." in tag or RE_TABINDEX.search(tag):
            continue
        # aria-hidden marca área auxiliar de mouse, com outro caminho para o teclado.
        if re.search(r"aria-hidden\s*=\s*[\"'{]+\s*true", tag):
            continue
        linhas.append(linha_de(t, m.start()))
    return sorted(set(linhas))


def checar_comportamento(raiz, codigo, mapa):
    saida = []
    for p, t in codigo:
        rel = p.relative_to(raiz).as_posix()
        if eh_peca_copiada(rel):
            continue
        deps = deps_de(p, raiz, mapa)
        # Página que carrega o Bootstrap por link já tem aviso e gaveta prontos.
        com_bootstrap = re.search(r"bootstrap(?:\.min)?\.(?:css|js|bundle)", t) is not None
        if not deps & LIBS_TOAST and not com_bootstrap:
            m = RE_TOAST.search(t)
            if m:
                saida.append(achado("comportamento", "toast-a-mao", rel, linha_de(t, m.start()),
                                    "Aviso (toast) feito à mão: costuma empilhar mal ou sumir antes da leitura.",
                                    pedido_peca("toast", deps, "Troque este aviso pelo {}, seguindo a instalação oficial.",
                                                "Troque este aviso por uma biblioteca pronta, adequada à tecnologia deste projeto.")))
        if not deps & LIBS_DRAWER and not com_bootstrap:
            m = RE_DRAWER.search(t)
            if m and not RE_ARRASTO.search(t):
                saida.append(achado("comportamento", "gaveta-sem-arrasto", rel, linha_de(t, m.start()),
                                    "Gaveta (drawer) sem nenhum tratamento de arrasto: no celular ela não segue o dedo.",
                                    pedido_peca("gaveta", deps, "Use o {} nesta gaveta e teste arrastar para fechar no celular.",
                                                "Use uma gaveta pronta, adequada à tecnologia deste projeto, e teste arrastar no celular.")))
        if not deps & LIBS_COMANDO:
            m = RE_COMANDO.search(t)
            if m and not RE_SETAS.search(t):
                saida.append(achado("comportamento", "comando-sem-teclado", rel, linha_de(t, m.start()),
                                    "Menu de comandos sem tratar as setas: quem usa teclado fica preso.",
                                    pedido_peca("comando", deps, "Use o {} neste menu e teste abrir, navegar e escolher só com o teclado.",
                                                "Use um menu pronto, adequado à tecnologia deste projeto, e teste só com o teclado.")))
        linhas = cliques_sem_teclado(t)
        if linhas:
            n = len(linhas)
            onde = ", ".join(map(str, linhas[:12])) + ("…" if n > 12 else "")
            texto = ("1 elemento clicável que o teclado não alcança." if n == 1
                     else f"{n} elementos clicáveis que o teclado não alcança (linhas {onde}).")
            saida.append(achado("comportamento", "clique-sem-teclado", rel, linhas[0], texto,
                                "Transforme estes elementos em <button> ou link, com foco visível. Se for só o fundo escuro de uma janela que já tem botão de fechar, pode manter."))
    return saida


def eh_pagina(rel: str) -> bool:
    if re.search(r"(^|/)app/(.*/)?page\.(tsx|jsx|js|mdx)$", rel):
        return True
    if re.search(r"(^|/)pages/(?!api/)(?!_).*\.(tsx|jsx|js|vue|astro)$", rel):
        return True
    if re.search(r"(^|/)(src/)?App\.(tsx|jsx|js|vue|svelte)$", rel):
        return True
    if rel.endswith("+page.svelte") or rel.endswith(".html"):
        return True
    return bool(re.search(r"(^|/)src/routes/.*\.(tsx|jsx)$", rel))


def resolver(origem: Path, alvo: str, raiz: Path, base_alias):
    base = base_alias / alvo[2:] if alvo.startswith(("@/", "~/")) else origem.parent / alvo
    for sufixo in ("", ".tsx", ".jsx", ".ts", ".js", ".vue", ".svelte", "/index.tsx", "/index.jsx", "/index.ts"):
        c = Path(str(base) + sufixo)
        if c.is_file():
            try:
                c.resolve().relative_to(raiz.resolve())
            except ValueError:
                return None
            return c
    return None


def efeitos_do_texto(t: str) -> set:
    fontes = {}
    for padrao, nomes, origem in RE_IMPORT_NOMES.findall(t):
        for n in ([padrao] if padrao else []) + nomes.split(","):
            n = n.strip()
            if n:
                fontes[n.split(" as ")[-1].strip()] = origem
    achados = set()
    for nome in set(RE_EFEITO.findall(t)):
        origem = fontes.get(nome, "")
        if origem and RE_PKG_ICONE.search(origem):
            continue
        if nome in AMBIGUOS and not RE_FONTE_EFEITO.search(origem):
            if not re.search(rf"\b(?:function|const)\s+{nome}\b", t):
                continue
        achados.add(familia(nome))
    achados.update(familia(a) for a in RE_ANIMA.findall(t))
    return achados


def checar_excesso(raiz, codigo):
    saida = []
    base_alias = raiz / "src" if (raiz / "src").is_dir() else raiz
    for p, t in codigo:
        rel = p.relative_to(raiz).as_posix()
        if not eh_pagina(rel):
            continue
        vistos, fila, efeitos = {p}, [(p, t, 0)], set()
        while fila:
            atual, texto, nivel = fila.pop()
            efeitos |= efeitos_do_texto(texto)
            if nivel >= 2:
                continue
            for alvo in RE_IMPORT.findall(texto):
                c = resolver(atual, alvo, raiz, base_alias)
                if c and c not in vistos and "components/ui/" not in c.as_posix():
                    vistos.add(c)
                    fila.append((c, sem_comentarios(ler(c)), nivel + 1))
        if len(efeitos) > 1:
            saida.append(achado("excesso", "muitos-destaques", rel, 1,
                                f"{len(efeitos)} efeitos disputando atenção na mesma página: " + ", ".join(sorted(efeitos)) + ".",
                                "Mantenha um único destaque nesta página e deixe o resto parado."))
    return saida


def analisar(raiz: Path) -> dict:
    arquivos = list(varrer(raiz))
    mapa = mapa_dependencias(arquivos)
    codigo, nao_lidas = [], []
    for p in arquivos:
        rel = p.relative_to(raiz).as_posix()
        if RE_TESTE.search(rel) or p.name.endswith(".min.js"):
            continue
        if p.suffix in EXT_TELA_NAO_LIDA or (p.suffix in EXT_TELA and grande_demais(p)):
            nao_lidas.append(rel)
        # Em public/ ficam arquivos prontos: só as páginas HTML interessam.
        elif p.suffix in EXT_CODIGO and not (re.search(r"(^|/)public/", rel) and p.suffix != ".html"):
            codigo.append((p, sem_comentarios(ler(p))))
    achados = (checar_identidade(raiz, arquivos, codigo, mapa)
               + checar_comportamento(raiz, codigo, mapa)
               + checar_excesso(raiz, codigo))
    grupos = {g: sum(1 for a in achados if a["grupo"] == g) for g in ("identidade", "comportamento", "excesso")}
    return {"versao": VERSAO, "pasta": str(raiz), "arquivos_lidos": len(codigo),
            "telas_lidas": sum(1 for p, t in codigo if p.suffix in EXT_TELA or (p.suffix == ".js" and RE_JSX.search(t))),
            "tema_encontrado": any(p.suffix in EXT_CSS and re.search(r"--primary\s*:", ler(p)) for p in arquivos),
            "telas_nao_lidas": len(nao_lidas), "exemplos_nao_lidos": nao_lidas[:5],
            "total": len(achados), "grupos": grupos, "achados": achados}


TITULOS = {
    "identidade": "Identidade: parece com todos os outros",
    "comportamento": "Comportamento: bonito no print, falha no uso",
    "excesso": "Excesso: tudo chama atenção, nada se destaca",
}


def aviso_identidade(r: dict) -> str:
    return "" if r["tema_encontrado"] else "Cor, fonte e cantos não foram avaliados: não achei um tema com --primary e --radius."


def aviso_nao_lidas(r: dict) -> str:
    if not r["telas_nao_lidas"]:
        return ""
    return (f"Atenção: {r['telas_nao_lidas']} arquivo(s) de tela não foram lidos, como "
            + ", ".join(r["exemplos_nao_lidos"][:3]) + ". O resultado não vale para eles.")


def texto_relatorio(r: dict) -> str:
    n = r["arquivos_lidos"]
    linhas = [f"ui-sem-cara-de-ia {r['versao']} · {n} {'arquivo lido' if n == 1 else 'arquivos lidos'}, {r['telas_lidas']} de tela"]
    linhas += [a for a in (aviso_nao_lidas(r), aviso_identidade(r)) if a]
    if not r["total"]:
        linhas.append("Nenhum alerta. Abra a tela mesmo assim: esta checagem lê o código, não vê o resultado.")
        return "\n".join(linhas)
    for g, titulo in TITULOS.items():
        itens = [a for a in r["achados"] if a["grupo"] == g]
        if itens:
            linhas += ["", f"{titulo} ({len(itens)})"]
            linhas += [f"  {a['arquivo']}:{a['linha']}  {a['alerta']}" for a in itens]
    nome = "alerta" if r["total"] == 1 else "alertas"
    linhas += ["", f"Total: {r['total']} {nome}. Use --pedido para gerar o texto de correção."]
    return "\n".join(linhas)


def texto_pedido(r: dict) -> str:
    if not r["total"]:
        return " ".join(x for x in ("Nenhum alerta: não há correção a pedir.", aviso_nao_lidas(r)) if x)
    linhas = ["Corrija a interface deste projeto. Antes de mudar, confira cada item: ele veio de uma checagem",
              "automática do código e pode ser falso. Diga quais descartou e por quê.", ""]
    for i, a in enumerate(r["achados"], 1):
        linhas.append(f"{i}. {a['arquivo']}:{a['linha']}. {a['alerta']} {a['pedido']}")
    if aviso_nao_lidas(r):
        linhas += ["", aviso_nao_lidas(r)]
    linhas += ["", "Regras: se o projeto já usa outra biblioteca para a mesma função, mantenha a dele.",
               "Instale o que faltar pelo caminho oficial, com o código dentro do projeto.",
               "Se a minha marca (cor, fonte, cantos) não estiver definida, pergunte antes de escolher.",
               "No fim, abra a tela, teste no celular e só com o teclado, e me mostre o que testou."]
    return "\n".join(linhas)


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="Aponta onde a interface entrega que foi feita no automático.")
    ap.add_argument("pasta")
    ap.add_argument("--json", action="store_true", help="saída em JSON")
    ap.add_argument("--pedido", action="store_true", help="imprime o pedido de correção para a IA")
    a = ap.parse_args(argv)
    raiz = Path(a.pasta).expanduser()
    if not raiz.is_dir():
        print(f"Pasta não encontrada: {raiz}", file=sys.stderr)
        return 2
    if eh_copia_do_kit(raiz):
        print("Esta é a pasta do próprio kit. Aponte para a pasta do seu projeto.", file=sys.stderr)
        return 2
    r = analisar(raiz)
    if not r["telas_lidas"]:
        print("Não encontrei telas que eu saiba ler (HTML, JSX, TSX, JavaScript com JSX, Vue, Svelte, Astro ou MDX). "
              "Isso não é aprovação: confira a pasta. " + aviso_nao_lidas(r), file=sys.stderr)
        return 2
    if a.json:
        print(json.dumps(r, ensure_ascii=False, indent=2))
    elif a.pedido:
        print(texto_pedido(r))
    else:
        print(texto_relatorio(r))
    return 1 if r["total"] else 0


if __name__ == "__main__":
    sys.exit(main())
