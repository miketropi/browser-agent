# -*- mode: python -*-
from PyInstaller.utils.hooks import collect_all, collect_data_files

# Include Playwright browsers
playwright_browsers = collect_data_files('playwright')

block_cipher = None

# Special handling for Playwright
def find_playwright_browsers():
    from pathlib import Path
    project_root = Path.cwd()  # Current working directory (project root)
    browser_path = project_root / 'playwright_browsers'
    return [(str(browser_path), 'playwright_browsers')]  # Bundle it into dist/

def get_playwright_data():
    return [('playwright_browsers', 'playwright_browsers')]

# Collect dependencies for specific packages
data = []
binaries = []
hiddenimports = []

# FastAPI/Uvicorn
data += collect_data_files('uvicorn')
hiddenimports += [
    'uvicorn.loops.auto',
    'uvicorn.protocols.http.auto',
    'uvicorn.protocols.websockets.auto'
]

# My libs
hiddenimports += [
    'database',
    'log',
    'models',
    'task_db_handle',
]

# Pydantic
hiddenimports += [
    'pydantic.json',
    'pydantic.typing',
    'pydantic.color',
    'pydantic.deprecated.decorator',
    'pydantic.deprecated.datetime',
    'pydantic.deprecated.json'

    'langchain_openai',
    'importlib.resources',
    'browser_use',
    'browser_use.agent'
]

# SQLAlchemy
hiddenimports += [
    'aiosqlite',
    'sqlalchemy.dialects.sqlite',
    'sqlalchemy.dialects.sqlite.aiosqlite',
    'sqlalchemy.ext.baked',
    'sqlalchemy.cprocessors'
]

# Playwright
hiddenimports += [
    'playwright._impl._browser_type',
    'playwright._impl._connection',
    'playwright.async_api'
]

# playwright_data = collect_all('playwright')[0]

# Combine all components
a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=binaries,
    datas=(
        # get_playwright_data() 
        [('static', './static')]
        # + [('.venv/lib/python3.11/site-packages/browser_use/agent/system_prompt.md', 'browser_use/agent')]
        + [('.venv/lib/python3.11/site-packages/browser_use', 'browser_use')]
        + [('templates/system_prompt.json', 'templates')]
        + [('playwright_browsers', 'playwright_browsers')]
        + [('.env', '.')] 
        + playwright_browsers
        # + collect_data_files('langchain_core')
    ),
    hiddenimports=hiddenimports,
    hookspath=[],
    runtime_hooks=[],
    excludes=[
        '__pycache__',
        'Chromium Framework.framework/Resources'
    ],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)
# 💡 Critical: Filter binaries after analysis
a.binaries = [b for b in a.binaries if 'playwright_browsers' not in b[1]]

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    name='AmebaeSeo',
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
    # Skip codesigning for Playwright browsers
    # codesign_skip=['Chromium', 'chrome_crashpad_handler', 'chromium', 'Chromium Framework.framework'],
)
