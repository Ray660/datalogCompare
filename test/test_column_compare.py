import pytest
import pandas as pd
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from src.column_compare import get_data_columns, compare_columns


class TestGetDataColumns:
    def test_get_data_columns(self):
        df = pd.DataFrame(columns=["Index", "Cord", "Time", "HBin", "SBin", "Site", "200000_0", "200001_0"])
        result = get_data_columns(df)
        assert result == ["200000_0", "200001_0"]


class TestCompareColumns:
    def test_compare_columns_all_same(self):
        base_row = pd.Series({"200000_0": "100", "200001_0": "200"})
        compare_row = pd.Series({"200000_0": "100", "200001_0": "200"})
        result = compare_columns(base_row, compare_row)
        assert result == {}

    def test_compare_columns_different(self):
        base_row = pd.Series({"200000_0": "100", "200001_0": "200"})
        compare_row = pd.Series({"200000_0": "150", "200001_0": "200"})
        result = compare_columns(base_row, compare_row)
        assert result == {"200000_0": "150-100"}

    def test_compare_columns_empty_equal(self):
        base_row = pd.Series({"200000_0": "", "200001_0": "200"})
        compare_row = pd.Series({"200000_0": "", "200001_0": "200"})
        result = compare_columns(base_row, compare_row)
        assert result == {}

    def test_compare_columns_one_empty(self):
        base_row = pd.Series({"200000_0": "100", "200001_0": "200"})
        compare_row = pd.Series({"200000_0": "", "200001_0": "200"})
        result = compare_columns(base_row, compare_row)
        assert result == {"200000_0": "-100"}

    def test_compare_columns_both_empty(self):
        base_row = pd.Series({"200000_0": ""})
        compare_row = pd.Series({"200000_0": ""})
        result = compare_columns(base_row, compare_row)
        assert result == {}
