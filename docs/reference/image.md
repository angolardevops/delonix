# `delonix image`

> Manage images (Docker/Podman compat: `image ls` = `images`)

```text
Manage images (Docker/Podman compat: `image ls` = `images`)

Usage: delonix image [OPTIONS] <COMMAND>

Commands:
  ls     List local images (= `delonix images`)
  build  Build an image (= `delonix build`)
  pull   Pull from an OCI registry or import a `.tar` (= `delonix pull`)
  push   Push a local image to an OCI registry (= `delonix push`)
  rm     Remove an image/tag (= `delonix rmi`)
  tag    Add a tag (= `delonix tag`)
  scan   Scan for vulnerabilities (= `delonix scan`)
  help   Print this message or the help of the given subcommand(s)

Options:
      --pt-pt  Show help in Portuguese (pt-PT) instead of English
  -h, --help   Print help
```

## `delonix image ls`

> List local images (= `delonix images`)

```text
List local images (= `delonix images`)

Usage: delonix image ls [OPTIONS]

Options:
      --pt-pt  Show help in Portuguese (pt-PT) instead of English
  -h, --help   Print help
```

## `delonix image build`

> Build an image (= `delonix build`)

```text
Build an image (= `delonix build`)

Usage: delonix image build [OPTIONS] --tag <TAG>

Options:
  -t, --tag <TAG>          Tag for the built image (`name:tag`)
  -f, --file <FILE>        Path to the build file (default: ./Delonixfile, then ./Dockerfile)
      --scan               Scan the base image (`FROM`) before building
      --fail-on <FAIL_ON>  Abort the build if the base has vulnerabilities >= this severity
      --pt-pt              Show help in Portuguese (pt-PT) instead of English
  -h, --help               Print help
```

## `delonix image pull`

> Pull from an OCI registry or import a `.tar` (= `delonix pull`)

```text
Pull from an OCI registry or import a `.tar` (= `delonix pull`)

Usage: delonix image pull [OPTIONS] <IMAGE>

Arguments:
  <IMAGE>  

Options:
      --pt-pt  Show help in Portuguese (pt-PT) instead of English
  -h, --help   Print help
```

## `delonix image push`

> Push a local image to an OCI registry (= `delonix push`)

```text
Push a local image to an OCI registry (= `delonix push`)

Usage: delonix image push [OPTIONS] <IMAGE> [DESTINATION]

Arguments:
  <IMAGE>        
  [DESTINATION]  

Options:
      --pt-pt  Show help in Portuguese (pt-PT) instead of English
  -h, --help   Print help
```

## `delonix image rm`

> Remove an image/tag (= `delonix rmi`)

```text
Remove an image/tag (= `delonix rmi`)

Usage: delonix image rm [OPTIONS] <IMAGE>

Arguments:
  <IMAGE>  

Options:
      --pt-pt  Show help in Portuguese (pt-PT) instead of English
  -h, --help   Print help
```

## `delonix image tag`

> Add a tag (= `delonix tag`)

```text
Add a tag (= `delonix tag`)

Usage: delonix image tag [OPTIONS] <SOURCE> <TARGET>

Arguments:
  <SOURCE>  
  <TARGET>  

Options:
      --pt-pt  Show help in Portuguese (pt-PT) instead of English
  -h, --help   Print help
```

## `delonix image scan`

> Scan for vulnerabilities (= `delonix scan`)

```text
Scan for vulnerabilities (= `delonix scan`)

Usage: delonix image scan [OPTIONS] [IMAGE]

Arguments:
  [IMAGE]  Image (`name:tag`) to scan (not needed with --update)

Options:
      --sbom               List the SBOM (installed packages) instead of scanning
      --fail-on <FAIL_ON>  Fail (exit 1) if there are vulnerabilities >= this severity
      --update             Sync the CVE feed into the local advisory DB (then used by every scan)
      --feed <FEED>        Feed source for --update: a URL or a file path (or $DELONIX_ADVISORY_FEED)
      --pt-pt              Show help in Portuguese (pt-PT) instead of English
  -h, --help               Print help
```
