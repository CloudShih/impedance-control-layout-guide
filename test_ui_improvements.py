"""
Test script for UI improvements (tooltips and help panel)
測試用戶界面改進功能
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / 'src'))

def test_tooltip_system():
    """Test tooltip system functionality"""
    print("測試工具提示系統...")
    
    try:
        from PyQt5.QtWidgets import QApplication, QWidget, QLineEdit, QVBoxLayout
        from src.widgets.tooltip_widget import add_tooltip, TOOLTIP_TEXTS
        
        # Create a test application
        app = QApplication([])
        
        # Create test widget
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        # Create test input field
        test_input = QLineEdit()
        test_input.setPlaceholderText("測試輸入欄位")
        
        # Add tooltip
        add_tooltip(test_input, TOOLTIP_TEXTS['signal_rule_name'])
        
        layout.addWidget(test_input)
        widget.setWindowTitle("工具提示測試")
        
        print("工具提示系統測試通過")
        return True
        
    except Exception as e:
        print(f"工具提示系統測試失敗: {e}")
        return False

def test_help_panel():
    """Test help panel functionality"""
    print("測試操作教學面板...")
    
    try:
        from PyQt5.QtWidgets import QApplication
        from src.widgets.help_panel import HelpPanel
        
        # Create a test application
        app = QApplication([])
        
        # Create help panel
        help_panel = HelpPanel()
        
        # Test context switching
        help_panel.switch_context("signal")
        help_panel.switch_context("layout")
        help_panel.switch_context("overview")
        
        print("操作教學面板測試通過")
        return True
        
    except Exception as e:
        print(f"操作教學面板測試失敗: {e}")
        return False

def test_advanced_gui_integration():
    """Test advanced GUI with new improvements"""
    print("測試進階GUI整合...")
    
    try:
        from PyQt5.QtWidgets import QApplication
        from src.advanced_gui import AdvancedImpedanceControlGUI
        
        # Create a test application
        app = QApplication([])
        
        # Create advanced GUI
        gui = AdvancedImpedanceControlGUI()
        
        # Test help panel integration
        assert hasattr(gui, 'help_panel'), "GUI should have help panel"
        
        # Test tab switching
        gui.tab_widget.setCurrentIndex(0)  # Signal rules tab
        gui.tab_widget.setCurrentIndex(1)  # Layout rules tab
        
        print("進階GUI整合測試通過")
        return True
        
    except Exception as e:
        print(f"進階GUI整合測試失敗: {e}")
        import traceback
        traceback.print_exc()
        return False

def run_all_ui_tests():
    """Run all UI improvement tests"""
    print("=" * 50)
    print("開始用戶界面改進測試")
    print("=" * 50)
    
    test_functions = [
        test_tooltip_system,
        test_help_panel,
        test_advanced_gui_integration
    ]
    
    passed = 0
    failed = 0
    
    for test_func in test_functions:
        try:
            if test_func():
                passed += 1
            else:
                failed += 1
        except Exception as e:
            print(f"測試異常 {test_func.__name__}: {e}")
            failed += 1
        print()
    
    print("=" * 50)
    print(f"測試結果: {passed} 通過, {failed} 失敗")
    print("=" * 50)
    
    return failed == 0

if __name__ == "__main__":
    success = run_all_ui_tests()
    
    if success:
        print("所有UI改進測試通過！")
        print()
        print("新功能說明:")
        print("1. 浮動提示視窗: 將滑鼠懸停在輸入欄位上0.5秒後會顯示詳細說明")
        print("2. 操作教學面板: 左側區域現在顯示上下文相關的操作指南")
        print("3. 智能導航: 教學面板中的快速操作按鈕可以直接跳轉到相關功能")
        print()
        print("啟動進階GUI來體驗新功能:")
        print("python test_advanced_gui.py")
        
        sys.exit(0)
    else:
        print("部分測試失敗，請檢查問題。")
        sys.exit(1)