# Arranque rápido

Este guia leva-te do nada ao teu primeiro container, imagem, rede e painel web.
Se já usaste Docker ou Podman, vais sentir-te em casa.

!!! note "Privilégios"
    As operações de rede *bridge* e os limites do host precisam de `sudo`. Para
    correr sem `sudo`, vê o guia [Rootless](guides/rootless.md).

## 1. Correr um container

```bash
delonix run alpine echo "olá, mundo"
```

O Delonix puxa a imagem `alpine` (se ainda não a tiver), cria um container com
*namespaces* novos, *seccomp*, *user namespace* e corre o comando.

Em segundo plano, com nome e rede:

```bash
sudo delonix run -d --name web --network -p 8080:80 nginx
sudo delonix ps
curl localhost:8080
```

## 2. Entrar no container

```bash
sudo delonix exec -it web sh        # shell interactiva (PTY real)
sudo delonix ssh web                # atalho equivalente, ao estilo ssh
```

## 3. Ver logs, estado e recursos

```bash
sudo delonix logs web
sudo delonix stats                  # CPU/MEM/NET/IO/PIDS ao vivo
sudo delonix top web
sudo delonix inspect web
```

## 4. Construir uma imagem

Cria um `Delonixfile` (ou usa um `Dockerfile` existente):

```dockerfile
FROM alpine:3.19
RUN apk add --no-cache curl
CMD ["sh"]
```

```bash
sudo delonix build -t minha-app:1 .
sudo delonix run minha-app:1 curl -s https://example.com
```

## 5. Criar uma rede e ligar containers

```bash
sudo delonix network create app-net
sudo delonix run -d --name api --network app-net minha-app:1 sleep 1000
sudo delonix run -d --name db  --network app-net alpine sleep 1000
# api e db comunicam; estão isolados de outras redes
```

## 6. Uma stack (compose)

`delonix.yaml`:

```yaml
apiVersion: delonix/v1
services:
  web:
    image: nginx
    ports: ["8080:80"]
    resources: { cpus: "0.5", memory: "128M" }
```

```bash
sudo delonix up                     # arranca a stack
sudo delonix service ps
sudo delonix down                   # pára e limpa
```

## 7. O painel web

```bash
sudo delonix serve ui               # http://127.0.0.1:9444
```

Gere containers, imagens, redes e stacks no browser — **sincronizado com a CLI**
(o que fazes num lado aparece no outro).

## 8. Limpar

```bash
sudo delonix stop web && sudo delonix rm web
sudo delonix prune                  # remove órfãos (containers/imagens/cgroups)
```

## Próximo passo

- Aprende por temas nos [Guias](guides/containers.md).
- Consulta **todos** os comandos na [Referência](reference/index.md).
- Vê como o Delonix se compara ao [Docker e Podman](compare.md).
