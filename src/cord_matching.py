from typing import List, Dict
import pandas as pd


def get_cords_from_base(base_file: str) -> List[str]:
    """从比较数据中获取所有非空Cord值（去重、忽略大小写）"""
    df = pd.read_csv(base_file, encoding='utf-8', skiprows=[1, 2, 3, 4])
    cords = df['Cord'].dropna().astype(str)
    cords = cords[cords != '']
    return sorted(cords.unique().tolist())


def match_cords(base_file: str, compare_files: List[str]) -> Dict[str, pd.DataFrame]:
    """
    匹配Cord值
    
    Args:
        base_file: 比较数据CSV文件路径
        compare_files: 被比较数据CSV文件路径列表
    
    Returns:
        dict: {文件路径: 匹配行的DataFrame}
    """
    base_cords = get_cords_from_base(base_file)
    base_cords_lower = [cord.lower() for cord in base_cords]
    
    result = {}
    for compare_file in compare_files:
        compare_df = pd.read_csv(compare_file, encoding='utf-8', skiprows=[1, 2, 3, 4])
        
        compare_df = compare_df[compare_df['Cord'].notna()]
        compare_df = compare_df[compare_df['Cord'].astype(str) != '']
        
        matched_mask = compare_df['Cord'].astype(str).str.lower().isin(base_cords_lower)
        matched_df = compare_df[matched_mask]
        
        if not matched_df.empty:
            result[compare_file] = matched_df
    
    return result
