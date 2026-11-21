---
name: ui-sem-cara-de-ia
description: Use ao criar ou alterar interface web (tela, formulário, aviso, gaveta, menu de comandos, landing page). Escolhe a peça pronta certa, aplica a identidade da marca e confere o comportamento antes de dizer que terminou.
---

# Interface sem cara de IA

## Antes de escrever código

1. Leia `package.json`. Se o projeto já usa uma biblioteca para a tarefa, continue com ela.
2. Procure a cor, a fonte e o formato dos cantos da marca. Se não houver, pergunte antes de escolher.

## Qual peça usar

| Preciso de | Use |
|---|---|
| Botão, campo, janela, abas, menu | shadcn/ui, Base UI ou Radix, conforme o projeto |
| Aviso na tela (toast) | Sonner |
| Gaveta arrastável no celular | Vaul |
| Menu de comandos com busca | cmdk |
| Número que muda com animação | NumberFlow |
| Peças de produto com agente: streaming, aprovação | Beautiful UI |
| Um destaque visual em landing page | Magic UI ou Aceternity UI |

Instale pelo caminho oficial e deixe o código no projeto quando a biblioteca permitir. Não escreva uma cópia parecida.
Antes de usar peça de marketplace ou de plano pago, confira a licença.

## Regras

- Troque cor, fonte e cantos antes de criar telas. Valor de fábrica não fica por descuido.
- Uma página tem um destaque visual. O resto fica parado.
- Elemento clicável é `button` ou link, com foco visível.

## Antes de dizer que terminou

1. Se tiver o kit numa pasta separada, rode `python3 <pasta-do-kit>/kit/checar_ui.py <pasta-do-projeto>` e confira cada alerta. Ele pode errar.
2. Abra a tela. Teste em largura de celular e só com o teclado.
3. Diga o que testou e o que não conseguiu testar.
