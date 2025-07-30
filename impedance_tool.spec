# -*- mode: python ; coding: utf-8 -*-
"""
PyInstaller spec file for Impedance Control Layout Guide Generator
阻抗控制佈局指南生成器的PyInstaller配置檔
"""

import os
from pathlib import Path

# Get project root directory
project_root = Path(SPECPATH)
src_dir = project_root / 'src'

block_cipher = None

# Main application analysis
a = Analysis(
    ['src/advanced_gui.py'],  # Entry point script
    pathex=[str(project_root), str(src_dir)],  # Additional paths to search
    binaries=[],
    datas=[
        # Include configuration files
        ('src/config/default_config.yaml', 'src/config/'),
        ('src/config/default_backup/default_config.yaml', 'src/config/default_backup/'),
        
        # Include example configurations
        ('examples/configs/*.yaml', 'examples/configs/'),
        
        # Include documentation
        ('README.md', '.'),
        ('USER_MANUAL.md', '.'),
    ],
    hiddenimports=[
        # PyQt5 modules
        'PyQt5.QtCore',
        'PyQt5.QtGui', 
        'PyQt5.QtWidgets',
        
        # Application modules
        'src.advanced_gui',
        'src.main',
        'src.config.config_manager',
        'src.controllers',
        'src.models',
        'src.views',
        'src.widgets',
        'src.core',
        
        # Data processing modules
        'pandas',
        'numpy',
        'openpyxl',
        'yaml',
        'jsonschema',
        
        # Standard library modules that might be missed
        'pathlib',
        'logging',
        're',
        'json',
        'csv',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        # Exclude testing modules
        'pytest',
        'pytest_cov',
        'tests',
        'test_*',
        
        # Exclude unnecessary modules
        'tkinter',
        'matplotlib',
        'scipy',
    ],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

# Remove duplicate entries
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

# Create executable
exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='阻抗控制佈局指南生成器',  # Executable name
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,  # Use UPX compression
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,  # Hide console window for GUI application
    disable_windowed_traceback=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=None,  # Add icon file if available
    version_file=None,  # Add version info if available
)

# Optional: Create a directory distribution instead of a single file
# Uncomment the following lines if you prefer a directory distribution:
"""
coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='ImpedanceControlTool'
)
"""