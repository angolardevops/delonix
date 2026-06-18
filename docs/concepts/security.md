# Modelo de segurança

O Delonix aplica **defesa em profundidade**: várias camadas independentes, todas
activas por omissão. Um container hostil tem de furar várias para escapar.

## Camadas

1. **User namespace** — o root do container mapeia para um uid não-privilegiado no
   host (base 100000 com root; o teu uid em rootless). Activo por omissão em `run`
   de imagens sem `--network`/`--pod`.
2. **Seccomp** — allowlist *default-deny* (estilo Docker). Os syscalls perigosos
   (`mount`, `ptrace`, `bpf`, `kexec`, `init_module`, `setns`, `unshare`, …) são
   negados. O `clone` é filtrado contra `CLONE_NEWUSER`; o **`clone3` devolve
   ENOSYS** para o glibc cair no `clone` filtrado (fecha o escape via userns que
   o `clone3` permitia — os seus flags vão num ponteiro e não são inspeccionáveis).
3. **`NO_NEW_PRIVS`** — sempre, antes de largar capabilities e aplicar seccomp;
   impede a re-escalada por binários setuid.
4. **Capabilities** — as perigosas ficam de fora (`SYS_ADMIN`, `SYS_MODULE`,
   `SYS_PTRACE`, `SYS_RAWIO`, `MKNOD`, `BPF`, …); ajustáveis com `--cap-add/--cap-drop`.
5. **Sistema de ficheiros** — `/` opcionalmente só-leitura (`--read-only`), `/sys`
   montado RO, `/proc` mascarado (`kcore`, `sysrq-trigger`, …), `/dev` mínimo.
6. **Dispositivos** — device cgroup eBPF; `--device` de **bloco** recusado em código
   (não confia só no eBPF best-effort).
7. **`--sysctl`** — só sysctls *namespaced* (rede/IPC); os globais do host recusados.

## Cadeia de fornecimento

- **Assinatura** cosign/sigstore (ECDSA P-256), ligada ao **digest** (anti-replay).
  `pull --verify` puxa **pelo digest verificado** (fecha o TOCTOU da etiqueta mutável).
- **Scan de CVE** nativo (SBOM apk/dpkg + feed de advisories actualizável).

## Plano de controlo

- **TLS/mTLS** na API REST (rustls); tokens comparados em **tempo constante**.
- **Audit log** append-only (`<root>/audit.log`, 0600) de todas as acções mutáveis.
- **Detecção em runtime** (tipo Falco): `run --detect` regista os syscalls negados
  (`dmesg type=1326`) sem deixar de os bloquear.

## Auditoria

O Delonix passou uma **auditoria E2E** adversarial (segurança, bugs, performance):
escape via `clone3`, SSRF do gateway, TOCTOU de verificação, *timing* de tokens,
reutilização de PID, fugas de recursos — todos corrigidos e verificados em runtime.

Vê o [guia prático de Segurança](../guides/security.md) para os comandos.
