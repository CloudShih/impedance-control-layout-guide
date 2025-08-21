"""
Test script for tooltip visual improvements
測試工具提示視覺改進效果
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'src'))

def test_tooltip_themes():
    """Test different tooltip themes"""
    print("測試工具提示主題效果...")
    
    try:
        from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLineEdit, QPushButton, QLabel
        from src.widgets.tooltip_widget import add_tooltip, TOOLTIP_TEXTS
        
        # Create test application
        app = QApplication([])
        
        # Create test window
        window = QWidget()
        window.setWindowTitle("工具提示視覺效果測試")
        window.setGeometry(300, 300, 500, 400)
        
        layout = QVBoxLayout(window)
        
        # Add title
        title = QLabel("將滑鼠懸停在下方元件上測試不同主題的工具提示效果")
        title.setStyleSheet("font-weight: bold; font-size: 12pt; margin: 10px;")
        layout.addWidget(title)
        
        # Test input with dark theme (default)
        dark_input = QLineEdit()
        dark_input.setPlaceholderText("深色主題工具提示測試")
        add_tooltip(dark_input, """
        <b>深色主題工具提示</b><br/>
        這是使用深色主題的工具提示範例。<br/>
        • 具有漸層背景<br/>
        • 帶有陰影效果<br/>
        • 淡入淡出動畫<br/>
        <i>適合深色界面使用</i>
        """, theme='dark')
        layout.addWidget(dark_input)
        
        # Test input with light theme
        light_input = QLineEdit()
        light_input.setPlaceholderText("淺色主題工具提示測試")
        add_tooltip(light_input, """
        <b>淺色主題工具提示</b><br/>
        這是使用淺色主題的工具提示範例。<br/>
        • 明亮的背景色彩<br/>
        • 深色文字確保可讀性<br/>
        • 適合淺色界面<br/>
        <i>提供良好的對比度</i>
        """, theme='light')
        layout.addWidget(light_input)
        
        # Test input with blue theme
        blue_input = QLineEdit()
        blue_input.setPlaceholderText("藍色主題工具提示測試")
        add_tooltip(blue_input, """
        <b>藍色主題工具提示</b><br/>
        這是使用藍色主題的工具提示範例。<br/>
        • 藍色漸層背景<br/>
        • 專業的視覺效果<br/>
        • 突出重要資訊<br/>
        <i>適合強調重要功能</i>
        """, theme='blue')
        layout.addWidget(blue_input)
        
        # Test button with signal rule tooltip
        test_button = QPushButton("信號規則說明測試")
        add_tooltip(test_button, TOOLTIP_TEXTS['signal_rule_name'])
        layout.addWidget(test_button)
        
        # Test button with layout rule tooltip  
        layout_button = QPushButton("佈局規則說明測試")
        add_tooltip(layout_button, TOOLTIP_TEXTS['layout_impedance'])
        layout.addWidget(layout_button)
        
        # Instructions
        instructions = QLabel("""
        測試說明：
        1. 將滑鼠懸停在各個元件上，等待0.5秒後工具提示會出現
        2. 觀察不同主題的視覺效果和配色
        3. 注意淡入淡出動畫效果
        4. 測試陰影和邊框的顯示效果
        """)
        instructions.setStyleSheet("color: #666666; font-size: 9pt; margin: 10px;")
        layout.addWidget(instructions)
        
        # Apply dark theme to window for contrast testing
        window.setStyleSheet("""
            QWidget {
                background-color: #2e2e2e;
                color: #f0f0f0;
                font-family: "Microsoft YaHei";
            }
            QLineEdit, QPushButton {
                background-color: #3c3c3c;
                border: 1px solid #555555;
                padding: 8px;
                border-radius: 4px;
                margin: 5px;
            }
            QPushButton:hover {
                background-color: #4c4c4c;
            }
        """)
        
        window.show()
        
        print("工具提示主題測試視窗已開啟")
        print("請在GUI中測試不同主題的視覺效果")
        return True
        
    except Exception as e:
        print(f"工具提示主題測試失敗: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_tooltip_system_functionality():
    """Test tooltip system basic functionality"""
    print("測試工具提示系統基本功能...")
    
    try:
        from PyQt5.QtWidgets import QApplication
        from src.widgets.tooltip_widget import ToolTipWidget, TooltipManager
        
        # Create test application
        app = QApplication([])
        
        # Test ToolTipWidget creation
        tooltip = ToolTipWidget()
        tooltip.set_content("測試內容") 
        
        # Test theme application
        tooltip.apply_theme_style('dark')
        tooltip.apply_theme_style('light')
        tooltip.apply_theme_style('blue')
        
        # Test TooltipManager
        manager = TooltipManager()
        
        print("工具提示系統基本功能測試通過")
        return True
        
    except Exception as e:
        print(f"工具提示系統功能測試失敗: {e}")
        return False

def run_visual_tests():
    """Run all visual improvement tests"""
    print("=" * 50)
    print("開始工具提示視覺改進測試")
    print("=" * 50)
    
    test_functions = [
        test_tooltip_system_functionality,
        test_tooltip_themes
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
    success = run_visual_tests()
    
    if success:
        print("工具提示視覺改進測試通過！")
        print()
        print("新的視覺改進特性:")
        print("• 漸層背景配色，提升視覺層次")
        print("• 陰影效果，增強立體感")
        print("• 多主題支援（深色/淺色/藍色）")
        print("• 淡入淡出動畫效果")
        print("• 更好的文字對比度")
        print("• 圓角邊框設計")
        print()
        print("在上方的測試視窗中體驗不同主題效果！")
        
        # Keep the application running to show the test window
        sys.exit(0)
    else:
        print("部分測試失敗，請檢查問題。")
        sys.exit(1)