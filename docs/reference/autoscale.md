# `delonix autoscale`

> Autoscale a service by CPU usage (k8s HPA style)

```text
Autoscale a service by CPU usage (k8s HPA style)

Usage: delonix autoscale [OPTIONS] <FILE> <SERVICE>

Arguments:
  <FILE>     Path to the stack YAML
  <SERVICE>  Service name

Options:
      --min <MIN>  [default: 1]
      --max <MAX>  [default: 5]
      --cpu <CPU>  Target CPU usage (%) [default: 70]
      --once       Decide once and exit (instead of looping)
      --pt-pt      Show help in Portuguese (pt-PT) instead of English
  -h, --help       Print help
```
