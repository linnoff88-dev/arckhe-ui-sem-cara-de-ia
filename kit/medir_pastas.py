#!/usr/bin/env python3
"""medir_pastas.py: roda o checar_ui em cada projeto React + Tailwind de uma pasta e mostra só o total.

Não imprime nome de projeto nem de arquivo, então o resultado pode ser mostrado em público.
Uso: python3 kit/medir_pastas.py ~/projetos [--dono "minha-conta|outra-conta"]
Com --dono, só entram as pastas cujo git remote origin contém um desses nomes.
"""
import argparse
import collections
import json
import re
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import checar_ui as c  # noqa: E402


def react_tailwind(pasta: Path) -> bool:
    try:
        d = json.loads((pasta / "package.json").read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return False
    deps = {**d.get("dependencies", {}), **d.get("devDependencies", {})}
    return "react" in deps and "tailwindcss" in deps


def origem(pasta: Path) -> str:
    r = subprocess.run(["git", "-C", str(pasta), "remote", "get-url", "origin"],
                       capture_output=True, text=True, check=False)
    return r.stdout.strip()


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("pasta")
    ap.add_argument("--dono", help="regex com as contas aceitas no git remote")
    a = ap.parse_args()
    raiz = Path(a.pasta).expanduser()
    if not raiz.is_dir():
        print(f"Pasta não encontrada: {raiz}", file=sys.stderr)
        return 2
    regras, grupos = collections.Counter(), collections.Counter()
    pastas = com_sinal = 0
    for p in sorted(raiz.iterdir()):
        if not p.is_dir() or not react_tailwind(p):
            continue
        if a.dono and not re.search(a.dono, origem(p)):
            continue
        if c.eh_copia_do_kit(p):
            continue
        r = c.analisar(p)
        if not r["telas_lidas"]:
            continue
        pastas += 1
        com_sinal += bool(r["total"])
        regras.update(x["regra"] for x in r["achados"])
        grupos.update(g for g, n in r["grupos"].items() if n)
    print(json.dumps({"pastas": pastas, "com_sinal": com_sinal, "sinais": sum(regras.values()),
                      "pastas_por_grupo": dict(grupos), "sinais_por_regra": dict(regras)},
                     ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
