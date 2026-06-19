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
| `Exec`/`Attach`/`PortForward` (streaming) | ❌ `UNIMPLEMENTED` |

Ou seja: o Delonix **corre** pods e containers para o kubelet e fornece-lhe
**métricas reais** (Summary API / HPA), mas `kubectl exec`, `logs -f` e
`port-forward` (streaming) ainda não estão disponíveis.

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

## Gerar manifests

```bash
delonix kube generate <container|pod>     # YAML para o kubectl
delonix convert -f delonix.yaml --to k8s -o k8s/
```

Próximo: [Referência `cri`](../reference/cri.md).
