"""
Layout Rule Editor widget
佈局規則編輯器
"""

from typing import Dict
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QTableWidget

from ..models.layout_rule_model import LayoutRuleModel
from ..controllers.layout_rule_controller import LayoutRuleController


class LayoutRuleEditor(QWidget):
    def __init__(self, layout_rules: Dict[str, LayoutRuleModel], 
                 controller: LayoutRuleController):
        super().__init__()
        self.layout_rules = layout_rules
        self.controller = controller
        
        layout = QVBoxLayout(self)
        layout.addWidget(QLabel("佈局規則編輯器 (開發中...)"))
        
        # Basic table for now
        self.rules_table = QTableWidget()
        layout.addWidget(self.rules_table)