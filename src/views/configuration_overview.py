"""
Configuration Overview widget
配置概覽
"""

from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QTextEdit

from ..models.configuration_model import ConfigurationModel
from ..controllers.configuration_controller import ConfigurationController


class ConfigurationOverview(QWidget):
    def __init__(self, config_model: ConfigurationModel, 
                 controller: ConfigurationController):
        super().__init__()
        self.config_model = config_model
        self.controller = controller
        
        layout = QVBoxLayout(self)
        title_label = QLabel("配置概覽")
        title_label.setStyleSheet("font-weight: bold; font-size: 14px; background-color: #2b2b2b; color: white; padding: 5px;")
        layout.addWidget(title_label)
        
        self.overview_text = QTextEdit()
        self.overview_text.setReadOnly(True)
        self.overview_text.setMaximumHeight(200)
        layout.addWidget(self.overview_text)
        
        # Update overview when config changes
        self.config_model.dataChanged.connect(self.update_overview)
        self.update_overview()
    
    def update_overview(self):
        """Update the overview display"""
        summary = self.controller.get_config_summary()
        
        overview_text = f"""
配置檔案: {summary.get('config_file', 'None')}
信號規則數量: {summary.get('signal_rules_count', 0)}
佈局規則數量: {summary.get('layout_rules_count', 0)}
模板欄位數量: {summary.get('template_columns', 0)}
驗證錯誤: {summary.get('validation_errors', 0)}
"""
        self.overview_text.setPlainText(overview_text.strip())