"""
Test script for the advanced impedance control GUI
進階阻抗控制GUI測試腳本
"""

import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'src'))

try:
    from src.advanced_gui import main
    
    if __name__ == '__main__':
        print("啟動進階阻抗控制GUI...")
        main()
        
except ImportError as e:
    print(f"導入錯誤: {e}")
    print("請確認所有必要的模組都已正確建立")
    
except Exception as e:
    print(f"啟動錯誤: {e}")
    import traceback
    traceback.print_exc()