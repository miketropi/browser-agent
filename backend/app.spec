# -*- mode: python -*-
import sys
import os
from PyInstaller.utils.hooks import collect_all
from PyInstaller import log as logging
from PyInstaller import compat
from PyInstaller.utils.hooks import collect_dynamic_libs

pydantic_core_bin = collect_dynamic_libs('pydantic_core')

logger = logging.getLogger(__name__)
logger.info("My custom logging message")

block_cipher = None

datas = [
    # React build output
    ("../frontend/dist", "frontend/dist"),
] + pydantic_core_bin

# Add all dependencies
data, binaries, hiddenimports = collect_all('main')

# Add additional hidden imports for Pydantic and other dependencies
additional_imports = [
    'database',
    'log',
    'models',
    'task_db_handle',

    'aiosqlite',
    'sqlalchemy.dialects.sqlite.aiosqlite',
    'sqlalchemy.dialects.sqlite',

    # Pydantic v2
    'pydantic_core',
    'pydantic_core._pydantic_core',
    'pydantic.json',
    'pydantic.deprecated.class_validators',
    'pydantic.deprecated.decorator',
    'pydantic.deprecated.decorator',
    'pydantic.deprecated.parse',
    'pydantic.deprecated.tools',
    'pydantic.deprecated.json',
    'pydantic.deprecated.config',
    'pydantic.deprecated.copy_internals',
    'pydantic.deprecated.v1',
    'pydantic.deprecated.v1.decorator',
    'pydantic.deprecated.v1.json',
    'pydantic.deprecated.v1.parse',
    'pydantic.deprecated.v1.tools',
    'pydantic.deprecated.v1.validators',
    'pydantic.deprecated.v1.config',
    'pydantic.deprecated.v1.copy_internals',
    
    # Langchain
    'langchain_core.tools',
    'langchain_openai.chat_models.base',
    'langchain_core._api.deprecation',
    
    # Other dependencies
    '_sqlite3',
    'sqlite3',
    'aiosqlite.dbapi2',

    'uvicorn.logging',
    'uvicorn.loops',
    'uvicorn.loops.auto',
    'uvicorn.protocols',
    'uvicorn.protocols.http',
    'uvicorn.protocols.websockets',
    'uvicorn.lifespan',
    'uvicorn.lifespan.on',
]

a = Analysis(
    ['main.py'],
    pathex=['.'],
    binaries=binaries,
    datas=datas + data,
    hiddenimports=hiddenimports + additional_imports,
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
    name='app',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,  # Set to False to hide console
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
