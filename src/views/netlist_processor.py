"""
Netlist Processor widget
Netlist處理器
"""

import sys
from pathlib import Path
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QLineEdit, QTextEdit, QFileDialog, QProgressBar, QGroupBox
)
from PyQt5.QtCore import QThread, pyqtSignal

from models.configuration_model import ConfigurationModel
from controllers.configuration_controller import ConfigurationController
from widgets.tooltip_widget import add_tooltip, TOOLTIP_TEXTS

# Import the main processing function
# Handle both development and PyInstaller environments
if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
    # Running in PyInstaller bundle - src is already in sys.path
    pass
else:
    # Running in development
    sys.path.append(str(Path(__file__).parent.parent))
from main import process_netlist_to_excel


class NetlistProcessingThread(QThread):
    """Background thread for netlist processing"""
    finished = pyqtSignal(str)  # output file path
    error = pyqtSignal(str)     # error message
    progress = pyqtSignal(str)  # progress message
    
    def __init__(self, netlist_path, output_path, config_model):
        super().__init__()
        self.netlist_path = netlist_path
        self.output_path = output_path
        self.config_model = config_model
    
    def run(self):
        try:
            self.progress.emit("開始處理 Netlist...")
            
            # Save current config to temporary file for processing
            import tempfile
            with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as temp_config:
                self.config_model.save_config(Path(temp_config.name))
                temp_config_path = Path(temp_config.name)
            
            # Process netlist using the main function
            result_path = process_netlist_to_excel(
                netlist_path=Path(self.netlist_path),
                output_path=Path(self.output_path) if self.output_path else None,
                config_path=temp_config_path
            )
            
            # Clean up temporary file
            temp_config_path.unlink()
            
            self.finished.emit(str(result_path))
            
        except Exception as e:
            self.error.emit(str(e))


