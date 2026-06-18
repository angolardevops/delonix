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

## IP fixo

Atribui um endereço escolhido (em vez do derivado do id), validado contra a
subnet da rede:

```bash
delonix run -d --network=frontend --ip 10.200.0.50 --name web nginx
delonix inspect web | grep ip            # 10.200.0.50
```

## Ligar/desligar redes a quente (multi-homing)

Um container **em execução** pode ser ligado a redes **adicionais** sem ser
recriado — ganha uma interface `eth1`, `eth2`, … por rede (estilo `docker
network connect`):

```bash
delonix run -d --name web --network=frontend nginx
delonix network connect backend web                 # web ganha eth1 na backend
delonix network connect dmz web --ip 10.50.0.9      # com IP fixo
delonix inspect web | grep -A4 extra_networks       # redes adicionais + IPs
delonix network disconnect backend web              # remove a interface
```

A rede **primária** (a do `run`) não se desliga a quente — pára/recria o
container para a mudar. As redes adicionais vivem no *netns* do container: ao
**parar**, são limpas (não são re-estabelecidas no arranque seguinte).

Na **consola web** (`serve ui`), o modal *Reconfigurar* de cada container lista
as suas redes e permite ligar/desligar ao vivo, com IP fixo opcional.

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
