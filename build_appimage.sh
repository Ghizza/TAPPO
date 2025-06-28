#!/bin/bash

set -e

# === CONFIG ===
APP_NAME="tappo"
APP_PY="tappo_1.0.2.py"
ICON_PNG="tappo_icon.png"
VENV_DIR="build_venv"
APPDIR="tappo.AppDir"
OUTPUT_APPIMAGE="${APP_NAME}-x86_64.AppImage"

# === PREPARAZIONE ===
echo "📦 Creo ambiente virtuale isolato..."
python3 -m venv "$VENV_DIR"
source "$VENV_DIR/bin/activate"

echo "⬇️  Installo PyInstaller..."
pip install --upgrade pip
pip install pyinstaller

echo "🛠️  Compilo l'app con PyInstaller..."
pyinstaller --onefile --noconfirm --windowed "$APP_PY" --name "$APP_NAME"

echo "📁 Preparo struttura AppDir..."
mkdir -p "$APPDIR/usr/bin"
mkdir -p "$APPDIR/usr/share/applications"
mkdir -p "$APPDIR/usr/share/icons/hicolor/256x256/apps"

cp "dist/$APP_NAME" "$APPDIR/usr/bin/"
cp "$ICON_PNG" "$APPDIR/usr/share/icons/hicolor/256x256/apps/${APP_NAME}.png"

cat > "$APPDIR/usr/share/applications/${APP_NAME}.desktop" <<EOF
[Desktop Entry]
Name=Tappo
Exec=$APP_NAME
Icon=$APP_NAME
Type=Application
Categories=Utility;
EOF

echo "🔧 Scarico appimagetool se non presente..."
if [ ! -f appimagetool ]; then
    wget -O appimagetool https://github.com/AppImage/AppImageKit/releases/download/continuous/appimagetool-x86_64.AppImage
    chmod +x appimagetool
fi

echo "📦 Creo AppImage..."
./appimagetool "$APPDIR" "$OUTPUT_APPIMAGE"

echo "✅ Fatto! File creato: $OUTPUT_APPIMAGE"
