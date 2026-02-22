---
name: video-to-portrait
description: 将横屏视频转换为 9:16 竖屏格式，使用毛玻璃背景填充。当用户需要转换视频为竖屏、适配短视频平台或提及抖音/TikTok/Instagram Reels时使用。
---

# 视频转竖屏

将横屏视频转换为 9:16 竖屏格式，使用毛玻璃背景填充。

## 功能说明

这个skill可以将横屏或方形视频转换为适合移动端和社交媒体的竖屏格式（9:16）。原视频居中显示，上下空白区域使用模糊放大的视频内容作为背景，呈现专业的毛玻璃效果。

## 功能特性

- ✓ 自动转换为 9:16 竖屏比例
- ✓ 原视频居中显示，保持完整内容
- ✓ 背景使用毛玻璃（高斯模糊）效果
- ✓ 支持自定义输出分辨率（1080x1920, 720x1280等）
- ✓ 支持批量处理
- ✓ 保持原视频质量和音频

## 使用方法

### 单个视频转换
```bash
python to_portrait.py video.mp4
```

### 指定输出分辨率
```bash
# 1080x1920 (默认)
python to_portrait.py video.mp4 --resolution 1080x1920

# 720x1280
python to_portrait.py video.mp4 --resolution 720x1280
```

### 批量处理
```bash
python to_portrait.py videos/*.mp4
```

### 自定义模糊强度
```bash
python to_portrait.py video.mp4 --blur 20
```

## 示例

```
# 基本用法
python to_portrait.py landscape.mp4

# 高清输出
python to_portrait.py video.mp4 -r 1080x1920

# 自定义模糊和输出路径
python to_portrait.py input.mp4 -o output/vertical.mp4 --blur 25
```

## 参数说明

| 参数 | 说明 | 默认值 |
|------|------|--------|
| input | 输入视频文件 | 必填 |
| -o, --output | 输出文件路径 | 自动生成 |
| -r, --resolution | 输出分辨率 | 1080x1920 |
| -b, --blur | 背景模糊强度 | 15 |

## 应用场景

- 抖音、快手等短视频平台
- Instagram Stories/Reels
- YouTube Shorts
- 微信视频号
- 其他竖屏社交媒体平台

## 依赖项

- FFmpeg（必需）

## 注意事项

- 确保已安装 FFmpeg
- 处理时间取决于视频长度和分辨率
- 输出文件默认添加 "_portrait" 后缀
- 建议使用 1080x1920 以获得最佳画质
