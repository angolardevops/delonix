# `delonix thermal`

> Thermal governor: throttle Delonix's CPU when the host overheats

```text
Thermal governor: throttle Delonix's CPU when the host overheats

Usage: delonix thermal [OPTIONS]

Options:
      --high <HIGH>          High watermark (°C): start cooling at/above this [default: 85]
      --low <LOW>            Low watermark (°C): restore full CPU at/below this [default: 75]
      --floor <FLOOR>        Floor: never throttle below this % of the CPU budget [default: 20]
      --interval <INTERVAL>  Poll interval in seconds [default: 3]
      --once                 Run a single evaluation and exit (for scripts/tests)
      --pt-pt                Show help in Portuguese (pt-PT) instead of English
  -h, --help                 Print help
```
