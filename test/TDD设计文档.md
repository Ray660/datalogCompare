# Datalog对比工具 - TDD设计文档

## 模块划分

| 模块 | 测试文件 | 描述 |
|------|----------|------|
| cord_matching | test_cord_matching.py | Cord值匹配 |
| hbin_compare | test_hbin_compare.py | HBin列比较 |
| column_compare | test_column_compare.py | 数据列对比（G列开始） |
| output_writer | test_output_writer.py | 输出生成 |
| gui | test_gui.py | UI界面 |

---

## 数据文件格式

### 输入CSV结构（比较数据.csv / 被比较数据.csv）

```
Index,Cord,Time,HBin,SBin,Site,200000_0,200001_0,...
TestText,,,,,,continuityToPWR X_PAD37,...
HiLimit,,,,,,650,...
Unit,,,,,,mV,...
0,10_0,5054,10,10,0,412.2162,...
1,11_0,5064,14,1425,0,417.4805,...
```

- 第1行：列名（Index, Cord, Time, HBin, SBin, Site, 数据列...）
- 第2行：TestText（测试项名称）
- 第3行：HiLimit（上限值）
- 第4行：Unit（单位）
- 第5行起：实际数据行

### 输出CSV结构（output.csv）

```
,Cord,401000_0,401001_0,...
Cord,DFT_CHIP_STUCK,DFT_CHIP_STUCK,...
6_2,1-0,1-0,1-0,,1-0
```

- 第1行：列名（Cord在前，后面是有差异的数据列）
- 第2行：TestText
- 第3行起：差异数据，格式 `被比较值-比较值`

---

## 模块1: Cord匹配 (cord_matching)

### 函数接口

```python
def get_cords_from_base(base_file: str) -> list[str]:
    """从比较数据中获取所有非空Cord值（去重、忽略大小写）"""

def match_cords(base_file: str, compare_files: list[str]) -> dict[str, pd.DataFrame]:
    """
    匹配Cord值
    
    Args:
        base_file: 比较数据CSV文件路径
        compare_files: 被比较数据CSV文件路径列表
    
    Returns:
        dict: {文件路径: 匹配行的DataFrame}
    """
```

### 测试用例

#### test_get_cords_from_base_basic
**输入**: 比较数据.csv（包含Cord: "10_0", "11_0", "12_0"）
**预期**: 返回 ["10_0", "11_0", "12_0"]（去重后）

#### test_get_cords_skip_empty
**输入**: 比较数据.csv（Cord包含空值 ""）
**预期**: 跳过空Cord，只返回非空值

#### test_get_cords_case_insensitive
**输入**: 比较数据.csv（Cord: "10_0", "11_0"）
**预期**: 返回去重后的Cord列表，不区分大小写处理

#### test_match_cords_single_file
**输入**:
- base_file: 比较数据.csv（Cord: "10_0", "11_0"）
- compare_files: ["被比较数据1.csv"]（Cord: "10_0"）
**预期**: 返回 {"被比较数据1.csv": 包含Cord="10_0"的DataFrame}

#### test_match_cords_multiple_files
**输入**:
- base_file: 比较数据.csv（Cord: "10_0", "11_0"）
- compare_files:
  - 被比较数据1.csv: Cord "10_0"
  - 被比较数据2.csv: Cord "11_0"
**预期**: 返回两个文件的匹配结果

#### test_match_cords_no_match
**输入**:
- base_file: 比较数据.csv（Cord: "10_0"）
- compare_files: ["被比较数据.csv"]（Cord: "99_0"）
**预期**: 返回空字典 {}

#### test_match_cords_case_insensitive
**输入**:
- base_file: 比较数据.csv（Cord: "10_0"）
- compare_files: ["被比较数据.csv"]（Cord: "10_0"）
**预期**: 能匹配（不区分大小写）

---

## 模块2: HBin比较 (hbin_compare)

### 函数接口

```python
def compare_hbin(base_row: pd.Series, compare_row: pd.Series) -> bool:
    """
    比较HBin列
    
    Args:
        base_row: 比较数据中的一行
        compare_row: 被比较数据中的一行
    
    Returns:
        bool: True表示HBin相同（不计为差异），False表示不同
    """
```

### 测试用例

#### test_hbin_same
**输入**:
- base_row: HBin = "10"
- compare_row: HBin = "10"
**预期**: 返回 True

#### test_hbin_different
**输入**:
- base_row: HBin = "10"
- compare_row: HBin = "14"
**预期**: 返回 False

#### test_hbin_empty_same
**输入**:
- base_row: HBin = ""
- compare_row: HBin = ""
**预期**: 返回 True（空值与空值视为相等）

#### test_hbin_one_empty
**输入**:
- base_row: HBin = "10"
- compare_row: HBin = ""
**预期**: 返回 False

---

## 模块3: 数据列对比 (column_compare)

### 函数接口

```python
def get_data_columns(df: pd.DataFrame) -> list[str]:
    """获取数据列列表（从G列开始，即Index,Cord,Time,HBin,SBin,Site之后的列）"""

def compare_columns(base_row: pd.Series, compare_row: pd.Series) -> dict[str, str]:
    """
    对比数据列
    
    Args:
        base_row: 比较数据中的一行
        compare_row: 被比较数据中的一行
    
    Returns:
        dict: {列名: 差异值}，无差异的列不返回
    """
```

