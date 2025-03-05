# -*- mode: python ; coding: utf-8 -*-
from PyInstaller.utils.hooks import copy_metadata, collect_submodules

# add commands
datas = [
    ('src/commands', 'commands'),
    ('src/modules', 'modules'),
    ('src/utils', 'utils')
]

# require for inquirer module
datas += copy_metadata('readchar')


a = Analysis(
    ['src/__main__.py'],
    pathex=['src'],
    binaries=[],
    datas=datas,
    hiddenimports=['log', 'inquirer', 'readchar', 'requests'],
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
    name='gitbenchmark',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
