"""
Template Mapping Editor widget
模板映射編輯器
"""

from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel

from ..models.template_mapping_model import TemplateMappingModel
from ..controllers.template_mapping_controller import TemplateMappingController


class TemplateMappingEditor(QWidget):
    def __init__(self, template_mapping: TemplateMappingModel, 
                 controller: TemplateMappingController):
        super().__init__()
        self.template_mapping = template_mapping
        self.controller = controller
        
        layout = QVBoxLayout(self)
        layout.addWidget(QLabel("模板映射編輯器 (開發中...)"))