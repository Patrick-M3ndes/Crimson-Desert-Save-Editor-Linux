#!/usr/bin/env bash
# =========================================================
# Crimson Desert Save Editor - Linux Quick Launcher
# =========================================================
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"

if [ ! -d ".venv" ]; then
    echo "⚙️ Criando ambiente virtual (.venv)..."
    python3 -m venv .venv || python -m venv .venv
fi

echo "📦 Instalando/Verificando dependências..."
if [ -f ".venv/bin/activate" ]; then
    source .venv/bin/activate
fi

pip install -q -r requirements.txt

echo "🚀 Abrindo o Crimson Desert Save Editor..."
python3 main.py || python main.py
