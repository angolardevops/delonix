# `delonix run`

> Create and run a container from an image (or a rootfs)

```text
Create and run a container from an image (or a rootfs)

Usage: delonix run [OPTIONS] <IMAGE> [COMMAND]...

Arguments:
  <IMAGE>       Image (`name:tag`) or a rootfs path (directory)
  [COMMAND]...  Command to run; if empty, uses the image's `CMD`

Options:
  -d, --detach                       Run in the background (detached) and print the id
      --name <NAME>                  Container name (also the internal hostname)
  -m, --memory <MEMORY>              Memory limit (e.g. 64M). Defaults to the image's, or 64M
  -c, --cpus <CPUS>                  CPU limit in cores (e.g. 0.5). Defaults to the image's, or 1.0
      --network[=<NETWORK>]          Attach to a network: bare `--network` = default `bridge`, or `--network=<name>` for a user-defined network (veth + bridge + NAT)
      --ip <IP>                      Assign a fixed IP on the network (must be inside its subnet), e.g. `10.88.0.50`
      --pod <POD>                    Join a pod (shares the pod's network, like Podman)
      --userns                       Isolate with a user namespace (container root ≠ host root)
      --cpu-weight <CPU_WEIGHT>      CPU priority/weight (1–10000) — scheduling (cgroup cpu.weight)
      --cpuset <CPUSET>              Core affinity (e.g. `0-1`) — pinning (cgroup cpuset.cpus)
      --io-weight <IO_WEIGHT>        Disk I/O weight (1–10000) — cgroup io.weight
      --apparmor <APPARMOR>          Apply an AppArmor profile (MAC), e.g. `delonix-default`
      --selinux <SELINUX>            Apply a SELinux context (SELinux hosts only), e.g. `system_u:system_r:container_t:s0`
  -v, --volume <VOLUMES>             Mount a volume or bind: `source:/dest[:ro]` (repeatable)
  -p, --publish <PUBLISH>            Publish a port: `hostPort:contPort[/tcp|udp]` (repeatable). Implies the default network
  -e, --env <ENV>                    Set an environment variable: `KEY=value` (repeatable)
      --read-only                    Mount the root filesystem read-only (hardening)
      --cap-drop <CAP_DROP>          Drop capabilities: a name or `ALL` (repeatable)
      --cap-add <CAP_ADD>            Add capabilities back: a name like `NET_BIND_SERVICE` (repeatable)
      --secret <SECRETS>             Mount a secret as a file under `/run/secrets/<name>`: `name=path` (repeatable)
      --security-opt <SECURITY_OPT>  Security option (Docker-compat): `seccomp=unconfined`, `apparmor=<profile>`
      --tmpfs <TMPFS>                Mount a tmpfs: `/path[:opts]` (repeatable)
      --ulimit <ULIMIT>              Set a resource limit: `name=soft[:hard]` (e.g. `nofile=1024`; repeatable)
      --sysctl <SYSCTL>              Set a namespaced sysctl: `key=value` (e.g. `net.ipv4.ip_forward=1`; repeatable)
      --device <DEVICE>              Expose a host device: `/dev/x[:/dev/y]` (repeatable)
      --gpus <GPUS>                  Expose GPUs (`all` or `nvidia`/`dri`): binds the matching /dev nodes
      --restart <RESTART>            Restart policy: `no`|`on-failure`|`always`|`unless-stopped` (used by the systemd unit)
      --log-driver <LOG_DRIVER>      Log driver: `file` (default), `journald` or `syslog`
      --detect                       Runtime detection: log denied syscalls to the kernel audit (Falco-lite)
      --no-userns                    Opt out of the default user namespace (root-in-container = root-on-host)
      --net-bps <NET_BPS>            Limit network bandwidth (download + upload) on the host-side veth, e.g. `10mbit`, `1g`, `512k`. Protects the host uplink. Needs a `--network`
      --net-burst <NET_BURST>        Burst (token bucket) for `--net-bps`, in bytes, e.g. `256k`. Defaults to ~100ms of the rate
      --pt-pt                        Show help in Portuguese (pt-PT) instead of English
  -h, --help                         Print help
```
