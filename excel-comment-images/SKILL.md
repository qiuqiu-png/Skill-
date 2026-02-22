---
name: excel-comment-images
description: 将图片以批注（备注）形式批量插入Excel单元格。鼠标悬停即可预览图片，不占用单元格空间。当用户需要在Excel批注中插入图片、添加产品预览图批注、或提到"批注插图"时使用。
---

# Excel 批注插图工具

将图片以**批注（备注）**形式插入到 Excel 单元格中。鼠标悬停在单元格上即可预览图片，不影响单元格内容和排版。

## 功能说明

根据 Excel 单元格中的文件名，自动在图片文件夹中查找匹配的图片，以批注背景图的方式插入。等效于 Windows VBA 中 `Shape.Fill.UserPicture` 的效果。

## 适用场景

- 产品款号列表，悬停查看款式图片
- 不想让图片占用单元格空间
- 需要类似 Windows VBA 批注插图的效果

## 使用方法

```bash
python excel_comment_images.py \
    --excel products.xlsx \
    --images product_images/ \
    --output products_with_comments.xlsx \
    --name-col C \
    --start-row 2 \
    --end-row 100 \
    --width 240 \
    --height 160
```

## 参数说明

| 参数 | 说明 | 默认值 |
|------|------|--------|
| --excel | Excel 文件路径 | 必填 |
| --images | 图片文件夹路径 | 必填 |
| --output | 输出文件路径 | 原文件名_批注.xlsx |
| --name-col | 文件名所在列 | C |
| --start-row | 起始行号 | 1 |
| --end-row | 结束行号 | 65536 |
| --width | 批注宽度（pt） | 240 |
| --height | 批注高度（pt） | 160 |

## 工作原理

1. 用 openpyxl 给匹配到图片的单元格添加空批注（生成 VML 骨架）
2. 保存后，将 xlsx（zip 包）中 openpyxl 生成的非标准 VML 替换为标准 VML
3. 在 VML 中使用 `v:fill type="frame"` 将图片设为批注背景
4. 图片文件写入 `xl/media/`，并添加关系引用

## 功能特性

- 根据文件名自动匹配图片（不含扩展名）
- 支持 PNG, JPG, JPEG, BMP, GIF 格式
- 自动跳过空单元格和未匹配图片
- 生成标准 VML（兼容 Excel for Mac / Windows）
- 详细的处理日志

## 依赖项

- openpyxl

## 与 excel-insert-images 的区别

| | excel-insert-images | excel-comment-images |
|---|---|---|
| 插入方式 | 直接嵌入单元格 | 以批注背景形式插入 |
| 是否占用空间 | 是，图片在单元格中显示 | 否，鼠标悬停才显示 |
| 适合场景 | 需要直接展示图片 | 不想影响表格排版 |
