# Protecção do host

A funcionalidade que distingue o Delonix do Docker e do Podman: **o host nunca
morre** por causa dos containers, mesmo sob uma enxurrada.

## A `delonix.slice`

Todos os containers ficam **aninhados** num cgroup-pai, a `delonix.slice`, com
limites **AGREGADOS** = uma fracção do host (`DELONIX_RESERVE_PCT`, def. **85%**):

- `memory.max` — memória total dos containers; o kernel OOM-mata **dentro** da
  slice (um container), nunca o host → ficam sempre ~15% de folga.
- `cpu.max` — quota total de CPU.
- `pids.max` — total de processos (anti *fork-bomb*).
- `io.max` — **largura de banda de disco** total, resolvendo o disco inteiro que
  suporta o store. Impede que um container a escrever a fundo afogue o host.

```bash
delonix info               # orçamento + uso actual + carga + containers
DELONIX_RESERVE_PCT=70 delonix run …    # reserva 70% do host ao Delonix
```

## Admissão graciosa

Antes de arrancar, o `run` **recusa com mensagem clara** se o orçamento agregado
estiver esgotado ou a carga do host for excessiva (`load1 > ncpu×4`) — em vez de
deixar a máquina afogar-se.

## Limite de banda de rede

Por container, opcional (`--net-bps`/`--net-burst`), via `tc` no `veth`: TBF no
egress (download host→container) e *police* no ingress (upload container→host).
Fecha o último eixo, a par de CPU/memória/PIDs/I-O de disco.

## Governador térmico

Quando o Delonix aquece a máquina, **reduz a fonte de calor** (baixa o `cpu.max`
da slice em degraus) em vez de mexer no PWM do firmware:

```bash
sudo delonix thermal --high 85 --low 75     # arrefece ≥85 °C, repõe ≤75 °C
```

## Robustez

- Extracção de *layers* **atómica** (temp + rename): dezenas de `run` da mesma
  imagem em paralelo não se atropelam.
- Sem fugas: o cgroup é removido com espera; `delonix prune` varre órfãos.

!!! warning "Rootless"
    Sem cgroup delegado (modo rootless), não há tecto agregado nem admissão —
    corre com `sudo` para a protecção do host completa.
