# `delonix service`

> docker-compose-style stack from a `delonix.yaml` (auto-discovered)

```text
docker-compose-style stack from a `delonix.yaml` (auto-discovered)

Usage: delonix service [OPTIONS] <COMMAND>

Commands:
  up     Start the stack (`delonix-stack.yaml` in the current dir, or `-f`)
  apply  Apply a stack from a file (k8s style; same as `up`)
  down   Stop and remove the stack
  rm     Remove the stack's containers (docker style; same as `down`)
  ps     List the stack's containers
  watch  Supervise the stack: health-probe, restart dead replicas, and drop unhealthy ones from load balancing (loop)
  help   Print this message or the help of the given subcommand(s)

Options:
      --pt-pt  Show help in Portuguese (pt-PT) instead of English
  -h, --help   Print help
```

## `delonix service up`

> Start the stack (`delonix-stack.yaml` in the current dir, or `-f`)

```text
Start the stack (`delonix-stack.yaml` in the current dir, or `-f`)

Usage: delonix service up [OPTIONS]

Options:
  -f, --file <FILE>  
      --dry-run      Show what would run, without starting anything (k8s style)
      --pt-pt        Show help in Portuguese (pt-PT) instead of English
  -h, --help         Print help
```

## `delonix service apply`

> Apply a stack from a file (k8s style; same as `up`)

```text
Apply a stack from a file (k8s style; same as `up`)

Usage: delonix service apply [OPTIONS]

Options:
  -f, --file <FILE>  
      --dry-run      Show what would change, without applying (k8s style)
      --pt-pt        Show help in Portuguese (pt-PT) instead of English
  -h, --help         Print help
```

## `delonix service down`

> Stop and remove the stack

```text
Stop and remove the stack

Usage: delonix service down [OPTIONS]

Options:
  -f, --file <FILE>  
      --pt-pt        Show help in Portuguese (pt-PT) instead of English
  -h, --help         Print help
```

## `delonix service rm`

> Remove the stack's containers (docker style; same as `down`)

```text
Remove the stack's containers (docker style; same as `down`)

Usage: delonix service rm [OPTIONS]

Options:
  -f, --file <FILE>  
      --pt-pt        Show help in Portuguese (pt-PT) instead of English
  -h, --help         Print help
```

## `delonix service ps`

> List the stack's containers

```text
List the stack's containers

Usage: delonix service ps [OPTIONS]

Options:
  -f, --file <FILE>  
      --pt-pt        Show help in Portuguese (pt-PT) instead of English
  -h, --help         Print help
```

## `delonix service watch`

> Supervise the stack: health-probe, restart dead replicas, and drop unhealthy ones from load balancing (loop)

```text
Supervise the stack: health-probe, restart dead replicas, and drop unhealthy ones from load balancing (loop)

Usage: delonix service watch [OPTIONS]

Options:
  -f, --file <FILE>          
      --interval <INTERVAL>  Interval between checks (ms) [default: 2000]
      --once                 Run a single check and exit
      --pt-pt                Show help in Portuguese (pt-PT) instead of English
  -h, --help                 Print help
```
