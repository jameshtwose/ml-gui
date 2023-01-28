# -*- mode: python ; coding: utf-8 -*-
from PyInstaller.utils.hooks import collect_submodules

hiddenimports = ['scipy', 'numpy', 'sklearn',
                'sklearn.utils._typedefs',
                'sklearn.metrics._typedefs',
                'sklearn.metrics._pairwise_distances_reduction._datasets_pair', 
                'sklearn.metrics._pairwise_distances_reduction._middle_term_computer',
                'sklearn.utils._heap',
                'sklearn.utils._sorting',
                'sklearn.utils._vector_sentinel',
                'sklearn.neighbors._partition_nodes']
hiddenimports += collect_submodules('scipy')
hiddenimports += collect_submodules('numpy')
hiddenimports += collect_submodules('sklearn')
hiddenimports += collect_submodules('sklearn.utils._typedefs')
hiddenimports += collect_submodules('sklearn.metrics._typedefs')
hiddenimports += collect_submodules('sklearn.metrics._pairwise_distances_reduction._datasets_pair')
hiddenimports += collect_submodules('sklearn.metrics._pairwise_distances_reduction._middle_term_computer')
hiddenimports += collect_submodules('sklearn.utils._heap')
hiddenimports += collect_submodules('sklearn.utils._sorting')
hiddenimports += collect_submodules('sklearn.utils._vector_sentinel')
hiddenimports += collect_submodules('sklearn.neighbors._partition_nodes')

block_cipher = None


a = Analysis(
    ['mlgui.py'],
    pathex=[],
    binaries=[],
    datas=[],
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='mlgui',
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
)
app = BUNDLE(
    exe,
    name='mlgui.app',
    icon=None,
    bundle_identifier=None,
)
