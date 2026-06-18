# `delonix llm`

> Run LLM models natively + an OpenAI-compatible gateway (AI platform)

```text
Run LLM models natively + an OpenAI-compatible gateway (AI platform)

Usage: delonix llm [OPTIONS] <COMMAND>

Commands:
  run       Run an LLM-serving container (GPU + memory + published port) and register it
  ollama    Integrate a running Ollama: discover its models and register them all
  pull      Pull a model into Ollama (uses the `ollama` CLI — não reinventa a roda)
  register  Register an external OpenAI-compatible backend as a model
  ls        List registered LLM models
  rm        Remove a model from the registry
  serve     Start the OpenAI-compatible gateway (/v1/models, /v1/chat/completions, ...)
  help      Print this message or the help of the given subcommand(s)

Options:
      --pt-pt  Show help in Portuguese (pt-PT) instead of English
  -h, --help   Print help
```

## `delonix llm run`

> Run an LLM-serving container (GPU + memory + published port) and register it

```text
Run an LLM-serving container (GPU + memory + published port) and register it

Usage: delonix llm run [OPTIONS] <NAME> <IMAGE> [COMMAND]...

Arguments:
  <NAME>        Model name (also the container name)
  <IMAGE>       Container image (an OpenAI-compatible server: llama.cpp/vLLM/ollama/...)
  [COMMAND]...  Extra command/args for the server (after the image)

Options:
      --port <PORT>      Port the server listens on (published to localhost) [default: 8000]
  -m, --memory <MEMORY>  Memory limit (default 4G — LLMs são pesados) [default: 4G]
      --gpus <GPUS>      Expose GPUs (`all`/`nvidia`/`dri`)
      --pt-pt            Show help in Portuguese (pt-PT) instead of English
  -h, --help             Print help
```

## `delonix llm ollama`

> Integrate a running Ollama: discover its models and register them all

```text
Integrate a running Ollama: discover its models and register them all

Usage: delonix llm ollama [OPTIONS]

Options:
      --addr <ADDR>  Ollama API address [default: 127.0.0.1:11434]
      --pt-pt        Show help in Portuguese (pt-PT) instead of English
  -h, --help         Print help
```

## `delonix llm pull`

> Pull a model into Ollama (uses the `ollama` CLI — não reinventa a roda)

```text
Pull a model into Ollama (uses the `ollama` CLI — não reinventa a roda)

Usage: delonix llm pull [OPTIONS] <MODEL>

Arguments:
  <MODEL>  Model name (e.g. `llama3.2`)

Options:
      --pt-pt  Show help in Portuguese (pt-PT) instead of English
  -h, --help   Print help
```

## `delonix llm register`

> Register an external OpenAI-compatible backend as a model

```text
Register an external OpenAI-compatible backend as a model

Usage: delonix llm register [OPTIONS] <NAME> <BACKEND>

Arguments:
  <NAME>     Model name
  <BACKEND>  Backend base URL (e.g. http://127.0.0.1:8000)

Options:
      --pt-pt  Show help in Portuguese (pt-PT) instead of English
  -h, --help   Print help
```

## `delonix llm ls`

> List registered LLM models

```text
List registered LLM models

Usage: delonix llm ls [OPTIONS]

Options:
      --pt-pt  Show help in Portuguese (pt-PT) instead of English
  -h, --help   Print help
```

## `delonix llm rm`

> Remove a model from the registry

```text
Remove a model from the registry

Usage: delonix llm rm [OPTIONS] <NAME>

Arguments:
  <NAME>  Model name

Options:
      --pt-pt  Show help in Portuguese (pt-PT) instead of English
  -h, --help   Print help
```

## `delonix llm serve`

> Start the OpenAI-compatible gateway (/v1/models, /v1/chat/completions, ...)

```text
Start the OpenAI-compatible gateway (/v1/models, /v1/chat/completions, ...)

Usage: delonix llm serve [OPTIONS]

Options:
      --addr <ADDR>    Listen address [default: 127.0.0.1:8090]
      --token <TOKEN>  Require `Authorization: Bearer <token>` (recommended for non-loopback binds)
      --pt-pt          Show help in Portuguese (pt-PT) instead of English
  -h, --help           Print help
```
