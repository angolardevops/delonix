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
| Pod sandbox = pod real (infra + netns partilhado, IP) | ✅ |
| Security context (readonly, caps, seccomp, apparmor, privileged) | ✅ |
| Namespaces de host (`namespace_options` PID/IPC = NODE) | ✅ |
| AppArmor (perfil carregado; rejeita não-carregado) + sysctls de pod | ✅ |
| `RemoveImage` idempotente | ✅ |
| `Exec`/`Attach`/`PortForward` (streaming interactivo) | ❌ `UNIMPLEMENTED` |

O **pod sandbox** cria um pod real do Delonix — um *infra container* que detém o
**network namespace partilhado** (estilo *pause*), ao qual os containers se juntam
(`--pod`); o IP do pod é reportado no `PodSandboxStatus`. O **security context**
do CRI é traduzido para as flags do `delonix run` (rootfs só-leitura, capabilities
add/drop, seccomp *unconfined*, AppArmor, privileged). O `ExecSync` corre comandos
no container (sondas `exec` do kubelet). Falta o **streaming interactivo**
(`kubectl exec -it`, `attach`, `port-forward`).

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

Estado actual: **29 Passed | 63 Failed | 30 Skipped** (92 de 122 specs). Passam o
ciclo de vida base, imagens e métricas. As falhas concentram-se em **Security
Context** (namespaces de host, seccomp por caminho, run-as-user), **Streaming**
(`Exec`/`Attach`/`PortForward`) e **partilha de namespaces do pod sandbox** — o
roteiro a seguir. (Honestidade: ainda não é conforme; é um número de partida real.)

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
