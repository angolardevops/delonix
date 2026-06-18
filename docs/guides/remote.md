# Host remoto (SSH)

Controla um Delonix noutra máquina por SSH — como `DOCKER_HOST=ssh://` no Docker
ou `--url ssh://` no Podman. Os comandos correm na máquina remota; o output volta
para o teu terminal.

## Usar

```bash
# por flag
delonix --host ssh://user@servidor ps
delonix --host ssh://user@servidor:2222 run -d --network -p 80:80 nginx

# por ambiente (aplica-se a todos os comandos)
export DELONIX_HOST=ssh://user@servidor
delonix images
delonix ssh web                 # shell interactiva num container REMOTO
```

## Como funciona

O Delonix re-executa o comando na máquina remota via `ssh`, com:

- alocação de **TTY** (`-t`) quando o teu `stdin` é um terminal (para `ssh`/`exec`/`stats`);
- *porta* opcional (`ssh://host:porta`);
- *escaping* seguro dos argumentos.

## Requisitos

- `ssh` configurado para a máquina remota (idealmente com chave, sem password).
- O binário **`delonix`** instalado e no `PATH` da máquina remota.
- As permissões habituais no remoto (`sudo` para operações privilegiadas).

!!! tip "Painel de um host remoto"
    Combina com o painel: corre `delonix serve ui` na máquina remota e faz
    *tunnel* da porta por SSH (`ssh -L 9444:127.0.0.1:9444 user@servidor`).
