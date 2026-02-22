---
name: video-crop-borders
description: 自动检测并裁剪视频中的黑边区域，保持原视频质量。当用户需要去除视频黑边、裁剪letterbox或提及视频裁剪时使用。
---

# 视频黑边裁剪

自动检测并裁剪视频中的黑边区域，保持原视频质量。

## 功能说明

这个skill可以自动检测视频中的黑边（letterbox/pillarbox），并精确裁剪掉黑边区域，生成无黑边的视频文件。支持单个视频和批量处理。

## 功能特性

- ✓ 自动检测黑边位置（上下左右）
- ✓ 精确裁剪，保持原视频质量
- ✓ 支持批量处理多个视频
- ✓ 保留原视频编码格式和参数
- ✓ 支持常见视频格式（mp4, avi, mkv, mov等）

## 使用方法

### 单个视频处理
```bash
python crop_video.py /path/to/video.mp4
```

### 批量处理
```bash
python crop_video.py /path/to/videos/*.mp4
```

### 指定输出目录
```bash
python crop_video.py video.mp4 --output /path/to/output
```

## 示例

```
# 单个视频
python crop_video.py movie.mp4

# 批量处理
python crop_video.py videos/*.mp4

# 自定义输出
python crop_video.py input.mp4 -o output/cropped.mp4
```

## 依赖项

- FFmpeg（系统工具）
- Python 3.6+

## 注意事项

- 需要先安装 FFmpeg：`brew install ffmpeg`（macOS）或其他平台的对应安装方式
- 处理时间取决于视频长度和分辨率
- 输出文件会自动添加 "_cropped" 后缀（如不指定输出路径）
- 黑边检测基于视频前30秒采样，确保足够准确
