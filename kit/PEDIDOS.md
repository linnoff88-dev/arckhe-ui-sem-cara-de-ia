# Pedidos prontos

Cole no Claude Code ou no Codex, dentro do seu projeto. Troque o que está entre colchetes.

## 1. Antes de construir: dar identidade

```text
Vou construir [o que é] para [quem usa]. Minha marca: cor [cor], fonte de títulos [fonte ou "sugira 3"],
cantos [firmes, médios ou redondos].
Use shadcn/ui como base e aplique essas escolhas no tema antes de criar qualquer tela.
Instale pelo caminho oficial, com o código dentro do projeto. Se faltar algo da marca, pergunte.
```

## 2. Comportamento: não reinventar peça difícil

```text
Não construa do zero aviso, gaveta nem menu de comandos.
Use Sonner para avisos, Vaul para gavetas e cmdk para o menu de comandos, só onde a tela precisar.
Depois teste: vários avisos seguidos, gaveta arrastada no celular e o menu usado só com o teclado.
Mostre o que testou e o que não conseguiu testar.
```

## 3. Página: um destaque só

```text
Escolha um único destaque visual nesta página e justifique a escolha em uma frase.
Todo o resto fica parado. Respeite quem pediu menos movimento no sistema (prefers-reduced-motion).
```

## 4. Depois de pronto: corrigir o que o verificador achou

Baixe o kit numa pasta separada do projeto e, dentro da pasta do kit, rode:

```bash
python3 kit/checar_ui.py /caminho/do/seu/projeto --pedido
```

Cole o texto gerado na sua IA. Ele manda conferir cada item antes de mudar, porque o verificador lê o código e não vê a tela.
