import pandas as pd


def generate_output(
    base_file: str,
    matched_data: dict[str, pd.DataFrame],
    output_file: str
) -> None:
    """
    生成输出CSV
    
    Args:
        base_file: 比较数据文件路径
        matched_data: {文件路径: 匹配行的DataFrame}
        output_file: 输出文件路径
    """
    pass
