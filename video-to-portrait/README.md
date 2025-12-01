# 视频转竖屏 Skill

将横屏视频转换为 9:16 竖屏格式，使用专业的毛玻璃背景效果，完美适配短视频平台。

## 功能特性

- ✓ 自动转换为 9:16 竖屏比例（抖音、快手等平台标准）
- ✓ 原视频内容完整居中显示
- ✓ 上下空白区域使用毛玻璃（高斯模糊）背景填充
- ✓ 支持多种输出分辨率（1080x1920, 720x1280, 1440x2560）
- ✓ 可自定义背景模糊强度
- ✓ 支持批量处理多个视频
- ✓ 保持原视频质量和音频
- ✓ 实时进度显示

## 效果预览

```
┌─────────────────┐
│  ╔═══════════╗  │  ← 模糊背景（上）
│  ║           ║  │
│  ║  原视频   ║  │  ← 原视频居中（保持比例）
│  ║  居中     ║  │
│  ╚═══════════╝  │
│  ╔═══════════╗  │  ← 模糊背景（下）
└─────────────────┘
    9:16 竖屏
```

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

- Python 3.6+
- 无需额外 Python 依赖（仅使用标准库）

## 使用方法

### 基本用法

**转换单个视频：**
```bash
python to_portrait.py landscape_video.mp4
```
输出：`landscape_video_portrait.mp4`（1080x1920）

### 指定输出分辨率

**Full HD (1080x1920)：**
```bash
python to_portrait.py video.mp4 -r 1080x1920
```

**HD (720x1280)：**
```bash
python to_portrait.py video.mp4 -r 720x1280
```

**2K (1440x2560)：**
```bash
python to_portrait.py video.mp4 -r 1440x2560
```

### 自定义输出路径

```bash
python to_portrait.py input.mp4 -o output/vertical_video.mp4
```

### 调整背景模糊强度

```bash
# 轻度模糊
python to_portrait.py video.mp4 -b 10

# 中度模糊（默认）
python to_portrait.py video.mp4 -b 15

# 重度模糊
python to_portrait.py video.mp4 -b 25
```

### 批量处理

```bash
# 处理当前目录所有 MP4 文件
python to_portrait.py *.mp4

# 处理指定目录
python to_portrait.py videos/*.mp4

# 批量处理并指定参数
python to_portrait.py videos/*.mp4 -r 720x1280 -b 20
```

### 命令行参数完整说明

```
usage: to_portrait.py [-h] [-o OUTPUT] [-r RESOLUTION] [-b BLUR] input [input ...]

参数:
  input              输入视频文件（支持通配符）
  -o, --output       输出文件路径（仅单文件时有效）
  -r, --resolution   输出分辨率，格式：宽x高（默认：1080x1920）
  -b, --blur         背景模糊强度 1-100（默认：15）
  -h, --help         显示帮助信息
```

## 工作原理

### 视频处理流程

1. **输入分析**
   - 读取原视频分辨率和时长
   - 验证视频格式

2. **创建背景层**
   - 将原视频放大到目标尺寸（1080x1920）
   - 应用高斯模糊滤镜（gblur）
   - 创建毛玻璃效果

3. **创建前景层**
   - 将原视频等比缩放适应竖屏高度
   - 保持原视频完整内容和比例

4. **合成输出**
   - 将前景层居中叠加到背景层
   - 使用 H.264 编码保证质量
   - 保持原音频轨道

### FFmpeg 滤镜链

```
[输入视频]
    ↓
[分割为两路]
    ↓           ↓
[背景路径]    [前景路径]
    ↓           ↓
[放大填充]    [等比缩放]
    ↓           ↓
[高斯模糊]    [保持比例]
    ↓           ↓
    └─[居中叠加]─┘
         ↓
    [9:16 输出]
```

## 使用场景

### 场景 1：短视频平台发布

将横屏录制的内容转为竖屏格式：

