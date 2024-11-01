# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['B:\\TestCasesGeneratorGUI\\tc_generator\\tc_gen.py'],
    pathex=[],
    binaries=[],
    datas=[('B:\\TestCasesGeneratorGUI\\venv\\Lib\\site-packages\\*', 'site-packages/'), ('B:\\TestCasesGeneratorGUI\\venv\\Scripts\\*', 'Scripts/'), ('B:\\TestCasesGeneratorGUI\\tc_generator\\_internal\\icons', 'icons/'), ('B:\\TestCasesGeneratorGUI\\venv\\Lib\\site-packages\\PIL', 'PIL/'), ('B:\\TestCasesGeneratorGUI\\tc_generator', 'tc_generator/')],
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
    [],
    exclude_binaries=True,
    name='tc_gen',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='tc_gen',
)
