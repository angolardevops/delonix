# Delonix Engine

**Delonix** — motor de containers **nativo do kernel, sem *daemon* e num único
binário**, escrito em Rust. Corre, constrói, distribui e orquestra containers OCI
com a ergonomia do Docker e do Podman, e acrescenta protecção do host, um painel
web embebido, um gateway de IA (OpenAI/Ollama) e conformidade OCI + CRI.

📖 **Documentação:** <https://angolardevops.github.io/delonix/>
📦 **Binários:** [Releases](https://github.com/angolardevops/delonix/releases)

## Instalação (um único binário estático)

```bash
curl -fsSL https://raw.githubusercontent.com/angolardevops/delonix/main/install.sh | sh
```

Instala (ou **actualiza**) o binário e configura o **autocomplete**. Correr de
novo actualiza para a última versão. Alternativa manual em
[Instalação](https://angolardevops.github.io/delonix/install/).

## Em 30 segundos

```bash
delonix run alpine echo "olá, mundo"
delonix run -d --network -p 8080:80 nginx
delonix serve ui            # painel web em http://127.0.0.1:9444
```

## Docker · Podman · Delonix

Já sabes Docker ou Podman? Então já sabes Delonix. Ganhas um único binário,
[protecção do host](https://angolardevops.github.io/delonix/concepts/host-protection/),
IA nativa e um painel web. Vê a
[tabela comparativa completa](https://angolardevops.github.io/delonix/compare/).

---

Este repositório aloja a **documentação** (GitHub Pages) e os **binários**
(Releases). A documentação cobre todos os comandos — vê o
[apêndice de referência](https://angolardevops.github.io/delonix/reference/).
