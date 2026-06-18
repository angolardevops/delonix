# Rootless (sem sudo)

Como o Podman, o Delonix corre **sem privilégios** — um utilizador normal cria,
constrói e corre containers. Nada de *daemon* root, nada de `sudo`.

## Como funciona

Quando corres como utilizador normal (euid ≠ 0), o Delonix:

- guarda tudo em **`$XDG_DATA_HOME/delonix`** (`~/.local/share/delonix`);
- cria um **user namespace** com um único mapeamento (`0 <teu-uid> 1`), por isso
  o "root" do container é o teu utilizador no host;
- usa um **rootfs vfs** (sem overlay, que precisa de privilégios);
- faz rede por **slirp4netns** (egress TCP + DNS sem root).

## Usar

```bash
delonix run alpine echo "olá rootless"            # store em ~/.local/share/delonix
delonix build -t meu:1 .                          # build vfs
delonix run --network alpine wget -qO- example.com  # egress via slirp4netns
delonix ps
```

## Publicar portas em rootless

Como o Podman, `-p` **funciona sem `sudo`** — o `slirp4netns` faz o
*host-forward* em *userspace* (e `-p` já liga à rede automaticamente):

```bash
delonix run -d -p 8080:80 minha-app          # host 8080 → container 80, sem root
curl localhost:8080
```

## Limites do modo rootless

- **Sem** `--pod` — precisa de `sudo`.
- **Sem** tecto agregado do host (`delonix.slice`) — não há cgroup delegado; a
  admissão é ignorada. Vê [Protecção do host](../concepts/host-protection.md).
- O `slirp4netns` tem de estar instalado para a rede.
- Portas de container **privilegiadas** (&lt;1024, p.ex. o nginx em `:80`) podem
  falhar a abrir dentro do container — usa uma porta alta no container
  (`-p 8080:8080`) ou uma imagem rootless-friendly.

Para todas as funcionalidades (bridge, portas, pods, protecção do host), corre
com `sudo`.

Próximo: [Segurança](security.md).
