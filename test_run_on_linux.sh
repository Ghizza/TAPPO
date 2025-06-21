#!/bin/bash

# Script per eseguire TAPPO con ambiente virtuale
# Cancellare la cartella tappo_env al termine dei test (non pushare su Github!)

#!/bin/bash

VENV_DIR="tappo_env"

echo "🔧 Preparazione ambiente per TAPPO..."

# Trova l'ultima versione di tappo_v**.py
SCRIPT_NAME=$(ls tappo_v*.py 2>/dev/null | sort -V | tail -n 1)

if [ -z "$SCRIPT_NAME" ]; then
    echo "❌ Nessun file tappo_v*.py trovato nella directory corrente"
    exit 1
fi

echo "📋 Rilevata versione: $SCRIPT_NAME"

# Controlla se l'ambiente virtuale esiste
if [ ! -d "$VENV_DIR" ]; then
    echo "📦 Creazione ambiente virtuale..."
    
    # Installa python3-venv se necessario
    if ! python3 -m venv --help > /dev/null 2>&1; then
        echo "📥 Installazione python3-venv..."
        sudo apt update
        sudo apt install -y python3-venv python3-full
    fi
    
    # Crea l'ambiente virtuale
    python3 -m venv "$VENV_DIR"
    
    # Attiva l'ambiente e installa dipendenze
    source "$VENV_DIR/bin/activate"
    echo "📥 Installazione customtkinter..."
    pip install --upgrade pip
    pip install customtkinter
    
    echo "✅ Ambiente virtuale creato e configurato!"
else
    echo "✅ Ambiente virtuale già esistente"
    source "$VENV_DIR/bin/activate"
fi

# Controlla se Ghostscript è installato
if ! command -v gs &> /dev/null; then
    echo "⚠️  Ghostscript non trovato. Installazione..."
    sudo apt install -y ghostscript
fi

# Esegui TAPPO
echo "🚀 Avvio TAPPO ($SCRIPT_NAME)..."
python "$SCRIPT_NAME"

# Deattiva l'ambiente virtuale
deactivate
echo "👋 Ambiente virtuale disattivato"
