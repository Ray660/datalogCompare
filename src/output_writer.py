from typing import Dict
import pandas as pd
from src.hbin_compare import compare_hbin
from src.column_compare import compare_columns, get_data_columns, format_value


def excel_escape(val: str) -> str:
    """防止Excel将数值型差异值(如10-14)识别为日期"""
    if val and isinstance(val, str):
        if val and val[0].isdigit() and val.replace('-', '').replace('.', '').isdigit():
            return '\t' + val
    return val


def generate_output(
    base_file: str,
    matched_data: Dict[str, pd.DataFrame],
    output_file: str
) -> None:
    """
    生成输出CSV
    
    Args:
        base_file: 比较数据文件路径
        matched_data: {文件路径: 匹配行的DataFrame}
        output_file: 输出文件路径
    """
    base_df = pd.read_csv(base_file, encoding='utf-8', skiprows=[1, 2, 3, 4])
    
    header_df = pd.read_csv(base_file, encoding='utf-8', nrows=0)
    testtext_df = pd.read_csv(base_file, encoding='utf-8', skiprows=1, header=None, nrows=1)
    testtext_df.columns = header_df.columns
    testtext_row = testtext_df.iloc[0] if len(testtext_df) > 0 else None
    
    fixed_columns = ["Index", "Cord", "Time", "SBin", "Site"]
    all_data_cols = [col for col in base_df.columns if col not in fixed_columns]
    
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
                for col in all_data_cols:
                    if col in diff_cols:
                        row_data[col] = diff_cols[col]
                    elif col in compare_row.index:
                        base_val = format_value(base_row[col])
                        compare_val = format_value(compare_row[col])
                        if base_val != compare_val:
                            row_data[col] = f"{compare_val}-{base_val}"
                        else:
                            row_data[col] = ""
                    else:
                        row_data[col] = "-1"
                all_diff_rows.append(row_data)
    
    if all_diff_rows:
        output_df = pd.DataFrame(all_diff_rows)
        output_df = output_df.sort_values(by="Cord")
    else:
        output_df = pd.DataFrame(columns=["Cord"])
    
    if testtext_row is not None and not output_df.empty:
        all_cols = ["Cord"] + all_data_cols
        
        testtext_values = {"Cord": "Cord"}
        for col in all_cols:
            if col != "Cord" and col in testtext_row.index:
                val = testtext_row[col]
                testtext_values[col] = val if pd.notna(val) else ""
            elif col != "Cord":
                testtext_values[col] = ""
        
        for col in all_cols:
            if col not in output_df.columns:
                output_df[col] = ""
        
        output_df = output_df[all_cols]
        
        testtext_df_output = pd.DataFrame([testtext_values])
        
        output_df = pd.concat([testtext_df_output, output_df], ignore_index=True)
    
    for col in output_df.columns:
        if col != "Cord":
            output_df[col] = output_df[col].apply(lambda x: excel_escape(str(x)) if pd.notna(x) else x)
    
    output_df.to_csv(output_file, index=False, encoding='utf-8')
