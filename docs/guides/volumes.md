# Volumes e dados

Os containers são efémeros; os **volumes** guardam dados que sobrevivem ao
container. O Delonix suporta volumes nomeados e *bind mounts* (zero-copy: o
kernel partilha os blocos).

## Volumes nomeados

```bash
delonix volume create dados
delonix volume ls
delonix volume inspect dados
delonix run -d -v dados:/var/lib/app minha-app:1
delonix volume rm dados
```

## Bind mounts

Monta um caminho do host directamente:

```bash
delonix run -v /home/user/projeto:/src minha-app:1
delonix run -v /etc/config:/app/config:ro minha-app:1   # só-leitura
```

## tmpfs (memória)

Para dados temporários que nunca tocam o disco (montado `nosuid,nodev`):

```bash
delonix run --tmpfs /tmp:size=64m alpine sh
```

## Segredos

Os segredos são montados em `/run/secrets/<nome>` (tmpfs) e **nunca** entram no
ambiente — não vazam por `/proc/<pid>/environ`:

```bash
delonix run --secret db-pass=/caminho/no/host/pass.txt minha-app:1
# dentro do container: cat /run/secrets/db-pass
```

Próximo: [Compose/Stacks](compose.md).
