# Pods

Um **pod** é um grupo de containers que **partilham o *network namespace*** (e
portanto o `localhost` e o IP) — exactamente o conceito do Kubernetes e do
Podman. Útil para *sidecars* (proxy, log shipper, etc.).

## Criar e povoar

```bash
delonix pod create web-pod
delonix run -d --pod web-pod --name app  minha-app:1
delonix run -d --pod web-pod --name proxy nginx
delonix pod ls
# app e proxy partilham o IP; o proxy alcança a app em 127.0.0.1
```

Publicar portas faz-se ao nível do pod (o `--pod` implica rede partilhada):

```bash
delonix pod create web-pod         # cria a infra-estrutura de rede do pod
delonix run -d --pod web-pod -p 8080:80 nginx
```

## Remover

```bash
delonix pod rm web-pod             # remove o pod e os seus containers
```

## Gerar manifest Kubernetes

```bash
delonix kube generate web-pod      # YAML de Pod pronto para o kubectl
```

!!! note "Rootless"
    `--pod` (como `-p`) ainda requer `sudo`. O modo rootless suporta containers
    simples; os pods e a publicação de portas estão na lista de melhorias.

Próximo: [Kubernetes/CRI](kubernetes.md).