### 测试用例

#### test_get_data_columns
**输入**: DataFrame列 ["Index", "Cord", "Time", "HBin", "SBin", "Site", "200000_0", "200001_0"]
**预期**: 返回 ["200000_0", "200001_0"]

#### test_compare_columns_all_same
**输入**:
- base_row: {"200000_0": "100", "200001_0": "200"}
- compare_row: {"200000_0": "100", "200001_0": "200"}
**预期**: 返回 {}

#### test_compare_columns_different
**输入**:
- base_row: {"200000_0": "100", "200001_0": "200"}
- compare_row: {"200000_0": "150", "200001_0": "200"}
**预期**: 返回 {"200000_0": "150-100"}

#### test_compare_columns_empty_equal
**输入**:
- base_row: {"200000_0": "", "200001_0": "200"}
- compare_row: {"200000_0": "", "200001_0": "200"}
**预期**: 返回 {}（空值与空值视为相等）

#### test_compare_columns_one_empty
**输入**:
- base_row: {"200000_0": "100", "200001_0": "200"}
- compare_row: {"200000_0": "", "200001_0": "200"}
**预期**: 返回 {"200000_0": "-100"}

#### test_compare_columns_both_empty
**输入**:
- base_row: {"200000_0": ""}
- compare_row: {"200000_0": ""}
**预期**: 返回 {}（空值与空值视为相等）

---

## 模块4: 输出生成 (output_writer)

### 函数接口

```python
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
```

### 测试用例

#### test_generate_output_basic
**输入**:
- base_file: 比较数据.csv
- matched_data: {"被比较数据1.csv": DataFrame(Cord="10_0", HBin="14", 200000_0="150")}
- output_file: "output.csv"
**预期**: 生成output.csv，包含差异行

#### test_generate_output_no_diff
**输入**:
- matched_data: 所有数据完全匹配
**预期**: 生成空内容的output.csv（只有表头）

#### test_generate_output_multiple_files
**输入**:
- matched_data: 多个被比较文件的匹配数据
**预期**: 合并所有差异到同一个output.csv

#### test_output_format_diff
**输入**:
- base: HBin="10", 200000_0="100"
- compare: HBin="14", 200000_0="150"
**预期**: 输出格式 "14-10", "150-100"

---

## 模块5: UI界面 (gui)

### 技术选型
- 框架：PySide6（简单优先）
- 测试：单元测试（模拟信号/槽）

### 函数接口

```python
class CompareApp:
    """主应用类"""
    
    def __init__(self):
        """初始化UI"""
        
    def select_base_file(self) -> str:
        """选择比较数据文件"""
        
    def select_compare_files(self) -> list[str]:
        """选择被比较数据文件（支持多选）"""
        
    def set_output_file(self, path: str) -> None:
        """设置输出文件路径"""
        
    def run_comparison(self) -> None:
        """执行对比任务"""
        
    def get_log_text(self) -> str:
        """获取日志文本"""
        
    def show_completion_dialog(self, output_path: str) -> None:
        """显示完成弹窗"""
```

### 测试用例

#### test_select_base_file
**描述**: 选择比较数据文件
**输入**: 模拟文件对话框返回路径
**预期**: 返回选中的文件路径

#### test_select_compare_files
**描述**: 选择被比较数据文件（多选）
**输入**: 模拟文件对话框返回多个路径
**预期**: 返回文件路径列表

#### test_set_output_file
**描述**: 设置输出文件路径
**输入**: "custom_output.csv"
**预期**: 输出路径设置为 "custom_output.csv"

#### test_set_output_file_default
**描述**: 默认输出文件
**输入**: 无输入
**预期**: 输出路径默认为 "output.csv"

#### test_run_comparison_success
**描述**: 执行对比成功
**输入**: 
- base_file: "比较数据.csv"
- compare_files: ["被比较数据1.csv"]
**预期**: 
- 生成输出文件
- 日志显示成功信息
- 调用完成弹窗

#### test_run_comparison_no_base_file
**描述**: 未选择比较数据文件
**输入**: base_file 为空
**预期**: 显示错误提示

#### test_run_comparison_no_compare_files
**描述**: 未选择被比较数据文件
**输入**: compare_files 为空
**预期**: 显示错误提示

#### test_log_display
**描述**: 日志显示
**输入**: 执行对比任务
**预期**: 日志文本框显示运行进度

#### test_show_completion_dialog
**描述**: 完成弹窗显示
**输入**: output_path = "output.csv"
**预期**: 弹窗显示 "对比完成，输出文件：output.csv"

---

## TDD开发顺序

1. **cord_matching** - 最底层，依赖CSV读取
2. **hbin_compare** - 单一列比较
3. **column_compare** - 多列对比，依赖hbin_compare
4. **output_writer** - 最终输出，整合所有模块
5. **gui** - UI界面

---

## 依赖关系

```
csv_reader (pandas)
    ↓
cord_matching
    ↓
hbin_compare ← column_compare
    ↓
output_writer
    ↓
      gui
```
