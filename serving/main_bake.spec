# -*- mode: python ; coding: utf-8 -*-


block_cipher = None

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[(R'C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v11.6\bin\cublas64_11.dll','.'),
	(R'C:\ProgramData\Anaconda3\envs\face\Lib\site-packages\faiss_cpu.libs\openblas-34e6e391ae70f97921193cc485380a5a.dll','.'),
	(R'C:\ProgramData\Anaconda3\envs\face\Lib\site-packages\faiss_cpu.libs\libomp-10696628d5be958139abcbad98e18607.dll','.'),
	(R'C:\ProgramData\Anaconda3\envs\face\Lib\site-packages\faiss_cpu.libs\flangrti-928596d9cbd274cc0ca9d378992f02e2.dll','.'),
	(R'C:\ProgramData\Anaconda3\envs\face\Lib\site-packages\faiss_cpu.libs\flang-6eb4555b6a5a30f68c242ed302be298b.dll','.'),],
    datas=[('facelib','facelib'),('lib','lib'),('static','static'),
	('logs','logs'),('model','model'),('config.yml','.'),('models/DB.sqlite','models')],
    hiddenimports=['tortoise.backends.sqlite','main'],
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
    [],
    exclude_binaries=True,
    name='main',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
	icon=r'C:\Users\Administrator\Downloads\face.ico'
)
coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='main',
)
