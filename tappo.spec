# -*- mode: python ; coding: utf-8 -*-

a = Analysis(
    ['tappo_1.2.0.py'],
    pathex=[],
    binaries=[],
    datas=[('tappo_icon.ico', '.')],  # Aggiunto l'icona ai dati
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='TappoApp',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='tappo_icon.ico',  # Rimossa la lista, basta il path diretto
)