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


def main():
    import sys
    from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QTextEdit, QLineEdit, QLabel
    
    app = QApplication(sys.argv)
    window = QMainWindow()
    window.setWindowTitle("Datalog对比工具")
    window.setGeometry(100, 100, 600, 400)
    
    central_widget = QWidget()
    layout = QVBoxLayout()
    
    base_layout = QHBoxLayout()
    base_label = QLabel("比较数据: 未选择")
    base_btn = QPushButton("选择文件")
    base_layout.addWidget(base_label)
    base_layout.addWidget(base_btn)
    layout.addLayout(base_layout)
    
    compare_layout = QHBoxLayout()
    compare_label = QLabel("被比较数据: 未选择")
    compare_btn = QPushButton("选择文件")
    compare_layout.addWidget(compare_label)
    compare_layout.addWidget(compare_btn)
    layout.addLayout(compare_layout)
    
    output_layout = QHBoxLayout()
    output_label = QLabel("输出文件:")
    output_input = QLineEdit("output.csv")
    output_layout.addWidget(output_label)
    output_layout.addWidget(output_input)
    layout.addLayout(output_layout)
    
    run_btn = QPushButton("开始执行")
    layout.addWidget(run_btn)
    
    log_label = QLabel("运行日志:")
    layout.addWidget(log_label)
    
    log_text = QTextEdit()
    log_text.setReadOnly(True)
    layout.addWidget(log_text)
    
    window.setCentralWidget(central_widget)
    central_widget.setLayout(layout)
    
    compare_app = CompareApp()
    
    def on_select_base():
        path = compare_app.select_base_file()
        if path:
            base_label.setText(f"比较数据: {path}")
    
    def on_select_compare():
        paths = compare_app.select_compare_files()
        if paths:
            compare_label.setText(f"被比较数据: {len(paths)} 个文件")
    
    def on_run():
        compare_app.set_output_file(output_input.text())
        compare_app.run_comparison()
        log_text.setText(compare_app.get_log_text())
    
    base_btn.clicked.connect(on_select_base)
    compare_btn.clicked.connect(on_select_compare)
    run_btn.clicked.connect(on_run)
    
    window.show()
    sys.exit(app.exec())
