import pandas as pd


def compare_hbin(base_row: pd.Series, compare_row: pd.Series) -> bool:
    """
    比较HBin列
    
    Args:
        base_row: 比较数据中的一行
        compare_row: 被比较数据中的一行
    
    Returns:
        bool: True表示HBin相同（不计为差异），False表示不同
    """
    base_hbin = str(base_row.get("HBin", ""))
    compare_hbin = str(compare_row.get("HBin", ""))
    
    if base_hbin == "" and compare_hbin == "":
        return True
    
    if base_hbin == "" or compare_hbin == "":
        return False
    
    return base_hbin == compare_hbin
