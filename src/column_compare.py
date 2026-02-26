from typing import List, Dict
import pandas as pd


def get_data_columns(df: pd.DataFrame) -> List[str]:
    """获取数据列列表（从G列开始，即Index,Cord,Time,HBin,SBin,Site之后的列）"""
    fixed_columns = ["Index", "Cord", "Time", "HBin", "SBin", "Site"]
    return [col for col in df.columns if col not in fixed_columns]


def format_value(val) -> str:
    if pd.isna(val) or str(val).strip() == '':
        return ''
    s = str(val)
    if '.' in s:
        try:
            f = float(s)
            if f == int(f):
                return str(int(f))
        except:
            pass
    return s


def compare_columns(base_row: pd.Series, compare_row: pd.Series) -> Dict[str, str]:
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
        base_val = format_value(base_row[col])
        compare_val = format_value(compare_row[col])
        
        if base_val == "" and compare_val == "":
            continue
        
        if base_val == compare_val:
            continue
        
        result[col] = f"{compare_val}-{base_val}"
    
    return result
