# `delonix scan`

> Scan an image for vulnerabilities (SBOM + advisories/CVE)

```text
Scan an image for vulnerabilities (SBOM + advisories/CVE)

Usage: delonix scan [OPTIONS] [IMAGE]

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
