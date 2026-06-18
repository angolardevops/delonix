# Instalação

O Delonix é **um único binário estático**. Não há *daemon* para instalar, nem
serviço para arrancar, nem dependências de runtime.

## Linux (x86-64)

=== "Instalador (recomendado)"

    ```bash
    curl -fsSL https://raw.githubusercontent.com/angolardevops/delonix/main/install.sh | sh
    ```

    O instalador descarrega o binário mais recente, **verifica o checksum**,
    **instala ou actualiza** (substitui mesmo se o `delonix` estiver a correr, via
    rename atómico — sem o erro *"Text file busy"*) e **configura o autocomplete**
    da tua shell (bash/zsh/fish). Correr de novo = **actualizar** para a última versão.

=== "Manual"

    ```bash
    curl -fsSL https://github.com/angolardevops/delonix/releases/latest/download/delonix-x86_64-linux -o delonix
    curl -fsSL https://github.com/angolardevops/delonix/releases/latest/download/SHA256SUMS -o SHA256SUMS
    sha256sum -c SHA256SUMS --ignore-missing
    chmod +x delonix && sudo mv delonix /usr/local/bin/      # `mv` substitui mesmo a correr
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

**Volta a correr o instalador** — ele substitui o binário pela versão mais
recente (mesmo se estiver a correr) e reinstala o autocomplete:

```bash
curl -fsSL https://raw.githubusercontent.com/angolardevops/delonix/main/install.sh | sh
```

Versões: [Releases](https://github.com/angolardevops/delonix/releases).

## Autocomplete

O instalador já o configura. Para o fazer à mão:

```bash
delonix completion bash | sudo tee /etc/bash_completion.d/delonix >/dev/null   # bash
delonix completion zsh  | sudo tee /usr/share/zsh/site-functions/_delonix >/dev/null   # zsh
delonix completion fish > ~/.config/fish/completions/delonix.fish              # fish
```

Reabre a shell para activar. O autocomplete é **dinâmico**: completa nomes reais
de containers, imagens, pods e volumes lidos do teu store.

## Desinstalar

```bash
sudo rm /usr/local/bin/delonix
sudo rm -rf /var/lib/delonix          # store (imagens, containers) — opcional
```
