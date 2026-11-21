# UI sem cara de IA

<div align="center">
  <img src="capa/logo.svg" alt="Arckhé AI" height="48" />
  <p><strong>Arckhé AI</strong></p>
</div>


[![UI sem cara de IA](guia/assets/banner.jpg)](https://inematds.github.io/ui-sem-cara-de-ia/guia/)

**ðŸ‡§ðŸ‡· [PortuguÃªs](README.md) Â· ðŸ‡ºðŸ‡¸ [English](README.en.md) Â· ðŸ‡ªðŸ‡¸ [EspaÃ±ol](README.es.md)**

## O que Ã©

UI sem cara de IA Ã© um kit gratuito para quem cria sites e aplicativos com Claude Code ou Codex. Ele traz um verificador que lÃª o seu projeto e aponta o que entrega o trabalho automÃ¡tico: cor e cantos de fÃ¡brica, aviso feito Ã  mÃ£o, botÃ£o que o teclado nÃ£o alcanÃ§a e excesso de efeitos. Depois, ele escreve o pedido de correÃ§Ã£o para vocÃª colar na sua IA. Precisa de Python 3 para rodar. NÃ£o instala nada no seu projeto e nÃ£o altera nenhum arquivo.

## ðŸ“– Guia de uso

Guia completo: **https://inematds.github.io/ui-sem-cara-de-ia/guia/**

[ðŸŽ¬ VÃ­deo: veja o kit em aÃ§Ã£o](https://www.youtube.com/watch?v=blXnqoGoltM)

## PeÃ§a para a sua IA analisar

```text
Baixe o kit https://github.com/inematds/ui-sem-cara-de-ia numa pasta temporÃ¡ria, fora do meu projeto.
Leia o README e rode o verificador kit/checar_ui.py apontando para a pasta do meu projeto.
Se faltar Python 3.9 ou mais novo, me avise antes de instalar qualquer coisa.
Confira cada alerta no cÃ³digo e me diga, em portuguÃªs simples, quais sÃ£o reais, quais sÃ£o falsos
e por onde vale comeÃ§ar. NÃ£o mude nenhum arquivo do projeto antes do meu sim.
```

---

## InstalaÃ§Ã£o tÃ©cnica

Requisito: Python 3.9 ou mais novo. O kit usa sÃ³ a biblioteca padrÃ£o.

```bash
git clone https://github.com/inematds/ui-sem-cara-de-ia
cd ui-sem-cara-de-ia
python3 kit/testes/run.py                      # 119 testes, sem rede
python3 kit/checar_ui.py exemplo/antes         # 8 alertas
python3 kit/checar_ui.py exemplo/depois        # nenhum alerta
python3 kit/checar_ui.py /caminho/do/projeto
python3 kit/checar_ui.py /caminho/do/projeto --pedido > pedido.txt
```

Substitua `/caminho/do/projeto` pela pasta real que deseja analisar. Mantenha o kit fora do seu projeto. CÃ³digos de saÃ­da: `0` sem alertas, `1` com alertas, `2` erro de uso ou nenhum arquivo de interface encontrado. Use `--json` para integrar com outras ferramentas.

### O que ele procura

| Grupo | Alerta | Como detecta |
|---|---|---|
| Identidade | Cantos de fÃ¡brica | `--radius` igual a `0.625rem` ou `0.5rem` num tema com `--primary` |
| Identidade | Cor sem marca | `--primary` igual a um padrÃ£o do shadcn/ui ou cinza em OKLCH, HSL ou hexadecimal |
| Identidade | Fonte de sempre | SÃ³ Geist ou Inter (next/font, @fontsource ou CSS), num projeto com esse tema |
| Comportamento | Aviso feito Ã  mÃ£o | Estado ou componente de toast sem biblioteca de avisos no `package.json` da pasta ou acima dela |
| Comportamento | Gaveta sem arrasto | Componente de gaveta sem eventos de toque ou ponteiro e sem biblioteca prÃ³pria |
| Comportamento | Menu sem setas | Menu de comandos sem `ArrowDown` e sem biblioteca prÃ³pria |
| Comportamento | Clique sem teclado | `div`, `span`, `p`, `li`, `tr`, `td`, `img`, seÃ§Ãµes, tÃ­tulos, `motion.*` ou `a` sem `href`, com clique (React, Vue ou Svelte) e sem `tabIndex` que permita foco |
| Excesso | Muitos destaques | Mais de um efeito conhecido em pÃ¡gina de rota, `App` ou HTML, olhando dois nÃ­veis de importaÃ§Ã£o |

SÃ£o alertas de leitura de cÃ³digo. O verificador nÃ£o abre a tela, nÃ£o mede contraste e nÃ£o julga se o design Ã© bom. A regra de clique verifica se o elemento recebe foco; nÃ£o confirma que Enter ou EspaÃ§o executam a aÃ§Ã£o. Um alerta pode ser falso, e uma tela sem alertas ainda pode estar ruim.

Limites: ignora arquivos de teste, comentÃ¡rios, `components/ui`, pastas geradas e, em `public/`, tudo que nÃ£o seja HTML. Elementos com `{...props}` nÃ£o sÃ£o acusados, porque as propriedades podem trazer o foco. `svg`, `i`, `label`, `ul`, `nav` e componentes prÃ³prios com clique nÃ£o sÃ£o analisados. Efeitos fora da lista interna nÃ£o sÃ£o contados. Cliques ligados por `addEventListener` nÃ£o sÃ£o vistos. Identidade sÃ³ Ã© analisada quando o projeto usa um tema com `--primary` e `--radius`, como o do shadcn/ui; cores direto em classes do Tailwind, temas dentro de `<style>` e fontes carregadas por link nÃ£o entram. Rode na raiz do projeto.

Cobertura: ele sÃ³ lÃª telas em HTML, JSX, TSX, Vue, Svelte, Astro e MDX. Sem nenhuma delas, sai com cÃ³digo `2` e nÃ£o aprova. Se encontrar telas em PHP, EJS, Blade, Pug, Twig ou parecidas ao lado das que sabe ler, avisa que o resultado nÃ£o vale para elas.

### Arquivos

| Caminho | Para quÃª |
|---|---|
| `kit/checar_ui.py` | Verificador |
| `kit/medir_pastas.py` | Total de vÃ¡rios projetos, sem nomes |
| `kit/PEDIDOS.md` | Pedidos prontos para a IA |
| `kit/bibliotecas.json` | Bibliotecas conferidas, com site e licenÃ§a |
| `kit/skill/ui-sem-cara-de-ia/` | Skill para Claude Code: copie para `.claude/skills/` |
| `exemplo/antes`, `exemplo/depois` | Mesmo cadastro, com e sem os problemas |
| `FATOS.md` | Fontes e mediÃ§Ãµes |

## O processo, do inÃ­cio ao fim

| # | Passo | Comando | Quem faz |
|---|---|---|---|
| 1 | Baixar o kit | `git clone https://github.com/inematds/ui-sem-cara-de-ia` | ðŸ§  vocÃª |
| 2 | Conferir que funciona | `python3 kit/testes/run.py` | âš™ï¸ script |
| 3 | Verificar o projeto | `python3 kit/checar_ui.py <pasta>` | âš™ï¸ script |
| 4 | Gerar o pedido | `python3 kit/checar_ui.py <pasta> --pedido > pedido.txt` | âš™ï¸ script |
| 5 | Corrigir | Cole `pedido.txt` no Claude Code ou no Codex | ðŸ¤– sua IA |
| 6 | Olhar a tela | Teste no celular e sÃ³ com o teclado | ðŸ§  vocÃª |
| 7 | Verificar de novo | `python3 kit/checar_ui.py <pasta>` | âš™ï¸ script |

## Veja tambÃ©m

[Kit Design com IA](https://github.com/inematds/kit-design-ia): skills para definir a direÃ§Ã£o visual. Este kit confere o resultado no cÃ³digo.

## LicenÃ§a

MIT para o cÃ³digo e os textos deste kit. As bibliotecas citadas tÃªm licenÃ§as prÃ³prias, listadas em `kit/bibliotecas.json`. Este kit Ã© independente e nÃ£o tem vÃ­nculo com elas.

GrÃ¡tis no [INEMA.CLUB](https://inema.club).

---

<div align="center">
  <img src="capa/logo.svg" alt="Arckhé AI" height="32" />
  <p><strong>Arckhé AI</strong></p>
</div>