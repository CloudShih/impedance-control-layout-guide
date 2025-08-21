"""Tests for :mod:`src.core.template_mapper`."""
import pandas as pd

from src.core.template_mapper import TemplateMapper


class TestTemplateMapper:
    """Test cases for Excel template mapping functionality."""

    def _sample_layout_data(self):
        return {
            "NET1": {
                "category": "Communication Interface",
                "signal_type": "I2C",
                "impedance": "50 Ohm",
                "description": "I2C line",
                "width": "5 mil",
                "length_limit": "6 inch",
                "spacing": "3W spacing",
                "shielding": "Ground guard",
                "layer_stack": "Any",
                "notes": "",
                "priority": 1,
            }
        }

    def test_map_to_standard_template(self, tmp_path, config_data):
        mapper = TemplateMapper(config_data)
        output = tmp_path / "out.xlsx"
        result = mapper.map_to_template(self._sample_layout_data(), output_path=output)
        assert result.exists()
        df = pd.read_excel(result)
        assert df["Net Name"].iloc[0] == "NET1"

    def test_column_mapping(self, tmp_path, config_data):
        mapper = TemplateMapper(config_data)
        result = mapper.map_to_template(self._sample_layout_data(), output_path=tmp_path / "out.xlsx")
        df = pd.read_excel(result)
        assert list(df.columns)[:3] == ["Category", "Net Name", "Pin (MT7921)"]

    def test_template_validation(self, sample_excel_template, config_data):
        mapper = TemplateMapper(config_data)
        assert mapper.validate_template(sample_excel_template)

    def test_missing_columns_handling(self, mock_excel_file, config_data):
        mapper = TemplateMapper(config_data)
        assert not mapper.validate_template(mock_excel_file)

    def test_excel_output_generation(self, tmp_path, config_data):
        mapper = TemplateMapper(config_data)
        path = mapper.map_to_template(self._sample_layout_data(), output_path=tmp_path / "out.xlsx")
        assert path.exists()