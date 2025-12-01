---
name: video-random-concatenate
description: 将视频按指定时长分段，随机打乱顺序后拼接成新视频。当用户需要创建混剪视频、随机播放效果或视频片段重组时使用。
---

# 视频随机拼接

将视频按指定时长分段，随机打乱顺序后拼接成新视频。

## 功能说明

这个skill可以将视频按照指定的时长分段，然后随机打乱这些片段的顺序，最后拼接成一个新的视频。非常适合用于创建有趣的混剪视频、随机播放效果等。

## 功能特性

- ✓ 按指定时长自动分段
- ✓ 随机打乱片段顺序
- ✓ 支持不打乱顺序（保持原顺序）
- ✓ 自动清理临时文件
- ✓ 支持批量处理
- ✓ 快速拼接（使用流复制，不重新编码）
- ✓ 支持设置随机种子（可重复结果）

## 使用方法

### 基本用法

```bash
# 每段5秒，随机打乱
python random_concatenate.py video.mp4 -d 5

# 指定输出文件
python random_concatenate.py video.mp4 -o output.mp4 -d 3
```

### 不打乱顺序

```bash
# 保持原顺序拼接（仅分段）
python random_concatenate.py video.mp4 -d 5 --no-shuffle
```

### 批量处理

```bash
python random_concatenate.py videos/*.mp4 -d 5
```

### 设置随机种子

```bash
# 使用固定种子，结果可重复
python random_concatenate.py video.mp4 -d 5 --seed 42
```

### 保留临时文件

```bash
# 用于调试，不自动清理临时文件
python random_concatenate.py video.mp4 -d 5 --no-cleanup
```

## 示例

```
# 基本用法：每段3秒，随机打乱
python random_concatenate.py movie.mp4 -d 3

# 指定输出路径
python random_concatenate.py input.mp4 -o output/random.mp4 -d 5

# 不打乱顺序，仅分段
python random_concatenate.py video.mp4 -d 2 --no-shuffle

# 批量处理多个视频
python random_concatenate.py *.mp4 -d 4
```

## 参数说明

| 参数 | 说明 | 默认值 |
|------|------|--------|
| input | 输入视频文件 | 必填 |
| -o, --output | 输出文件路径 | 自动生成（添加 _random 后缀） |
| -d, --duration | 每段时长（秒） | 必填 |
| --no-shuffle | 不打乱顺序 | False（默认打乱） |
| --no-cleanup | 不清理临时文件 | False（默认清理） |
| --seed | 随机种子 | None（随机） |

## 工作原理

1. **分段**：使用 FFmpeg 将视频按指定时长切分成多个片段
2. **打乱**：随机打乱片段顺序（可选）
3. **拼接**：使用 FFmpeg concat demuxer 将片段拼接成新视频
4. **清理**：自动删除临时分段文件

## 应用场景

- 创建随机混剪视频
- 视频随机播放效果
- 视频片段重组实验
- 快速视频编辑原型
- 创意视频制作

## 依赖项

- FFmpeg（必需）

## 注意事项

- 确保已安装 FFmpeg
- 分段时长建议根据视频总时长合理设置
- 处理时间取决于视频长度和分段数量
- 输出文件默认添加 "_random" 后缀
- 使用流复制模式，处理速度快，但要求所有片段编码格式一致
- 如果视频编码格式不一致，可能需要重新编码（速度较慢）

## 技术细节

- 使用 FFmpeg 的 `-ss` 和 `-t` 参数进行精确分段
- 使用 `-c copy` 直接复制流，避免重新编码，提高速度
- 使用 FFmpeg concat demuxer 进行拼接
- 临时文件存储在系统临时目录，处理完成后自动清理


