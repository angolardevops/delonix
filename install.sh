#!/bin/sh
# Instalador do Delonix Engine — descarrega o binário mais recente, verifica o
# checksum, instala/ACTUALIZA (substitui mesmo se já estiver a correr) e configura
# o autocomplete da shell.
#
#   curl -fsSL https://raw.githubusercontent.com/angolardevops/delonix/main/install.sh | sh
#
# Variáveis: DELONIX_INSTALL_DIR (def. /usr/local/bin)
set -eu

REPO="angolardevops/delonix"
ASSET="delonix-x86_64-linux"
BASE="https://github.com/$REPO/releases/latest/download"
DEST="${DELONIX_INSTALL_DIR:-/usr/local/bin}"

say() { printf '\033[1;38;5;208m›\033[0m %s\n' "$1"; }
err() { printf '\033[1;31m✗\033[0m %s\n' "$1" >&2; exit 1; }

command -v curl >/dev/null 2>&1 || err "preciso de 'curl'."
[ "$(uname -s)" = "Linux" ] || err "o Delonix corre em Linux."
case "$(uname -m)" in x86_64|amd64) : ;; *) err "arquitectura não suportada: $(uname -m) (só x86_64)";; esac

# sudo só se o destino não for escrevível
SUDO=""
if [ ! -w "$DEST" ]; then
  if command -v sudo >/dev/null 2>&1; then SUDO="sudo"; else err "sem permissão de escrita em $DEST e sem sudo."; fi
fi

TMP="$(mktemp -d)"
trap 'rm -rf "$TMP"' EXIT INT TERM

say "A descarregar o Delonix ($ASSET)…"
curl -fSL --proto '=https' "$BASE/$ASSET" -o "$TMP/$ASSET" || err "falha no download do binário."

if curl -fsSL "$BASE/SHA256SUMS" -o "$TMP/SHA256SUMS" 2>/dev/null; then
  say "A verificar o checksum…"
  ( cd "$TMP" && sha256sum -c SHA256SUMS --ignore-missing >/dev/null 2>&1 ) || err "checksum NÃO confere — abortado."
else
  say "(aviso) SHA256SUMS indisponível — a saltar a verificação."
fi

chmod +x "$TMP/$ASSET"
# `mv` (rename atómico) substitui o binário mesmo que esteja A CORRER — evita o
# erro "Text file busy" que o `cp`/`install` (escrita no mesmo inode) daria.
$SUDO mkdir -p "$DEST"
$SUDO mv -f "$TMP/$ASSET" "$DEST/delonix"
say "Instalado: $("$DEST/delonix" --version) em $DEST/delonix"

# ---- autocomplete -------------------------------------------------------
gen() { "$DEST/delonix" completion "$1" 2>/dev/null; }
add_comp() { # $1=shell $2=ficheiro-destino
  d="$(dirname "$2")"
  if [ -d "$d" ] && { [ -w "$d" ] || [ -n "$SUDO" ]; }; then
    if gen "$1" | $SUDO tee "$2" >/dev/null 2>&1; then say "autocomplete $1 → $2"; return 0; fi
  fi
  return 1
}

installed_any=0
# bash
if command -v bash >/dev/null 2>&1; then
  add_comp bash /etc/bash_completion.d/delonix \
    || add_comp bash "${XDG_DATA_HOME:-$HOME/.local/share}/bash-completion/completions/delonix" \
    && installed_any=1
fi
# zsh
if command -v zsh >/dev/null 2>&1; then
  add_comp zsh /usr/share/zsh/site-functions/_delonix \
    || { mkdir -p "$HOME/.zfunc" 2>/dev/null && add_comp zsh "$HOME/.zfunc/_delonix" \
         && say "(zsh) garante 'fpath+=~/.zfunc' e 'autoload -U compinit && compinit' no ~/.zshrc"; } \
    && installed_any=1
fi
# fish
if command -v fish >/dev/null 2>&1; then
  add_comp fish "${XDG_CONFIG_HOME:-$HOME/.config}/fish/completions/delonix.fish" && installed_any=1
fi
[ "$installed_any" = 1 ] && say "Autocomplete instalado — reabre a shell (ou 'source' o teu rc) para activar." \
  || say "Para activar o autocomplete manualmente:  delonix completion bash | sudo tee /etc/bash_completion.d/delonix"

cat <<EOF

  O Delonix está pronto. Próximos passos:

    delonix run alpine echo "olá, mundo"
    delonix serve ui            # painel web em http://127.0.0.1:9444

  Docs: https://angolardevops.github.io/delonix/
EOF
