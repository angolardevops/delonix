# Stacks (compose)

Define aplicações multi-container num ficheiro YAML e gere-as como uma unidade —
ao estilo `docker compose`, mas nativo.

## O ficheiro `delonix.yaml`

```yaml
apiVersion: delonix/v1
services:
  web:
    image: nginx
    ports: ["8080:80"]
    resources:
      cpus: "0.5"
      memory: "128M"
    restart: always
  api:
    image: minha-api:1
    env:
      - DATABASE_URL=postgres://db/app
    replicas: 3            # escala horizontal + LB L4
  db:
    image: postgres:16
    volumes: ["pgdata:/var/lib/postgresql/data"]
```

Gera um esqueleto com `delonix init`.

!!! note "Campos tolerantes"
    `kind` (aceita `Stack`/`kind`/`Kind` ou omitido) e `apiVersion` são opcionais —
    por omissão assumem `Stack` e `delonix/v1`. Se não puseres `metadata.name`, o
    nome do stack é derivado do **nome do ficheiro** (ex.: `stack.yaml` → `stack`).

## Ciclo de vida da stack

```bash
delonix up                       # arranca tudo (cria rede, volumes, containers)
delonix service ps               # estado dos serviços
delonix service watch            # acompanha ao vivo
delonix down                     # pára e remove a stack
```

`service apply` reconcilia a stack com o ficheiro (cria/actualiza/remove o
necessário).

## Escala e autoscale

```bash
delonix scale -f delonix.yaml api 5         # 5 réplicas do serviço api
delonix autoscale api --min 2 --max 10 --cpu 70   # autoscale por CPU
```

As réplicas de um serviço ficam atrás de um **VIP** com balanceamento L4.

## Ingress L7

```bash
delonix ingress --port 80 \
  --route /api=api:8080 \
  --route /=web:80
```

## Converter para Kubernetes

```bash
delonix convert -f delonix.yaml --to k8s -o k8s/      # manifests separados
delonix kube generate web                              # de um container/pod
```

Próximo: [Pods](pods.md) · [Kubernetes/CRI](kubernetes.md).
