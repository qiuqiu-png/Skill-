---
name: excel-insert-images-horizontal
description: 将图片按行横向插入Excel表格，根据单元格名称自动匹配图片文件。当用户需要在Excel中按行插入图片、批量添加产品图片或根据文件名匹配图片时使用。
---

# Excel 横向插图

将图片按行横向插入 Excel 表格，根据指定列的文件名自动匹配图片。

## 功能说明

这个 skill 可以根据 Excel 表格中某一列的文件名，自动查找对应的图片并插入到相邻列中。适合批量处理产品图片、员工照片等需要按行排列的场景。

## 功能特性

- ✓ 根据文件名自动匹配图片
- ✓ 支持指定行范围批量插入
- ✓ 支持多种图片格式（PNG, JPG, JPEG, BMP, GIF）
- ✓ 自动跳过未找到图片的行
- ✓ 可自定义文件名列和插入位置
- ✓ 详细的处理日志

## 使用方法

### 基本用法

```bash
python insert_images_horizontal.py \
    --excel /path/to/excel.xlsx \
    --images /path/to/images/
```

### 完整参数

```bash
python insert_images_horizontal.py \
    --excel /path/to/excel.xlsx \
    --images /path/to/images/ \
    --output /path/to/output.xlsx \
    --start-row 1 \
    --end-row 100 \
    --name-col B
```

## 参数说明

| 参数 | 说明 | 默认值 |
|------|------|--------|
| --excel | Excel 文件路径 | 必填 |
| --images | 图片文件夹路径 | 必填 |
| --output | 输出文件路径 | 覆盖原文件 |
| --start-row | 起始行号 | 1 |
| --end-row | 结束行号 | 30 |
| --name-col | 文件名所在列 | B |

## 示例场景

### 场景 1：产品表格插入图片

Excel 表格结构：
```
A列: 编号  | B列: 产品名称 | C列: (插入图片)
1         | product1     | (自动插入 product1.jpg)
2         | product2     | (自动插入 product2.png)
```

命令：
```bash
python insert_images_horizontal.py \
    --excel products.xlsx \
    --images product_images/ \
    --name-col B
```

### 场景 2：员工信息表

```bash
python insert_images_horizontal.py \
    --excel employees.xlsx \
    --images photos/ \
    --start-row 2 \
    --end-row 500 \
    --name-col A
```

## 工作原理

1. 读取指定列的文件名（自动去除扩展名）
2. 在图片文件夹中查找匹配的图片
3. 将图片插入到文件名列的下一列
4. 自动处理指定行范围内的所有行

## 依赖项

- openpyxl

## 注意事项

- 图片文件名需要与 Excel 单元格的值匹配（不含扩展名）
- 图片会插入到文件名列的下一列
- 如果单元格为空或找不到对应图片，会跳过该行
- 默认会覆盖原文件，建议先备份
