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
| `Exec`/`Attach`/`PortForward` (streaming) | ❌ `UNIMPLEMENTED` |
| `ContainerStats`/`PodSandboxStats` | ❌ vazio |

Ou seja: o Delonix **corre** pods e containers para o kubelet, mas `kubectl exec`,
`logs -f`, `port-forward` e as métricas por-pod ainda não estão disponíveis.

## Gerar manifests

```bash
delonix kube generate <container|pod>     # YAML para o kubectl
delonix convert -f delonix.yaml --to k8s -o k8s/
```

Próximo: [Referência `cri`](../reference/cri.md).
