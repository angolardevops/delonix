# Plataforma de IA (LLM)

O Delonix corre **modelos LLM** em containers e expõe-os pelo **padrão aberto da
OpenAI** — para qualquer cliente ou agente integrar sem adaptações. Junto com o
servidor **MCP**, forma o *harness* de IA do Delonix: **tools** (MCP) + **modelos**
(OpenAI).

## Integração com o Ollama (sem reinventar a roda)

O Ollama já gere modelos e faz inferência, e já fala OpenAI em `/v1`. O Delonix
descobre-o e regista os modelos:

```bash
delonix llm pull llama3.2          # puxa um modelo (via o CLI do ollama)
delonix llm ollama                 # descobre e regista TODOS os modelos do Ollama
delonix llm serve --token SEGREDO  # gateway OpenAI → Ollama
curl http://127.0.0.1:8090/v1/chat/completions \
  -d '{"model":"llama3.2:latest","messages":[{"role":"user","content":"olá"}]}'
```

## Servidor LLM próprio ou backend externo

```bash
# corre um servidor LLM (imagem OpenAI-compatível) com GPU + memória + porta
sudo delonix llm run llama3 ghcr.io/.../llamacpp-server --gpus all --port 8000 -m 8G
sudo delonix llm register externo http://10.0.0.5:8000     # backend externo
delonix llm ls
delonix llm rm llama3
```

## O gateway OpenAI

```bash
delonix llm serve --addr 127.0.0.1:8090
curl http://127.0.0.1:8090/v1/models
```

Serve `/v1/models`, `/v1/chat/completions`, `/v1/completions`, `/v1/embeddings` e
faz **proxy** para o backend do modelo pedido. Características:

- **Streaming** (`stream:true`/SSE token-a-token) — não bufferiza a resposta inteira.
- **`--token`** (Bearer, tempo constante) e **sem seguir redireccionamentos** (anti-SSRF).
- Loopback por omissão — usa `--token` em binds expostos.

## Servidor MCP (agentes de IA)

```bash
delonix mcp        # servidor MCP (stdio) — expõe ferramentas do Delonix a agentes
```

Próximo: [Host remoto](remote.md) · [Referência `llm`](../reference/llm.md).
