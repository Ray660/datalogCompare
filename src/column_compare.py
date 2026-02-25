import pandas as pd


def get_data_columns(df: pd.DataFrame) -> list[str]:
    """获取数据列列表（从G列开始，即Index,Cord,Time,HBin,SBin,Site之后的列）"""
    fixed_columns = ["Index", "Cord", "Time", "HBin", "SBin", "Site"]
    return [col for col in df.columns if col not in fixed_columns]


def compare_columns(base_row: pd.Series, compare_row: pd.Series) -> dict[str, str]:
    """
    对比数据列
    
    Args:
        base_row: 比较数据中的一行
        compare_row: 被比较数据中的一行
    
    Returns:
        dict: {列名: 差异值}，无差异的列不返回
    """
    result = {}
    common_cols = base_row.index.intersection(compare_row.index)
    
    for col in common_cols:
        base_val = str(base_row[col]) if pd.notna(base_row[col]) else ""
        compare_val = str(compare_row[col]) if pd.notna(compare_row[col]) else ""
        
        if base_val == "" and compare_val == "":
            continue
        
        if base_val == compare_val:
            continue
        
        result[col] = f"{compare_val}-{base_val}"
    
    return result
