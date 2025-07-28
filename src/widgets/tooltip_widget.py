"""
Custom tooltip widget with enhanced functionality
增強功能的自定義工具提示元件
"""

from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout, QGraphicsDropShadowEffect
from PyQt5.QtCore import QTimer, QPoint, Qt, pyqtSignal
from PyQt5.QtGui import QPalette, QFont, QColor
import typing


class ToolTipWidget(QWidget):
    """
    Custom tooltip widget with rich formatting and delayed display
    支援豐富格式化和延遲顯示的自定義工具提示元件
    """
    
    def __init__(self, parent=None):
        super().__init__(parent, Qt.ToolTip)
        self.setWindowFlags(Qt.ToolTip | Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        
        # Setup UI
        self.init_ui()
        
        # Timer for delayed showing
        self.show_timer = QTimer()
        self.show_timer.setSingleShot(True)
        self.show_timer.timeout.connect(self.show_tooltip)
        
        # Timer for auto-hide
        self.hide_timer = QTimer()
        self.hide_timer.setSingleShot(True)
        self.hide_timer.timeout.connect(self.hide)
        
        self.target_widget = None
        self.tooltip_text = ""
        self.show_delay = 500  # 0.5 seconds
        self.hide_delay = 5000  # 5 seconds
    
    def init_ui(self):
        """Initialize the tooltip UI"""
        self.setFixedWidth(320)
        
        # Main layout
        layout = QVBoxLayout(self)
        layout.setContentsMargins(12, 10, 12, 10)
        
        # Content label
        self.content_label = QLabel()
        self.content_label.setWordWrap(True)
        self.content_label.setAlignment(Qt.AlignLeft | Qt.AlignTop)
        
        # Set font
        font = QFont()
        font.setFamily("Microsoft YaHei")
        font.setPointSize(9)
        self.content_label.setFont(font)
        
        layout.addWidget(self.content_label)
        
        # Apply enhanced styling with better background and shadow effect
        self.apply_theme_style()
        
        # Add drop shadow effect
        self.add_shadow_effect()
    
    def apply_theme_style(self, theme='dark'):
        """Apply theme-based styling to the tooltip"""
        if theme == 'dark':
            # Dark theme with high contrast
            style = """
                ToolTipWidget {
                    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                        stop:0 #505050, stop:1 #404040);
                    border: 2px solid #707070;
                    border-radius: 10px;
                    color: #ffffff;
                }
                QLabel {
                    background-color: transparent;
                    color: #ffffff;
                    padding: 8px;
                    line-height: 1.5;
                }
            """
        elif theme == 'light':
            # Light theme for better contrast
            style = """
                ToolTipWidget {
                    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                        stop:0 #f8f8f8, stop:1 #e8e8e8);
                    border: 2px solid #cccccc;
                    border-radius: 10px;
                    color: #333333;
                }
                QLabel {
                    background-color: transparent;
                    color: #333333;
                    padding: 8px;
                    line-height: 1.5;
                }
            """
        elif theme == 'blue':
            # Blue accent theme
            style = """
                ToolTipWidget {
                    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                        stop:0 #4a90e2, stop:1 #357abd);
                    border: 2px solid #5ba0f2;
                    border-radius: 10px;
                    color: #ffffff;
                }
                QLabel {
                    background-color: transparent;
                    color: #ffffff;
                    padding: 8px;
                    line-height: 1.5;
                }
            """
        else:
            # Default dark theme
            style = """
                ToolTipWidget {
                    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                        stop:0 #505050, stop:1 #404040);
                    border: 2px solid #707070;
                    border-radius: 10px;
                    color: #ffffff;
                }
                QLabel {
                    background-color: transparent;
                    color: #ffffff;
                    padding: 8px;
                    line-height: 1.5;
                }
            """
        
        self.setStyleSheet(style)
    
    def add_shadow_effect(self):
        """Add drop shadow effect to the tooltip"""
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(15)  # 陰影模糊半徑
        shadow.setXOffset(3)      # 水平偏移
        shadow.setYOffset(3)      # 垂直偏移
        shadow.setColor(QColor(0, 0, 0, 150))  # 陰影顏色（黑色，透明度150）
        self.setGraphicsEffect(shadow)
    
    def set_tooltip_for_widget(self, widget: QWidget, text: str, show_delay: int = 500):
        """
        Set tooltip for a specific widget
        為特定元件設定工具提示
        """
        self.target_widget = widget
        self.tooltip_text = text
        self.show_delay = show_delay
        
        # Install event filter on target widget
        widget.installEventFilter(self)
    
    def eventFilter(self, obj, event):
        """Handle events for target widget"""
        if obj == self.target_widget:
            if event.type() == event.Enter:
                self.on_enter()
            elif event.type() == event.Leave:
                self.on_leave()
            elif event.type() == event.MouseMove:
                self.update_position(event.globalPos())
        
        return super().eventFilter(obj, event)
    
    def on_enter(self):
        """Handle mouse enter event"""
        if self.tooltip_text:
            self.show_timer.start(self.show_delay)
    
    def on_leave(self):
        """Handle mouse leave event with fade-out"""
        self.show_timer.stop()
        self.hide_timer.stop()
        self.start_fade_out()
    
    def update_position(self, global_pos: QPoint):
        """Update tooltip position"""
        # Position tooltip near mouse cursor
        x = global_pos.x() + 15
        y = global_pos.y() - 10
        
        # Make sure tooltip stays on screen
        screen = self.screen().availableGeometry()
        
        if x + self.width() > screen.right():
            x = global_pos.x() - self.width() - 15
        
        if y + self.height() > screen.bottom():
            y = global_pos.y() - self.height() + 10
        
        if x < screen.left():
            x = screen.left()
        
        if y < screen.top():
            y = screen.top()
        
        self.move(x, y)
    
    def show_tooltip(self):
        """Show the tooltip with enhanced visual effects"""
        if not self.tooltip_text:
            return
        
        # Set content with improved HTML formatting
        formatted_text = self.format_tooltip_text(self.tooltip_text)
        self.content_label.setText(formatted_text)
        
        # Adjust size based on content with minimum dimensions
        self.adjustSize()
        
        # Ensure minimum size for better appearance
        min_height = max(80, self.height())
        self.setMinimumHeight(min_height)
        
        # Show tooltip with fade-in effect
        self.setWindowOpacity(0.0)
        self.show()
        self.raise_()
        
        # Simple fade-in animation using timer
        self.fade_timer = QTimer()
        self.fade_timer.timeout.connect(self.fade_in_step)
        self.fade_opacity = 0.0
        self.fade_timer.start(20)  # 20ms intervals for smooth animation
        
        # Start auto-hide timer
        self.hide_timer.start(self.hide_delay)
    
    def format_tooltip_text(self, text: str) -> str:
        """Format tooltip text with enhanced styling"""
        # Add consistent styling to HTML content
        styled_text = f"""
        <div style="font-family: Microsoft YaHei; line-height: 1.5;">
            {text}
        </div>
        """
        return styled_text
    
    def fade_in_step(self):
        """Perform fade-in animation step"""
        self.fade_opacity += 0.1
        if self.fade_opacity >= 0.95:
            self.fade_opacity = 0.95
            self.fade_timer.stop()
        self.setWindowOpacity(self.fade_opacity)
    
    def start_fade_out(self):
        """Start fade-out animation"""
        if hasattr(self, 'fade_timer') and self.fade_timer.isActive():
            self.fade_timer.stop()
        
        self.fade_out_timer = QTimer()
        self.fade_out_timer.timeout.connect(self.fade_out_step)
        self.fade_out_opacity = self.windowOpacity()
        self.fade_out_timer.start(20)  # 20ms intervals for smooth animation
    
    def fade_out_step(self):
        """Perform fade-out animation step"""
        self.fade_out_opacity -= 0.15
        if self.fade_out_opacity <= 0.0:
            self.fade_out_opacity = 0.0
            self.fade_out_timer.stop()
            self.hide()
        self.setWindowOpacity(self.fade_out_opacity)
    
    def set_content(self, text: str):
        """Set tooltip content"""
        self.tooltip_text = text


class TooltipManager:
    """
    Global tooltip manager to handle multiple tooltips
    全域工具提示管理器
    """
    
    def __init__(self):
        self.tooltips = {}
        self.current_tooltip = None
    
    def add_tooltip(self, widget: QWidget, text: str, show_delay: int = 500, theme: str = 'dark'):
        """Add tooltip to a widget"""
        tooltip = ToolTipWidget()
        tooltip.apply_theme_style(theme)  # Apply theme before setting up
        tooltip.set_tooltip_for_widget(widget, text, show_delay)
        self.tooltips[widget] = tooltip
    
    def remove_tooltip(self, widget: QWidget):
        """Remove tooltip from a widget"""
        if widget in self.tooltips:
            tooltip = self.tooltips[widget]
            widget.removeEventFilter(tooltip)
            tooltip.deleteLater()
            del self.tooltips[widget]
    
    def clear_all(self):
        """Clear all tooltips"""
        for widget, tooltip in self.tooltips.items():
            widget.removeEventFilter(tooltip)
            tooltip.deleteLater()
        self.tooltips.clear()


# Global tooltip manager instance
_tooltip_manager = TooltipManager()


def add_tooltip(widget: QWidget, text: str, show_delay: int = 500, theme: str = 'dark'):
    """
    Convenience function to add tooltip to any widget
    為任何元件添加工具提示的便利函數
    
    Args:
        widget: Target widget
        text: Tooltip text (supports HTML formatting)
        show_delay: Delay in milliseconds before showing (default: 500ms)
        theme: Visual theme ('dark', 'light', 'blue')
    """
    _tooltip_manager.add_tooltip(widget, text, show_delay, theme)


def remove_tooltip(widget: QWidget):
    """Remove tooltip from widget"""
    _tooltip_manager.remove_tooltip(widget)


def clear_all_tooltips():
    """Clear all tooltips"""
    _tooltip_manager.clear_all()


# Predefined tooltip texts for common fields
TOOLTIP_TEXTS = {
    # Signal Rule Editor tooltips
    'signal_rule_name': """
    <b>規則名稱</b><br/>
    定義信號分類規則的名稱，例如 "I2C", "SPI", "USB" 等。<br/>
    <i>注意：名稱必須是唯一的，不能與現有規則重複。</i>
    """,
    
    'signal_category': """
    <b>信號類別</b><br/>
    定義信號所屬的大類別，常見類別包括：<br/>
    • Communication Interface - 通訊介面<br/>
    • High Speed Interface - 高速介面<br/>
    • RF - 射頻信號<br/>
    • Power - 電源信號<br/>
    • Clock - 時鐘信號
    """,
    
    'signal_type': """
    <b>信號類型</b><br/>
    定義信號的電氣特性，常見類型包括：<br/>
    • Single-End - 單端信號<br/>
    • Differential - 差分信號<br/>
    • I2C - I2C通訊協定<br/>
    • SPI - SPI通訊協定<br/>
    • Power - 電源信號<br/>
    • Clock - 時鐘信號
    """,
    
    'signal_priority': """
    <b>優先級</b><br/>
    設定規則的匹配優先級 (0-100)。<br/>
    數值越高，優先級越高。當多個規則都符合同一個網路名稱時，<br/>
    系統會選擇優先級最高的規則。<br/>
    <i>建議：I2C/SPI等通訊介面設為10，高速信號設為15-20。</i>
    """,
    
    'signal_keywords': """
    <b>關鍵字匹配</b><br/>
    輸入用逗號分隔的關鍵字列表，例如："I2C, SCL, SDA"<br/>
    系統會檢查網路名稱是否包含這些關鍵字。<br/>
    <i>匹配方式：不區分大小寫的子字串匹配。</i>
    """,
    
    'signal_patterns': """
    <b>正則表達式模式</b><br/>
    每行輸入一個正則表達式模式，用於精確匹配網路名稱。<br/>
    常用模式範例：<br/>
    • .*I2C.* - 匹配包含I2C的所有名稱<br/>
    • ^USB_D[PM]$ - 精確匹配USB_DP或USB_DM<br/>
    • CLK[0-9]+ - 匹配CLK後面跟數字的名稱
    """,
    
    'signal_description': """
    <b>規則描述</b><br/>
    對此規則的詳細說明，包括使用場景、注意事項等。<br/>
    這個描述會顯示在生成的佈局指南中，幫助工程師理解設計要求。
    """,
    
    # Layout Rule Editor tooltips
    'layout_impedance': """
    <b>阻抗控制</b><br/>
    設定走線的特徵阻抗，常見值：<br/>
    • 50 Ohm - 單端信號標準阻抗<br/>
    • 90 Ohm - USB差分阻抗<br/>
    • 100 Ohm - 高速差分信號標準阻抗<br/>
    <i>格式：數值 + 單位（Ohm 或 Ω）</i>
    """,
    
    'layout_width': """
    <b>走線寬度</b><br/>
    設定走線的寬度要求，通常以mil為單位。<br/>
    常見設定：<br/>
    • 5 mil - 一般信號線<br/>
    • 計算值 - 根據阻抗要求計算的寬度<br/>
    <i>1 mil = 0.0254 mm</i>
    """,
    
    'layout_spacing': """
    <b>走線間距</b><br/>
    設定走線之間的最小間距要求。<br/>
    常見設定：<br/>
    • 3W spacing - 3倍線寬間距<br/>
    • 5W spacing - 5倍線寬間距（高頻信號）<br/>
    • 具體數值 - 如 "0.1mm"
    """,
    
    # Template Mapping tooltips
    'template_column_internal': """
    <b>內部欄位名稱</b><br/>
    系統內部使用的欄位識別名稱，不會顯示給最終用戶。<br/>
    常見內部名稱：<br/>
    • Net_Name - 網路名稱<br/>
    • Category - 信號類別<br/>
    • Impedance - 阻抗要求<br/>
    • Description - 描述說明
    """,
    
    'template_column_display': """
    <b>顯示欄位名稱</b><br/>
    在最終Excel檔案中顯示的欄位標題。<br/>
    可以使用中文或英文，建議使用易懂的描述性名稱。<br/>
    <i>例如："網路名稱", "Pin (MT7921)", "阻抗要求"</i>
    """,
    
    # Netlist Processor tooltips
    'netlist_input_file': """
    <b>Netlist 輸入檔案</b><br/>
    選擇要處理的網表檔案，支援格式：<br/>
    • .net - 標準網表格式<br/>
    • .sp - SPICE網表格式<br/>
    • .cir - 電路網表格式<br/>
    • .txt - 文字格式網表<br/>
    <i>檔案應包含網路名稱清單，每行一個名稱。</i>
    """,
    
    'netlist_output_file': """
    <b>Excel 輸出檔案</b><br/>
    指定生成的佈局指南Excel檔案的儲存位置。<br/>
    系統會根據目前的配置規則，將網路分類並套用對應的佈局要求，<br/>
    最終生成包含完整設計指南的Excel檔案。<br/>
    <i>建議使用 .xlsx 格式以獲得最佳相容性。</i>
    """
}