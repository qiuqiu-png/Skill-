# 视频黑边裁剪 Skill

自动检测并裁剪视频中的黑边区域，保持原视频质量的实用工具。

## 功能特性

- ✓ 自动检测黑边位置（上下左右全方位）
- ✓ 精确裁剪，保持原视频质量
- ✓ 支持批量处理多个视频文件
- ✓ 保留原视频编码参数
- ✓ 音频流无损复制
- ✓ 实时显示处理进度
- ✓ 支持所有 FFmpeg 支持的视频格式

## 前置要求

### 安装 FFmpeg

**macOS:**
```bash
brew install ffmpeg
```

**Ubuntu/Debian:**
```bash
sudo apt update
sudo apt install ffmpeg
```

**Windows:**
从 [FFmpeg 官网](https://ffmpeg.org/download.html) 下载并安装

**验证安装:**
```bash
ffmpeg -version
```

### Python 环境

- Python 3.6 或更高版本
- 无需额外 Python 依赖（仅使用标准库）

## 使用方法

### 基本用法

**处理单个视频：**
```bash
python crop_video.py movie.mp4
```
输出：`movie_cropped.mp4`

**指定输出路径：**
```bash
python crop_video.py input.mp4 -o output/result.mp4
```

**批量处理：**
```bash
python crop_video.py videos/*.mp4
```

**自定义采样时长：**
```bash
python crop_video.py video.mp4 --sample 60
```
使用前60秒进行黑边检测（默认30秒）

### 命令行参数

```
usage: crop_video.py [-h] [-o OUTPUT] [-s SAMPLE] input [input ...]

参数:
  input              输入视频文件（支持通配符）
  -o, --output       输出文件路径（仅单文件时有效）
  -s, --sample       黑边检测采样时长（秒），默认30秒
  -h, --help         显示帮助信息
```

## 工作原理

### 1. 黑边检测

工具使用 FFmpeg 的 `cropdetect` 滤镜分析视频：

- 采样视频前 N 秒（默认30秒）
- 检测上下左右的黑边区域
- 计算最优裁剪参数
- 参数格式：`width:height:x:y`

### 2. 视频裁剪

使用检测到的参数裁剪视频：

- 应用 `crop` 滤镜进行裁剪
- 音频流直接复制（无损）
- 视频流重编码为原格式
- 保持原视频质量参数

## 使用场景

### 场景 1：电影黑边裁剪

许多电影有上下黑边（letterbox格式）：

```bash
python crop_video.py movie.mkv
```

**效果：**
- 原始：1920x1080（含黑边）
- 裁剪后：1920x800（实际画面）

### 场景 2：批量处理剧集

```bash
python crop_video.py "TV Show/Season 1"/*.mp4
```

自动处理整季剧集的黑边。

### 场景 3：屏幕录制优化

屏幕录制可能包含黑色边框：

```bash
python crop_video.py screencast.mov -o clean_screencast.mov
```

### 场景 4：社交媒体优化

为社交媒体优化视频尺寸：

```bash
python crop_video.py raw_video.mp4 -o social_optimized.mp4
```

## 输出示例

```
============================================================
视频黑边裁剪工具
============================================================

正在分析视频: movie.mp4
采样前 30 秒进行黑边检测...
✓ 检测到黑边
  裁剪参数: 1920:800:0:140
  输出尺寸: 1920x800
  偏移位置: x=0, y=140

开始裁剪视频...
输入: movie.mp4
输出: movie_cropped.mp4
处理进度: 00:45:32.18
✓ 裁剪完成: movie_cropped.mp4
  原文件大小: 1250.45 MB
  新文件大小: 1048.32 MB
```

## 高级用法

### 批量处理脚本示例

创建 `batch_crop.sh`：

```bash
#!/bin/bash

# 批量处理指定目录下的所有视频
for file in ~/Videos/*.mp4; do
    python crop_video.py "$file" -o ~/Videos/Cropped/
done
```

### 与其他工具集成

```python
from crop_video import detect_crop, crop_video

# 在 Python 脚本中使用
crop_params = detect_crop('input.mp4')
if crop_params:
    crop_video('input.mp4', 'output.mp4', crop_params)
```

## 性能说明

**处理时间：**
- 检测阶段：通常 < 10秒（仅分析前30秒）
- 裁剪阶段：约等于视频时长的 0.5-2 倍
  - 1小时视频 ≈ 30-120分钟处理时间
  - 取决于：CPU性能、视频分辨率、编码格式

**文件大小：**
- 裁剪后文件通常略小于原文件
- 黑边越多，节省空间越明显
- 示例：裁剪掉20%黑边 → 文件减小约15-20%

## 注意事项

### 1. 黑边检测

- 采样时长影响准确性
- 场景变化大的视频建议增加采样时长（`--sample 60`）
- 如果检测不准确，可能是视频开头为黑屏/片头

### 2. 视频质量

- 工具会保持原视频的质量参数
- 重编码可能会有轻微质量损失（通常不可察觉）
- 音频始终无损复制

### 3. 文件管理

- 默认输出文件名添加 `_cropped` 后缀
- 如果输出文件已存在会被覆盖
- 建议先测试单个文件再批量处理

### 4. 兼容性

- 支持所有 FFmpeg 支持的格式
- 常见格式：mp4, avi, mkv, mov, wmv, flv
- 编解码器：H.264, H.265, VP9 等

## 故障排除

### 问题：未检测到黑边

**可能原因：**
- 视频实际没有黑边
- 黑边太小（<16像素）
- 采样时长不够

**解决方案：**
```bash
# 增加采样时长到60秒
python crop_video.py video.mp4 --sample 60
```

### 问题：FFmpeg 未找到

**错误信息：**
```
✗ 错误：未找到 FFmpeg
```

**解决方案：**
安装 FFmpeg 并确保在系统 PATH 中：
```bash
# macOS
brew install ffmpeg

# Ubuntu
sudo apt install ffmpeg

# 验证
which ffmpeg
```

### 问题：处理速度慢

**优化建议：**
- 关闭其他占用 CPU 的程序
- 检查硬盘读写速度（SSD 更快）
- 考虑使用硬件加速（需 FFmpeg 支持）

### 问题：输出文件过大

**可能原因：**
重编码使用了较高的比特率

**解决方案：**
修改脚本中的 FFmpeg 参数，添加 `-crf` 控制质量：
```python
# 在 crop_video 函数中添加
'-crf', '23',  # 质量因子，18-28，数值越小质量越高
```

## 技术细节

### cropdetect 参数说明

```
cropdetect=24:16:0
```

- `24`：黑色阈值（0-255），低于此值视为黑色
- `16`：圆整值，裁剪尺寸按此值对齐（编码器要求）
- `0`：跳过帧数，0表示分析所有帧

### crop 滤镜格式

```
crop=width:height:x:y
```

- `width`：裁剪后的宽度
- `height`：裁剪后的高度
- `x`：左上角 x 坐标偏移
- `y`：左上角 y 坐标偏移

## 扩展功能建议

可以基于此脚本扩展的功能：

- 添加 GUI 界面
- 支持预览裁剪效果
- 批量转换格式同时裁剪
- 添加其他视频滤镜（降噪、锐化等）
- 生成处理报告

## 许可证

本工具基于 Python 标准库和 FFmpeg，可自由使用和修改。

## 相关资源

- [FFmpeg 官方文档](https://ffmpeg.org/documentation.html)
- [cropdetect 滤镜文档](https://ffmpeg.org/ffmpeg-filters.html#cropdetect)
- [crop 滤镜文档](https://ffmpeg.org/ffmpeg-filters.html#crop)
