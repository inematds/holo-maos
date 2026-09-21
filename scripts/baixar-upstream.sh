#!/usr/bin/env bash
# Baixa o HOLO original (Zubair Trabzada, MIT) em upstream/.
# Não versionamos o código dele aqui: são ~51 MB (MediaPipe wasm + modelos 3D) e o
# repo oficial já existe. Assim a gente acompanha as atualizações dele de graça.
set -euo pipefail
REPO="https://github.com/zubair-trabzada/holo-gestures.git"
DEST="$(cd "$(dirname "$0")/.." && pwd)/upstream"
if [ -d "$DEST/.git" ]; then
  echo "[holo] upstream já existe — atualizando"; git -C "$DEST" pull --ff-only
else
  echo "[holo] clonando $REPO"; git clone --depth 1 "$REPO" "$DEST"
fi
echo "[holo] pronto. Rodar:  cd upstream && python3 server.py   → http://localhost:4890"
echo "[holo] sem câmera:     http://localhost:4890/?sim=1"
echo "[holo] autoteste:      http://localhost:4890/?probe=1  (esperado: 26/26)"
