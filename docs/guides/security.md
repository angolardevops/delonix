# Segurança

O Delonix é **seguro por omissão** — não tens de pedir o endurecimento, ele já
está ligado. Esta página mostra o que está activo e como o ajustar.

## O que está activo por omissão

| Defesa | Por omissão |
|---|---|
| **User namespace** | activo em `run` de imagens sem `--network`/`--pod` (root do container ≠ root do host) |
| **Seccomp** | allowlist *default-deny* (estilo Docker); `clone3` → ENOSYS para bloquear escape via userns |
| **`NO_NEW_PRIVS`** | sempre (impede re-escalada por setuid) |
| **Capabilities** | as perigosas (`SYS_ADMIN`, `SYS_MODULE`, `SYS_PTRACE`, `BPF`, …) ficam de fora |
| **`/sys`** | só-leitura; **`/proc`** mascarado (`kcore`, `sysrq-trigger`, …) |
| **device cgroup** | eBPF nega dispositivos; `--device` de **bloco** é recusado em código |
| **`--sysctl`** | só sysctls *namespaced* (rede, IPC) — os globais do host são recusados |

## Ajustar

```bash
delonix run --cap-drop ALL --cap-add NET_BIND_SERVICE minha-app
delonix run --read-only minha-app                 # rootfs só-leitura
delonix run --security-opt seccomp=unconfined app  # desliga o seccomp (confiável)
delonix run --no-userns app                        # desliga o user namespace
delonix run --apparmor delonix-default app         # perfil AppArmor (se disponível)
```

## Segredos

```bash
delonix run --secret api-key=/host/secret.txt app   # em /run/secrets/api-key (tmpfs), fora do ambiente
```

## Assinatura e CVE

```bash
delonix verify registry/app:1 --key cosign.pub      # cosign/sigstore (ECDSA P-256)
delonix pull registry/app:1 --verify cosign.pub     # puxa pelo digest verificado
delonix scan app:1 --fail-on high                   # vulnerabilidades
```

## Detecção em runtime (tipo Falco)

```bash
delonix run --detect alpine ...      # regista (sem bloquear) os syscalls negados
sudo dmesg | grep 'type=1326'        # auditoria do kernel (seccomp LOG)
```

## TLS/mTLS e audit

A API REST suporta **TLS** e **mTLS** (`delonix serve --tls-cert ... --client-ca ...`).
Todas as acções mutáveis ficam num **audit log** append-only (`<root>/audit.log`, 0600).

```bash
delonix audit              # ver o registo de auditoria
```

Para o modelo de ameaça completo, vê [Conceitos → Segurança](../concepts/security.md).
