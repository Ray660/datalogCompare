import os


class CompareApp:
    def __init__(self):
        self.base_file = ""
        self.compare_files = []
        self.output_file = "output.csv"
        self.log_text = ""
    
    def select_base_file(self) -> str:
        from PySide6.QtWidgets import QFileDialog
        file_path, _ = QFileDialog.getOpenFileName(
            None, "选择比较数据文件", "", "CSV Files (*.csv)"
        )
        if file_path:
            self.base_file = file_path
        return file_path
    
    def select_compare_files(self) -> list[str]:
        from PySide6.QtWidgets import QFileDialog
        file_paths, _ = QFileDialog.getOpenFileNames(
            None, "选择被比较数据文件", "", "CSV Files (*.csv)"
        )
        if file_paths:
            self.compare_files = file_paths
        return file_paths
    
    def set_output_file(self, path: str) -> None:
        self.output_file = path
    
    def run_comparison(self) -> None:
        if not self.base_file:
            self._log("错误：请选择比较数据文件")
            return
        
        if not self.compare_files:
            self._log("错误：请选择被比较数据文件")
            return
        
        self._log("开始对比...")
        
        from src.cord_matching import match_cords
        matched_data = match_cords(self.base_file, self.compare_files)
        
        if not matched_data:
            self._log("没有匹配的Cord")
            return
        
        self._log(f"匹配到 {len(matched_data)} 个文件")
        
        from src.output_writer import generate_output
        generate_output(self.base_file, matched_data, self.output_file)
        
        self._log(f"对比完成，输出文件：{self.output_file}")
        
        self.show_completion_dialog(self.output_file)
    
    def get_log_text(self) -> str:
        return self.log_text
    
    def _log(self, message: str) -> None:
        self.log_text += message + "\n"
    
    def show_completion_dialog(self, output_path: str) -> None:
        from PySide6.QtWidgets import QMessageBox
        QMessageBox.about(None, "完成", f"对比完成，输出文件：{output_path}")
