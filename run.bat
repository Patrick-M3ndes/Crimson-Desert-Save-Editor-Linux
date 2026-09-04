@echo off
title Crimson Desert Save Editor (Windows Launcher)
cd /d "%~dp0"

if not exist ".venv" (
    echo ⚙️ Criando ambiente virtual Python (.venv)...
    python -m venv .venv
)

echo 📦 Instalando/Verificando dependencias...
call .venv\Scripts\activate
pip install -q -r requirements.txt

echo 🚀 Iniciando o Crimson Desert Save Editor...
python main.py
pause
