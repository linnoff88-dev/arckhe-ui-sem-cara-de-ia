ï»¿# UI sem cara de IA

<div align="center">
  <img src="capa/logo.svg" alt="Arckhé AI" height="48" />
  <p><strong>Arckhé AI</strong></p>
</div>


[![UI sem cara de IA](guia/assets/banner.jpg)](https://linnoff88-dev.github.io/arckhe-/guia/)

**ê°Å¸â¡Â§ê°Å¸â¡Â· [PortuguêÂªs](README.md) êÂ· ê°Å¸â¡Âºê°Å¸â¡Â¸ [English](README.en.md) êÂ· ê°Å¸â¡Âªê°Å¸â¡Â¸ [EspaêÂ±ol](README.es.md)**

## O que êÂ©

UI sem cara de IA êÂ© um kit gratuito para quem cria sites e aplicativos com Claude Code ou Codex. Ele traz um verificador que lêÂª o seu projeto e aponta o que entrega o trabalho automêÂ¡tico: cor e cantos de fêÂ¡brica, aviso feito êÂ  mêÂ£o, botêÂ£o que o teclado nêÂ£o alcanêÂ§a e excesso de efeitos. Depois, ele escreve o pedido de correêÂ§êÂ£o para vocêÂª colar na sua IA. Precisa de Python 3 para rodar. NêÂ£o instala nada no seu projeto e nêÂ£o altera nenhum arquivo.

## ê°Å¸ââ Guia de uso

Guia completo: **https://linnoff88-dev.github.io/arckhe-/guia/**

[ê°Å¸Å½Â¬ VêÂ­deo: veja o kit em aêÂ§êÂ£o](https://www.youtube.com/watch?v=blXnqoGoltM)

## PeêÂ§a para a sua IA analisar

```text
Baixe o kit https://github.com/linnoff88-dev/ui-sem-cara-de-ia numa pasta temporêÂ¡ria, fora do meu projeto.
Leia o README e rode o verificador kit/checar_ui.py apontando para a pasta do meu projeto.
Se faltar Python 3.9 ou mais novo, me avise antes de instalar qualquer coisa.
Confira cada alerta no cêÂ³digo e me diga, em portuguêÂªs simples, quais sêÂ£o reais, quais sêÂ£o falsos
e por onde vale comeêÂ§ar. NêÂ£o mude nenhum arquivo do projeto antes do meu sim.
```

---

## InstalaêÂ§êÂ£o têÂ©cnica

Requisito: Python 3.9 ou mais novo. O kit usa sêÂ³ a biblioteca padrêÂ£o.

```bash
git clone https://github.com/linnoff88-dev/ui-sem-cara-de-ia
cd ui-sem-cara-de-ia
python3 kit/testes/run.py                      # 119 testes, sem rede
python3 kit/checar_ui.py exemplo/antes         # 8 alertas
python3 kit/checar_ui.py exemplo/depois        # nenhum alerta
python3 kit/checar_ui.py /caminho/do/projeto
python3 kit/checar_ui.py /caminho/do/projeto --pedido > pedido.txt
```

Substitua `/caminho/do/projeto` pela pasta real que deseja analisar. Mantenha o kit fora do seu projeto. CêÂ³digos de saêÂ­da: `0` sem alertas, `1` com alertas, `2` erro de uso ou nenhum arquivo de interface encontrado. Use `--json` para integrar com outras ferramentas.

### O que ele procura

| Grupo | Alerta | Como detecta |
|---|---|---|
| Identidade | Cantos de fêÂ¡brica | `--radius` igual a `0.625rem` ou `0.5rem` num tema com `--primary` |
| Identidade | Cor sem marca | `--primary` igual a um padrêÂ£o do shadcn/ui ou cinza em OKLCH, HSL ou hexadecimal |
| Identidade | Fonte de sempre | SêÂ³ Geist ou Inter (next/font, @fontsource ou CSS), num projeto com esse tema |
| Comportamento | Aviso feito êÂ  mêÂ£o | Estado ou componente de toast sem biblioteca de avisos no `package.json` da pasta ou acima dela |
| Comportamento | Gaveta sem arrasto | Componente de gaveta sem eventos de toque ou ponteiro e sem biblioteca prêÂ³pria |
| Comportamento | Menu sem setas | Menu de comandos sem `ArrowDown` e sem biblioteca prêÂ³pria |
| Comportamento | Clique sem teclado | `div`, `span`, `p`, `li`, `tr`, `td`, `img`, seêÂ§êÂµes, têÂ­tulos, `motion.*` ou `a` sem `href`, com clique (React, Vue ou Svelte) e sem `tabIndex` que permita foco |
| Excesso | Muitos destaques | Mais de um efeito conhecido em pêÂ¡gina de rota, `App` ou HTML, olhando dois nêÂ­veis de importaêÂ§êÂ£o |

SêÂ£o alertas de leitura de cêÂ³digo. O verificador nêÂ£o abre a tela, nêÂ£o mede contraste e nêÂ£o julga se o design êÂ© bom. A regra de clique verifica se o elemento recebe foco; nêÂ£o confirma que Enter ou EspaêÂ§o executam a aêÂ§êÂ£o. Um alerta pode ser falso, e uma tela sem alertas ainda pode estar ruim.

Limites: ignora arquivos de teste, comentêÂ¡rios, `components/ui`, pastas geradas e, em `public/`, tudo que nêÂ£o seja HTML. Elementos com `{...props}` nêÂ£o sêÂ£o acusados, porque as propriedades podem trazer o foco. `svg`, `i`, `label`, `ul`, `nav` e componentes prêÂ³prios com clique nêÂ£o sêÂ£o analisados. Efeitos fora da lista interna nêÂ£o sêÂ£o contados. Cliques ligados por `addEventListener` nêÂ£o sêÂ£o vistos. Identidade sêÂ³ êÂ© analisada quando o projeto usa um tema com `--primary` e `--radius`, como o do shadcn/ui; cores direto em classes do Tailwind, temas dentro de `<style>` e fontes carregadas por link nêÂ£o entram. Rode na raiz do projeto.

Cobertura: ele sêÂ³ lêÂª telas em HTML, JSX, TSX, Vue, Svelte, Astro e MDX. Sem nenhuma delas, sai com cêÂ³digo `2` e nêÂ£o aprova. Se encontrar telas em PHP, EJS, Blade, Pug, Twig ou parecidas ao lado das que sabe ler, avisa que o resultado nêÂ£o vale para elas.

### Arquivos

| Caminho | Para quêÂª |
|---|---|
| `kit/checar_ui.py` | Verificador |
| `kit/medir_pastas.py` | Total de vêÂ¡rios projetos, sem nomes |
| `kit/PEDIDOS.md` | Pedidos prontos para a IA |
| `kit/bibliotecas.json` | Bibliotecas conferidas, com site e licenêÂ§a |
| `kit/skill/ui-sem-cara-de-ia/` | Skill para Claude Code: copie para `.claude/skills/` |
| `exemplo/antes`, `exemplo/depois` | Mesmo cadastro, com e sem os problemas |
| `FATOS.md` | Fontes e mediêÂ§êÂµes |

## O processo, do inêÂ­cio ao fim

| # | Passo | Comando | Quem faz |
|---|---|---|---|
| 1 | Baixar o kit | `git clone https://github.com/linnoff88-dev/ui-sem-cara-de-ia` | ê°Å¸Â§Â  vocêÂª |
| 2 | Conferir que funciona | `python3 kit/testes/run.py` | ê¢Å¡â¢ê¯Â¸Â script |
| 3 | Verificar o projeto | `python3 kit/checar_ui.py <pasta>` | ê¢Å¡â¢ê¯Â¸Â script |
| 4 | Gerar o pedido | `python3 kit/checar_ui.py <pasta> --pedido > pedido.txt` | ê¢Å¡â¢ê¯Â¸Â script |
| 5 | Corrigir | Cole `pedido.txt` no Claude Code ou no Codex | ê°Å¸Â¤â sua IA |
| 6 | Olhar a tela | Teste no celular e sêÂ³ com o teclado | ê°Å¸Â§Â  vocêÂª |
| 7 | Verificar de novo | `python3 kit/checar_ui.py <pasta>` | ê¢Å¡â¢ê¯Â¸Â script |

## Veja tambêÂ©m

[Kit Design com IA](https://github.com/linnoff88-dev/kit-design-ia): skills para definir a direêÂ§êÂ£o visual. Este kit confere o resultado no cêÂ³digo.

## LicenêÂ§a

MIT para o cêÂ³digo e os textos deste kit. As bibliotecas citadas têÂªm licenêÂ§as prêÂ³prias, listadas em `kit/bibliotecas.json`. Este kit êÂ© independente e nêÂ£o tem vêÂ­nculo com elas.

GrêÂ¡tis no [ARCKHÉ AI](https://ARCKHÉ AI).

---

<div align="center">
  <img src="capa/logo.svg" alt="Arckhé AI" height="32" />
  <p><strong>Arckhé AI</strong></p>
</div>