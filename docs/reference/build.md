# `delonix build`

> Build an image from a Delonixfile (Dockerfile-compatible)

```text
Build an image from a Delonixfile (Dockerfile-compatible)

Usage: delonix build [OPTIONS] --tag <TAG>

Options:
  -t, --tag <TAG>          Tag for the built image (`name:tag`)
  -f, --file <FILE>        Path to the build file (default: ./Delonixfile, then ./Dockerfile)
      --scan               Scan the base image (`FROM`) before building
      --fail-on <FAIL_ON>  Abort the build if the base has vulnerabilities >= this severity
      --pt-pt              Show help in Portuguese (pt-PT) instead of English
  -h, --help               Print help
```
