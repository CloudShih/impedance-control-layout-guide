#!/usr/bin/env python3
"""
Simple GUI launcher script for impedance control tool
簡單 GUI 啟動腳本
"""

import sys
from pathlib import Path

# Add src directory to Python path
src_dir = Path(__file__).parent / 'src'
if str(src_dir) not in sys.path:
    sys.path.insert(0, str(src_dir))

if __name__ == '__main__':
    # Import and run the simple GUI
    from src.simple_gui import main
    main()