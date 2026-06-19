# Kubernetes (CRI)

O Delonix implementa o **CRI** (Container Runtime Interface) por gRPC, para que um
**kubelet** ou o `crictl` o usem como *runtime* de nó — como o `containerd` ou o
CRI-O.

## Arrancar o servidor CRI

```bash
sudo delonix cri --addr unix:///run/delonix-cri.sock
```

## Verificar com o `crictl`

```bash
sudo crictl --runtime-endpoint unix:///run/delonix-cri.sock version   # RuntimeName: delonix
sudo crictl pull alpine:3.19
sudo crictl runp pod.json && sudo crictl create <pod> ctr.json pod.json
sudo crictl start <ctr>                # → CONTAINER_RUNNING
```

O ciclo de vida completo (`pull` → `runp` → `create` → `start` → `stop`/`rm`/`rmp`)
está implementado e verificado, com o **código de saída real** propagado.

## Âmbito (honesto)

| RPC | Estado |
|---|---|
| `Version`, `Status` | ✅ |
| `RunPodSandbox`/`StopPodSandbox`/`RemovePodSandbox` | ✅ |
| `CreateContainer`/`StartContainer`/`StopContainer`/`RemoveContainer` | ✅ |
| `ListContainers`/`ContainerStatus` (com exit code) | ✅ |
| `ImageService` (pull/list/remove) | ✅ |
| `ContainerStats`/`ListContainerStats` (CPU+memória) | ✅ |
| `PodSandboxStats`/`ListPodSandboxStats` (agregado) | ✅ |
| `ExecSync` (sondas exec do kubelet, `crictl exec -s`) | ✅ |
| `Exec` **interactivo** (`kubectl exec -it`, `crictl exec -it`) — SPDY + WebSocket | ✅ |
| Pod sandbox = pod real (infra + netns partilhado, IP) | ✅ |
| Security context (readonly, caps, seccomp, apparmor, privileged) | ✅ |
| Namespaces de host (`namespace_options` PID/IPC = NODE) | ✅ |
| AppArmor (perfil carregado; rejeita não-carregado) + sysctls de pod | ✅ |
| `RemoveImage` idempotente | ✅ |
| `Attach`/`PortForward` (streaming) | ❌ `UNIMPLEMENTED` |

O **pod sandbox** cria um pod real do Delonix — um *infra container* que detém o
**network namespace partilhado** (estilo *pause*), ao qual os containers se juntam
(`--pod`); o IP do pod é reportado no `PodSandboxStatus`. O **security context**
do CRI é traduzido para as flags do `delonix run` (rootfs só-leitura, capabilities
add/drop, seccomp *unconfined*, AppArmor, privileged). O `ExecSync` corre comandos
no container (sondas `exec` do kubelet).

### Streaming interactivo (`kubectl exec -it`)

O `Exec` devolve uma **URL** para um servidor de streaming embebido que fala o
protocolo *remotecommand* do Kubernetes em **dois transportes**:

- **SPDY/3.1** — o que o `crictl` e o `kubelet` de hoje usam (com compressão de
  cabeçalhos zlib + o dicionário fixo SPDY/3, controlo de fluxo por-stream).
- **WebSocket** (`v5.channel.k8s.io`) — o transporte futuro para que o Kubernetes
  está a migrar.

Suporta stdin, stdout/stderr separados, **TTY** (aloca um *pty* real no devpts do
container, à `runc`), redimensionamento e **propagação do exit code**. Verificado
com `crictl exec`/`exec -it` e pela suite `critest` (specs de exec a passar).

Falta ainda o **`Attach`** (ligar ao processo principal de um container já a
correr) e o **`PortForward`** — em curso.

### Métricas (CRI stats)

```bash
crictl --runtime-endpoint unix:///run/delonix-cri.sock stats     # por container
crictl --runtime-endpoint unix:///run/delonix-cri.sock statsp    # por pod sandbox
```

CPU vem do `cpu.stat` do cgroup v2 (cumulativa, em core-nanossegundos); a memória
do RSS real dos processos do cgroup. É o que o **kubelet** lê para a Summary API e
o **HPA** para escalar.

## Conformância (critest)

Baseline objectivo medido com a suite **`critest`** (cri-tools), com o servidor a
correr e ambas as endpoints (runtime + image) a apontar para o socket do Delonix:

```bash
sudo critest -runtime-endpoint unix:///run/delonix-cri.sock \
             -image-endpoint   unix:///run/delonix-cri.sock
```

Baseline anterior: **29 Passed | 63 Failed | 30 Skipped**. Passam o ciclo de vida
base, imagens e métricas. **Novidade:** os specs de **`Exec`** (incluindo o
streaming interactivo) passam agora a verde — uma corrida focada do `critest`
(`-ginkgo.focus 'Exec'`) dá **5 Passed | 0 Failed**. As falhas restantes
concentram-se em **Security Context** (namespaces de host, segmento de memória
partilhada, run-as-user), **`Attach`/`PortForward`** e **partilha de namespaces
do pod sandbox** — o roteiro a seguir. (Honestidade: ainda não é totalmente
conforme; são números reais e medidos.)

## Criar um cluster (real)

O Delonix **deteta** as ferramentas de cluster instaladas e **cria clusters
reais**, delegando na ferramenta escolhida — não reimplementa o instalador.

```bash
delonix cluster tools                 # deteta Kind/k3d/minikube/kubeadm/k0s/Talos (versão + caminho)
delonix cluster create --tool kind --name dev --control-plane 1 --workers 2
delonix cluster ls                    # clusters existentes
delonix cluster rm dev                # remove
```

- **Single-host multi-nó** (criados de verdade): **Kind**, **k3d**, **minikube**.
- **kubeadm / k0s / Talos** são detetados mas exigem várias máquinas — o Delonix
  recusa-os no modo local com uma explicação (não há magia escondida).
- A topologia (control-plane, workers), o **CNI** e a **versão do K8s** são
  configuráveis — nada está fixo.

No **painel embebido** (`sudo delonix serve ui`, sem flags) há uma vista
**Kubernetes** na barra lateral: lista as ferramentas detetadas e os clusters, e
o botão **Criar cluster** abre o assistente — que cria o cluster **de verdade**
(mesma origem da API). Os endpoints REST são:

```
GET  /api/k8s/tools           # deteção
GET  /api/k8s/clusters        # lista
POST /api/k8s/cluster         # cria  { tool, name, control_plane, workers, cni?, k8s_version? }
POST /api/k8s/cluster/<n>/rm  # remove
```

> Depois de criar, o `kubectl` fica com o contexto do novo cluster. O Delonix
> pode então servir os pods como **CRI** (`delonix cri`).

## Gerar manifests

```bash
delonix kube generate <container|pod>     # YAML para o kubectl
delonix convert -f delonix.yaml --to k8s -o k8s/
```

Próximo: [Referência `cri`](../reference/cri.md).
