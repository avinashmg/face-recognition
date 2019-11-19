# -*- mode: python ; coding: utf-8 -*-

block_cipher = None


a = Analysis(['main.py'],
             pathex=['/Users/suryarajendhran/Developer/face-recognition/UI/testDesign'],
             binaries=[],
             datas=[],
             hiddenimports=['PySide2.QtXml'],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          [],
          exclude_binaries=True,
          name='APFS',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          console=False )
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               upx_exclude=[],
               name='APFS')
app = BUNDLE(coll,
             name='APFS.app',
             icon='/Users/suryarajendhran/Developer/face-recognition/UI/testDesign/some.icns',
             bundle_identifier=None,
             info_plist={
        'NSHighResolutionCapable': 'True'
        })
