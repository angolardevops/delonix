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

A **Engine Console** (tema escuro, denso, estilo enterprise) recolhe **todo o
ecossistema** do Engine num único snapshot (`/api/state`) e actualiza-se sozinha:

- **Painel** — host (SO, kernel, CPU, carga, memória, swap, disco, PIDs, uptime),
  containers a correr/total, imagens, eventos recentes.
- **Containers** — iniciar, parar, reiniciar, pausar, remover; estado, imagem,
  portas, rede, stack, memória (do cgroup); ver **logs** e **consola**.
- **Imagens** — repositório, tag, em-uso-por, dangling.
- **Redes** — bridges, subnets, gateways, nº de containers.
- **Volumes** — armazenamento persistente.
- **Stacks** — aplicações multi-container (serviços a correr / total).
- **Topologia AO VIVO** — mapa dos containers reais segmentado por rede, com a
  **animação de tráfego real** (das métricas de rede) e as **ligações externas**:
  quando alguém de fora acede a um container, aparece o **IP de origem** a fluir
  para ele. Métricas reais por container: CPU% (cgroup) e rede (veth).
- **Eventos** — o `audit.log` do Engine (acções mutáveis).
- **Idioma** — selector **PT/EN** no topo (a escolha fica guardada).

### Segurança & operações (na consola)

- **Risco** — containers com posturas perigosas (seccomp off, capabilities
  perigosas, sem userns, dispositivos do host) ficam a **vermelho** com os motivos.
- **Defesa em profundidade** — no detalhe de cada container: seccomp, user
  namespace, **filtro eBPF de dispositivos**, rootfs RO, capabilities.
- **CVE** — botão por imagem que corre o `scan` e mostra CRITICAL/HIGH/MEDIUM/LOW.
- **Redes** — criar/remover redes a partir da UI.
- **Novo projecto** — colar um **Delonixfile** + **delonix-stack.yaml**, construir
  e executar a stack sem ir à CLI.
- **Volumes** — criar/remover, incluindo volumes **NFS/TrueNAS** (`--driver nfs
  --device servidor:/export`; requer `nfs-common`).
- **Reconfigurar recursos** — mudar memória/CPU/política de reinício de um
  container ao vivo (sem recriar).
- **Monitor** (`sudo delonix monitor`) — serviço do *engine* que mostra ao vivo o
  que cada container acede para fora e quem o acede de fora (conntrack/netfilter).
  Isolado: nenhum container consegue ver isto (sem `CAP_NET_ADMIN`, netns próprio).

!!! note "Ligações externas ao vivo"
    O mapa de ligações externas usa o `conntrack` (netlink). Instala-o com
    `sudo apt install conntrack` e corre o painel como root (`sudo delonix serve ui`).
    Sem ele, a topologia mostra à mesma os containers e o tráfego; só não traça as
    ligações externas com o IP de origem.

## Login & utilizadores internos

Por omissão a consola não tem ecrã de login (escuta em loopback). Para exigir
autenticação, arranca com `--login`:

```bash
sudo delonix serve ui --login                      # http://127.0.0.1:9444
sudo delonix serve ui --addr 0.0.0.0:9444 --login  # exposto, com login
```

- **1.º acesso (bootstrap)** — a página mostra *Criar administrador*. O primeiro
  utilizador registado é o admin.
- **Sessões** — por *cookie* (`HttpOnly`, `SameSite=Strict`, validade 12 h).
- **Palavras-passe** — guardadas com **PBKDF2-HMAC-SHA256** (600 000 iterações,
  via `ring`); nunca em claro. Ficam em `$DELONIX_ROOT/users/<nome>.json`.
- **Adicionar utilizadores** — em **Definições**, um admin autenticado cria novos
  utilizadores internos. Registar fora do bootstrap **exige sessão** (`401` sem ela).
- **Terminar sessão** — botão no topo (ou em *Definições*).
- **Automação** — com `--login`, o `--token` (Bearer) continua a funcionar para
  chamadas à API sem cookie.

!!! note "Utilizadores internos, não PAM"
    São contas **internas do Engine**, não utilizadores do sistema (PAM). Num
    binário **estático único** não é possível ligar à `libpam`, por isso o Delonix
    implementa autenticação própria (PBKDF2 + sessões) — a opção segura e sem
    dependências. Para SSO/LDAP, põe a consola atrás de um proxy autenticado.

## Sincronização

O painel lê o **mesmo store** que a CLI (`$DELONIX_ROOT`) e **delega as mutações
no próprio binário `delonix`**. Resultado: o que fazes na CLI aparece no painel e
vice-versa, sem estado duplicado.

## Segurança

- Por omissão escuta em **loopback** (`127.0.0.1`).
- Para expor (`--addr 0.0.0.0:...`), usa **`--token`** (Bearer, comparado em tempo
  constante). Em produção, põe-o atrás de um proxy TLS ou usa a API REST com mTLS.

Próximo: [Plataforma de IA](ai-llm.md) · [Host remoto](remote.md).
