#!/usr/bin/env python3
"""
Advanced GUI launcher script for impedance control tool
進階 GUI 啟動腳本
"""

import sys
from pathlib import Path

# Add src directory to Python path
src_dir = Path(__file__).parent / 'src'
if str(src_dir) not in sys.path:
    sys.path.insert(0, str(src_dir))

if __name__ == '__main__':
    # Run the advanced GUI as a module to properly handle relative imports
    import subprocess
    import os
    
    # Change to project directory and run as module
    project_dir = Path(__file__).parent
    os.chdir(project_dir)
    
    try:
        # Use python -m to run as module - this properly handles relative imports
        subprocess.run([sys.executable, '-m', 'src.advanced_gui'])
    except Exception as e:
        print(f"Failed to start advanced GUI: {e}")
        print("Please run from project root: python -m src.advanced_gui")