import sys
import os

os.environ['QT_QPA_PLATFORM'] = 'offscreen'

from unittest.mock import MagicMock
sys.modules['PySide6'] = MagicMock()
sys.modules['PySide6.QtWidgets'] = MagicMock()

from src.gui import CompareApp


class TestCompareApp:
    def test_set_output_file(self):
        app = CompareApp()
        app.set_output_file("custom_output.csv")
        assert app.output_file == "custom_output.csv"

    def test_set_output_file_default(self):
        app = CompareApp()
        assert app.output_file == "output.csv"

    def test_run_comparison_no_base_file(self):
        app = CompareApp()
        app.base_file = ""
        app.compare_files = ["/path/to/compare1.csv"]
        
        app.run_comparison()
        
        assert "请选择比较数据文件" in app.get_log_text()

    def test_run_comparison_no_compare_files(self):
        app = CompareApp()
        app.base_file = "/path/to/base.csv"
        app.compare_files = []
        
        app.run_comparison()
        
        assert "请选择被比较数据文件" in app.get_log_text()

    def test_run_comparison_success(self):
        import tempfile
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False, encoding='utf-8') as f:
            f.write("Index,Cord,Time,HBin\n")
            f.write("TestText,,,\n")
            f.write("HiLimit,,,\n")
            f.write("LoLimit,,,\n")
            f.write("Unit,,,\n")
            f.write("0,10_0,5054,10\n")
            base_file = f.name

        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False, encoding='utf-8') as f:
            f.write("Index,Cord,Time,HBin\n")
            f.write("TestText,,,\n")
            f.write("HiLimit,,,\n")
            f.write("LoLimit,,,\n")
            f.write("Unit,,,\n")
            f.write("0,10_0,5054,14\n")
            compare_file = f.name

        app = CompareApp()
        app.base_file = base_file
        app.compare_files = [compare_file]
        app.output_file = "output.csv"
        
        app.run_comparison()
        
        assert "完成" in app.get_log_text()
        
        os.unlink(base_file)
        os.unlink(compare_file)

    def test_log_display(self):
        app = CompareApp()
        app.log_text = ""
        app._log("测试日志")
        assert "测试日志" in app.get_log_text()

    def test_show_completion_dialog(self):
        app = CompareApp()
        app.show_completion_dialog("/path/to/output.csv")
        assert True
