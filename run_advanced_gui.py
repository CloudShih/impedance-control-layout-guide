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
    # Import and run the advanced GUI as a module
    from src.advanced_gui import main
    main()