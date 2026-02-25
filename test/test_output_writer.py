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
            f.write("LoLimit,,,\n")
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
            f.write("LoLimit,,,\n")
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
            f.write("LoLimit,,,\n")
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
            f.write("Index,Cord,Time,HBin,200000_0\n")
            f.write("TestText,,,TestName,MeasValue\n")
            f.write("HiLimit,,,100\n")
            f.write("LoLimit,,,0\n")
            f.write("Unit,,,mV\n")
            f.write("0,10_0,5054,10,150\n")
            base_file = f.name

        matched_data = {
            "compare1.csv": pd.DataFrame({
                "Cord": ["10_0"],
                "HBin": ["14"],
                "200000_0": ["180"]
            })
        }

        output_file = tempfile.mktemp(suffix='.csv')
        try:
            generate_output(base_file, matched_data, output_file)
            df = pd.read_csv(output_file, encoding='utf-8')
            assert "200000_0" in df.columns, f"Expected 200000_0 in columns, got {df.columns.tolist()}"
            val = df["200000_0"].iloc[1]
            assert "180-150" in str(val), f"Expected '180-150' in {val}"
            assert "\t14-10" in str(df["HBin"].iloc[1])
        finally:
            os.unlink(base_file)
            if os.path.exists(output_file):
                os.unlink(output_file)

    def test_output_includes_testtext_row(self):
        """输出应包含TestText行(第2行)"""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False, encoding='utf-8') as f:
            f.write("Index,Cord,Time,HBin,200000_0\n")
            f.write("TestText,,,TestName,MeasValue\n")
            f.write("HiLimit,,,100\n")
            f.write("LoLimit,,,0\n")
            f.write("Unit,,,mV\n")
            f.write("0,10_0,5054,10,150\n")
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
            
            with open(output_file, 'r', encoding='utf-8') as f:
                lines = f.readlines()
            
            assert len(lines) >= 2, f"Output should have at least 2 lines, got {len(lines)}: {lines}"
            second_line = lines[1].strip()
            assert "TestName" in second_line, f"Second line should contain TestText, got: {second_line}"
        finally:
            os.unlink(base_file)
            if os.path.exists(output_file):
                os.unlink(output_file)
