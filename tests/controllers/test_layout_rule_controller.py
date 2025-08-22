import importlib.util
import logging
import sys
from pathlib import Path

import pytest
from PyQt5.QtCore import QCoreApplication

# Add src directory to path for model imports
base_path = Path(__file__).resolve().parents[2] / "src"
sys.path.append(str(base_path))

# Import LayoutRuleController without triggering controllers package imports
spec = importlib.util.spec_from_file_location(
    "layout_rule_controller", base_path / "controllers" / "layout_rule_controller.py"
)
layout_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(layout_module)
LayoutRuleController = layout_module.LayoutRuleController

from models.layout_rule_model import LayoutRuleModel


def test_add_rule_logs_and_raises(monkeypatch, caplog):
    app = QCoreApplication.instance() or QCoreApplication([])
    controller = LayoutRuleController({})
    errors = []
    controller.errorOccurred.connect(errors.append)

    def fake_load_from_dict(self, name, data):
        raise ValueError("bad data")

    monkeypatch.setattr(LayoutRuleModel, "load_from_dict", fake_load_from_dict)

    with caplog.at_level(logging.ERROR):
        with pytest.raises(ValueError):
            controller.add_rule("rule1", {"foo": "bar"})

    assert errors and "bad data" in errors[0]
    record = next(r for r in caplog.records if "Failed to add rule rule1" in r.getMessage())
    assert record.exc_info is not None
