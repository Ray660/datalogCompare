"""
Datalog对比工具 - 主入口

使用方法:
    GUI模式: python main.py
    命令行模式: python main.py --base 比较数据.csv --compare 被比较数据1.csv --compare 被比较数据2.csv --output output.csv
"""

import argparse
import sys
from src.cord_matching import match_cords
from src.output_writer import generate_output


def run_comparison(base_file: str, compare_files: list[str], output_file: str = "output.csv"):
    """执行对比"""
    print(f"比较数据: {base_file}")
    print(f"被比较数据: {compare_files}")
    print(f"输出文件: {output_file}")
    print("-" * 50)
    
    matched_data = match_cords(base_file, compare_files)
    
    if not matched_data:
        print("没有匹配的Cord")
        return
    
    print(f"匹配到 {len(matched_data)} 个文件")
    
    generate_output(base_file, matched_data, output_file)
    
    print(f"对比完成，输出文件: {output_file}")


def main():
    parser = argparse.ArgumentParser(description="Datalog对比工具")
    parser.add_argument("--base", required=True, help="比较数据文件路径")
    parser.add_argument("--compare", action="append", required=True, help="被比较数据文件路径（可多次使用）")
    parser.add_argument("--output", default="output.csv", help="输出文件路径（默认: output.csv）")
    parser.add_argument("--gui", action="store_true", help="启动GUI模式")
    
    args = parser.parse_args()
    
    if args.gui:
        from src.gui import main as gui_main
        gui_main()
    else:
        run_comparison(args.base, args.compare, args.output)


if __name__ == "__main__":
    main()