```bash
python to_portrait.py gameplay.mp4 -r 1080x1920 -b 15
```

**适用平台：**
- 抖音 / TikTok
- 快手
- Instagram Reels
- YouTube Shorts
- 微信视频号

### 场景 2：批量处理教程视频

```bash
python to_portrait.py tutorials/*.mp4 -r 720x1280
```

适合将电脑录屏转为手机观看格式。

### 场景 3：电影片段转短视频

```bash
python to_portrait.py movie_clip.mp4 -r 1080x1920 -b 20
```

保持电影宽画幅的视觉效果，同时适配竖屏。

### 场景 4：横屏直播回放转竖屏

```bash
python to_portrait.py livestream.mp4 -r 1080x1920 -b 18
```

## 输出示例

```
============================================================
视频转竖屏工具 - 9:16 格式 + 毛玻璃背景
============================================================

开始转换视频...
输入: landscape_video.mp4
输出: landscape_video_portrait.mp4
分辨率: 1080x1920
模糊强度: 15
原始尺寸: 1920x1080

处理中...
进度: 100.0% (125/125秒)
✓ 转换完成: landscape_video_portrait.mp4
  原文件: 45.32 MB
  新文件: 38.76 MB
```

## 质量与性能

### 输出质量

- **编码器：** H.264 (libx264)
- **质量因子 (CRF)：** 23（平衡质量与文件大小）
- **编码预设：** medium（平衡速度与压缩率）
- **音频编码：** AAC 192kbps

### 处理性能

**处理时间估算：**
| 视频长度 | 分辨率 | 大致时间 |
|---------|--------|---------|
| 1分钟 | 1080x1920 | 30-60秒 |
| 5分钟 | 1080x1920 | 3-5分钟 |
| 15分钟 | 1080x1920 | 10-15分钟 |
| 1分钟 | 720x1280 | 15-30秒 |

*实际时间取决于 CPU 性能和原视频编码格式*

### 文件大小

- 通常比原文件略小（10-20%）
- 取决于原视频比特率和压缩程度
- 可通过调整 CRF 值控制大小/质量平衡

## 高级用法

### 修改编码参数

编辑 `to_portrait.py` 中的 FFmpeg 命令：

```python
# 提高质量（文件更大）
'-crf', '18',  # 默认 23

# 加快编码速度（质量略降）
'-preset', 'fast',  # 默认 medium

# 更高音频质量
'-b:a', '256k',  # 默认 192k
```

### 添加水印

在滤镜链中添加水印：

```python
filter_complex = (
    # ... 现有滤镜 ...
    f"[blurred][scaled]overlay=(W-w)/2:(H-h)/2[main];"
    f"[main]drawtext=text='@YourName':x=10:y=H-30:fontsize=24:fontcolor=white[final]"
)
```

### 批处理脚本示例

创建 `batch_convert.sh`：

```bash
#!/bin/bash

INPUT_DIR="$1"
OUTPUT_DIR="$2"

mkdir -p "$OUTPUT_DIR"

for video in "$INPUT_DIR"/*.mp4; do
    filename=$(basename "$video" .mp4)
    python to_portrait.py "$video" \
        -o "$OUTPUT_DIR/${filename}_portrait.mp4" \
        -r 1080x1920 \
        -b 15
done

echo "批量转换完成！"
```

使用：
```bash
chmod +x batch_convert.sh
./batch_convert.sh input_videos/ output_videos/
```

## 常见问题

### 问题 1：背景模糊不够明显

**解决方案：**
增加模糊强度参数：
```bash
python to_portrait.py video.mp4 -b 25
```

模糊强度建议范围：
- 轻度：10-15
- 中度：15-20
- 重度：20-30

### 问题 2：原视频在竖屏中太小

**原因：** 原视频的宽高比与目标比例差异较大

**解决方案：**
这是正常现象，工具保持原视频完整内容。如需放大，可修改缩放策略：

