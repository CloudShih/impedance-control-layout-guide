"""
Comprehensive testing tool for impedance control system
阻抗控制系統綜合測試工具
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / 'src'))

def quick_functionality_test():
    """Run a quick functionality test."""
    print("=== 阻抗控制工具快速功能測試 ===")
    
    try:
        from main import process_netlist_to_excel
        
        # Test with sample data
        netlist_path = Path("tests/data/sample_netlist.net")
        output_path = Path("quick_test_output.xlsx")
        
        if not netlist_path.exists():
            print("錯誤: 測試檔案不存在")
            return False
        
        print("正在處理範例檔案...")
        result_path = process_netlist_to_excel(
            netlist_path=netlist_path,
            output_path=output_path
        )
        
        if result_path and result_path.exists():
            print(f"✅ 快速測試成功! 輸出檔案: {result_path}")
            print(f"檔案大小: {result_path.stat().st_size} 位元組")
            return True
        else:
            print("❌ 快速測試失敗: 輸出檔案未生成")
            return False
            
    except Exception as e:
        print(f"❌ 快速測試異常: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_configuration_model():
    """Test configuration model functionality"""
    print("\n=== 測試配置模型 ===")
    
    try:
        from src.models.configuration_model import ConfigurationModel
        from src.models.signal_rule_model import SignalRuleModel
        from src.models.layout_rule_model import LayoutRuleModel
        
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
        
        print("✅ 配置模型測試通過")
        return True
        
    except Exception as e:
        print(f"❌ 配置模型測試失敗: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_layout_rule_model():
    """Test layout rule model functionality"""
    print("\n=== 測試佈局規則模型 ===")
    
    try:
        from src.models.layout_rule_model import LayoutRuleModel
        
        layout_rule = LayoutRuleModel()
        layout_rule.name = "I2C_Rule"
        layout_rule.set_impedance("50 Ohm")
        layout_rule.set_width("5 mil")
        layout_rule.set_spacing("3W spacing")
        layout_rule.set_description("I2C通訊佈局規則")
        
        # Test validation
        errors = layout_rule.validate()
        assert len(errors) == 0, f"Layout rule validation failed: {errors}"
        
        # Test export
        export_data = layout_rule.to_dict()
        assert export_data['impedance'] == "50 Ohm"
        assert export_data['width'] == "5 mil"
        
        print("✅ 佈局規則模型測試通過")
        return True
        
    except Exception as e:
        print(f"❌ 佈局規則模型測試失敗: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_template_mapping():
    """Test template mapping functionality"""
    print("\n=== 測試模板映射功能 ===")
    
    try:
        from src.models.template_mapping_model import TemplateMappingModel
        
        template_model = TemplateMappingModel()
        
        # Test column mapping
        template_model.add_column_mapping("Net_Name", "網路名稱")
        template_model.add_column_mapping("Category", "信號類別")
        template_model.add_column_mapping("Impedance", "阻抗要求")
        
        # Test validation
        errors = template_model.validate()
        assert len(errors) == 0, f"Template mapping validation failed: {errors}"
        
        # Test export
        mappings = template_model.get_column_mappings()
        assert "Net_Name" in mappings
        assert mappings["Net_Name"] == "網路名稱"
        
        print("✅ 模板映射測試通過")
        return True
        
    except Exception as e:
        print(f"❌ 模板映射測試失敗: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_controllers():
    """Test controller functionality"""
    print("\n=== 測試控制器功能 ===")
    
    try:
        from src.controllers.configuration_controller import ConfigurationController
        
        controller = ConfigurationController()
        
        # Test loading default configuration
        controller.load_default_config()
        config = controller.get_current_config()
        
        assert config is not None, "Configuration should not be None"
        assert len(config.signal_rules) > 0, "Should have signal rules"
        assert len(config.layout_rules) > 0, "Should have layout rules"
        
        # Test saving and loading
        test_config_path = Path("test_config.yaml")
        controller.save_config(test_config_path)
        assert test_config_path.exists(), "Config file should be created"
        
        # Clean up
        test_config_path.unlink()
        
        print("✅ 控制器測試通過")
        return True
        
    except Exception as e:
        print(f"❌ 控制器測試失敗: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_core_functionality():
    """Test core module functionality"""
    print("\n=== 測試核心模組功能 ===")
    
    try:
        from src.core.netlist_parser import NetlistParser
        from src.core.net_classifier import NetClassifier
        from src.core.rule_engine import RuleEngine
        
        # Test netlist parser
        parser = NetlistParser()
        test_netlist = Path("tests/data/sample_netlist.net")
        
        if test_netlist.exists():
            net_names = parser.parse(test_netlist)
            assert len(net_names) > 0, "Should parse net names"
            print(f"  解析到 {len(net_names)} 個網路名稱")
        
        # Test classifier
        classifier = NetClassifier()
        if test_netlist.exists():
            classified = classifier.classify(net_names)
            assert len(classified) > 0, "Should classify networks"
            print(f"  分類了 {len(classified)} 個網路")
        
        # Test rule engine
        rule_engine = RuleEngine()
        config = rule_engine.get_default_config()
        assert config is not None, "Should have default config"
        print(f"  載入了 {len(config.get('net_classification_rules', {}))} 個分類規則")
        
        print("✅ 核心模組測試通過")
        return True
        
    except Exception as e:
        print(f"❌ 核心模組測試失敗: {e}")
        import traceback
        traceback.print_exc()
        return False


def run_all_tests():
    """Run all comprehensive tests"""
    print("🚀 開始阻抗控制系統綜合測試")
    print("=" * 60)
    
    test_functions = [
        quick_functionality_test,
        test_configuration_model,
        test_layout_rule_model,
        test_template_mapping,
        test_controllers,
        test_core_functionality
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
            print(f"❌ 測試異常 {test_func.__name__}: {e}")
            failed += 1
    
    print("\n" + "=" * 60)
    print(f"📊 測試結果總結:")
    print(f"✅ 通過: {passed}")
    print(f"❌ 失敗: {failed}")
    print(f"📈 成功率: {passed/(passed+failed)*100:.1f}%" if (passed+failed) > 0 else "0%")
    
    if failed == 0:
        print("\n🎉 所有測試通過! 系統運作正常")
        return True
    else:
        print(f"\n⚠️  {failed} 個測試失敗，請檢查相關模組")
        return False


if __name__ == "__main__":
    success = run_all_tests()
    
    if success:
        print("\n✨ 恭喜! 阻抗控制工具已準備好使用")
        print("📖 接下來可以參考 USER_MANUAL.md 進行實際操作")
        sys.exit(0)
    else:
        print("\n🔧 請根據錯誤訊息進行問題排除")
        sys.exit(1)