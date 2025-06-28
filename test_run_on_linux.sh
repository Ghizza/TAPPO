#!/bin/bash

# Cartella dello script
APP_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENV_DIR="$APP_DIR/venv"
APP_FILE="$APP_DIR/tappo_1.0.2.py"

# Verifica se Python 3 è installato
if ! command -v python3 &> /dev/null; then
    echo "❌ Errore: Python 3 non è installato. Installa con: sudo apt install python3"
    exit 1
fi

# Crea ambiente virtuale se non esiste
if [ ! -d "$VENV_DIR" ]; then
    echo "📦 Creo ambiente virtuale..."
    python3 -m venv "$VENV_DIR"
fi

# Attiva l’ambiente
source "$VENV_DIR/bin/activate"

# Installa CustomTkinter se mancante
if ! python -c "import customtkinter" &> /dev/null; then
    echo "⬇️  Installo customtkinter..."
    pip install --upgrade pip
    pip install customtkinter
fi

# Avvia l’app
echo "🚀 Avvio TAPPO..."
python "$APP_FILE"
