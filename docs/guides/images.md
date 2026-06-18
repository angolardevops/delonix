# Imagens

O Delonix usa o formato **OCI** — as imagens são interoperáveis com o Docker e o
Podman. Puxa, constrói, assina, examina e publica.

## Puxar e listar

```bash
delonix pull alpine:3.19
delonix pull ghcr.io/org/app:tag
delonix images                    # lista local
delonix inspect alpine:3.19       # config OCI
```

## Construir

Aceita `Delonixfile` ou `Dockerfile` (mesma sintaxe). Suporta *multi-stage* e
**cache** por hash dos passos.

```dockerfile
# Delonixfile
FROM golang:1.22 AS build
WORKDIR /src
COPY . .
RUN go build -o /app ./cmd

FROM alpine:3.19
COPY --from=build /app /usr/local/bin/app
HEALTHCHECK CMD wget -qO- localhost:8080/health || exit 1
CMD ["app"]
```

```bash
delonix build -t app:1 .
delonix build -t app:1 -f caminho/Delonixfile .
```

Extensões do `Delonixfile` (não existem no Docker): `CPUS`, `MEMORY` e `SECURITY`
embebem limites e postura de segurança na própria imagem.

## Etiquetar, remover, publicar

```bash
delonix tag app:1 registry.example.com/app:1
delonix push registry.example.com/app:1
delonix rmi app:1                 # remove etiqueta/imagem
delonix prune                     # remove órfãos e blobs não referenciados
```

As etiquetas são **únicas**: re-etiquetar **move** a etiqueta (como o Docker).

## Assinatura (cosign/sigstore)

```bash
delonix verify registry.example.com/app:1 --key cosign.pub
delonix pull registry.example.com/app:1 --verify cosign.pub
```

A verificação usa ECDSA P-256 e liga a assinatura ao **digest** (anti-replay). Com
`pull --verify`, o Delonix puxa **pelo digest verificado** — fecha o TOCTOU de uma
etiqueta mutável.

## Vulnerabilidades (scan de CVE)

```bash
delonix scan app:1                       # SBOM (apk/dpkg) + advisories
delonix scan app:1 --fail-on high        # falha o CI se houver CVE alta
delonix scan --update <url|ficheiro>     # actualiza o feed de advisories
```

## Interoperabilidade

- O **Docker puxa e corre** imagens construídas pelo Delonix (OCI image-spec).
- `delonix oci-export <img> <dir>` gera um *bundle* runtime-spec que o **`runc` corre**.

Próximo: [Volumes](volumes.md) · [Compose/Stacks](compose.md).