```python
# 修改脚本中的前景缩放部分
f"[fg]scale=-2:'min({target_height}*0.9,ih)':..."  # 增大到高度的90%
```

### 问题 3：处理速度慢

**优化建议：**

1. 使用较低分辨率：
   ```bash
   python to_portrait.py video.mp4 -r 720x1280
   ```

2. 修改编码预设为 fast：
   ```python
   '-preset', 'fast',  # 在脚本中修改
   ```

3. 使用硬件加速（需 FFmpeg 支持）：
   ```python
   '-hwaccel', 'auto',  # 添加到 FFmpeg 命令
   ```

### 问题 4：输出文件质量不佳

**解决方案：**

降低 CRF 值提高质量（编辑脚本）：
```python
'-crf', '20',  # 默认 23，越小质量越高
```

CRF 建议值：
- 高质量：18-20
- 标准质量：22-24（默认）
- 节省空间：26-28

### 问题 5：音频不同步

**原因：** 可能是原视频的音视频流存在问题

**解决方案：**
添加音频重采样参数（编辑脚本）：
```python
'-af', 'aresample=async=1',  # 音频同步
```

## 技术细节

### FFmpeg 滤镜说明

**split 滤镜：**
```
[0:v]split=2[bg][fg]
```
将输入视频流分为两路，用于背景和前景

**scale 滤镜（背景）：**
```
scale=1080:1920:force_original_aspect_ratio=increase
```
放大视频以填充目标尺寸，保持比例

**crop 滤镜：**
```
crop=1080:1920
```
裁剪到精确的目标尺寸

**gblur 滤镜：**
```
gblur=sigma=15
```
高斯模糊，sigma 值越大越模糊

**scale 滤镜（前景）：**
```
scale=-2:'min(1920,ih)':force_original_aspect_ratio=decrease
```
等比缩放原视频适应竖屏高度，-2 保证宽度为偶数

**overlay 滤镜：**
```
overlay=(W-w)/2:(H-h)/2
```
将前景居中叠加到背景，(W-w)/2 水平居中，(H-h)/2 垂直居中

### 推荐分辨率对照

| 平台 | 推荐分辨率 | 比例 |
|------|-----------|------|
| 抖音 | 1080x1920 | 9:16 |
| 快手 | 1080x1920 | 9:16 |
| Instagram Reels | 1080x1920 | 9:16 |
| YouTube Shorts | 1080x1920 | 9:16 |
| 微信视频号 | 1080x1920 | 9:16 |
| TikTok | 1080x1920 | 9:16 |

*所有主流短视频平台均支持 9:16 比例*

## 扩展建议

基于此工具可以扩展的功能：

1. **添加文字标题**
   - 在视频顶部或底部添加标题栏
   - 使用 drawtext 滤镜

2. **添加片头片尾**
   - 拼接品牌 logo 动画
   - 使用 concat 滤镜

3. **批量添加BGM**
   - 为静音视频添加背景音乐
   - 使用 amix 滤镜混音

4. **自动裁剪黑边**
   - 结合"视频黑边裁剪" skill
   - 先裁剪黑边再转竖屏

5. **智能内容检测**
   - 使用 AI 检测画面主体
   - 自动调整缩放中心点

## 许可证

本工具基于 Python 标准库和 FFmpeg，可自由使用和修改。

## 相关资源

- [FFmpeg 官方文档](https://ffmpeg.org/documentation.html)
- [FFmpeg 滤镜文档](https://ffmpeg.org/ffmpeg-filters.html)
- [视频滤镜示例](https://trac.ffmpeg.org/wiki/FilteringGuide)
- [短视频平台规范](https://support.google.com/youtube/answer/6375112)

## 相关 Skills

- **视频黑边裁剪** - 处理前先去除黑边
- **视频压缩** - 减小文件大小（待开发）
- **视频加速** - 调整播放速度（待开发）
