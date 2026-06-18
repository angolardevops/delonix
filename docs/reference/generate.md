# `delonix generate`

> Generate integration artifacts (systemd units) — Podman parity

```text
Generate integration artifacts (systemd units) — Podman parity

Usage: delonix generate [OPTIONS] <COMMAND>

Commands:
  systemd      Emit a systemd `.service` unit for an existing container
  systemd-api  Emit a systemd `.service` unit for the REST API (`delonix serve`)
  help         Print this message or the help of the given subcommand(s)

Options:
      --pt-pt  Show help in Portuguese (pt-PT) instead of English
  -h, --help   Print help
```

## `delonix generate systemd`

> Emit a systemd `.service` unit for an existing container

```text
Emit a systemd `.service` unit for an existing container

Usage: delonix generate systemd [OPTIONS] <CONTAINER>

Arguments:
  <CONTAINER>  Container name or id

Options:
      --restart <RESTART>  Restart policy (Restart=always) [default: always]
      --pt-pt              Show help in Portuguese (pt-PT) instead of English
  -h, --help               Print help
```

## `delonix generate systemd-api`

> Emit a systemd `.service` unit for the REST API (`delonix serve`)

```text
Emit a systemd `.service` unit for the REST API (`delonix serve`)

Usage: delonix generate systemd-api [OPTIONS]

Options:
      --addr <ADDR>  Listen address [default: 127.0.0.1:8080]
      --pt-pt        Show help in Portuguese (pt-PT) instead of English
  -h, --help         Print help
```
