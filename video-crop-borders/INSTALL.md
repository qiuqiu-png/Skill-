# 安装指南

## 系统要求

- Python 3.6 或更高版本
- FFmpeg（必需）

## 安装步骤

### 1. 安装 FFmpeg

#### macOS

使用 Homebrew：
```bash
brew install ffmpeg
```

#### Ubuntu/Debian

```bash
sudo apt update
sudo apt install ffmpeg
```

#### CentOS/RHEL

```bash
sudo yum install ffmpeg
```

#### Windows

1. 访问 [FFmpeg 官网](https://ffmpeg.org/download.html#build-windows)
2. 下载 Windows 构建版本
3. 解压到目录，如 `C:\ffmpeg`
4. 添加到系统 PATH：
   - 右键"此电脑" → 属性 → 高级系统设置
   - 环境变量 → 系统变量 → Path
   - 添加 `C:\ffmpeg\bin`

### 2. 验证 FFmpeg 安装

```bash
ffmpeg -version
```

应该看到 FFmpeg 的版本信息。

### 3. 使用 Skill

无需安装 Python 依赖包，脚本仅使用 Python 标准库。

直接运行：
```bash
python crop_video.py --help
```

## 快速测试

### 下载测试视频

```bash
# 使用 curl 下载一个测试视频（需要有黑边的视频）
curl -o test_video.mp4 "https://sample-videos.com/video123/mp4/720/big_buck_bunny_720p_1mb.mp4"
```

### 运行测试

```bash
python crop_video.py test_video.mp4
```

## 常见问题

### FFmpeg 未找到

**错误信息：**
```
✗ 错误：未找到 FFmpeg
```

**解决：**
1. 确认已安装 FFmpeg
2. 检查是否在 PATH 中：`which ffmpeg` (Unix) 或 `where ffmpeg` (Windows)
3. 重新启动终端

### Python 版本过低

**错误信息：**
```
SyntaxError: invalid syntax
```

**解决：**
确保使用 Python 3.6+：
```bash
python3 --version
# 或
python --version
```

如果版本过低，升级 Python：
- macOS: `brew upgrade python3`
- Ubuntu: `sudo apt install python3.9`

### 权限问题

**错误信息：**
```
Permission denied
```

**解决：**
```bash
# 添加执行权限
chmod +x crop_video.py

# 然后运行
./crop_video.py video.mp4
```

## 卸载

删除 skill 目录即可：
```bash
rm -rf /path/to/视频黑边裁剪
```

如果不再需要 FFmpeg：
- macOS: `brew uninstall ffmpeg`
- Ubuntu: `sudo apt remove ffmpeg`
