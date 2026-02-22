# 表格复制行数 Skill

批量复制Excel/WPS表格的指定行数据的实用工具。

## 功能特性

- ✓ 支持读取Excel文件的指定列和行数
- ✓ 可自定义每行的复制次数
- ✓ 支持命令行参数和交互式输入两种模式
- ✓ 自动创建输出目录
- ✓ 友好的进度提示和错误处理

## 安装依赖

```bash
pip install -r requirements.txt
```

或者手动安装：

```bash
pip install pandas openpyxl
```

## 使用方法

### 方法一：交互式运行

```bash
python copy_rows.py
```

然后按提示输入：
- 源文件路径
- 输出文件路径（可留空，自动生成）
- 读取的列范围（如：A:A 或 A:C）
- 读取的行数
- 每行复制次数

### 方法二：命令行参数

```bash
python copy_rows.py <输入文件> <输出文件> <列范围> <行数> <复制次数>
```

示例：

```bash
python copy_rows.py "/Users/nanyu/Desktop/复制专用.xlsx" "/Users/nanyu/Desktop/输出.xlsx" "A:A" 22 128
```

## 参数说明

| 参数 | 说明 | 默认值 | 示例 |
|------|------|--------|------|
| 输入文件 | 源Excel文件路径 | 必填 | /path/to/input.xlsx |
| 输出文件 | 输出Excel文件路径 | 自动生成 | /path/to/output.xlsx |
| 列范围 | 要读取的列 | A:A | A:A, A:C, B:D |
| 行数 | 从第一行开始读取的行数 | 22 | 22, 50, 100 |
| 复制次数 | 每行重复的次数 | 128 | 128, 100, 200 |

## 示例场景

### 场景1：复制单列数据

将A列的前22行，每行复制128次：

```bash
python copy_rows.py data.xlsx output.xlsx A:A 22 128
```

### 场景2：复制多列数据

将A到C列的前50行，每行复制100次：

```bash
python copy_rows.py data.xlsx output.xlsx A:C 50 100
```

## 注意事项

- 确保输入的Excel文件存在且可访问
- 输出目录不存在时会自动创建
- 复制次数过大可能导致生成的文件很大，请根据实际需求设置
- 支持的文件格式：.xlsx, .xls

## 输出示例

```
==================================================
表格复制行数工具
==================================================

处理参数:
  源文件: /Users/nanyu/Desktop/复制专用.xlsx
  输出文件: /Users/nanyu/Desktop/输出.xlsx
  读取列: A:A
  读取行数: 22
  复制次数: 128

正在读取文件: /Users/nanyu/Desktop/复制专用.xlsx
读取列: A:A, 读取行数: 22
每行复制 128 次...
✓ 数据已成功复制并保存到: /Users/nanyu/Desktop/输出.xlsx
原始行数: 22, 输出行数: 2816

处理完成！
```

## 故障排除

### 问题：找不到文件

确保文件路径正确，可以使用绝对路径。

### 问题：缺少依赖

运行 `pip install -r requirements.txt` 安装所需的库。

### 问题：输出文件太大

减少复制次数或读取的行数。

## 技术栈

- Python 3.6+
- pandas: 数据处理
- openpyxl: Excel文件读写
