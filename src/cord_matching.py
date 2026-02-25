import pandas as pd


def get_cords_from_base(base_file: str) -> list[str]:
    """从比较数据中获取所有非空Cord值（去重、忽略大小写）"""
    df = pd.read_csv(base_file, encoding='utf-8', skiprows=[1, 2, 3])
    cords = df['Cord'].dropna().astype(str)
    cords = cords[cords != '']
    return sorted(cords.unique().tolist())


def match_cords(base_file: str, compare_files: list[str]) -> dict[str, pd.DataFrame]:
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
        compare_df = pd.read_csv(compare_file, encoding='utf-8', skiprows=[1, 2, 3])
        compare_cords = compare_df['Cord'].dropna().astype(str)
        compare_cords = compare_cords[compare_cords != '']
        
        matched_mask = compare_cords.str.lower().isin(base_cords_lower)
        matched_df = compare_df[matched_mask]
        
        if not matched_df.empty:
            result[compare_file] = matched_df
    
    return result
