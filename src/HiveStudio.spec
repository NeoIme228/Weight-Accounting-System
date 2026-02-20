# HiveStudio.spec
a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('../data/jsonbase.json', 'data'),
        ('../res/icons', 'res/icons'),
    ],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    cipher=None,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=None)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='Hive Studio',
    debug=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False, 
    codesign_identity=None,
    entitlements_file=None,
    icon='../res/icons/honeycomb.ico'
)