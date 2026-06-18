# `delonix update`

> Update a container's resource limits / restart policy (live)

```text
Update a container's resource limits / restart policy (live)

Usage: delonix update [OPTIONS] <CONTAINER>

Arguments:
  <CONTAINER>  

Options:
  -m, --memory <MEMORY>        New memory limit (e.g. 256M)
  -c, --cpus <CPUS>            New CPU limit in cores (e.g. 0.5)
      --restart <RESTART>      Restart policy: `no`|`on-failure`|`always`|`unless-stopped`
  -p, --publish <PUBLISH>      Publish an extra port live: `hostPort:contPort[/proto]` (repeatable)
      --unpublish <UNPUBLISH>  Unpublish a host port live (repeatable)
      --dns <DNS>              Set the container's DNS resolver(s) live: an IP (repeatable)
      --add-host <ADD_HOST>    Add a host entry (link) live: `name:ip` (repeatable)
      --rm-host <RM_HOST>      Remove a host entry (link) live by name (repeatable)
      --pt-pt                  Show help in Portuguese (pt-PT) instead of English
  -h, --help                   Print help
```
