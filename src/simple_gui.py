"""
Simple GUI wrapper for the impedance control tool.
基於新架構的簡單圖形介面包裝器
"""
import sys
import os
from pathlib import Path
from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout, 
                             QPushButton, QLineEdit, QLabel, QTextEdit, QFileDialog,
                             QMessageBox)
from PyQt5.QtCore import QThread, pyqtSignal
from main import process_netlist_to_excel


class ProcessingThread(QThread):
    """後台處理線程"""
    finished = pyqtSignal(str)  # 完成信號
    error = pyqtSignal(str)     # 錯誤信號
    
    def __init__(self, netlist_path, output_path):
        super().__init__()
        self.netlist_path = netlist_path
        self.output_path = output_path
    
    def run(self):
        try:
            result_path = process_netlist_to_excel(
                netlist_path=Path(self.netlist_path),
                output_path=Path(self.output_path) if self.output_path else None
            )
            self.finished.emit(str(result_path))
        except Exception as e:
            self.error.emit(str(e))


class SimpleGUI(QWidget):
    """簡單的圖形使用者介面"""
    
    def __init__(self):
        super().__init__()
        self.processing_thread = None
        self.initUI()
    
    def initUI(self):
        self.setWindowTitle('阻抗控制佈局指南生成器 v2.0')
        self.setGeometry(300, 300, 600, 400)
        
        layout = QVBoxLayout()
        
        # Netlist 檔案選擇
        netlist_layout = QHBoxLayout()
        self.netlist_input = QLineEdit()
        self.netlist_input.setPlaceholderText("選擇 Netlist 檔案 (.net, .sp, .cir, .txt)")
        netlist_button = QPushButton("瀏覽...")
        netlist_button.clicked.connect(self.browse_netlist)
        
        netlist_layout.addWidget(QLabel("Netlist 檔案:"))
        netlist_layout.addWidget(self.netlist_input)
        netlist_layout.addWidget(netlist_button)
        layout.addLayout(netlist_layout)
        
        # 輸出檔案選擇
        output_layout = QHBoxLayout()
        self.output_input = QLineEdit()
        self.output_input.setPlaceholderText("選擇輸出 Excel 檔案位置")
        output_button = QPushButton("另存為...")
        output_button.clicked.connect(self.browse_output)
        
        output_layout.addWidget(QLabel("輸出檔案:"))
        output_layout.addWidget(self.output_input)
        output_layout.addWidget(output_button)
        layout.addLayout(output_layout)
        
        # 生成按鈕
        self.generate_button = QPushButton("生成佈局指南")
        self.generate_button.clicked.connect(self.generate_guide)
        layout.addWidget(self.generate_button)
        
        # 狀態顯示區域
        self.status_text = QTextEdit()
        self.status_text.setReadOnly(True)
        self.status_text.setMaximumHeight(200)
        layout.addWidget(QLabel("處理狀態:"))
        layout.addWidget(self.status_text)
        
        self.setLayout(layout)
        
        # 套用深色主題
        self.setStyleSheet("""
            QWidget {
                background-color: #2e2e2e;
                color: #f0f0f0;
                font-family: "Microsoft YaHei", "微軟雅黑";
            }
            QLineEdit, QTextEdit {
                background-color: #3c3c3c;
                border: 1px solid #555555;
                padding: 5px;
                border-radius: 3px;
            }
            QPushButton {
                background-color: #555555;
                border: 1px solid #666666;
                padding: 8px 15px;
                border-radius: 3px;
            }
            QPushButton:hover {
                background-color: #666666;
            }
            QPushButton:pressed {
                background-color: #444444;
            }
            QLabel {
                color: #f0f0f0;
            }
        """)
    
    def browse_netlist(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, "選擇 Netlist 檔案", "", 
            "Netlist Files (*.net *.sp *.cir *.txt);;All Files (*)"
        )
        if file_path:
            self.netlist_input.setText(file_path)
    
    def browse_output(self):
        file_path, _ = QFileDialog.getSaveFileName(
            self, "儲存 Excel 檔案", "", 
            "Excel Files (*.xlsx);;All Files (*)"
        )
        if file_path:
            if not file_path.endswith('.xlsx'):
                file_path += '.xlsx'
            self.output_input.setText(file_path)
    
    def generate_guide(self):
        netlist_path = self.netlist_input.text().strip()
        output_path = self.output_input.text().strip()
        
        if not netlist_path:
            QMessageBox.warning(self, "錯誤", "請選擇 Netlist 檔案")
            return
        
        if not Path(netlist_path).exists():
            QMessageBox.warning(self, "錯誤", "Netlist 檔案不存在")
            return
        
        # 禁用按鈕，開始處理
        self.generate_button.setEnabled(False)
        self.generate_button.setText("處理中...")
        self.status_text.clear()
        self.status_text.append("🚀 開始處理 Netlist 檔案...")
        
        # 啟動後台處理
        self.processing_thread = ProcessingThread(netlist_path, output_path)
        self.processing_thread.finished.connect(self.on_processing_finished)
        self.processing_thread.error.connect(self.on_processing_error)
        self.processing_thread.start()
    
    def on_processing_finished(self, result_path):
        self.status_text.append(f"✅ 處理完成!")
        self.status_text.append(f"📄 輸出檔案: {result_path}")
        
        # 重新啟用按鈕
        self.generate_button.setEnabled(True)
        self.generate_button.setText("生成佈局指南")
        
        # 顯示成功訊息
        reply = QMessageBox.information(
            self, "成功", 
            f"佈局指南已成功生成!\n\n檔案位置:\n{result_path}\n\n要開啟檔案嗎?",
            QMessageBox.Yes | QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            os.startfile(result_path)  # Windows
    
    def on_processing_error(self, error_message):
        self.status_text.append(f"❌ 處理失敗: {error_message}")
        
        # 重新啟用按鈕
        self.generate_button.setEnabled(True)
        self.generate_button.setText("生成佈局指南")
        
        QMessageBox.critical(self, "錯誤", f"處理失敗:\n{error_message}")


def main():
    app = QApplication(sys.argv)
    window = SimpleGUI()
    window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
