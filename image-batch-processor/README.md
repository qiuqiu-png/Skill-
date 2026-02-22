# 图片批量处理 Skill

批量压缩图片到指定大小并转换为 JPG 格式，保留原文件名。

## 功能特性

- ✓ 自动压缩图片到指定大小（默认 500KB）
- ✓ 智能质量调整，使用二分查找算法确保文件大小符合要求
- ✓ 转换所有图片为 JPG 格式
- ✓ 保留原文件名（仅改变扩展名）
- ✓ 自动创建输出目录（默认 output/）
- ✓ 支持多种输入格式（PNG, JPEG, WebP, BMP, TIFF, GIF）
- ✓ 处理透明背景（自动转为白色背景）
- ✓ 批量处理多个文件
- ✓ 详细的处理统计和进度显示

## 安装依赖

```bash
pip install -r requirements.txt
```

或直接安装：

```bash
pip install Pillow
```

## 使用方法

### 基本用法

**处理单个图片：**
```bash
python process_images.py photo.png
```
输出：`output/photo.jpg`（≤ 500KB）

**批量处理：**
```bash
python process_images.py *.png
```

**处理指定目录：**
```bash
python process_images.py images/*.jpg
```

### 自定义参数

**指定目标大小：**
```bash
# 压缩到 300KB
python process_images.py *.png --max-size 300

# 压缩到 1MB
python process_images.py *.jpg -s 1024
```

**自定义输出目录：**
```bash
python process_images.py *.png --output compressed_images
python process_images.py *.jpg -o my_output
```

**调整初始质量：**
```bash
# 使用较高初始质量（适合高质量图片）
python process_images.py *.png --quality 95

# 使用较低初始质量（快速压缩）
python process_images.py *.jpg -q 70
```

**组合参数：**
```bash
python process_images.py photos/*.png -s 300 -o compressed -q 90
```

## 命令行参数

```
usage: process_images.py [-h] [-s MAX_SIZE] [-o OUTPUT] [-q QUALITY] input [input ...]

参数:
  input                  输入图片文件（支持通配符）
  -s, --max-size        目标文件大小上限（KB），默认: 500
  -o, --output          输出目录，默认: output
  -q, --quality         初始 JPEG 质量（1-100），默认: 85
  -h, --help            显示帮助信息
```

## 工作原理

### 压缩算法

工具使用**二分查找算法**智能调整 JPEG 质量：

1. **初始化**：设置初始质量（默认 85）
2. **二分查找**：
   - 尝试不同质量值
   - 检查输出文件大小
   - 调整质量范围
3. **找到最佳质量**：在满足大小限制的前提下，使用最高质量
4. **保存图片**：使用最佳质量保存为 JPG

### 格式转换

- **RGB 图片**：直接处理
- **RGBA/透明图片**：添加白色背景后转换
- **其他模式**：自动转换为 RGB

## 使用场景

### 场景 1：网站图片优化

优化网站图片以提升加载速度：

```bash
python process_images.py website/images/*.png -s 300 -o optimized
```

### 场景 2：社交媒体发布

压缩图片以符合平台大小限制：

```bash
python process_images.py photos/*.jpg -s 500 -o social_media
```

### 场景 3：邮件附件

减小图片大小以便发送邮件：

```bash
python process_images.py documents/*.png -s 200 -o email_attachments
```

### 场景 4：存储空间优化

批量压缩照片以节省磁盘空间：

```bash
python process_images.py ~/Photos/*.jpg -s 800 -o ~/Photos_Compressed
```

## 输出示例

```
============================================================
图片批量处理工具
============================================================

输出目录: /Users/nanyu/output
目标大小: 500 KB
初始质量: 85
------------------------------------------------------------
处理: photo1.png ... ✓ 完成
  原始: 2456.3 KB → 压缩后: 487.2 KB
  压缩率: 80.2% | 质量: 78

处理: photo2.jpg ... ✓ 完成
  原始: 1234.5 KB → 压缩后: 498.7 KB
  压缩率: 59.6% | 质量: 82

处理: image3.webp ... ✓ 完成
  原始: 890.1 KB → 压缩后: 495.3 KB
  压缩率: 44.4% | 质量: 85

============================================================
处理完成！
成功: 3 | 失败: 0 | 总计: 3

统计:
  原始总大小: 4.39 MB
  压缩后总大小: 1.45 MB
  节省空间: 2.94 MB (66.9%)
```

## 支持的图片格式

### 输入格式

- JPEG/JPG
- PNG（包括透明背景）
- WebP
- BMP
- TIFF
- GIF

### 输出格式

- JPG（所有图片统一转换为 JPG）

## 性能说明

### 处理速度

