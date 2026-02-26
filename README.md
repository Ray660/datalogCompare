# DatalogCompare - 数据日志比较工具

用于比较两个CSV数据文件的工具，支持CLI和GUI两种模式。

## 功能特点

- Cord匹配：自动匹配两个文件中的Cord值
- HBin比较：比较HBin值是否相同
- 数据列比较：比较测试项数值差异
- Excel友好：防止Excel将数值识别为日期
- 支持多个被比较文件同时对比

## 输出格式

| 情况 | 输出 |
|------|------|
| 值不同 | `A_B`（A=被比较数据, B=比较数据） |
| 被比较数据不存在该列 | `_B`（B=比较数据） |
| 值相同 | 留空 |

## 项目结构

```
datalogCompare/
├── main.py              # CLI入口
├── src/
│   ├── cord_matching.py    # Cord匹配
│   ├── hbin_compare.py     # HBin比较
│   ├── column_compare.py   # 数据列比较
│   ├── output_writer.py    # 输出生成
│   └── gui.py              # GUI界面
├── test/                 # 测试文件
├── 比较数据.csv           # 比较基准文件
├── 被比较数据1.csv       # 被比较文件1
├── 被比较数据2.csv       # 被比较文件2
├── 被比较数据3.csv       # 被比较文件3
└── output.csv            # 输出结果
```

## 安装依赖

```bash
pip install pandas pytest PySide6
```

## 使用方法

### GUI模式（推荐）

直接运行 `Datalog对比工具.exe`，或使用Python：

```bash
python main.py
```

### CLI模式

```bash
# 基本用法
python main.py --cli --base 比较数据.csv --compare 被比较数据1.csv --output output.csv

# 多个被比较文件
python main.py --cli --base 比较数据.csv --compare 被比较数据1.csv --compare 被比较数据2.csv --output output.csv
```

### 打包的exe

下载 releases 中的 `Datalog对比工具_v1.x.x.exe` 直接运行，无需Python环境。

## CSV文件格式

输入CSV文件需要包含5行表头：
1. Index,Cord,Time,HBin,...
2. TestText（测试项名称）
3. HiLimit（上限）
4. LoLimit（下限）
5. Unit（单位）

数据从第6行开始。

## 运行测试

```bash
pytest test/ -v
```

## 技术栈

- Python 3.14+
- pandas - 数据处理
- pytest - 单元测试
- PySide6 - GUI界面

## 许可证

MIT License
