"""
Advanced features testing tool for impedance control GUI
進階功能測試工具
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / 'src'))

from src.models.configuration_model import ConfigurationModel
from src.models.signal_rule_model import SignalRuleModel
from src.models.layout_rule_model import LayoutRuleModel
from src.models.template_mapping_model import TemplateMappingModel
from src.controllers.configuration_controller import ConfigurationController


def test_configuration_model():
    """Test configuration model functionality"""
    print("測試配置模型...")
    
    config_model = ConfigurationModel()
    
    # Test adding signal rule
    signal_rule = config_model.add_signal_rule("TEST_I2C")
    signal_rule.set_category("Communication Interface")
    signal_rule.set_signal_type("I2C")
    signal_rule.add_keyword("I2C")
    signal_rule.add_pattern(".*I2C.*")
    
    # Test validation
    errors = signal_rule.validate()
    assert len(errors) == 0, f"Signal rule validation failed: {errors}"
    
    # Test matching
    assert signal_rule.matches_net("I2C_SCL"), "Should match I2C_SCL"
    assert signal_rule.matches_net("SDA_I2C"), "Should match SDA_I2C"
    assert not signal_rule.matches_net("SPI_CLK"), "Should not match SPI_CLK"
    
    print("配置模型測試通過")


def test_layout_rule_model():
    """Test layout rule model functionality"""
    print("測試佈局規則模型...")
    
    layout_rule = LayoutRuleModel()
    layout_rule.name = "I2C_Rule"
    layout_rule.set_impedance("50 Ohm")
    layout_rule.set_width("5 mil") 
    layout_rule.set_max_length_mm(150.0)
    
    # Test validation
    errors = layout_rule.validate() 
    assert len(errors) == 0, f"Layout rule validation failed: {errors}"
    
    # Test impedance value extraction
    impedance_value = layout_rule.get_impedance_value()
    assert impedance_value == 50.0, f"Expected 50.0, got {impedance_value}"
    
    print("佈局規則模型測試通過")


def test_template_mapping_model():
    """Test template mapping model functionality"""
    print("測試模板映射模型...")
    
    template = TemplateMappingModel()
    
    # Test adding custom column
    template.add_column("Custom_Field", "自定義欄位")
    assert "Custom_Field" in template.columns
    
    # Test column ordering
    original_order = template.column_order.copy()
    template.move_column_up("Custom_Field")
    assert template.column_order != original_order
    
    # Test validation
    errors = template.validate()
    assert len(errors) == 0, f"Template validation failed: {errors}"
    
    print("模板映射模型測試通過")


def test_yaml_config_io():
    """Test YAML configuration I/O"""
    print("測試YAML配置讀寫...")
    
    config_model = ConfigurationModel()
    
    # Add some test data
    signal_rule = config_model.add_signal_rule("TEST_RULE")
    signal_rule.set_category("Test")
    signal_rule.set_signal_type("Test")
    signal_rule.add_keyword("TEST")
    
    layout_rule = config_model.add_layout_rule("TEST_LAYOUT")
    layout_rule.set_impedance("100 Ohm")
    
    # Save to temporary file
    import tempfile
    with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as temp_file:
        temp_path = Path(temp_file.name)
    
    success = config_model.save_config(temp_path)
    assert success, "Failed to save config"
    
    # Load from file
    new_config = ConfigurationModel()
    success = new_config.load_config(temp_path)
    assert success, "Failed to load config"
    
    # Verify data integrity
    assert "TEST_RULE" in new_config.signal_rules
    assert "TEST_LAYOUT" in new_config.layout_rules
    
    # Clean up
    temp_path.unlink()
    
    print("YAML配置讀寫測試通過")


def test_integration_with_existing_code():
    """Test integration with existing processing code"""
    print("測試與現有程式碼整合...")
    
    # Test that we can import and use the main processing function
    try:
        from src.main import process_netlist_to_excel
        print("成功導入主要處理函數")
    except ImportError as e:
        print(f"導入失敗: {e}")
        return False
    
    # Test configuration compatibility
    config_model = ConfigurationModel()
    
    # Verify that default config loads properly
    assert len(config_model.signal_rules) > 0, "Should have signal rules"
    assert len(config_model.layout_rules) > 0, "Should have layout rules"
    
    print("整合測試通過")


def run_all_tests():
    """Run all tests"""
    print("=" * 50)
    print("開始進階功能測試")
    print("=" * 50)
    
    test_functions = [
        test_configuration_model,
        test_layout_rule_model, 
        test_template_mapping_model,
        test_yaml_config_io,
        test_integration_with_existing_code
    ]
    
    passed = 0
    failed = 0
    
    for test_func in test_functions:
        try:
            test_func()
            passed += 1
        except Exception as e:
            print(f"測試失敗 {test_func.__name__}: {e}")
            import traceback
            traceback.print_exc()
            failed += 1
        print()
    
    print("=" * 50)
    print(f"測試結果: {passed} 通過, {failed} 失敗")
    print("=" * 50)
    
    return failed == 0


if __name__ == "__main__":
    success = run_all_tests()
    
    if success:
        print("所有測試通過！進階功能準備就緒。")
        sys.exit(0)
    else:
        print("部分測試失敗，請檢查問題。")
        sys.exit(1)