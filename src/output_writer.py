import pandas as pd
from src.hbin_compare import compare_hbin
from src.column_compare import compare_columns, get_data_columns


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
    base_df = pd.read_csv(base_file, encoding='utf-8', skiprows=[1, 2, 3])
    
    all_diff_rows = []
    
    for compare_file, compare_df in matched_data.items():
        for _, compare_row in compare_df.iterrows():
            cord = compare_row.get("Cord", "")
            base_rows = base_df[base_df["Cord"].astype(str).str.lower() == cord.lower()]
            
            if base_rows.empty:
                continue
            
            base_row = base_rows.iloc[0]
            
            if compare_hbin(base_row, compare_row):
                continue
            
            diff_cols = compare_columns(base_row, compare_row)
            
            if diff_cols:
                row_data = {"Cord": cord}
                row_data.update(diff_cols)
                all_diff_rows.append(row_data)
    
    if all_diff_rows:
        output_df = pd.DataFrame(all_diff_rows)
        output_df = output_df.sort_values(by="Cord")
    else:
        output_df = pd.DataFrame(columns=["Cord"])
    
    output_df.to_csv(output_file, index=False, encoding='utf-8')
