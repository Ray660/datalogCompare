import pytest
import pandas as pd
import os
import sys
import tempfile

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from src.output_writer import generate_output


class TestGenerateOutput:
    def test_generate_output_basic(self):
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False, encoding='utf-8') as f:
            f.write("Index,Cord,Time,HBin\n")
            f.write("TestText,,,\n")
            f.write("HiLimit,,,\n")
            f.write("Unit,,,\n")
            f.write("0,10_0,5054,10\n")
            base_file = f.name

        matched_data = {
            "compare1.csv": pd.DataFrame({
                "Cord": ["10_0"],
                "HBin": ["14"],
                "200000_0": ["150"]
            })
        }

        output_file = tempfile.mktemp(suffix='.csv')
        try:
            generate_output(base_file, matched_data, output_file)
            assert os.path.exists(output_file)
            df = pd.read_csv(output_file, encoding='utf-8')
            assert "Cord" in df.columns
        finally:
            os.unlink(base_file)
            if os.path.exists(output_file):
                os.unlink(output_file)

    def test_generate_output_no_diff(self):
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False, encoding='utf-8') as f:
            f.write("Index,Cord,Time,HBin\n")
            f.write("TestText,,,\n")
            f.write("HiLimit,,,\n")
            f.write("Unit,,,\n")
            f.write("0,10_0,5054,10\n")
            base_file = f.name

        matched_data = {}

        output_file = tempfile.mktemp(suffix='.csv')
        try:
            generate_output(base_file, matched_data, output_file)
            assert os.path.exists(output_file)
            df = pd.read_csv(output_file, encoding='utf-8')
            assert len(df) == 0
        finally:
            os.unlink(base_file)
            if os.path.exists(output_file):
                os.unlink(output_file)

    def test_generate_output_multiple_files(self):
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False, encoding='utf-8') as f:
            f.write("Index,Cord,Time,HBin\n")
            f.write("TestText,,,\n")
            f.write("HiLimit,,,\n")
            f.write("Unit,,,\n")
            f.write("0,10_0,5054,10\n")
            f.write("1,11_0,5064,10\n")
            base_file = f.name

        matched_data = {
            "compare1.csv": pd.DataFrame({
                "Cord": ["10_0"],
                "HBin": ["14"]
            }),
            "compare2.csv": pd.DataFrame({
                "Cord": ["11_0"],
                "HBin": ["14"]
            })
        }

        output_file = tempfile.mktemp(suffix='.csv')
        try:
            generate_output(base_file, matched_data, output_file)
            assert os.path.exists(output_file)
            df = pd.read_csv(output_file, encoding='utf-8')
            assert len(df) >= 1
        finally:
            os.unlink(base_file)
            if os.path.exists(output_file):
                os.unlink(output_file)

    def test_output_format_diff(self):
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False, encoding='utf-8') as f:
            f.write("Index,Cord,Time,HBin\n")
            f.write("TestText,,,\n")
            f.write("HiLimit,,,\n")
            f.write("Unit,,,\n")
            f.write("0,10_0,5054,10\n")
            base_file = f.name

        matched_data = {
            "compare1.csv": pd.DataFrame({
                "Cord": ["10_0"],
                "HBin": ["14"],
                "200000_0": ["150"]
            })
        }

        output_file = tempfile.mktemp(suffix='.csv')
        try:
            generate_output(base_file, matched_data, output_file)
            df = pd.read_csv(output_file, encoding='utf-8')
            hbin_col = [col for col in df.columns if "HBin" in col][0]
            hbin_val = df[hbin_col].iloc[0]
            assert "14-10" in str(hbin_val)
        finally:
            os.unlink(base_file)
            if os.path.exists(output_file):
                os.unlink(output_file)
