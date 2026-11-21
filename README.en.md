# UI Without the AI Look

[![UI Without the AI Look](guia/assets/banner-en.jpg)](https://inematds.github.io/ui-sem-cara-de-ia/guia/en/)

**🇧🇷 [Português](README.md) · 🇺🇸 [English](README.en.md) · 🇪🇸 [Español](README.es.md)**

## What it is

UI Without the AI Look is a free toolkit for people who build websites and apps with Claude Code or Codex. It includes a checker that reads your project and points out signs of automated work: default colors and rounded corners, hand-built alerts, buttons the keyboard can’t reach, and too many effects. Then it writes a fix request for you to paste into your AI. You need Python 3 to run it. It doesn’t install anything in your project or change any files.

## 📖 User guide

Full guide: **https://inematds.github.io/ui-sem-cara-de-ia/guia/en/**

[🎬 Video: see the kit in action](https://www.youtube.com/watch?v=blXnqoGoltM)

## Ask your AI to analyze it

```text
Download the toolkit from https://github.com/inematds/ui-sem-cara-de-ia into a temporary folder outside my project.
Read the README and run the checker kit/checar_ui.py on my project folder.
If Python 3.9 or newer is missing, tell me before installing anything.
Check each warning in the code and tell me in simple English which ones are real, which ones are false
alarms, and where it makes sense to start. Don’t change any project files before I say yes.
```

---

## Technical installation

Requirement: Python 3.9 or newer. The toolkit uses only the standard library.

```bash
git clone https://github.com/inematds/ui-sem-cara-de-ia
cd ui-sem-cara-de-ia
python3 kit/testes/run.py                      # 119 tests, no network
python3 kit/checar_ui.py exemplo/antes         # 8 warnings
python3 kit/checar_ui.py exemplo/depois        # no warnings
python3 kit/checar_ui.py /caminho/do/projeto
python3 kit/checar_ui.py /caminho/do/projeto --pedido > pedido.txt
```

Replace `/caminho/do/projeto` with the actual folder you want to analyze. Keep the toolkit outside your project. Exit codes: `0` no warnings, `1` warnings found, `2` usage error or no interface files found. Use `--json` to connect it to other tools.

### What it checks

| Group | Warning | How it detects it |
|---|---|---|
| Identity | Default rounded corners | `--radius` equal to `0.625rem` or `0.5rem` in a theme with `--primary` |
| Identity | Unbranded color | `--primary` equal to a shadcn/ui preset or gray in OKLCH, HSL, or hexadecimal |
| Identity | Usual font | Only Geist or Inter (next/font, @fontsource, or CSS) in a project with this theme |
| Behavior | Hand-built alert | Toast state or component without an alert library in the folder’s `package.json` or above it |
| Behavior | Drawer without dragging | Drawer component without touch or pointer events and without its own library |
| Behavior | Menu without arrow keys | Command menu without `ArrowDown` and without its own library |
| Behavior | Click without keyboard access | `div`, `span`, `p`, `li`, `tr`, `td`, `img`, sections, headings, `motion.*`, or `a` without `href`, with a click handler (React, Vue, or Svelte) and no `tabIndex` that allows focus |
| Excess | Too many highlights | More than one known effect on a route page, `App`, or HTML, checking two import levels |

These are code-reading warnings. The checker doesn’t open the screen, measure contrast, or judge whether the design is good. The click rule checks whether an element can receive focus; it doesn’t confirm that Enter or Space runs the action. A warning can be false, and a screen with no warnings can still be poorly designed.

Limits: it ignores test files, comments, `components/ui`, generated folders, and everything in `public/` except HTML. Elements with `{...props}` aren’t flagged because those properties may add focus. `svg`, `i`, `label`, `ul`, `nav`, and custom components with click handlers aren’t analyzed. Effects outside the built-in list aren’t counted. Clicks connected through `addEventListener` aren’t detected. Identity is checked only when the project uses a theme with `--primary` and `--radius`, such as shadcn/ui. Colors written directly in Tailwind classes, themes inside `<style>` tags, and fonts loaded by link aren’t included. Run it from the project root.

Coverage: it reads screens in HTML, JSX, TSX, Vue, Svelte, Astro, and MDX only. If it finds none, it exits with code `2` and doesn’t approve the project. If it finds screens in PHP, EJS, Blade, Pug, Twig, or similar files alongside the ones it can read, it warns that the results don’t cover those files.

### Files

| Path | What it’s for |
|---|---|
| `kit/checar_ui.py` | Checker |
| `kit/medir_pastas.py` | Total across several projects, without names |
| `kit/PEDIDOS.md` | Ready-to-use requests for AI |
| `kit/bibliotecas.json` | Reviewed libraries, with websites and licenses |
| `kit/skill/ui-sem-cara-de-ia/` | Skill for Claude Code: copy it to `.claude/skills/` |
| `exemplo/antes`, `exemplo/depois` | The same form with and without the problems |
| `FATOS.md` | Sources and measurements |

## The process, from start to finish

| # | Step | Command | Who does it |
|---|---|---|---|
| 1 | Download the toolkit | `git clone https://github.com/inematds/ui-sem-cara-de-ia` | 🧠 you |
| 2 | Check that it works | `python3 kit/testes/run.py` | ⚙️ script |
| 3 | Check the project | `python3 kit/checar_ui.py <pasta>` | ⚙️ script |
| 4 | Create the request | `python3 kit/checar_ui.py <pasta> --pedido > pedido.txt` | ⚙️ script |
| 5 | Make fixes | Paste `pedido.txt` into Claude Code or Codex | 🤖 your AI |
| 6 | Check the screen | Test it on a phone and using only the keyboard | 🧠 you |
| 7 | Run the check again | `python3 kit/checar_ui.py <pasta>` | ⚙️ script |

## See also

[AI Design Kit](https://github.com/inematds/kit-design-ia): skills for setting the visual direction. This toolkit checks the result in the code.

## License

MIT for the code and text in this toolkit. The libraries mentioned have their own licenses, listed in `kit/bibliotecas.json`. This toolkit is independent and has no connection to them.

Free at [INEMA.CLUB](https://inema.club).
