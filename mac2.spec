# -*- mode: python ; coding: utf-8 -*-

block_cipher = None


a = Analysis(['mac2.py'],
             pathex=['/Users/tommaso/Desktop/apple'],
             binaries=[('/usr/local/lib/libavbin.11.dylib','.')],
             datas=[('/usr/local/lib/libavbin.11.dylib','.'),
		    ('/anaconda3/lib/python3.6/site-packages/imageio/plugins/avbin.py', '.')],
             hiddenimports=[],
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
          a.binaries,
          a.zipfiles,
          a.datas,
          [],
          name='mac2',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          runtime_tmpdir=None,
          console=True,
	  icon='/Users/tommaso/Desktop/apple/smile.icns' )
