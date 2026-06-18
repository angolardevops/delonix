# `delonix network`

> Networking and firewall operations

```text
Networking and firewall operations

Usage: delonix network [OPTIONS] <COMMAND>

Commands:
  create           Create a user-defined network (own bridge + subnet, isolated from others)
  ls               List networks (the default `bridge` plus user-defined ones)
  rm               Remove a user-defined network (its bridge + nft rules)
  inspect          Show a network's details (bridge, subnet, gateway, members)
  policy           Micro-segmentation: deny/allow traffic between two containers (B14)
  block            Block traffic to/from a container (per-container firewall)
  unblock          Unblock a previously blocked container
  import-iptables  Import and summarize an `iptables-save` file (does not change the host)
  prune            Remove the `delonix0` bridge and Delonix's nft table
  help             Print this message or the help of the given subcommand(s)

Options:
      --pt-pt  Show help in Portuguese (pt-PT) instead of English
  -h, --help   Print help
```

## `delonix network create`

> Create a user-defined network (own bridge + subnet, isolated from others)

```text
Create a user-defined network (own bridge + subnet, isolated from others)

Usage: delonix network create [OPTIONS] <NAME>

Arguments:
  <NAME>  Network name (e.g. `frontend`)

Options:
      --pt-pt  Show help in Portuguese (pt-PT) instead of English
  -h, --help   Print help
```

## `delonix network ls`

> List networks (the default `bridge` plus user-defined ones)

```text
List networks (the default `bridge` plus user-defined ones)

Usage: delonix network ls [OPTIONS]

Options:
      --pt-pt  Show help in Portuguese (pt-PT) instead of English
  -h, --help   Print help
```

## `delonix network rm`

> Remove a user-defined network (its bridge + nft rules)

```text
Remove a user-defined network (its bridge + nft rules)

Usage: delonix network rm [OPTIONS] <NAME>

Arguments:
  <NAME>  Network name

Options:
      --pt-pt  Show help in Portuguese (pt-PT) instead of English
  -h, --help   Print help
```

## `delonix network inspect`

> Show a network's details (bridge, subnet, gateway, members)

```text
Show a network's details (bridge, subnet, gateway, members)

Usage: delonix network inspect [OPTIONS] <NAME>

Arguments:
  <NAME>  Network name

Options:
      --pt-pt  Show help in Portuguese (pt-PT) instead of English
  -h, --help   Print help
```

## `delonix network policy`

> Micro-segmentation: deny/allow traffic between two containers (B14)

```text
Micro-segmentation: deny/allow traffic between two containers (B14)

Usage: delonix network policy [OPTIONS] <ACTION> <CONTAINER_A> <CONTAINER_B>

Arguments:
  <ACTION>       `deny` or `allow`
  <CONTAINER_A>  
  <CONTAINER_B>  

Options:
      --pt-pt  Show help in Portuguese (pt-PT) instead of English
  -h, --help   Print help
```

## `delonix network block`

> Block traffic to/from a container (per-container firewall)

```text
Block traffic to/from a container (per-container firewall)

Usage: delonix network block [OPTIONS] <CONTAINER>

Arguments:
  <CONTAINER>  

Options:
      --pt-pt  Show help in Portuguese (pt-PT) instead of English
  -h, --help   Print help
```

## `delonix network unblock`

> Unblock a previously blocked container

```text
Unblock a previously blocked container

Usage: delonix network unblock [OPTIONS] <CONTAINER>

Arguments:
  <CONTAINER>  

Options:
      --pt-pt  Show help in Portuguese (pt-PT) instead of English
  -h, --help   Print help
```

## `delonix network import-iptables`

> Import and summarize an `iptables-save` file (does not change the host)

```text
Import and summarize an `iptables-save` file (does not change the host)

Usage: delonix network import-iptables [OPTIONS] <FILE>

Arguments:
  <FILE>  

Options:
      --pt-pt  Show help in Portuguese (pt-PT) instead of English
  -h, --help   Print help
```

## `delonix network prune`

> Remove the `delonix0` bridge and Delonix's nft table

```text
Remove the `delonix0` bridge and Delonix's nft table

Usage: delonix network prune [OPTIONS]

Options:
      --pt-pt  Show help in Portuguese (pt-PT) instead of English
  -h, --help   Print help
```
