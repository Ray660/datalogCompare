import pytest
import pandas as pd
import os
import tempfile
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from src.cord_matching import get_cords_from_base, match_cords


class TestGetCordsFromBase:
    def test_get_cords_from_base_basic(self):
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False, encoding='utf-8') as f:
            f.write("Index,Cord,Time,HBin\n")
            f.write("TestText,,,\n")
            f.write("HiLimit,,,\n")
            f.write("Unit,,,\n")
            f.write("0,10_0,5054,10\n")
            f.write("1,11_0,5064,14\n")
            f.write("2,12_0,4871,10\n")
            base_file = f.name
        try:
            result = get_cords_from_base(base_file)
            assert sorted(result) == ["10_0", "11_0", "12_0"]
        finally:
            os.unlink(base_file)

    def test_get_cords_skip_empty(self):
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False, encoding='utf-8') as f:
            f.write("Index,Cord,Time,HBin\n")
            f.write("TestText,,,\n")
            f.write("HiLimit,,,\n")
            f.write("Unit,,,\n")
            f.write("0,,5054,10\n")
            f.write("1,11_0,5064,14\n")
            f.write("2,,4871,10\n")
            base_file = f.name
        try:
            result = get_cords_from_base(base_file)
            assert result == ["11_0"]
        finally:
            os.unlink(base_file)

    def test_get_cords_case_insensitive(self):
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False, encoding='utf-8') as f:
            f.write("Index,Cord,Time,HBin\n")
            f.write("TestText,,,\n")
            f.write("HiLimit,,,\n")
            f.write("Unit,,,\n")
            f.write("0,10_0,5054,10\n")
            f.write("1,10_0,5064,14\n")
            f.write("2,11_0,4871,10\n")
            base_file = f.name
        try:
            result = get_cords_from_base(base_file)
            assert sorted(result) == ["10_0", "11_0"]
        finally:
            os.unlink(base_file)


class TestMatchCords:
    def test_match_cords_single_file(self):
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False, encoding='utf-8') as f:
            f.write("Index,Cord,Time,HBin\n")
            f.write("TestText,,,\n")
            f.write("HiLimit,,,\n")
            f.write("Unit,,,\n")
            f.write("0,10_0,5054,10\n")
            f.write("1,11_0,5064,14\n")
            base_file = f.name

        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False, encoding='utf-8') as f:
            f.write("Index,Cord,Time,HBin\n")
            f.write("TestText,,,\n")
            f.write("HiLimit,,,\n")
            f.write("Unit,,,\n")
            f.write("0,10_0,5054,14\n")
            compare_file = f.name

        try:
            result = match_cords(base_file, [compare_file])
            assert compare_file in result
            assert "10_0" in result[compare_file]["Cord"].values
        finally:
            os.unlink(base_file)
            os.unlink(compare_file)

    def test_match_cords_multiple_files(self):
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False, encoding='utf-8') as f:
            f.write("Index,Cord,Time,HBin\n")
            f.write("TestText,,,\n")
            f.write("HiLimit,,,\n")
            f.write("Unit,,,\n")
            f.write("0,10_0,5054,10\n")
            f.write("1,11_0,5064,14\n")
            base_file = f.name

        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False, encoding='utf-8') as f:
            f.write("Index,Cord,Time,HBin\n")
            f.write("TestText,,,\n")
            f.write("HiLimit,,,\n")
            f.write("Unit,,,\n")
            f.write("0,10_0,5054,14\n")
            compare_file1 = f.name

        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False, encoding='utf-8') as f:
            f.write("Index,Cord,Time,HBin\n")
            f.write("TestText,,,\n")
            f.write("HiLimit,,,\n")
            f.write("Unit,,,\n")
            f.write("0,11_0,5064,14\n")
            compare_file2 = f.name

        try:
            result = match_cords(base_file, [compare_file1, compare_file2])
            assert compare_file1 in result
            assert compare_file2 in result
            assert "10_0" in result[compare_file1]["Cord"].values
            assert "11_0" in result[compare_file2]["Cord"].values
        finally:
            os.unlink(base_file)
            os.unlink(compare_file1)
            os.unlink(compare_file2)

    def test_match_cords_no_match(self):
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False, encoding='utf-8') as f:
            f.write("Index,Cord,Time,HBin\n")
            f.write("TestText,,,\n")
            f.write("HiLimit,,,\n")
            f.write("Unit,,,\n")
            f.write("0,10_0,5054,10\n")
            base_file = f.name

        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False, encoding='utf-8') as f:
            f.write("Index,Cord,Time,HBin\n")
            f.write("TestText,,,\n")
            f.write("HiLimit,,,\n")
            f.write("Unit,,,\n")
            f.write("0,99_0,5054,14\n")
            compare_file = f.name

        try:
            result = match_cords(base_file, [compare_file])
            assert result == {}
        finally:
            os.unlink(base_file)
            os.unlink(compare_file)

    def test_match_cords_case_insensitive(self):
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False, encoding='utf-8') as f:
            f.write("Index,Cord,Time,HBin\n")
            f.write("TestText,,,\n")
            f.write("HiLimit,,,\n")
            f.write("Unit,,,\n")
            f.write("0,10_0,5054,10\n")
            base_file = f.name

        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False, encoding='utf-8') as f:
            f.write("Index,Cord,Time,HBin\n")
            f.write("TestText,,,\n")
            f.write("HiLimit,,,\n")
            f.write("Unit,,,\n")
            f.write("0,10_0,5054,14\n")
            compare_file = f.name

        try:
            result = match_cords(base_file, [compare_file])
            assert compare_file in result
            assert "10_0" in result[compare_file]["Cord"].values
        finally:
            os.unlink(base_file)
            os.unlink(compare_file)
