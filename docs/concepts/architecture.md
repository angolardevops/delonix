# Arquitectura

## Sem daemon, um único binário

Não há `delonixd`. Cada `delonix run` é um processo normal que faz `clone(2)`
com os *namespaces* pedidos e torna-se o init do container. Quando o container
corre em segundo plano (`-d`), o processo daemoniza-se e o estado fica num
**store** em ficheiros (`/var/lib/delonix`, ou `~/.local/share/delonix` em
rootless). Qualquer `delonix` posterior lê esse store — é assim que a CLU, a API
REST e o painel web ficam **sincronizados** sem um processo central.

```
delonix run ──clone(NEWPID|NEWNS|NEWNET|NEWUSER…)──▶ init do container
     │                                                    │
     └── escreve estado em <root>/containers/<id>.json ◀──┘
            ▲                         ▲
     delonix ps / serve ui / api  (lêem o mesmo store)
```

Tudo vive **num executável estático** (~4,5 MB, musl): a CLI, a API REST, o
servidor MCP, o servidor CRI e o painel web (HTML embebido por `include_str!`).

## As peças (internamente)

O código está organizado em *crates* Rust, mas o produto é **um binário**:

| Crate | Papel |
|---|---|
| `delonix-core` | tipos partilhados, estado, store, audit |
| `delonix-runtime` | clone/namespaces, pivot_root, cgroups, seccomp, caps, PTY |
| `delonix-image` | imagens OCI, overlay/CAS, build, push/pull, assinatura |
| `delonix-net` | bridge/veth/netns, NAT, firewall (nftables), LB |
| `delonix-volume` | volumes nomeados e binds |
| `delonix-api` | API REST + métricas + **painel web** + gateway OpenAI |
| `delonix-orchestrator` | stacks, réplicas, autoscale |
| `delonix-scan` | SBOM + CVE |
| `delonix-mcp` | servidor MCP (agentes de IA) |
| `delonix-ingress` | proxy L7 |
| `delonix-cri` | servidor CRI (gRPC) para o Kubernetes |
| `delonix-cli` | a linha de comandos que liga tudo |

## Conformidade

- **OCI image-spec**: as imagens do Delonix correm no Docker e vice-versa.
- **OCI runtime-spec**: `oci-export` gera um *bundle* que o `runc` corre.
- **CRI v1**: o kubelet/`crictl` usam o Delonix como runtime (ciclo de vida + imagens).

Vê também [Protecção do host](host-protection.md) e [Segurança](security.md).
