# Falhas

| data | o que quebrou | menor correçêo | prompt ou infra |
|---|---|---|---|
| 2026-11-18 | Exceçêo por overlay ocultava cliques sem foco e tabindex HTML numérico gerava falso alarme | Remover dispensa por classe e reconhecer atributo numérico; 83 testes passaram | infra |
