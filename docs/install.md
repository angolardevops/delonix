# Instalação

O Delonix é **um único binário estático**. Não há *daemon* para instalar, nem
serviço para arrancar, nem dependências de runtime.

## Linux (x86-64)

=== "Uma linha (recomendado)"

    ```bash
    curl -fsSL https://github.com/angolardevops/delonix/releases/latest/download/delonix-x86_64-linux -o delonix
    chmod +x delonix
    sudo mv delonix /usr/local/bin/delonix
    delonix --version
    ```

=== "Verificar o checksum"

    ```bash
    curl -fsSL https://github.com/angolardevops/delonix/releases/latest/download/delonix-x86_64-linux -o delonix
    curl -fsSL https://github.com/angolardevops/delonix/releases/latest/download/SHA256SUMS -o SHA256SUMS
    sha256sum -c SHA256SUMS --ignore-missing
    chmod +x delonix && sudo mv delonix /usr/local/bin/
    ```

O binário é **estático (musl)** — corre em qualquer distribuição Linux x86-64
(glibc ou musl, com ou sem bibliotecas de sistema).

## Requisitos

O binário não tem dependências, mas o *runtime* usa funcionalidades do kernel
Linux. Para tudo funcionar:

- **Kernel Linux** com **cgroup v2** (qualquer distro de 2021+).
- Para operações privilegiadas (rede *bridge*, cgroups do host, alguns
  *namespaces*), corre com `sudo`. Para o modo **rootless** (sem `sudo`), basta
  um utilizador normal.
- Ferramentas do sistema usadas pelo runtime quando presentes: `ip` (iproute2),
  `nft` (nftables), `slirp4netns` (rede rootless), `tc` (limite de banda).

## Verificar a instalação

```bash
delonix --version
delonix --help                 # visão geral didáctica
delonix run alpine echo ok     # primeiro container (precisa de rede para o pull)
```

## Autocompletion

```bash
# bash
delonix completion bash | sudo tee /etc/bash_completion.d/delonix >/dev/null
# zsh / fish: ver `delonix completion --help`
```

## Atualizar

Repete o passo de instalação — o binário substitui o anterior. Para ver a versão
mais recente: [Releases](https://github.com/angolardevops/delonix/releases).

## Desinstalar

```bash
sudo rm /usr/local/bin/delonix
sudo rm -rf /var/lib/delonix          # store (imagens, containers) — opcional
```
