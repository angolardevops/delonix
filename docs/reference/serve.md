# `delonix serve`

> Start the REST API (control plane), or the web UI with `serve ui`

```text
Start the REST API (control plane), or the web UI with `serve ui`

Usage: delonix serve [OPTIONS] [TARGET]

Arguments:
  [TARGET]  `ui` launches the embedded web dashboard (Portainer-like); empty = REST API [possible values: ui, api]

Options:
      --addr <ADDR>            Listen address (UI defaults to 127.0.0.1:9444 if unset)
      --token <TOKEN>          Required Bearer token (or `$DELONIX_TOKEN`). No token = open
      --login                  (UI) Require login with internal users (page + sessions; first user bootstraps)
      --tls-cert <TLS_CERT>    TLS server certificate chain (PEM). Enables HTTPS (needs --tls-key)
      --tls-key <TLS_KEY>      TLS server private key (PEM: PKCS#8, RSA or EC)
      --client-ca <CLIENT_CA>  Client CA (PEM): require a client certificate (mTLS)
      --pt-pt                  Show help in Portuguese (pt-PT) instead of English
  -h, --help                   Print help
```
