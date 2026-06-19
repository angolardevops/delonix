# A Consola (painel web)

A **Delonix Console** é um painel web **enterprise** de gestão de containers
(estilo Docker Desktop / Portainer) que vive **dentro do próprio binário** — sem
Node, sem CDN, sem dependências. Liga-se com um comando e gere todo o ecossistema
do Engine no browser, **sincronizado com a CLI**.

```bash
sudo delonix serve ui                 # painel embebido em http://127.0.0.1:9444
sudo delonix serve ui --console ./delonix-console.html   # serve a Console completa
```

!!! tip "Embebido vs Console completa"
    O `serve ui` traz um painel embebido. Para a **Console completa** (com
    assistente de cluster, mapa de calor, alertas, editor…), passa-a com
    `--console <ficheiro.html>` — fica na **mesma origem** da API, por isso tudo
    o que ela faz é **real** (ver [Criar um cluster](kubernetes.md#criar-um-cluster-real)).

---

## As telas

A Console organiza-se numa barra lateral (Gestão · Kubernetes · Sistema) e uma
área principal que se reconstrói por vista. Todas as telas são navegáveis,
populadas e **atualizam-se ao vivo**.

### Gestão

| Tela | O que mostra / faz |
|---|---|
| **Painel** | 6 *stat cards* (containers, imagens, CPU, carga, memória, PIDs) com *sparklines*; **Health Score** (donut 0–100) + 8 sinais SRE (disponibilidade, P95, erros, reinícios, OOM, throttling, I/O, rede); containers a correr; gauges de host (CPU/Mem/Disco); atividade e stacks. |
| **Containers** | Lista filtrável (todos/a correr/pausados/parados) em **tabela ou cards**, seleção múltipla + **ações em lote**, ações inline por estado, e o **drawer de detalhe** (8 abas) ao clicar. |
| **Imagens** | Repositório/tag/tamanho/arquitetura/uso; *pull* com **progresso por camadas**; executar (deploy pré-preenchido); limpar pendentes. |
| **Redes** | Driver/subnet/gateway/ligados; criar rede; **drawer** com mapa de tráfego *hub-and-spoke* animado, conntrack ao vivo e firewall. |
| **Volumes** | Tamanho/uso/montagens; **drawer** com atividade de I/O animada (leitura verde / escrita âmbar) e métricas IOPS/débito/latência ao vivo; **editor de ficheiros** → nova camada. |
| **Stacks** | Apps multi-container (compose): serviços, estado, reiniciar/parar/**mapa**; nova stack. |
| **Topologia** | Mapa de comunicação **animado** (rAF): nós com ícone tipado, arestas por tipo, **pacotes a fluir** proporcionais ao tráfego, *ingress*, e realce ao passar o rato. |

### Kubernetes (modo CRI)

Ativa-se no seletor de workspace. Aparece a secção **Kubernetes · CRI**:

| Tela | O que mostra / faz |
|---|---|
| **Pods** | Por namespace, com owner (Deployment/StatefulSet/CronJob), *Ready*, estado (Running/Pending/CrashLoopBackOff), reinícios, CPU/Mem, nó; **drawer de Pod** (Resumo/Containers/Eventos/YAML). |
| **Workloads** | Deployments/StatefulSets — réplicas, **escalar** (+/−), *rollout restart*. |
| **Namespaces / Nós** | Cartões de namespace; tabela de nós (função, estado, CPU/Mem, pods). **Botão "Criar cluster"** → assistente. |

O **assistente de cluster** deteta as ferramentas do host (Kind, k3d, minikube,
kubeadm, …), deixa escolher a topologia (control-plane, workers, CNI, versão) e
**cria o cluster** — de verdade quando ligado ao engine. Ver
[Criar um cluster](kubernetes.md#criar-um-cluster-real).

### Sistema

- **Mapa de calor** — grelha de núcleos de CPU (frio→crítico), subsistemas ao
  longo do tempo (CPU, memória, swap, I/O wait, rede, PSI, térmico) e **causas de
  saturação** acionáveis.
- **Eventos** — o `audit.log` do Engine.
- **Definições** — Geral, Rede & DNS, Registos, Recursos, **Integrações**
  (webhooks), Segurança.

---

## Drawer de detalhe do container (8 abas)

Ao clicar num container abre um painel deslizante com: **Resumo** (métricas com
mini-gráficos + tabela), **Registos** (streaming ao vivo, níveis coloridos),
**Métricas** (4 canvases a 1 s), **Configurar** (edição *a quente* — portas, DNS,
redes, links, redirect com diagrama animado), **Firewall** (regras ingress/egress),
**Consola** (sessão `sh` interativa), **Inspecionar** (JSON com *highlight*),
**Ficheiros** (árvore do sistema de ficheiros).

---

## Funcionalidades de destaque

- **Tudo ao vivo** — métricas, logs, conntrack, I/O, topologia e mapa de calor
  com *jitter* realista, sem recarregar a página.
- **Modo manutenção** — drena o tráfego de um container/pod (nos mapas deixa de
  receber/enviar pacotes, com anel âmbar tracejado) sem o destruir.
- **Edição não-destrutiva** — aplica só os campos que mudaram; preserva IP, DNS,
  uptime e métricas; avisa o que exige recriar vs muda a quente.
- **Editor → camada → imagem** — editar um ficheiro num volume RW cria uma
  **nova camada**; *commit* gera uma **nova imagem**.
- **Alertas em tempo real** — motor de regras (crash-loop, OOM, CPU/memória
  altas…) com **sino**, *popover*, e **entrega a webhooks** (Slack, Mattermost,
  **WhatsApp**) com teste de entrega.
- **Multi-runtime + Kubernetes** — alternar Docker/Podman/Delonix e ativar o
  modo **CRI**; cada recurso filtrado por workspace.
- **i18n** (EN/PT/PT-BR) e **Tweaks** (acento, layout, densidade).

---

## Vantagens

- **Um binário, zero dependências** — sem Docker Desktop, sem Electron, sem conta.
  Liga em loopback; offline.
- **Sincronizada com a CLI** — lê o mesmo *store* e delega as mutações no próprio
  `delonix`; o que fazes na CLI aparece no painel e vice-versa.
- **Rootless e remoto** — funciona sem root (slirp4netns) e contra um host remoto
  por SSH.
- **Observabilidade nativa** — SRE/health score, mapa de calor e topologia que o
  Docker Desktop não traz.
- **Kubernetes integrado** — pods, workloads e **criação de cluster** no mesmo
  painel.
- **Leve** — ~13 MB no total (engine + painel), arranque instantâneo.

## Desvantagens / limitações

- **Sem streaming interativo completo** ainda — `kubectl exec -it` / `attach` /
  `port-forward` interativos estão em curso (o `exec` não-interativo funciona).
- **Single-host** por omissão — não orquestra uma frota como uma plataforma
  cloud (usa o modo Kubernetes para isso).
- **Sem GUI nativa de SO** — é um painel web (browser), não uma app de tabuleiro
  com auto-update gráfico como o Docker Desktop.
- **Ecossistema mais jovem** — menos extensões/integrações de terceiros que o
  Docker Desktop.

---

## Comparação com o Docker Desktop

| | Docker Desktop | **Delonix Console** |
|---|---|---|
| Modelo | App de SO (Electron) + VM/daemon | **Binário único**, sem daemon, painel embebido |
| Licença | Paga para empresas grandes | **Aberta**, sem conta |
| Instalação | Instalador + VM | `curl … \| sh` ou um binário |
| Rootless | Limitado | **Sim** (slirp4netns) |
| Host remoto | Contextos | **Sim** (SSH) |
| Topologia / tráfego ao vivo | — | **Sim** (mapa animado) |
| Mapa de calor / SRE | — | **Sim** |
| Edição a quente não-destrutiva | Recria | **Diff, preserva estado** |
| Editor → camada → imagem | — | **Sim** |
| Alertas + webhooks (Slack/WhatsApp) | — | **Sim** |
| Kubernetes | Liga um single-node | **Modo CRI + criar cluster** (Kind/k3d/minikube) |
| Multi-runtime (Docker/Podman) | Docker | **Docker · Podman · Delonix** |
| Footprint | Vários GB + VM | **~13 MB**, sem VM |
| Imagens OCI / `runc` | Sim | **Sim** (compatível) |
| GUI de SO nativa | **Sim** | Painel web |
| Maturidade do ecossistema | **Alta** | A crescer |

> Resumindo: o Docker Desktop é uma app de SO madura e gráfica; a Delonix Console
> é um painel **mais leve, aberto e observável**, embebido no engine, com
> Kubernetes e criação de cluster integrados — ao custo de ser web (não nativo) e
> de um ecossistema mais novo.

---

Próximo: [Criar um cluster](kubernetes.md#criar-um-cluster-real) ·
[Plataforma de IA](ai-llm.md) · [Host remoto](remote.md).
