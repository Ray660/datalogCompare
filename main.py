from typing import List
import argparse
import sys
from src.cord_matching import match_cords
from src.output_writer import generate_output


def run_comparison(base_file: str, compare_files: List[str], output_file: str = "output.csv"):
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
    parser.add_argument("--base", help="比较数据文件路径")
    parser.add_argument("--compare", action="append", help="被比较数据文件路径（可多次使用）")
    parser.add_argument("--output", default="output.csv", help="输出文件路径（默认: output.csv）")
    parser.add_argument("--cli", action="store_true", help="使用命令行模式")
    
    args = parser.parse_args()
    
    if args.cli:
        if not args.base or not args.compare:
            parser.error("命令行模式需要 --base 和 --compare 参数")
        run_comparison(args.base, args.compare, args.output)
    else:
        from src.gui import main as gui_main
        gui_main()


if __name__ == "__main__":
    main()
