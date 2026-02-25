import pytest
import pandas as pd
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from src.hbin_compare import compare_hbin


class TestCompareHBin:
    def test_hbin_same(self):
        base_row = pd.Series({"Cord": "10_0", "HBin": "10"})
        compare_row = pd.Series({"Cord": "10_0", "HBin": "10"})
        assert compare_hbin(base_row, compare_row) is True

    def test_hbin_different(self):
        base_row = pd.Series({"Cord": "10_0", "HBin": "10"})
        compare_row = pd.Series({"Cord": "10_0", "HBin": "14"})
        assert compare_hbin(base_row, compare_row) is False

    def test_hbin_empty_same(self):
        base_row = pd.Series({"Cord": "10_0", "HBin": ""})
        compare_row = pd.Series({"Cord": "10_0", "HBin": ""})
        assert compare_hbin(base_row, compare_row) is True

    def test_hbin_one_empty(self):
        base_row = pd.Series({"Cord": "10_0", "HBin": "10"})
        compare_row = pd.Series({"Cord": "10_0", "HBin": ""})
        assert compare_hbin(base_row, compare_row) is False
