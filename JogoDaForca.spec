# -*- mode: python ; coding: utf-8 -*-
# Spec multiplataforma: funciona igual no Windows e no Linux.
# Uso: pyinstaller JogoDaForca.spec

a = Analysis(
    ['forca_pygame.py'],
    pathex=[],
    binaries=[],
    datas=[('forca_assets', 'forca_assets')],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=['tkinter', 'unittest', 'pytest'],
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
    name='JogoDaForca',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=False,
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
