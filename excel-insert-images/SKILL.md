---
name: excel-insert-images
description: 将图片批量插入Excel表格，支持横向（按行）和竖向（按列）两种模式，根据单元格名称自动匹配图片文件。当用户需要在Excel中插入图片、批量添加产品图片、创建产品对比表或根据文件名匹配图片时使用。
---

# Excel 批量插图工具

将图片批量插入 Excel 表格，支持**横向（按行）**和**竖向（按列）**两种插入模式。

## 功能说明

根据 Excel 单元格中的文件名，自动在图片文件夹中查找匹配图片并插入表格。适合产品图片、员工照片、对比表等场景。

## 两种模式

### 横向模式（horizontal）
- 文件名在**某一列**，图片插入到**该列的下一列**
- 逐行处理，适合产品列表、员工信息表等

```
A列: 编号 | B列: 产品名称  | C列: (插入图片)
1        | product1      | (自动插入 product1.jpg)
2        | product2      | (自动插入 product2.png)
```

### 竖向模式（vertical）
- 文件名在**某一行**，图片插入到**该行的下一行**
- 逐列处理，适合产品对比表、横向展示

```
      A列        B列        C列
1行: product1  product2  product3   (文件名)
2行: (图片1)   (图片2)   (图片3)    (自动插入)
```

## 使用方法

### 横向插入
```bash
python excel_insert_images.py \
    --excel products.xlsx \
    --images product_images/ \
    --mode horizontal \
    --name-col B \
    --start-row 1 \
    --end-row 100
```

### 竖向插入
```bash
python excel_insert_images.py \
    --excel comparison.xlsx \
    --images products/ \
    --mode vertical \
    --name-row 1 \
    --img-row 2 \
    --start-col 1 \
    --end-col 20 \
    --img-height 300
```

## 参数说明

### 通用参数

| 参数 | 说明 | 默认值 |
|------|------|--------|
| --excel | Excel 文件路径 | 必填 |
| --images | 图片文件夹路径 | 必填 |
| --mode | 插入模式：horizontal 或 vertical | horizontal |
| --output | 输出文件路径 | 覆盖原文件 |

### 横向模式参数

| 参数 | 说明 | 默认值 |
|------|------|--------|
| --name-col | 文件名所在列 | B |
| --start-row | 起始行号 | 1 |
| --end-row | 结束行号 | 30 |

### 竖向模式参数

| 参数 | 说明 | 默认值 |
|------|------|--------|
| --name-row | 文件名所在行 | 1 |
| --img-row | 图片插入行 | 2 |
| --start-col | 起始列号（1=A列） | 1 |
| --end-col | 结束列号（26=Z列） | 26 |
| --img-height | 图片高度（像素） | 300 |

## 功能特性

- 根据文件名自动匹配图片（不含扩展名）
- 支持 PNG, JPG, JPEG, BMP, GIF 格式
- 自动跳过空单元格和未匹配图片
- 竖向模式自动调整图片大小、列宽和居中
- 详细的处理日志

## 依赖项

- openpyxl

## 注意事项

- 图片文件名需要与 Excel 单元格的值匹配（不含扩展名）
- 默认会覆盖原文件，建议先备份
