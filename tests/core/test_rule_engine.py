"""Tests for the RuleEngine using ConfigManager rules."""
from src.core.net_classifier import NetClassifier
from src.core.rule_engine import RuleEngine
from src.config.config_manager import ConfigManager


class TestRuleEngine:
    """Test cases for layout rule application."""

    def test_apply_rules_with_config_manager(self, config_data):
        cm = ConfigManager()
        cm.config_data = config_data

        classifier = NetClassifier(cm)
        classified = classifier.classify(["SPI_MOSI"])

        engine = RuleEngine(cm)
        layout = engine.apply_rules(classified)

        assert layout["SPI_MOSI"]["impedance"] == "50 Ohm"

