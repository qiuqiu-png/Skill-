---
name: excel-insert-images-vertical
description: 将图片按列竖向插入Excel表格，根据首行单元格名称自动匹配图片文件。当用户需要在Excel中按列插入图片、创建产品对比表或横向展示多个图片时使用。
---

# Excel 竖向插图

将图片按列竖向插入 Excel 表格，根据首行的文件名自动匹配图片。

## 功能说明

这个 skill 可以根据 Excel 表格首行（或指定行）的文件名，自动查找对应的图片并插入到该列的下一行。适合创建产品对比表、横向展示多个产品图片等场景。

## 功能特性

- ✓ 根据文件名自动匹配图片
- ✓ 支持指定列范围批量插入
- ✓ 自动调整图片大小和列宽
- ✓ 图片水平居中对齐
- ✓ 支持自定义图片高度
- ✓ 支持多种图片格式（PNG, JPG, JPEG, BMP, GIF）
- ✓ 详细的处理日志

## 使用方法

### 基本用法

```bash
python insert_images_vertical.py \
    --excel /path/to/excel.xlsx \
    --images /path/to/images/
```

### 完整参数

```bash
python insert_images_vertical.py \
    --excel /path/to/excel.xlsx \
    --images /path/to/images/ \
    --output /path/to/output.xlsx \
    --name-row 1 \
    --img-row 2 \
    --start-col 1 \
    --end-col 26 \
    --img-height 300
```

## 参数说明

| 参数 | 说明 | 默认值 |
|------|------|--------|
| --excel | Excel 文件路径 | 必填 |
| --images | 图片文件夹路径 | 必填 |
| --output | 输出文件路径 | 覆盖原文件 |
| --name-row | 文件名所在行 | 1 |
| --img-row | 图片插入行 | 2 |
| --start-col | 起始列号（1=A列） | 1 |
| --end-col | 结束列号（26=Z列） | 26 |
| --img-height | 图片高度（像素） | 300 |

## 示例场景

### 场景 1：产品对比表

Excel 表格结构：
```
      A列        B列        C列        D列
1行: product1  product2  product3  product4  (文件名)
2行: (图片1)   (图片2)   (图片3)   (图片4)   (自动插入)
3行: 价格      价格      价格      价格
```

命令：
```bash
python insert_images_vertical.py \
    --excel comparison.xlsx \
    --images products/ \
    --name-row 1 \
    --img-row 2 \
    --start-col 1 \
    --end-col 10
```

### 场景 2：横向产品展示

```bash
python insert_images_vertical.py \
    --excel showcase.xlsx \
    --images photos/ \
    --img-height 400 \
    --start-col 1 \
    --end-col 20
```

## 工作原理

1. 读取指定行的文件名（自动去除扩展名）
2. 在图片文件夹中查找匹配的图片
3. 将图片插入到该列的指定行
4. 自动调整图片大小保持比例
5. 自动调整列宽以适应图片
6. 图片水平居中对齐

## 依赖项

- openpyxl

## 注意事项

- 图片文件名需要与 Excel 单元格的值匹配（不含扩展名）
- 图片会插入到指定的图片行
- 图片大小会按指定高度等比缩放
- 列宽会自动调整以适应图片宽度
- 图片会在单元格中水平居中
- 默认会覆盖原文件，建议先备份
