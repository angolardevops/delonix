# Delonix Engine

**Delonix** é um motor de containers **nativo do kernel, sem *daemon* e num único
binário** — escrito em Rust. Corre, constrói, distribui e orquestra containers
OCI com a ergonomia do Docker e do Podman, mas acrescenta o que faltava: **um
host que nunca morre** (governação agregada de CPU/memória/PIDs/I-O), um
**painel web** embebido, um **gateway de IA** compatível com a OpenAI, e
conformidade total **OCI** e **CRI** (Kubernetes).

<div class="grid cards" markdown>

-   :material-flash: __Sem daemon__

    Não há processo de fundo a correr como root. Cada `delonix run` é um processo
    normal — como o Podman, mas levado ao osso.

-   :material-package-variant-closed: __Um único binário__

    Um executável estático de ~4,5 MB. Sem dependências, sem runtime, sem instalador.
    A CLI, a API REST, o servidor MCP, o CRI e o **painel web** vivem todos dentro dele.

-   :material-shield-check: __Seguro por omissão__

    *User namespace*, *seccomp* por allowlist, `NO_NEW_PRIVS`, capabilities reduzidas,
    `/sys` só-leitura e `/proc` mascarado — sem pedir nada.

-   :material-heart-pulse: __O host nunca morre__

    Todos os containers vivem numa `delonix.slice` com um tecto **agregado** de CPU,
    memória, PIDs e I/O de disco. Sob enxurrada, o kernel mata *dentro* da slice — nunca o host.

</div>

## Em 30 segundos

```bash
# instala o binário (uma linha — ver "Instalação")
curl -fsSL https://github.com/angolardevops/delonix/releases/latest/download/delonix-x86_64-linux -o delonix
chmod +x delonix && sudo mv delonix /usr/local/bin/

delonix run alpine echo "olá, mundo"          # corre um container
delonix run -d --network -p 8080:80 nginx     # nginx em segundo plano, porta publicada
delonix ps                                     # lista
delonix serve ui                               # painel web em http://127.0.0.1:9444
```

## Porquê o Delonix?

O Docker trouxe a ergonomia. O Podman tirou o *daemon*. O **Delonix** vai mais
longe: empacota tudo num binário, **protege o host de si próprio** (nenhuma
enxurrada de containers o derruba), traz uma **plataforma de IA** nativa
(modelos LLM + gateway OpenAI + servidor MCP para agentes) e um **painel web**
sem dependências — mantendo a compatibilidade com imagens OCI, com o `runc` e
com o Kubernetes.

Vê a [tabela comparativa Docker · Podman · Delonix](compare.md) para a fotografia completa.

## Por onde começar

<div class="grid cards" markdown>

-   [:material-download: __Instalação__](install.md) — põe o binário a correr.
-   [:material-rocket-launch: __Arranque rápido__](quickstart.md) — o teu primeiro container, imagem e rede.
-   [:material-school: __Guias__](guides/containers.md) — aprende por temas, ao estilo *get started*.
-   [:material-book-open-variant: __Referência de comandos__](reference/index.md) — apêndice de **todos** os comandos.

</div>
