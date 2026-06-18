# Containers

Um container no Delonix é um **processo normal do host** isolado por *namespaces*
(o que vê), *cgroups* (o que consome) e uma imagem (o que tem). Não há *daemon*:
cada container é filho do `delonix` que o arrancou.

## Correr

```bash
delonix run alpine echo olá                 # efémero, em primeiro plano
delonix run -d --name web nginx             # em segundo plano (detached)
delonix run -it ubuntu bash                 # interactivo com TTY
```

!!! note "Nomes e portas são validados"
    Como no Docker/Podman, o `run` **recusa** um `--name` que já exista e uma
    **porta de host já ocupada** — quer por outro container do Delonix, quer por
    outro processo/engine do host (p.ex. um container do Docker). Escolhe outro
    nome/porta, ou remove o container que está a usar (`delonix rm <nome>`).

Flags de execução mais comuns:

| Flag | Efeito |
|---|---|
| `-d, --detach` | corre em segundo plano, imprime o id |
| `--name <n>` | dá-lhe um nome **único** (rejeitado se já existir) |
| `-e KEY=val` | variável de ambiente |
| `-v /host:/cont` | monta um volume/bind |
| `-p 8080:80` | publica uma porta (precisa de `--network`) |
| `--network[=nome]` | liga à bridge por omissão ou a uma rede |
| `-m 256M` `-c 0.5` | limites de memória e CPU |
| `--restart always` | política de reinício (via systemd) |
| `--read-only` | rootfs só-leitura |

## Ciclo de vida

```bash
delonix ps               # a correr        |  delonix ps -a   # todos
delonix ps -q            # só IDs (scripting) | delonix ps -aq # todos, só IDs
delonix rm -f $(delonix ps -aq)   # remove todos (como no Docker/Podman)
```

A saída segue o formato do Docker (colunas de largura dinâmica):

```text
CONTAINER ID   IMAGE   COMMAND                  CREATED         STATUS         PORTS                  NAMES
ae04ef086f59   nginx   "nginx -g daemon off;"   5 minutes ago   Up 5 minutes   0.0.0.0:8000->80/tcp   web
delonix stop web         # SIGTERM → SIGKILL
delonix start web        # rearranca um container parado
delonix restart web
delonix pause web        # congela (cgroup freezer)
delonix unpause web
delonix rm web           # remove (use -f para forçar)
```

## Inspeccionar e depurar

```bash
delonix logs web --tail 100      # stdout/stderr capturados
delonix logs -f web              # segue ao vivo (como `tail -f`)
delonix exec -it web sh          # comando dentro do container (PTY)
delonix ssh web                  # atalho: shell interactiva
delonix top web                  # processos
delonix stats                    # uso ao vivo (CPU/MEM/NET/IO/PIDS)
delonix inspect web              # JSON completo
delonix diff web                 # ficheiros alterados (upperdir)
delonix cp web:/etc/hostname .   # copiar para/de o container
```

## Recursos e limites

O Delonix aplica limites por *cgroup v2* e — ao contrário do Docker/Podman —
**todos os containers partilham um tecto agregado** (a `delonix.slice`), de modo
que nenhuma enxurrada derruba o host. Vê [Protecção do host](../concepts/host-protection.md).

```bash
delonix run -m 256M -c 0.5 --io-weight 50 alpine sleep 100
delonix update web -m 512M          # altera limites ao vivo
```

## Persistir e capturar estado

```bash
delonix commit web minha-imagem:1   # imagem a partir do container
delonix export web > web.tar        # (via oci-export para um bundle)
```

Próximo: [Imagens](images.md) · [Redes](networks.md) · [Segurança](security.md).
