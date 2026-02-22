---
name: image-batch-processor
description: 批量处理图片，压缩到指定大小并转换为 JPG 格式。当用户需要压缩图片、批量转换图片格式或优化图片大小时使用。
---

# 图片批量处理

批量压缩图片到指定大小并转换为 JPG 格式。

## 功能说明

这个 skill 可以批量处理图片文件，自动压缩到指定大小（默认 500KB）并转换为 JPG 格式，保留原文件名，输出到指定目录。

## 功能特性

- ✓ 自动压缩图片到指定大小（默认 500KB）
- ✓ 转换所有图片为 JPG 格式
- ✓ 保留原文件名
- ✓ 自动创建 output 输出目录
- ✓ 支持多种输入格式（PNG, JPEG, WebP, BMP, TIFF 等）
- ✓ 智能质量调整，确保文件大小符合要求
- ✓ 批量处理多个文件

## 使用方法

### 基本用法

```bash
# 处理单个图片
python process_images.py image.png

# 批量处理
python process_images.py *.png

# 处理指定目录
python process_images.py images/*.jpg
```

### 自定义参数

```bash
# 指定目标大小（KB）
python process_images.py *.png --max-size 300

# 自定义输出目录
python process_images.py *.png --output custom_output

# 指定初始质量
python process_images.py *.png --quality 85
```

## 示例

```bash
# 压缩到 500KB（默认）
python process_images.py photo.png

# 压缩到 300KB
python process_images.py *.jpg --max-size 300

# 批量处理并输出到指定目录
python process_images.py photos/*.png -o compressed_photos
```

## 参数说明

| 参数 | 说明 | 默认值 |
|------|------|--------|
| input | 输入图片文件（支持通配符） | 必填 |
| -s, --max-size | 目标文件大小上限（KB） | 500 |
| -o, --output | 输出目录 | output |
| -q, --quality | 初始 JPEG 质量（1-100） | 85 |

## 依赖项

- Pillow (PIL)

安装依赖：
```bash
pip install -r requirements.txt
```

或直接安装：
```bash
pip install Pillow
```

## 注意事项

- 输出目录不存在时会自动创建
- 如果图片已经小于目标大小，仍会转换为 JPG 格式
- 极小的目标大小可能导致图片质量明显下降
- 透明背景的图片（PNG）转换为 JPG 时会使用白色背景
- 建议目标大小设置在 200KB - 1MB 之间以保证质量
