"""Tests for :mod:`src.core.rule_engine`."""
from src.core.net_classifier import NetClassifier
from src.core.rule_engine import RuleEngine


class TestRuleEngine:
    """Test cases for layout rule engine functionality."""

    def test_apply_i2c_rules(self, config_data):
        classifier = NetClassifier(config_data)
        classified = classifier.classify(["I2C_SCL"])
        engine = RuleEngine(config_data)
        layout = engine.apply_rules(classified)
        info = layout["I2C_SCL"]
        assert info["impedance"] == "50 Ohm"
        assert info["signal_type"] == "I2C"

    def test_apply_spi_rules(self, config_data):
        classifier = NetClassifier(config_data)
        classified = classifier.classify(["SPI_CLK"])
        engine = RuleEngine(config_data)
        layout = engine.apply_rules(classified)
        assert layout["SPI_CLK"]["description"].startswith("SPI")

    def test_apply_rf_rules(self, config_data):
        classifier = NetClassifier(config_data)
        classified = classifier.classify(["RF_TX1"])
        engine = RuleEngine(config_data)
        layout = engine.apply_rules(classified)
        assert layout["RF_TX1"]["category"] == "RF"

    def test_apply_default_rules(self):
        classifier = NetClassifier()
        classified = classifier.classify(["UNKNOWN_NET"])
        engine = RuleEngine()
        layout = engine.apply_rules(classified)
        assert layout["UNKNOWN_NET"]["rule_matched"] == "default"
        assert layout["UNKNOWN_NET"]["impedance"] == "50 Ohm"

    def test_rule_priority_handling(self, config_data):
        classifier = NetClassifier(config_data)
        classified = classifier.classify(["I2C_SCL"])
        engine = RuleEngine(config_data)
        layout = engine.apply_rules(classified)
        assert layout["I2C_SCL"]["priority"] == classified["I2C_SCL"]["priority"]

    def test_custom_rule_application(self, config_data):
        engine = RuleEngine(config_data)
        engine.add_custom_rule("CUSTOM", {"impedance": "75 Ohm", "description": "Custom"})
        assert "CUSTOM" in engine.layout_rules

    def test_rule_validation(self):
        engine = RuleEngine()
        assert engine.validate_rule_config({"impedance": "50 Ohm", "description": "desc"})
        assert not engine.validate_rule_config({"impedance": "50 Ohm"})