"""
Advanced GUI for impedance control tool with configuration editing capabilities
進階阻抗控制工具GUI，具備配置編輯功能
"""

import sys
from pathlib import Path
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QWidget,
    QTabWidget, QMenuBar, QMenu, QAction, QStatusBar, QSplitter,
    QMessageBox, QProgressBar, QLabel, QToolBar
)
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QIcon, QKeySequence

# Import models and controllers
from .models.configuration_model import ConfigurationModel
from .controllers.configuration_controller import ConfigurationController
from .controllers.signal_rule_controller import SignalRuleController
from .controllers.layout_rule_controller import LayoutRuleController
from .controllers.template_mapping_controller import TemplateMappingController

# Import view widgets
from .views.signal_rule_editor import SignalRuleEditor
from .views.layout_rule_editor import LayoutRuleEditor
from .views.template_mapping_editor import TemplateMappingEditor
from .views.netlist_processor import NetlistProcessor
from .widgets.help_panel import HelpPanel


class AdvancedImpedanceControlGUI(QMainWindow):
    """
    Advanced GUI main window with tabbed interface for configuration editing
    進階GUI主視窗，具備標籤式配置編輯介面
    """
    
    def __init__(self):
        super().__init__()
        
        # Initialize models and controllers
        self.config_model = ConfigurationModel()
        self.config_controller = ConfigurationController(self.config_model)
        self.signal_rule_controller = SignalRuleController(self.config_model.signal_rules)
        self.layout_rule_controller = LayoutRuleController(self.config_model.layout_rules)
        self.template_controller = TemplateMappingController(self.config_model.template_mapping)
        
        # Initialize UI
        self.init_ui()
        self.setup_connections()
        self.update_window_title()
        
        # Status tracking
        self.progress_bar = None
        self.status_timer = QTimer()
        self.status_timer.setSingleShot(True)
        self.status_timer.timeout.connect(self.clear_status_message)
    
    def init_ui(self):
        """Initialize the user interface"""
        self.setWindowTitle("阻抗控制佈局指南生成器 - 進階版")
        self.setGeometry(100, 100, 1400, 900)
        
        # Create menu bar
        self.create_menu_bar()
        
        # Create toolbar
        self.create_toolbar()
        
        # Create central widget with splitter
        self.create_central_widget()
        
        # Create status bar
        self.create_status_bar()
        
        # Apply dark theme
        self.apply_dark_theme()
    
    def create_menu_bar(self):
        """Create the menu bar"""
        menubar = self.menuBar()
        
        # File menu
        file_menu = menubar.addMenu('檔案(&F)')
        
        new_action = QAction('新增配置(&N)', self)
        new_action.setShortcut(QKeySequence.New)
        new_action.triggered.connect(self.config_controller.create_new_config)
        file_menu.addAction(new_action)
        
        open_action = QAction('開啟配置(&O)', self)
        open_action.setShortcut(QKeySequence.Open)
        open_action.triggered.connect(self.config_controller.load_config_file)
        file_menu.addAction(open_action)
        
        file_menu.addSeparator()
        
        save_action = QAction('儲存(&S)', self)
        save_action.setShortcut(QKeySequence.Save)
        save_action.triggered.connect(self.config_controller.save_config_file)
        file_menu.addAction(save_action)
        
        save_as_action = QAction('另存新檔(&A)', self)
        save_as_action.setShortcut(QKeySequence.SaveAs)
        save_as_action.triggered.connect(self.config_controller.save_config_file_as)
        file_menu.addAction(save_as_action)
        
        file_menu.addSeparator()
        
        exit_action = QAction('結束(&X)', self)
        exit_action.setShortcut(QKeySequence.Quit)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)
        
        # Edit menu
        edit_menu = menubar.addMenu('編輯(&E)')
        
        undo_action = QAction('復原(&U)', self)
        undo_action.setShortcut(QKeySequence.Undo)
        undo_action.triggered.connect(self.config_controller.undo)
        edit_menu.addAction(undo_action)
        
        redo_action = QAction('重做(&R)', self)
        redo_action.setShortcut(QKeySequence.Redo)
        redo_action.triggered.connect(self.config_controller.redo)
        edit_menu.addAction(redo_action)
        
        edit_menu.addSeparator()
        
        validate_action = QAction('驗證配置(&V)', self)
        validate_action.setShortcut('Ctrl+Shift+V')
        validate_action.triggered.connect(self.config_controller.validate_all_rules)
        edit_menu.addAction(validate_action)
        
        reset_action = QAction('重設為預設值(&D)', self)
        reset_action.triggered.connect(self.confirm_reset_to_defaults)
        edit_menu.addAction(reset_action)
        
        # Tools menu
        tools_menu = menubar.addMenu('工具(&T)')
        
        export_summary_action = QAction('匯出配置摘要(&E)', self)
        export_summary_action.triggered.connect(self.export_config_summary)
        tools_menu.addAction(export_summary_action)
        
        # Help menu
        help_menu = menubar.addMenu('說明(&H)')
        
        about_action = QAction('關於(&A)', self)
        about_action.triggered.connect(self.show_about)
        help_menu.addAction(about_action)
    
    def create_toolbar(self):
        """Create the toolbar"""
        toolbar = self.addToolBar('主要工具列')
        toolbar.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        
        # New config
        new_action = toolbar.addAction('新增')
        new_action.triggered.connect(self.config_controller.create_new_config)
        
        # Open config
        open_action = toolbar.addAction('開啟')
        open_action.triggered.connect(self.config_controller.load_config_file)
        
        # Save config
        save_action = toolbar.addAction('儲存')
        save_action.triggered.connect(self.config_controller.save_config_file)
        
        toolbar.addSeparator()
        
        # Validate
        validate_action = toolbar.addAction('驗證')
        validate_action.triggered.connect(self.config_controller.validate_all_rules)
        
        toolbar.addSeparator()
        
        # Undo/Redo
        undo_action = toolbar.addAction('復原')
        undo_action.triggered.connect(self.config_controller.undo)
        
        redo_action = toolbar.addAction('重做')
        redo_action.triggered.connect(self.config_controller.redo)
    
    def create_central_widget(self):
        """Create the central widget with tabs"""
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Main layout
        main_layout = QHBoxLayout(central_widget)
        
        # Create splitter for overview and main content
        splitter = QSplitter(Qt.Horizontal)
        main_layout.addWidget(splitter)
        
        # Help panel (left panel)
        self.help_panel = HelpPanel()
        self.help_panel.navigateToTab.connect(self.handle_navigation_request)
        splitter.addWidget(self.help_panel)
        
        # Main tab widget (right panel)
        self.tab_widget = QTabWidget()
        splitter.addWidget(self.tab_widget)
        
        # Create editor tabs
        self.create_editor_tabs()
        
        # Connect tab change signal
        self.tab_widget.currentChanged.connect(self.on_tab_changed)
        
        # Set splitter proportions
        splitter.setSizes([300, 1100])
    
    def create_editor_tabs(self):
        """Create the editor tabs"""
        
        # Signal Rules Editor
        self.signal_editor = SignalRuleEditor(
            self.config_model.signal_rules,
            self.signal_rule_controller
        )
        self.tab_widget.addTab(self.signal_editor, "信號規則")
        
        # Layout Rules Editor
        self.layout_editor = LayoutRuleEditor(
            self.config_model.layout_rules,
            self.layout_rule_controller
        )
        self.tab_widget.addTab(self.layout_editor, "佈局規則")
        
        # Template Mapping Editor
        self.template_editor = TemplateMappingEditor(
            self.config_model.template_mapping,
            self.template_controller
        )
        self.tab_widget.addTab(self.template_editor, "模板設定")
        
        # Netlist Processor
        self.netlist_processor = NetlistProcessor(
            self.config_model,
            self.config_controller
        )
        self.tab_widget.addTab(self.netlist_processor, "Netlist處理")
    
    def create_status_bar(self):
        """Create the status bar"""
        self.status_bar = self.statusBar()
        
        # Add permanent widgets to status bar
        self.config_status_label = QLabel("配置: 未載入")
        self.status_bar.addPermanentWidget(self.config_status_label)
        
        # Progress bar (hidden by default)
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        self.status_bar.addWidget(self.progress_bar)
    
    def setup_connections(self):
        """Setup signal connections"""
        
        # Configuration controller signals
        self.config_controller.configLoaded.connect(self.on_config_loaded)
        self.config_controller.configSaved.connect(self.on_config_saved)
        self.config_controller.errorOccurred.connect(self.on_error_occurred)
        self.config_controller.validationCompleted.connect(self.on_validation_completed)
        self.config_controller.operationProgress.connect(self.on_operation_progress)
        
        # Model change signals
        self.config_model.dataChanged.connect(self.on_config_changed)
    
    def on_config_loaded(self, config_path: str):
        """Handle configuration loaded"""
        self.update_window_title()
        self.config_status_label.setText(f"配置: {Path(config_path).name}")
        self.show_status_message(f"配置已載入: {config_path}", 3000)
    
    def on_config_saved(self, config_path: str):
        """Handle configuration saved"""
        self.update_window_title()
        self.config_status_label.setText(f"配置: {Path(config_path).name}")
        self.show_status_message(f"配置已儲存: {config_path}", 3000)
    
    def on_error_occurred(self, error_message: str):
        """Handle error occurred"""
        QMessageBox.critical(self, "錯誤", error_message)
        self.show_status_message(f"錯誤: {error_message}", 5000)
    
    def on_validation_completed(self, success: bool, errors: list):
        """Handle validation completed"""
        if success:
            QMessageBox.information(self, "驗證結果", "配置驗證通過！")
            self.show_status_message("配置驗證通過", 3000)
        else:
            error_text = "\\n".join(errors)
            QMessageBox.warning(self, "驗證失敗", f"發現以下錯誤:\\n\\n{error_text}")
            self.show_status_message(f"驗證失敗，發現 {len(errors)} 個錯誤", 5000)
    
    def on_operation_progress(self, message: str):
        """Handle operation progress"""
        self.show_status_message(message, 2000)
    
    def on_config_changed(self):
        """Handle configuration data changed"""
        self.update_window_title()
    
    def update_window_title(self):
        """Update the window title"""
        base_title = "阻抗控制佈局指南生成器 - 進階版"
        
        if self.config_model.config_file_path:
            file_name = self.config_model.config_file_path.name
            modified_indicator = " *" if self.config_controller.is_modified else ""
            self.setWindowTitle(f"{base_title} - {file_name}{modified_indicator}")
        else:
            modified_indicator = " *" if self.config_controller.is_modified else ""
            self.setWindowTitle(f"{base_title} - 未命名{modified_indicator}")
    
    def show_status_message(self, message: str, timeout: int = 2000):
        """Show a status message"""
        self.status_bar.showMessage(message, timeout)
        
        # Auto-clear after timeout
        self.status_timer.stop()
        self.status_timer.start(timeout)
    
    def clear_status_message(self):
        """Clear the status message"""
        self.status_bar.clearMessage()
    
    def confirm_reset_to_defaults(self):
        """Confirm before resetting to defaults"""
        reply = QMessageBox.question(
            self, "重設配置",
            "確定要重設為預設配置嗎？\\n\\n這將會清空目前所有設定。",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            self.config_controller.reset_to_defaults()
    
    def export_config_summary(self):
        """Export configuration summary"""
        from PyQt5.QtWidgets import QFileDialog
        
        file_path, _ = QFileDialog.getSaveFileName(
            self, "匯出配置摘要",
            str(Path.home() / "impedance_config_summary.json"),
            "JSON Files (*.json);;All Files (*)"
        )
        
        if file_path:
            success = self.config_controller.export_config_summary(Path(file_path))
            if success:
                QMessageBox.information(self, "匯出成功", f"配置摘要已匯出至:\\n{file_path}")
    
    def show_about(self):
        """Show about dialog"""
        about_text = '''
        <h3>阻抗控制佈局指南生成器 - 進階版</h3>
        <p>版本: 2.0.0</p>
        <p>智能阻抗控制佈局指南生成工具，支援完整的配置自定義功能。</p>
        
        <p><b>主要功能:</b></p>
        <ul>
        <li>YAML配置檔案編輯</li>
        <li>信號分類規則自定義</li>
        <li>佈局規則編輯</li>
        <li>Excel模板映射配置</li>
        <li>即時驗證與測試</li>
        </ul>
        
        <p><b>開發時間:</b> 2025年7月</p>
        '''
        
        QMessageBox.about(self, "關於", about_text)
    
    def closeEvent(self, event):
        """Handle window close event"""
        if self.config_controller.is_modified:
            reply = QMessageBox.question(
                self, "結束程式",
                "配置尚未儲存，是否要先儲存？",
                QMessageBox.Save | QMessageBox.Discard | QMessageBox.Cancel,
                QMessageBox.Save
            )
            
            if reply == QMessageBox.Save:
                if self.config_controller.save_config_file():
                    event.accept()
                else:
                    event.ignore()
            elif reply == QMessageBox.Discard:
                event.accept()
            else:
                event.ignore()
        else:
            event.accept()
    
    def on_tab_changed(self, index):
        """Handle tab change to update help panel"""
        if index >= 0:
            tab_name = self.tab_widget.tabText(index)
            self.help_panel.set_context_from_tab(tab_name)
    
    def handle_navigation_request(self, target):
        """Handle navigation requests from help panel"""
        if target == "load_config":
            self.config_controller.load_config_file()
        elif target == "validate_config":
            self.config_controller.validate_all_rules()
        else:
            # Navigate to specific tab
            for i in range(self.tab_widget.count()):
                if self.tab_widget.tabText(i) == target:
                    self.tab_widget.setCurrentIndex(i)
                    break
    
    def apply_dark_theme(self):
        """Apply dark theme to the application"""
        self.setStyleSheet("""
            QMainWindow {
                background-color: #2e2e2e;
                color: #f0f0f0;
            }
            QWidget {
                background-color: #2e2e2e;
                color: #f0f0f0;
                font-family: "Microsoft YaHei", "微軟雅黑";
            }
            QTabWidget::pane {
                border: 1px solid #555555;
                background-color: #3c3c3c;
            }
            QTabBar::tab {
                background-color: #444444;
                color: #f0f0f0;
                padding: 8px 15px;
                margin: 2px;
                border-radius: 3px;
            }
            QTabBar::tab:selected {
                background-color: #555555;
            }
            QTabBar::tab:hover {
                background-color: #666666;
            }
            QMenuBar {
                background-color: #3c3c3c;
                color: #f0f0f0;
                border-bottom: 1px solid #555555;
            }
            QMenuBar::item {
                background-color: transparent;
                padding: 4px 8px;
            }
            QMenuBar::item:selected {
                background-color: #555555;
            }
            QMenu {
                background-color: #3c3c3c;
                color: #f0f0f0;
                border: 1px solid #555555;
            }
            QMenu::item:selected {
                background-color: #555555;
            }
            QToolBar {
                background-color: #3c3c3c;
                border: 1px solid #555555;
                color: #f0f0f0;
            }
            QStatusBar {
                background-color: #3c3c3c;
                color: #f0f0f0;
                border-top: 1px solid #555555;
            }
            QSplitter::handle {
                background-color: #555555;
            }
        """)


def main():
    """Main function to run the advanced GUI"""
    app = QApplication(sys.argv)
    app.setApplicationName("阻抗控制佈局指南生成器")
    app.setApplicationVersion("2.0.0")
    
    window = AdvancedImpedanceControlGUI()
    window.show()
    
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()