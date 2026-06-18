# `delonix prune`

> Reclaim space: remove stopped containers, dangling images and orphan blobs

```text
Reclaim space: remove stopped containers, dangling images and orphan blobs

Usage: delonix prune [OPTIONS]

Options:
  -a, --all                    Also remove ALL unused images (not just dangling/untagged)
      --auto                   Only prune if disk usage exceeds --threshold (for scheduled GC)
      --threshold <THRESHOLD>  Disk-usage percentage that triggers --auto (default 80) [default: 80]
      --pt-pt                  Show help in Portuguese (pt-PT) instead of English
  -h, --help                   Print help
```
