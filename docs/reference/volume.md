# `delonix volume`

> Manage named volumes

```text
Manage named volumes

Usage: delonix volume [OPTIONS] <COMMAND>

Commands:
  create   Create a named volume (`--driver nfs --device server:/export` for NFS/TrueNAS)
  ls       List volumes
  inspect  Inspect a volume
  rm       Remove a volume (and its data)
  help     Print this message or the help of the given subcommand(s)

Options:
      --pt-pt  Show help in Portuguese (pt-PT) instead of English
  -h, --help   Print help
```

## `delonix volume create`

> Create a named volume (`--driver nfs --device server:/export` for NFS/TrueNAS)

```text
Create a named volume (`--driver nfs --device server:/export` for NFS/TrueNAS)

Usage: delonix volume create [OPTIONS] <NAME>

Arguments:
  <NAME>  

Options:
      --driver <DRIVER>  Driver: `local` (default) or `nfs` [default: local]
      --device <DEVICE>  For `nfs`: the export (`server:/path`)
      --opt <OPT>        Mount options (`mount -o ...`), e.g. `vers=4,ro`
      --pt-pt            Show help in Portuguese (pt-PT) instead of English
  -h, --help             Print help
```

## `delonix volume ls`

> List volumes

```text
List volumes

Usage: delonix volume ls [OPTIONS]

Options:
      --pt-pt  Show help in Portuguese (pt-PT) instead of English
  -h, --help   Print help
```

## `delonix volume inspect`

> Inspect a volume

```text
Inspect a volume

Usage: delonix volume inspect [OPTIONS] <NAME>

Arguments:
  <NAME>  

Options:
      --pt-pt  Show help in Portuguese (pt-PT) instead of English
  -h, --help   Print help
```

## `delonix volume rm`

> Remove a volume (and its data)

```text
Remove a volume (and its data)

Usage: delonix volume rm [OPTIONS] <NAME>

Arguments:
  <NAME>  

Options:
      --pt-pt  Show help in Portuguese (pt-PT) instead of English
  -h, --help   Print help
```
