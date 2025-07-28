"""
Quick integration test script to verify the complete workflow.
"""
from pathlib import Path
import sys

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / 'src'))

# Change working directory to src for relative imports
import os
os.chdir(str(Path(__file__).parent / 'src'))

from main import process_netlist_to_excel


def test_integration():
    """Test the complete workflow with sample data."""
    print("開始整合測試...")
    
    # Use existing sample netlist
    netlist_path = Path("../tests/data/sample_netlist.net")
    output_path = Path("../test_output.xlsx")
    
    try:
        if not netlist_path.exists():
            print(f"測試檔案不存在: {netlist_path}")
            return False
            
        # Run the complete pipeline
        result_path = process_netlist_to_excel(
            netlist_path=netlist_path,
            output_path=output_path
        )
        
        if result_path.exists():
            print(f"整合測試成功! 輸出檔案: {result_path}")
            print(f"檔案大小: {result_path.stat().st_size} 位元組")
            return True
        else:
            print("輸出檔案未生成")
            return False
            
    except Exception as e:
        print(f"整合測試失敗: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = test_integration()
    sys.exit(0 if success else 1)