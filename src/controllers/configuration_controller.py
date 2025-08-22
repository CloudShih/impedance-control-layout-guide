"""
Configuration Controller for managing overall configuration operations
配置控制器，用於管理整體配置操作
"""

import json
from pathlib import Path
from typing import List, Dict, Any, Optional
from PyQt5.QtCore import QObject, pyqtSignal
from PyQt5.QtWidgets import QMessageBox, QFileDialog

from models.configuration_model import ConfigurationModel


class ConfigurationController(QObject):
    """
    Main controller for managing configuration operations
    主要配置控制器，管理配置操作
    """
    
    # Signals for notifying view updates
    configLoaded = pyqtSignal(str)      # config file path
    configSaved = pyqtSignal(str)       # config file path
    errorOccurred = pyqtSignal(str)     # error message
    validationCompleted = pyqtSignal(bool, list)  # success, error list
    operationProgress = pyqtSignal(str)  # progress message
    
    def __init__(self, config_model: ConfigurationModel):
        super().__init__()
        self.config_model = config_model
        self.is_modified = False
        self.undo_stack: List[Dict[str, Any]] = []
        self.redo_stack: List[Dict[str, Any]] = []
        self.max_undo_levels = 50
        
        # Connect to model signals
        self.config_model.dataChanged.connect(self._on_model_changed)
        self.config_model.configLoaded.connect(self._on_config_loaded)
        self.config_model.configSaved.connect(self._on_config_saved)
        self.config_model.validationError.connect(self._on_validation_error)
    
    def _on_model_changed(self):
        """Handle model data changes"""
        self.is_modified = True
        self._save_state_for_undo()
    
    def _on_config_loaded(self, config_path: str):
        """Handle successful config loading"""
        self.is_modified = False
        self.undo_stack.clear()
        self.redo_stack.clear()
        self.configLoaded.emit(config_path)
        self.operationProgress.emit(f"配置已載入: {config_path}")
    
    def _on_config_saved(self, config_path: str):
        """Handle successful config saving"""
        self.is_modified = False
        self.configSaved.emit(config_path)
        self.operationProgress.emit(f"配置已儲存: {config_path}")
    
    def _on_validation_error(self, error_message: str):
        """Handle validation errors from model"""
        self.errorOccurred.emit(error_message)
    
    def _save_state_for_undo(self):
        """Save current state for undo functionality"""
        try:
            current_state = self.config_model._build_config_data()
            self.undo_stack.append(current_state)
            
            # Limit undo stack size
            if len(self.undo_stack) > self.max_undo_levels:
                self.undo_stack.pop(0)
            
            # Clear redo stack when new action is performed
            self.redo_stack.clear()
            
        except Exception as e:
            print(f"Warning: Could not save state for undo: {e}")
    
    def load_config_file(self, config_path: Optional[Path] = None) -> bool:
        """
        Load configuration from file with user dialog if path not provided
        載入配置檔案，如果未提供路徑則顯示使用者對話框
        """
        try:
            if config_path is None:
                file_path, _ = QFileDialog.getOpenFileName(
                    None,
                    "載入配置檔案",
                    str(Path.home()),
                    "YAML Files (*.yaml *.yml);;JSON Files (*.json);;All Files (*)"
                )
                if not file_path:
                    return False
                config_path = Path(file_path)
            
            self.operationProgress.emit(f"正在載入配置: {config_path}")
            
            success = self.config_model.load_config(config_path)
            if success:
                self.operationProgress.emit("配置載入成功")
            
            return success
            
        except Exception as e:
            error_msg = f"載入配置檔案時發生錯誤: {str(e)}"
            self.errorOccurred.emit(error_msg)
            return False
    
    def save_config_file(self, config_path: Optional[Path] = None) -> bool:
        """
        Save configuration to file with user dialog if path not provided
        儲存配置檔案，如果未提供路徑則顯示使用者對話框
        """
        try:
            if config_path is None:
                if self.config_model.config_file_path:
                    # Save to current file
                    config_path = self.config_model.config_file_path
                else:
                    # Show save dialog
                    return self.save_config_file_as()
            
            self.operationProgress.emit(f"正在儲存配置: {config_path}")
            
            success = self.config_model.save_config(config_path)
            if success:
                self.operationProgress.emit("配置儲存成功")
            
            return success
            
        except Exception as e:
            error_msg = f"儲存配置檔案時發生錯誤: {str(e)}"
            self.errorOccurred.emit(error_msg)
            return False
    
    def save_config_file_as(self) -> bool:
        """
        Save configuration to new file with user dialog
        使用對話框另存新檔
        """
        try:
            file_path, _ = QFileDialog.getSaveFileName(
                None,
                "另存配置檔案",
                str(Path.home() / "impedance_config.yaml"),
                "YAML Files (*.yaml *.yml);;JSON Files (*.json);;All Files (*)"
            )
            
            if not file_path:
                return False
            
            config_path = Path(file_path)
            
            # Ensure proper extension
            if not config_path.suffix:
                config_path = config_path.with_suffix('.yaml')
            
            return self.save_config_file(config_path)
            
        except Exception as e:
            error_msg = f"另存配置檔案時發生錯誤: {str(e)}"
            self.errorOccurred.emit(error_msg)
            return False
    
    def validate_all_rules(self) -> bool:
        """
        Validate all configuration rules
        驗證所有配置規則
        """
        self.operationProgress.emit("正在驗證配置...")
        
        errors = self.config_model.validate_config()
        success = len(errors) == 0
        
        self.validationCompleted.emit(success, errors)
        
        if success:
            self.operationProgress.emit("配置驗證通過")
        else:
            self.operationProgress.emit(f"配置驗證失敗，發現 {len(errors)} 個錯誤")
        
        return success
    
    def reset_to_defaults(self) -> bool:
        """
        Reset configuration to default values
        重設配置為預設值
        """
        try:
            self.operationProgress.emit("正在重設為預設配置...")
            
            # Load default configuration
            self.config_model._load_default_config()
            
            self.is_modified = True
            self.operationProgress.emit("已重設為預設配置")
            
            return True
            
        except Exception as e:
            error_msg = f"重設配置時發生錯誤: {str(e)}"
            self.errorOccurred.emit(error_msg)
            return False
    
    def create_new_config(self) -> bool:
        """
        Create a new empty configuration
        創建新的空白配置
        """
        try:
            if self.is_modified:
                reply = QMessageBox.question(
                    None, "創建新配置",
                    "目前配置尚未儲存，是否要先儲存？",
                    QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel
                )
                
                if reply == QMessageBox.Yes:
                    if not self.save_config_file():
                        return False
                elif reply == QMessageBox.Cancel:
                    return False
            
            self.operationProgress.emit("正在創建新配置...")
            
            # Clear current configuration
            self.config_model.signal_rules.clear()
            self.config_model.layout_rules.clear()
            self.config_model.template_mapping.reset_to_defaults()
            self.config_model.config_file_path = None
            
            self.is_modified = False
            self.undo_stack.clear()
            self.redo_stack.clear()
            
            self.config_model.dataChanged.emit()
            self.operationProgress.emit("新配置已創建")
            
            return True
            
        except Exception as e:
            error_msg = f"創建新配置時發生錯誤: {str(e)}"
            self.errorOccurred.emit(error_msg)
            return False
    
    def undo(self) -> bool:
        """Undo last action"""
        if not self.undo_stack:
            return False
        
        try:
            # Save current state to redo stack
            current_state = self.config_model._build_config_data()
            self.redo_stack.append(current_state)
            
            # Restore previous state
            previous_state = self.undo_stack.pop()
            self.config_model._parse_config_data(previous_state)
            
            self.operationProgress.emit("已復原上一步操作")
            return True
            
        except Exception as e:
            error_msg = f"復原操作時發生錯誤: {str(e)}"
            self.errorOccurred.emit(error_msg)
            return False
    
    def redo(self) -> bool:
        """Redo last undone action"""
        if not self.redo_stack:
            return False
        
        try:
            # Save current state to undo stack
            current_state = self.config_model._build_config_data()
            self.undo_stack.append(current_state)
            
            # Restore next state
            next_state = self.redo_stack.pop()
            self.config_model._parse_config_data(next_state)
            
            self.operationProgress.emit("已重做上一步操作")
            return True
            
        except Exception as e:
            error_msg = f"重做操作時發生錯誤: {str(e)}"
            self.errorOccurred.emit(error_msg)
            return False
    
    def can_undo(self) -> bool:
        """Check if undo is available"""
        return len(self.undo_stack) > 0
    
    def can_redo(self) -> bool:
        """Check if redo is available"""
        return len(self.redo_stack) > 0
    
    def get_config_summary(self) -> Dict[str, Any]:
        """Get summary of current configuration"""
        summary = self.config_model.get_config_summary()
        summary['is_modified'] = self.is_modified
        summary['can_undo'] = self.can_undo()
        summary['can_redo'] = self.can_redo()
        return summary
    
    def export_config_summary(self, output_path: Path) -> bool:
        """Export configuration summary to JSON file"""
        try:
            summary = self.get_config_summary()
            
            # Add detailed information 
            summary['signal_rules'] = {
                name: rule.get_summary() 
                for name, rule in self.config_model.signal_rules.items()
            }
            summary['layout_rules'] = {
                name: rule.get_summary()
                for name, rule in self.config_model.layout_rules.items()
            }
            summary['template_summary'] = self.config_model.template_mapping.get_summary()
            
            with open(output_path, 'w', encoding='utf-8') as file:
                json.dump(summary, file, indent=2, ensure_ascii=False)
            
            self.operationProgress.emit(f"配置摘要已匯出: {output_path}")
            return True
            
        except Exception as e:
            error_msg = f"匯出配置摘要時發生錯誤: {str(e)}"
            self.errorOccurred.emit(error_msg)
            return False
