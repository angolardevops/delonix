# `delonix pod`

> Pods: groups of containers that share a network (Podman parity)

```text
Pods: groups of containers that share a network (Podman parity)

Usage: delonix pod [OPTIONS] <COMMAND>

Commands:
  create  Create a pod (starts an infra container holding the shared network)
  ls      List pods and their members
  rm      Remove a pod and all its containers
  help    Print this message or the help of the given subcommand(s)

Options:
      --pt-pt  Show help in Portuguese (pt-PT) instead of English
  -h, --help   Print help
```

## `delonix pod create`

> Create a pod (starts an infra container holding the shared network)

```text
Create a pod (starts an infra container holding the shared network)

Usage: delonix pod create [OPTIONS] <NAME>

Arguments:
  <NAME>  Pod name

Options:
      --network            Attach the pod to the `delonix0` network (veth + bridge + NAT)
  -p, --publish <PUBLISH>  Publish a pod port: `hostPort:contPort[/proto]` (implies --network)
      --pt-pt              Show help in Portuguese (pt-PT) instead of English
  -h, --help               Print help
```

## `delonix pod ls`

> List pods and their members

```text
List pods and their members

Usage: delonix pod ls [OPTIONS]

Options:
      --pt-pt  Show help in Portuguese (pt-PT) instead of English
  -h, --help   Print help
```

## `delonix pod rm`

> Remove a pod and all its containers

```text
Remove a pod and all its containers

Usage: delonix pod rm [OPTIONS] <NAME>

Arguments:
  <NAME>  Pod name

Options:
      --pt-pt  Show help in Portuguese (pt-PT) instead of English
  -h, --help   Print help
```
