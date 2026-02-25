import pandas as pd


def get_data_columns(df: pd.DataFrame) -> list[str]:
    """获取数据列列表（从G列开始，即Index,Cord,Time,HBin,SBin,Site之后的列）"""
    pass


def compare_columns(base_row: pd.Series, compare_row: pd.Series) -> dict[str, str]:
    """
    对比数据列
    
    Args:
        base_row: 比较数据中的一行
        compare_row: 被比较数据中的一行
    
    Returns:
        dict: {列名: 差异值}，无差异的列不返回
    """
    pass