class NetlistProcessor(QWidget):
    def __init__(self, config_model: ConfigurationModel, 
                 controller: ConfigurationController):
        super().__init__()
        self.config_model = config_model
        self.controller = controller
        self.processing_thread = None
        
        self.init_ui()
        self.setup_connections()
    
    def init_ui(self):
        """Initialize the user interface"""
        layout = QVBoxLayout(self)
        
        # Title
        title_label = QLabel("Netlist 處理器")
        title_label.setAutoFillBackground(True)
        title_label.setStyleSheet("font-weight: bold; font-size: 14px; color: white; padding: 5px; background: #2b2b2b; border: none;")
        layout.addWidget(title_label)
        
        # Input group
        input_group = QGroupBox("輸入設定")
        input_layout = QVBoxLayout(input_group)
        
        # Netlist file selection
        netlist_layout = QHBoxLayout()
        netlist_layout.addWidget(QLabel("Netlist 檔案:"))
        
        self.netlist_input = QLineEdit()
        self.netlist_input.setPlaceholderText("選擇 Netlist 檔案 (.net, .sp, .cir, .txt)")
        add_tooltip(self.netlist_input, TOOLTIP_TEXTS['netlist_input_file'])
        netlist_layout.addWidget(self.netlist_input)
        
        self.browse_netlist_btn = QPushButton("瀏覽...")
        self.browse_netlist_btn.clicked.connect(self.browse_netlist_file)
        netlist_layout.addWidget(self.browse_netlist_btn)
        
        input_layout.addLayout(netlist_layout)
        
        # Output file selection
        output_layout = QHBoxLayout()
        output_layout.addWidget(QLabel("輸出檔案:"))
        
        self.output_input = QLineEdit()
        self.output_input.setPlaceholderText("選擇輸出 Excel 檔案位置")
        add_tooltip(self.output_input, TOOLTIP_TEXTS['netlist_output_file'])
        output_layout.addWidget(self.output_input)
        
        self.browse_output_btn = QPushButton("另存為...")
        self.browse_output_btn.clicked.connect(self.browse_output_file)
        output_layout.addWidget(self.browse_output_btn)
        
        input_layout.addLayout(output_layout)
        layout.addWidget(input_group)
        
        # Processing controls
        controls_layout = QHBoxLayout()
        
        self.process_btn = QPushButton("生成佈局指南")
        self.process_btn.clicked.connect(self.start_processing)
        controls_layout.addWidget(self.process_btn)
        
        controls_layout.addStretch()
        layout.addLayout(controls_layout)
        
        # Progress bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        layout.addWidget(self.progress_bar)
        
        # Status display
        status_group = QGroupBox("處理狀態")
        status_layout = QVBoxLayout(status_group)
        
        self.status_text = QTextEdit()
        self.status_text.setReadOnly(True)
        self.status_text.setMaximumHeight(200)
        status_layout.addWidget(self.status_text)
        
        layout.addWidget(status_group)
        
        layout.addStretch()
    
    def setup_connections(self):
        """Setup signal connections"""
        pass
    
    def browse_netlist_file(self):
        """Browse for netlist file"""
        file_path, _ = QFileDialog.getOpenFileName(
            self, "選擇 Netlist 檔案", "",
            "Netlist Files (*.net *.sp *.cir *.txt);;All Files (*)"
        )
        if file_path:
            self.netlist_input.setText(file_path)
    
    def browse_output_file(self):
        """Browse for output file"""
        file_path, _ = QFileDialog.getSaveFileName(
            self, "儲存 Excel 檔案", "",
            "Excel Files (*.xlsx);;All Files (*)"
        )
        if file_path:
            if not file_path.endswith('.xlsx'):
                file_path += '.xlsx'
            self.output_input.setText(file_path)
    
    def start_processing(self):
        """Start netlist processing"""
        netlist_path = self.netlist_input.text().strip()
        output_path = self.output_input.text().strip()
        
        # Validate inputs
        if not netlist_path:
            self.status_text.append("❌ 錯誤: 請選擇 Netlist 檔案")
            return
        
        if not Path(netlist_path).exists():
            self.status_text.append("❌ 錯誤: Netlist 檔案不存在")
            return
        
        # Validate configuration first
        errors = self.config_model.validate_config()
        if errors:
            self.status_text.append("❌ 配置驗證失敗:")
            for error in errors[:5]:  # Show first 5 errors
                self.status_text.append(f"  • {error}")
            if len(errors) > 5:
                self.status_text.append(f"  ... 還有 {len(errors) - 5} 個錯誤")
            return
        
        # Disable UI during processing
        self.process_btn.setEnabled(False)
        self.process_btn.setText("處理中...")
        self.progress_bar.setVisible(True)
        self.progress_bar.setRange(0, 0)  # Indeterminate progress
        
        self.status_text.clear()
        self.status_text.append("🚀 開始處理 Netlist 檔案...")
        
        # Start background processing
        self.processing_thread = NetlistProcessingThread(
            netlist_path, output_path, self.config_model
        )
        self.processing_thread.finished.connect(self.on_processing_finished)
        self.processing_thread.error.connect(self.on_processing_error)
        self.processing_thread.progress.connect(self.on_processing_progress)
        self.processing_thread.start()
    
    def on_processing_finished(self, output_file):
        """Handle processing completion"""
        self.status_text.append("✅ 處理完成!")
        self.status_text.append(f"📄 輸出檔案: {output_file}")
        
        # Re-enable UI
        self.process_btn.setEnabled(True)
        self.process_btn.setText("生成佈局指南")
        self.progress_bar.setVisible(False)
        
        # Show success message
        from PyQt5.QtWidgets import QMessageBox
        reply = QMessageBox.information(
            self, "處理完成",
            f"佈局指南已成功生成!\\n\\n檔案位置:\\n{output_file}\\n\\n要開啟檔案嗎?",
            QMessageBox.Yes | QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            import os
            os.startfile(output_file)  # Windows
    
    def on_processing_error(self, error_message):
        """Handle processing error"""
        self.status_text.append(f"❌ 處理失敗: {error_message}")
        
        # Re-enable UI
        self.process_btn.setEnabled(True)
        self.process_btn.setText("生成佈局指南")
        self.progress_bar.setVisible(False)
        
        from PyQt5.QtWidgets import QMessageBox
        QMessageBox.critical(self, "處理錯誤", f"處理失敗:\\n{error_message}")
    
    def on_processing_progress(self, message):
        """Handle processing progress updates"""
        self.status_text.append(message)