# Fatos e medições

Tudo conferido em 18/11/2026. O que não está aqui não deve ser afirmado no guia, no vídeo nem nos posts.

## Medições do verificador (versão 1.0.4)

| O que foi medido | Resultado | Como repetir |
|---|---|---|
| Testes do kit | 119 de 119 passaram | `python3 kit/testes/run.py` |
| Exemplo com problemas | 8 alertas | `python3 kit/checar_ui.py exemplo/antes` |
| Exemplo corrigido | 0 alertas | `python3 kit/checar_ui.py exemplo/depois` |
| 34 pastas de projetos React + Tailwind das nossas contas | 24 com algum alerta, 137 alertas no total | `python3 kit/medir_pastas.py <pasta> --dono "<contas>"` |
| Nessas pastas, comportamento | 21 pastas com alerta; 103 arquivos com clique fora do alcance do teclado; 6 arquivos com aviso feito à mão | mesmo comando |
| Nessas pastas, identidade | 11 pastas com alerta; 10 raios, 9 cores e 9 fontes de fábrica | mesmo comando |
| Nessas pastas, excesso | 0 alertas | mesmo comando |
| `shadcn-ui/taxonomy` (298a885) | 2 alertas de identidade, 0 de comportamento | clone público + `checar_ui.py` |
| `shadcn-ui/next-template` (d117bd0) | 2 alertas de identidade, 0 de comportamento | clone público + `checar_ui.py` |
| `vercel/ai-chatbot` (a8989b5) | 2 alertas de identidade, 1 de comportamento | clone público + `checar_ui.py` |

### Limites destas medições

- Algumas das 34 pastas podem ser versões do mesmo projeto. Não sabemos quantas foram geradas por IA.
- Alerta não é defeito confirmado. Conferimos uma amostra à mão e uma revisão independente apontou falsos alarmes e casos perdidos, que viraram testes. Não medimos a taxa de acerto.
- Não testamos o antes e depois com pessoas nem medimos conversão.
- Os exemplos `antes` e `depois` foram escritos para demonstrar as regras e não rodam sem instalar as dependências.

## Valores padrão do shadcn/ui

Lidos no repositório oficial `shadcn-ui/ui`: `--radius: 0.625rem` e `--primary: oklch(0.205 0 0)` no registro atual; `--radius: 0.5rem` e as cores primárias de zinc, slate, stone, gray e neutral em `_legacy-base-colors.ts`; e Geist como fonte no modelo `next-app`.

## Bibliotecas

Site, repositório e licença de cada uma estão em `kit/bibliotecas.json`. O que cada site diz:

- Beautiful UI: "copy-paste components for chat agents, thinking states, human-in-the-loop approvals"; o site informa licença MIT e "Built by Turbo".
- Aceternity UI: o site informa "200+ copy-paste components, blocks, and landing page templates" e tem área paga.
- 21st.dev: o site informa "12,000+ hand-crafted React and Tailwind CSS components, templates, and shadcn themes" e tem planos pagos.

## Não confirmado, por isso fora do kit

- Rare UI: o site não respondeu na conferência.
- "Mais de 150 componentes" da Magic UI: o número não apareceu nas páginas consultadas.
