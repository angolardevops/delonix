# Painel web

O Delonix traz um **painel web embebido** (estilo Portainer) — dentro do próprio
binário, **offline**, sem Node nem CDN. Gere containers, imagens, redes e stacks
no browser, **sincronizado com a CLI**.

## Arrancar

```bash
sudo delonix serve ui                              # http://127.0.0.1:9444
sudo delonix serve ui --addr 0.0.0.0:9444 --token SEGREDO   # exposto, com Bearer
```

Abre `http://127.0.0.1:9444` no browser.

## O que faz

- **Painel** — visão geral: containers a correr/total, imagens, CPU/carga do host,
  memória e PIDs da `delonix.slice`.
- **Containers** — iniciar, parar, reiniciar, remover; ver **logs**; **consola**
  (executa comandos dentro do container a partir do browser).
- **Imagens** — listar e remover.
- **Redes** — bridges, subnets, gateways.
- **Stacks** — aplicações multi-container, com a contagem de réplicas a correr.

## Sincronização

O painel lê o **mesmo store** que a CLI (`$DELONIX_ROOT`) e **delega as mutações
no próprio binário `delonix`**. Resultado: o que fazes na CLI aparece no painel e
vice-versa, sem estado duplicado.

## Segurança

- Por omissão escuta em **loopback** (`127.0.0.1`).
- Para expor (`--addr 0.0.0.0:...`), usa **`--token`** (Bearer, comparado em tempo
  constante). Em produção, põe-o atrás de um proxy TLS ou usa a API REST com mTLS.

Próximo: [Plataforma de IA](ai-llm.md) · [Host remoto](remote.md).
