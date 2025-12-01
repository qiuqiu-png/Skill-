# 视频随机拼接工具

将视频按指定时长分段，随机打乱顺序后拼接成新视频。

## 快速开始

### 安装依赖

确保已安装 FFmpeg：

```bash
# macOS
brew install ffmpeg

# Ubuntu
sudo apt install ffmpeg

# Windows
# 从 https://ffmpeg.org/download.html 下载
```

### 基本使用

```bash
# 每段5秒，随机打乱
python random_concatenate.py video.mp4 -d 5
```

## 功能特性

- ✅ 按指定时长自动分段
- ✅ 随机打乱片段顺序
- ✅ 支持保持原顺序
- ✅ 自动清理临时文件
- ✅ 支持批量处理
- ✅ 快速拼接（流复制模式）

## 详细文档

查看 [skill.md](./skill.md) 获取完整文档。


