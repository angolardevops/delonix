#!/usr/bin/env python3
"""Gera a referência de comandos do Delonix a partir do `--help` real do binário.
Uma página por comando de topo (subcomandos inline). Também escreve o nav YAML
da secção Referência para o mkdocs.yml."""
import os, re, subprocess, sys

BIN = os.environ.get("DELONIX_BIN", "/usr/local/bin/delonix")
HERE = os.path.dirname(os.path.abspath(__file__))
REF = os.path.join(HERE, "docs", "reference")
os.makedirs(REF, exist_ok=True)

ANSI = re.compile(r"\x1b\[[0-9;]*m")

def help_of(args):
    env = dict(os.environ, COLUMNS="100", NO_COLOR="1")
    try:
        out = subprocess.run([BIN, *args, "--help"], capture_output=True, text=True, env=env, timeout=10)
        return ANSI.sub("", (out.stdout or out.stderr)).rstrip()
    except Exception as e:
        return f"(sem ajuda: {e})"

def subcommands(text):
    """Extrai nomes de subcomandos da secção Commands: do --help."""
    subs, in_cmds = [], False
    for line in text.splitlines():
        if re.match(r"^\s*Commands:", line):
            in_cmds = True; continue
        if in_cmds:
            if re.match(r"^\s*Options:", line) or not line.strip():
                if re.match(r"^\s*Options:", line): break
                continue
            m = re.match(r"^\s{2,}([a-z][a-z0-9-]+)\b", line)
            if m and m.group(1) != "help":
                subs.append(m.group(1))
    return subs

def first_desc(text):
    """A 1.ª linha não-vazia do --help = descrição curta do comando."""
    for line in text.splitlines():
        if line.strip() and not line.startswith("Usage:"):
            return line.strip()
    return ""

# comandos de topo (do enum Cmd), em ordem temática
TOP = [
    "run","ps","exec","ssh","logs","start","stop","rm","pause","unpause","stats",
    "inspect","top","diff","cp","commit","update","prune","history","healthcheck","events",
    "pull","push","images","build","tag","rmi","login","logout","scan","verify","oci-export",
    "network","volume","pod","service","up","down","scale","autoscale","ingress","convert",
    "container","image","generate","kube",
    "serve","mcp","cri","llm","info","thermal","audit","completion","init",
]

GROUP_TITLES = {
    "run":"Containers","ps":"Containers","exec":"Containers","ssh":"Containers","logs":"Containers",
    "start":"Containers","stop":"Containers","rm":"Containers","pause":"Containers","unpause":"Containers",
    "stats":"Containers","inspect":"Containers","top":"Containers","diff":"Containers","cp":"Containers",
    "commit":"Containers","update":"Containers","prune":"Containers","history":"Containers",
    "healthcheck":"Containers","events":"Containers","container":"Containers",
    "pull":"Imagens","push":"Imagens","images":"Imagens","build":"Imagens","tag":"Imagens",
    "rmi":"Imagens","login":"Imagens","logout":"Imagens","scan":"Imagens","verify":"Imagens",
    "oci-export":"Imagens","image":"Imagens",
    "network":"Rede & orquestração","volume":"Rede & orquestração","pod":"Rede & orquestração",
    "service":"Rede & orquestração","up":"Rede & orquestração","down":"Rede & orquestração",
    "scale":"Rede & orquestração","autoscale":"Rede & orquestração","ingress":"Rede & orquestração",
    "convert":"Rede & orquestração","generate":"Rede & orquestração","kube":"Rede & orquestração",
    "serve":"Plataforma & servidores","mcp":"Plataforma & servidores","cri":"Plataforma & servidores",
    "llm":"Plataforma & servidores","info":"Plataforma & servidores","thermal":"Plataforma & servidores",
    "audit":"Plataforma & servidores","completion":"Plataforma & servidores","init":"Plataforma & servidores",
}

def slug(cmd): return cmd.replace(" ", "-")

pages = []
for cmd in TOP:
    text = help_of([cmd])
    subs = subcommands(text)
    md = [f"# `delonix {cmd}`\n", f"> {first_desc(text)}\n", "```text", text, "```\n"]
    for s in subs:
        st = help_of([cmd, s])
        md += [f"## `delonix {cmd} {s}`\n", f"> {first_desc(st)}\n", "```text", st, "```\n"]
    with open(os.path.join(REF, f"{slug(cmd)}.md"), "w") as f:
        f.write("\n".join(md))
    pages.append((cmd, GROUP_TITLES.get(cmd, "Outros"), len(subs)))

# índice da referência
groups = {}
for cmd, grp, n in pages:
    groups.setdefault(grp, []).append((cmd, n))
idx = ["# Referência de comandos\n",
       "Apêndice de **todos** os comandos e subcomandos do Delonix, gerado a partir "
       "do `--help` real do binário. Cada página inclui o uso completo, flags e subcomandos.\n"]
for grp in ["Containers","Imagens","Rede & orquestração","Plataforma & servidores","Outros"]:
    if grp not in groups: continue
    idx.append(f"## {grp}\n")
    for cmd, n in groups[grp]:
        extra = f" — {n} subcomandos" if n else ""
        idx.append(f"- [`delonix {cmd}`]({slug(cmd)}.md){extra}")
    idx.append("")
with open(os.path.join(REF, "index.md"), "w") as f:
    f.write("\n".join(idx))

# nav YAML para a secção Referência
nav = ["  - Referência:", "      - Visão geral: reference/index.md"]
for grp in ["Containers","Imagens","Rede & orquestração","Plataforma & servidores","Outros"]:
    if grp not in groups: continue
    nav.append(f"      - {grp}:")
    for cmd, n in groups[grp]:
        nav.append(f"          - 'delonix {cmd}': reference/{slug(cmd)}.md")
with open(os.path.join(HERE, "_nav_reference.yml"), "w") as f:
    f.write("\n".join(nav) + "\n")

print(f"gerado: {len(pages)} páginas de referência em {REF}")
print(f"nav em _nav_reference.yml")
