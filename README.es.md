# UI sin cara de IA

[![UI sin cara de IA](guia/assets/banner-es.jpg)](https://inematds.github.io/ui-sem-cara-de-ia/guia/es/)

**🇧🇷 [Português](README.md) · 🇺🇸 [English](README.en.md) · 🇪🇸 [Español](README.es.md)**

## Qué es

UI sin cara de IA es un kit gratuito para quienes crean sitios web y aplicaciones con Claude Code o Codex. Incluye un verificador que lee tu proyecto y señala lo que hace que parezca hecho automáticamente: colores y bordes de fábrica, avisos hechos a mano, botones que no se pueden alcanzar con el teclado y demasiados efectos. Después, prepara una solicitud de corrección para que la pegues en tu IA. Necesita Python 3 para funcionar. No instala nada en tu proyecto ni modifica ningún archivo.

## 📖 Guía de uso

Guía completa: **https://inematds.github.io/ui-sem-cara-de-ia/guia/es/**

[🎬 Video: mira el kit en acción](https://www.youtube.com/watch?v=blXnqoGoltM)

## Pídele a tu IA que lo analice

```text
Descarga el kit https://github.com/inematds/ui-sem-cara-de-ia en una carpeta temporal, fuera de mi proyecto.
Lee el README y ejecuta el verificador kit/checar_ui.py indicando la carpeta de mi proyecto.
Si falta Python 3.9 o una versión más nueva, avísame antes de instalar cualquier cosa.
Revisa cada alerta en el código y dime, en español latinoamericano sencillo, cuáles son reales, cuáles son falsas
y por dónde conviene empezar. No cambies ningún archivo del proyecto antes de que te dé el visto bueno.
```

---

## Instalación técnica

Requisito: Python 3.9 o una versión más nueva. El kit solo usa la biblioteca estándar.

```bash
git clone https://github.com/inematds/ui-sem-cara-de-ia
cd ui-sem-cara-de-ia
python3 kit/testes/run.py                      # 119 pruebas, sin conexión
python3 kit/checar_ui.py exemplo/antes         # 8 alertas
python3 kit/checar_ui.py exemplo/depois        # ninguna alerta
python3 kit/checar_ui.py /caminho/do/projeto
python3 kit/checar_ui.py /caminho/do/projeto --pedido > pedido.txt
```

Reemplaza `/caminho/do/projeto` por la carpeta real que quieras analizar. Mantén el kit fuera de tu proyecto. Códigos de salida: `0` sin alertas, `1` con alertas, `2` error de uso o si no se encuentra ningún archivo de interfaz. Usa `--json` para integrarlo con otras herramientas.

### Qué busca

| Grupo | Alerta | Cómo lo detecta |
|---|---|---|
| Identidad | Bordes de fábrica | `--radius` igual a `0.625rem` o `0.5rem` en un tema con `--primary` |
| Identidad | Color sin identidad propia | `--primary` igual a un valor predeterminado de shadcn/ui o a un gris en OKLCH, HSL o hexadecimal |
| Identidad | La fuente de siempre | Solo Geist o Inter (next/font, @fontsource o CSS), en un proyecto con este tema |
| Comportamiento | Aviso hecho a mano | Estado o componente de toast sin una biblioteca de avisos en el `package.json` de la carpeta o de una carpeta superior |
| Comportamiento | Panel deslizable sin arrastre | Componente de panel deslizable sin eventos táctiles o de puntero y sin una biblioteca propia |
| Comportamiento | Menú sin flechas | Menú de comandos sin `ArrowDown` y sin una biblioteca propia |
| Comportamiento | Elemento que no se puede activar con el teclado | `div`, `span`, `p`, `li`, `tr`, `td`, `img`, secciones, títulos, `motion.*` o `a` sin `href`, con clic (React, Vue o Svelte) y sin un `tabIndex` que permita enfocarlo |
| Exceso | Demasiados efectos | Más de un efecto conocido en una página de ruta, `App` o HTML, revisando hasta dos niveles de importación |

Son alertas basadas en la lectura del código. El verificador no abre la pantalla, no mide el contraste ni evalúa si el diseño es bueno. La regla de clic comprueba si se puede enfocar el elemento; no confirma que Enter o Espacio ejecuten la acción. Una alerta puede ser falsa, y una pantalla sin alertas aún puede tener problemas.

Límites: ignora archivos de prueba, comentarios, `components/ui`, carpetas generadas y, en `public/`, todo lo que no sea HTML. No marca elementos con `{...props}`, porque las propiedades pueden permitir enfocarlos. No analiza `svg`, `i`, `label`, `ul`, `nav` ni componentes propios con clic. No cuenta los efectos que no están en la lista interna. No detecta los clics asociados con `addEventListener`. Solo analiza la identidad si el proyecto usa un tema con `--primary` y `--radius`, como el de shadcn/ui; no incluye colores escritos directamente en clases de Tailwind, temas dentro de `<style>` ni fuentes cargadas mediante un enlace. Ejecútalo desde la raíz del proyecto.

Cobertura: solo lee pantallas en HTML, JSX, TSX, Vue, Svelte, Astro y MDX. Si no encuentra ninguna, termina con el código `2` y no aprueba el proyecto. Si encuentra pantallas en PHP, EJS, Blade, Pug, Twig o formatos parecidos junto a las que sí sabe leer, avisa que el resultado no se aplica a ellas.

### Archivos

| Ruta | Para qué sirve |
|---|---|
| `kit/checar_ui.py` | Verificador |
| `kit/medir_pastas.py` | Total de varios proyectos, sin nombres |
| `kit/PEDIDOS.md` | Solicitudes listas para la IA |
| `kit/bibliotecas.json` | Bibliotecas revisadas, con sitio web y licencia |
| `kit/skill/ui-sem-cara-de-ia/` | Skill para Claude Code: cópiala a `.claude/skills/` |
| `exemplo/antes`, `exemplo/depois` | El mismo formulario, con y sin los problemas |
| `FATOS.md` | Fuentes y mediciones |

## El proceso, de principio a fin

| # | Paso | Comando | Quién lo hace |
|---|---|---|---|
| 1 | Descargar el kit | `git clone https://github.com/inematds/ui-sem-cara-de-ia` | 🧠 tú |
| 2 | Comprobar que funciona | `python3 kit/testes/run.py` | ⚙️ script |
| 3 | Revisar el proyecto | `python3 kit/checar_ui.py <pasta>` | ⚙️ script |
| 4 | Preparar la solicitud | `python3 kit/checar_ui.py <pasta> --pedido > pedido.txt` | ⚙️ script |
| 5 | Corregir | Pega `pedido.txt` en Claude Code o Codex | 🤖 tu IA |
| 6 | Revisar la pantalla | Pruébala en el celular y usando solo el teclado | 🧠 tú |
| 7 | Volver a revisar | `python3 kit/checar_ui.py <pasta>` | ⚙️ script |

## También puedes ver

[Kit Design con IA](https://github.com/inematds/kit-design-ia): skills para definir la dirección visual. Este kit revisa el resultado en el código.

## Licencia

MIT para el código y los textos de este kit. Las bibliotecas mencionadas tienen sus propias licencias, listadas en `kit/bibliotecas.json`. Este kit es independiente y no tiene relación con ellas.

Gratis en [INEMA.CLUB](https://inema.club).