| 图片数量 | 平均大小 | 处理时间 |
|---------|---------|---------|
| 10 张 | 2MB | ~5 秒 |
| 50 张 | 2MB | ~25 秒 |
| 100 张 | 2MB | ~50 秒 |

*速度取决于 CPU 性能和原始图片大小*

### 压缩效果

| 目标大小 | 适用场景 | 质量表现 |
|---------|---------|---------|
| 100-200KB | 缩略图、图标 | 可接受 |
| 300-500KB | 网页图片 | 良好 |
| 500-800KB | 社交媒体 | 优秀 |
| 1MB+ | 高质量展示 | 极佳 |

## 高级用法

### 批处理脚本

创建 `batch_compress.sh`：

```bash
#!/bin/bash

# 批量处理不同目录
for dir in Photos1 Photos2 Photos3; do
    echo "处理目录: $dir"
    python process_images.py "$dir"/*.jpg -s 500 -o "Compressed_$dir"
done

echo "全部完成！"
```

### 递归处理子目录

```bash
#!/bin/bash

# 查找并处理所有子目录中的图片
find . -type f \( -name "*.jpg" -o -name "*.png" \) -print0 | \
while IFS= read -r -d '' file; do
    python process_images.py "$file" -o output
done
```

### 与其他工具集成

```python
from process_images import compress_image

# 在 Python 脚本中使用
success, size, quality = compress_image(
    'input.png',
    'output.jpg',
    max_size_kb=500,
    initial_quality=85
)

if success:
    print(f"压缩成功！大小: {size/1024:.1f}KB, 质量: {quality}")
```

## 注意事项

### 1. 透明背景处理

PNG 图片的透明背景会自动转换为白色：

```
输入: logo.png (透明背景)
输出: logo.jpg (白色背景)
```

如需保留透明背景，原始图片应保持为 PNG 格式。

### 2. 文件命名

- 保留原文件名，仅改变扩展名为 `.jpg`
- 如果输出目录已存在同名文件，会被覆盖

### 3. 质量与大小

- 极小的目标大小（< 100KB）可能导致明显质量损失
- 建议目标大小设置在 200KB - 1MB 之间
- 对于大尺寸图片，可能需要更高的目标大小

### 4. 原始图片已很小

如果原始图片已经小于目标大小：
- 仍会转换为 JPG 格式
- 使用初始质量保存
- 可能会略微增大文件大小（取决于原始格式）

## 常见问题

### 问题 1：压缩后文件仍然过大

**原因：** 图片分辨率太高

**解决方案：**
```bash
# 降低目标大小
python process_images.py image.jpg -s 300
```

或使用图片编辑工具先降低分辨率。

### 问题 2：质量损失明显

**原因：** 目标大小设置过小

**解决方案：**
```bash
# 增加目标大小
python process_images.py image.jpg -s 800

# 或提高初始质量
python process_images.py image.jpg -q 95
```

### 问题 3：处理速度慢

**原因：** 图片文件很大或数量很多

**解决方案：**
- 使用较低的初始质量加快处理（-q 70）
- 分批处理
- 考虑使用更强的 CPU

### 问题 4：输出目录权限问题

**错误：** Permission denied

**解决方案：**
```bash
# 确保有写入权限
chmod 755 output

# 或使用其他目录
python process_images.py *.jpg -o ~/Documents/compressed
```

## 故障排除

### 依赖安装失败

```bash
# 升级 pip
pip install --upgrade pip

# 重新安装 Pillow
pip install --upgrade Pillow
```

### 图片格式不支持

确保输入文件是有效的图片文件：

```bash
# 检查文件类型
file image.png
```

### 内存不足

处理大量高分辨率图片时可能内存不足：

**解决方案：**
- 分批处理
- 关闭其他占用内存的程序
- 先降低图片分辨率

## 扩展功能建议

基于此工具可扩展的功能：

1. **调整分辨率**
   - 在压缩前先缩小图片尺寸
   - 更激进的文件大小控制

2. **添加水印**
   - 批量添加文字或图片水印
   - 自定义水印位置和透明度

3. **图片增强**
   - 自动调整亮度、对比度
   - 锐化、降噪处理

4. **元数据处理**
   - 移除 EXIF 信息以减小文件
   - 保留或添加版权信息

5. **多线程处理**
   - 并行处理多个图片
   - 充分利用多核 CPU

## 技术栈

- **Python 3.6+**
- **Pillow (PIL)**：图片处理库

## 许可证

本工具基于 Python 标准库和 Pillow 库，可自由使用和修改。

## 相关资源

- [Pillow 文档](https://pillow.readthedocs.io/)
- [JPEG 压缩原理](https://en.wikipedia.org/wiki/JPEG)
- [图片优化最佳实践](https://web.dev/fast/#optimize-your-images)
