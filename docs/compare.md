# Docker · Podman · Delonix

Os três correm containers OCI e partilham grande parte da linha de comandos. As
diferenças estão na **arquitectura**, na **segurança por omissão** e nas
**funcionalidades de plataforma**. Esta página é a fotografia honesta — incluindo
o que o Delonix ainda **não** faz.

## Resumo

| | **Docker** | **Podman** | **Delonix** |
|---|---|---|---|
| Arquitectura | *daemon* (`dockerd`) como root | sem daemon (fork/exec) | **sem daemon**, **um único binário** |
| Distribuição | pacote + daemon + CLI | múltiplos binários (podman, conmon, …) | **1 binário estático** (~4,5 MB) |
| Escrito em | Go | Go | **Rust** |
| Rootless | sim (com setup) | sim (nativo) | **sim** (XDG store + slirp4netns) |
| *User namespace* por omissão | não | não | **sim** (em `run` sem `--network`/`--pod`) |

## Imagens e build

| | Docker | Podman | Delonix |
|---|---|---|---|
| Pull/push OCI | ✅ | ✅ | ✅ |
| Build (Dockerfile) | ✅ BuildKit | ✅ Buildah | ✅ (`Delonixfile`/`Dockerfile`, multi-stage, cache) |
| Imagens correm no Docker | — | ✅ | ✅ (conformidade OCI image-spec) |
| Assinatura de imagens | Notary/cosign (externo) | sigstore | ✅ **cosign nativo** (`pull --verify`, anti-replay) |
| Scan de CVE | Scout (externo) | externo | ✅ **nativo** (`scan`, feed `--update`) |

## Execução e ciclo de vida

| | Docker | Podman | Delonix |
|---|---|---|---|
| `run`/`exec -it`/`logs`/`cp` | ✅ | ✅ | ✅ |
| Shell rápida tipo `ssh` | — | — | ✅ `delonix ssh <container>` |
| `pause`/`unpause` (freezer) | ✅ | ✅ | ✅ |
| `commit`/`diff`/`top`/`stats` | ✅ | ✅ | ✅ |
| Healthcheck | ✅ | ✅ | ✅ |
| Restart policy → systemd | ✅ | ✅ (`generate systemd`) | ✅ (`generate systemd`) |

## Rede

| | Docker | Podman | Delonix |
|---|---|---|---|
| Bridge + NAT + publicar portas | ✅ | ✅ | ✅ (nftables nativo) |
| Subnet por omissão | `172.17/16` | `10.88/16` | **`/16` auto-detectado livre** (sem colidir) |
| Redes de utilizador isoladas | ✅ | ✅ | ✅ |
| IP fixo no `run` | ✅ `--ip` | ✅ `--ip` | ✅ `--ip` (validado na subnet) |
| Ligar/desligar redes a quente (multi-homing) | ✅ `network connect/disconnect` | ✅ | ✅ `network connect/disconnect` (`eth<n>`, com `--ip`) |
| Micro-segmentação (policy entre containers) | parcial | parcial | ✅ `network policy deny/allow` |
| DNS interno + LB L4 + Ingress L7 | parcial | parcial | ✅ |
| Limite de banda por container | — | — | ✅ `--net-bps`/`--net-burst` (`tc`) |

## Orquestração

| | Docker | Podman | Delonix |
|---|---|---|---|
| Compose | `docker compose` | `podman compose`/play | ✅ `service`/`up`/`down`/`scale` |
| Pods | — | ✅ | ✅ (`pod`, rede partilhada) |
| Gerar manifests k8s | — | ✅ `generate kube` | ✅ `kube generate` |
| **CRI** (kubelet usa-o como runtime) | via cri-dockerd | — | ✅ ciclo de vida + imagens (¹) |
| Autoscale local | — | — | ✅ `autoscale` |

## Plataforma — o que distingue o Delonix

| | Docker | Podman | Delonix |
|---|---|---|---|
| **Protecção do host** (tecto agregado CPU/mem/PIDs/I-O) | — | — | ✅ `delonix.slice` + admissão |
| **Governador térmico** (baixa CPU ao sobreaquecer) | — | — | ✅ `delonix thermal` |
| **Painel web** embebido | Desktop (externo) | Desktop/Cockpit (externo) | ✅ `delonix serve ui` (no binário, offline) |
| **Gateway de IA** OpenAI + Ollama | — | — | ✅ `delonix llm` |
| **Servidor MCP** para agentes de IA | — | — | ✅ `delonix mcp` |
| **Host remoto** por SSH | ✅ `DOCKER_HOST=ssh://` | ✅ `--url ssh://` | ✅ `--host ssh://` |
| API REST + métricas Prometheus | API do daemon | API REST | ✅ `delonix serve` (+ TLS/mTLS) |
| Audit log | via daemon | — | ✅ append-only 0600 |

## Segurança por omissão

| | Docker | Podman | Delonix |
|---|---|---|---|
| Seccomp | allowlist (perfil) | allowlist | ✅ allowlist default-deny |
| `NO_NEW_PRIVS` | com perfil | com perfil | ✅ sempre |
| Capabilities reduzidas | sim | sim | ✅ (perigosas fora; `--cap-add`) |
| `clone3` filtrado (bloqueio de escape userns) | ✅ | ✅ | ✅ (→ ENOSYS, glibc cai no `clone`) |
| `/sys` RO · `/proc` mascarado | ✅ | ✅ | ✅ |
| Segredos fora do ambiente | ✅ | ✅ | ✅ (`--secret`, tmpfs) |

## O que o Delonix ainda **não** faz

A honestidade faz parte da documentação:

- **CRI streaming** — o ciclo de vida de pods/containers e o `ImageService` são reais
  e verificados com `crictl`, mas `exec`/`attach`/`port-forward` e as estatísticas
  por-pod ainda devolvem `UNIMPLEMENTED` (¹). `kubectl exec`/`logs -f`/`port-forward`
  não funcionam sobre o Delonix por agora.
- **HA** — réplica activo-activo por armazenamento partilhado funciona; falta o
  *kvstore* replicado para resolver conflitos de escrita entre nós.
- **Rootless** — `-p` (port-forwarding) já funciona (via slirp4netns); falta `--pod` sem root.

---

> Em resumo: se já sabes Docker ou Podman, já sabes Delonix. Ganhas um único
> binário, protecção do host, IA nativa e um painel web; aceitas que algumas
> arestas (CRI streaming, HA) ainda estão a ser limadas.
