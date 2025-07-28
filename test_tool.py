"""
Quick test script to verify tool functionality.
"""
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / 'src'))

def quick_test():
    """Run a quick functionality test."""
    print("=== 阻抗控制工具快速測試 ===")
    
    try:
        from main import process_netlist_to_excel
        
        # Test with sample data
        netlist_path = Path("tests/data/sample_netlist.net")
        output_path = Path("quick_test_output.xlsx")
        
        if not netlist_path.exists():
            print("錯誤: 測試檔案不存在")
            return False
        
        print("正在處理範例檔案...")
        result_path = process_netlist_to_excel(
            netlist_path=netlist_path,
            output_path=output_path
        )
        
        if result_path.exists():
            file_size = result_path.stat().st_size
            print("測試成功!")
            print(f"輸出檔案: {result_path}")
            print(f"檔案大小: {file_size} bytes")
            print()
            print("工具已準備就緒! 使用方法:")
            print("   GUI:     python src/simple_gui.py")
            print("   命令列:   python src/main.py your_file.net -o output.xlsx")
            return True
        else:
            print("錯誤: 輸出檔案未生成")
            return False
            
    except Exception as e:
        print(f"測試失敗: {e}")
        return False

if __name__ == "__main__":
    success = quick_test()
    if not success:
        print()
        print("請確認:")
        print("1. Python 3.8+ 已安裝")
        print("2. 必要套件已安裝: pip install pandas openpyxl pyyaml")
        print("3. 在正確目錄執行此腳本")
        sys.exit(1)