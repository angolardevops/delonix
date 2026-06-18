# `delonix update`

> Update a container's resource limits / restart policy (live)

```text
Update a container's resource limits / restart policy (live)

Usage: delonix update [OPTIONS] <CONTAINER>

Arguments:
  <CONTAINER>  

Options:
  -m, --memory <MEMORY>    New memory limit (e.g. 256M)
  -c, --cpus <CPUS>        New CPU limit in cores (e.g. 0.5)
      --restart <RESTART>  Restart policy: `no`|`on-failure`|`always`|`unless-stopped`
      --pt-pt              Show help in Portuguese (pt-PT) instead of English
  -h, --help               Print help
```
