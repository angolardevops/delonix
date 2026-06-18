# Redes

O Delonix faz rede com as ferramentas nativas do kernel — `ip` (iproute2) e
`nft` (nftables) — atrás de uma API limpa. O modelo é o mesmo do Docker: uma
*bridge*, um `veth` por container, NAT de saída e DNAT para publicar portas.

## Subnet auto-detectada (sem colisões)

A bridge por omissão (`delonix0`) **não usa uma subnet fixa**: o Delonix
**detecta um `/16` livre** ao arrancar, varrendo as rotas/endereços do host e
evitando o Docker (`172.17/16`), o Podman (`10.88/16`) e qualquer rede já em uso.
O valor é **persistido** (os IPs ficam estáveis). Força-o com `DELONIX_SUBNET_BASE`.

```bash
delonix run -d --network alpine sleep 100
delonix inspect <id> | grep ip          # ex.: 10.200.x.y
```

## Publicar portas

```bash
sudo delonix run -d --network -p 8080:80 -p 9000:9000/udp nginx
curl localhost:8080
```

## Redes de utilizador (isoladas)

Cada rede tem *bridge* e subnet próprias e está **isolada** das outras por omissão.

```bash
delonix network create frontend
delonix network create backend
delonix run -d --name web --network frontend nginx
delonix run -d --name db  --network backend  postgres
delonix network ls
delonix network inspect frontend
# web e db NÃO comunicam (redes diferentes)
```

## Micro-segmentação

Bloqueia/permite tráfego entre containers específicos (firewall por elemento,
reversível):

```bash
delonix network policy deny  web db      # web deixa de alcançar db
delonix network policy allow web db      # repõe
delonix network block <container>        # isola totalmente um container
delonix network unblock <container>
```

## Limite de largura de banda

Impede que um container sature o uplink/bridge (e degrade o host):

```bash
delonix run --network --net-bps 50mbit --net-burst 256k alpine ...
tc qdisc show dev dlx<id>                # confirma o TBF + ingress
```

## DNS, load-balancing e ingress

- **DNS interno**: containers na mesma rede resolvem-se por nome.
- **LB L4**: um VIP estável distribui por réplicas de um serviço (compose).
- **Ingress L7**: `delonix ingress` encaminha por path/host para *backends*.

## Limpar

```bash
delonix network rm frontend
delonix network prune                    # remove redes não usadas
delonix network import-iptables          # interopera com regras existentes
```

Próximo: [Compose/Stacks](compose.md) · [Pods](pods.md).
