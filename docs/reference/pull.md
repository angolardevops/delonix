# `delonix pull`

> Pull an image from an OCI registry (Docker Hub, ghcr.io, ...), or import a `docker save` archive if given a file path

```text
Pull an image from an OCI registry (Docker Hub, ghcr.io, ...), or import a `docker save` archive if given a file path

Usage: delonix pull [OPTIONS] <IMAGE>

Arguments:
  <IMAGE>  Reference (`nginx`, `ghcr.io/owner/app:tag`) or a `.tar` path

Options:
      --verify <VERIFY>  Verify a cosign signature with this public key before pulling
      --pt-pt            Show help in Portuguese (pt-PT) instead of English
  -h, --help             Print help
```
