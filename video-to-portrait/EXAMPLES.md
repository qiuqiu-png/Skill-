# 使用示例

这里提供了各种实际使用场景的详细示例。

## 基础示例

### 示例 1：最简单的用法

将横屏视频转为竖屏：

```bash
python to_portrait.py landscape.mp4
```

**效果：**
- 输入：`landscape.mp4` (1920x1080)
- 输出：`landscape_portrait.mp4` (1080x1920)
- 背景：默认模糊强度 (15)

---

### 示例 2：指定输出路径

```bash
python to_portrait.py input.mp4 -o outputs/vertical_video.mp4
```

输出文件保存到 `outputs/` 目录。

---

### 示例 3：选择不同分辨率

**Full HD (推荐)：**
```bash
python to_portrait.py video.mp4 -r 1080x1920
```

**HD (节省空间)：**
```bash
python to_portrait.py video.mp4 -r 720x1280
```

**2K (高质量)：**
```bash
python to_portrait.py video.mp4 -r 1440x2560
```

---

## 平台优化示例

### 抖音/TikTok

```bash
# 标准设置
python to_portrait.py video.mp4 -r 1080x1920 -b 15

# 高质量版本
python to_portrait.py video.mp4 -r 1080x1920 -b 12
```

**输出规格：**
- 分辨率：1080x1920
- 比例：9:16
- 适合：抖音、TikTok 推荐页

---

### Instagram Reels

```bash
python to_portrait.py reel_content.mp4 -r 1080x1920 -b 18
```

**输出规格：**
- 分辨率：1080x1920
- 模糊背景增强视觉效果
- 适合：Instagram Reels、Stories

---

### YouTube Shorts

```bash
python to_portrait.py shorts_video.mp4 -r 1080x1920 -b 15
```

**输出规格：**
- 分辨率：1080x1920
- 标准模糊强度
- 适合：YouTube Shorts

---

### 微信视频号

```bash
python to_portrait.py wechat_video.mp4 -r 1080x1920 -b 16
```

**输出规格：**
- 分辨率：1080x1920
- 适中模糊效果
- 适合：微信视频号

---

## 批量处理示例

### 示例 1：处理整个文件夹

```bash
# 处理当前目录所有视频
python to_portrait.py *.mp4

# 处理指定目录
python to_portrait.py videos/*.mp4

# 处理多种格式
python to_portrait.py videos/*.{mp4,mov,avi}
```

---

### 示例 2：批量处理并统一参数

```bash
# 批量转为 HD 分辨率
python to_portrait.py videos/*.mp4 -r 720x1280 -b 20

# 批量高模糊效果
python to_portrait.py *.mp4 -b 25
```

---

### 示例 3：使用 Shell 脚本批量处理

创建 `batch_process.sh`：

```bash
#!/bin/bash

# 设置参数
RESOLUTION="1080x1920"
BLUR=15
INPUT_DIR="./raw_videos"
OUTPUT_DIR="./processed_videos"

# 创建输出目录
mkdir -p "$OUTPUT_DIR"

# 批量处理
for video in "$INPUT_DIR"/*.mp4; do
    filename=$(basename "$video" .mp4)
    echo "处理: $filename"

    python to_portrait.py "$video" \
        -o "$OUTPUT_DIR/${filename}_portrait.mp4" \
        -r "$RESOLUTION" \
        -b "$BLUR"
done

echo "全部完成！"
```

使用：
```bash
chmod +x batch_process.sh
./batch_process.sh
```

---

## 模糊效果对比

### 轻度模糊 (blur=10)

```bash
python to_portrait.py video.mp4 -b 10
```

**效果：** 背景细节清晰，模糊感较弱
**适用：** 需要展示背景内容时

---

### 中度模糊 (blur=15, 默认)

```bash
python to_portrait.py video.mp4 -b 15
```

**效果：** 平衡的模糊效果，视觉舒适
**适用：** 大多数场景

---

### 重度模糊 (blur=25)

```bash
python to_portrait.py video.mp4 -b 25
```

**效果：** 强烈模糊，突出前景内容
**适用：** 背景干扰较多的视频

---

### 超重模糊 (blur=35)

```bash
python to_portrait.py video.mp4 -b 35
```

**效果：** 几乎看不出背景细节
**适用：** 特殊艺术效果

---

## 特殊场景示例

### 场景 1：游戏录屏转竖屏

```bash
# 游戏画面通常是 16:9，需要强模糊
python to_portrait.py gameplay.mp4 -r 1080x1920 -b 20
```

**说明：**
- 游戏画面细节丰富，增加模糊强度
- Full HD 分辨率保证清晰度

---

### 场景 2：教程视频转竖屏

```bash
# 教程视频保持较清晰的背景
python to_portrait.py tutorial.mp4 -r 1080x1920 -b 12
```

**说明：**
- 轻度模糊，背景仍可辨识
- 方便观众看到完整内容

---

### 场景 3：电影片段转短视频

```bash
# 电影画幅通常更宽，需要适中模糊
python to_portrait.py movie_clip.mp4 -r 1080x1920 -b 18
```

**说明：**
- 保持电影质感
- 适中模糊保证美观

---

### 场景 4：Vlog 转竖屏

```bash
# Vlog 内容多样，使用标准设置
python to_portrait.py vlog.mp4 -r 1080x1920 -b 15
```

**说明：**
- 标准参数适合大多数 Vlog
- 平衡质量和处理速度

---

### 场景 5：直播回放转短视频

```bash
# 直播回放通常较长，可用 HD 加快处理
python to_portrait.py livestream.mp4 -r 720x1280 -b 16
```

**说明：**
- HD 分辨率减少处理时间
- 文件大小更小

---

## 分辨率选择指南

### 1080x1920 (Full HD)

```bash
python to_portrait.py video.mp4 -r 1080x1920
```

**优点：**
- 高清画质
- 主流平台推荐
- 细节丰富

**缺点：**
- 文件较大
- 处理时间较长

**适用：** 重要内容、专业发布

---

### 720x1280 (HD)

```bash
python to_portrait.py video.mp4 -r 720x1280
```

**优点：**
- 处理快速
- 文件较小
- 流量友好

**缺点：**
- 清晰度略降

**适用：** 日常发布、批量处理

---

### 1440x2560 (2K)

```bash
python to_portrait.py video.mp4 -r 1440x2560
```

**优点：**
- 超高清画质
- 适合大屏显示

**缺点：**
- 文件巨大
- 处理缓慢
- 多数手机无法充分利用

**适用：** 专业作品展示

---

## 组合其他工具

### 示例 1：先裁剪黑边，再转竖屏

```bash
# 步骤 1：裁剪黑边
cd ../视频黑边裁剪
python crop_video.py ../input.mp4 -o cropped.mp4

# 步骤 2：转竖屏
cd ../视频转竖屏
python to_portrait.py ../视频黑边裁剪/cropped.mp4 -r 1080x1920
```

---

### 示例 2：批量处理工作流

创建 `workflow.sh`：

```bash
#!/bin/bash

# 完整工作流：黑边裁剪 → 转竖屏

INPUT_DIR="./raw"
TEMP_DIR="./temp_cropped"
OUTPUT_DIR="./final_vertical"

mkdir -p "$TEMP_DIR" "$OUTPUT_DIR"

# 步骤 1：批量裁剪黑边
for video in "$INPUT_DIR"/*.mp4; do
    filename=$(basename "$video")
    python ../视频黑边裁剪/crop_video.py "$video" -o "$TEMP_DIR/$filename"
done

# 步骤 2：批量转竖屏
for video in "$TEMP_DIR"/*.mp4; do
    filename=$(basename "$video")
    python to_portrait.py "$video" -o "$OUTPUT_DIR/$filename" -r 1080x1920 -b 15
done

echo "工作流完成！"
```

---

## 性能优化示例

### 快速处理（牺牲少量质量）

修改脚本，使用 `fast` 预设：

```python
# 在 to_portrait.py 中修改
'-preset', 'fast',  # 原为 'medium'
```

然后运行：
```bash
python to_portrait.py video.mp4
```

**效果：** 处理速度提升 30-50%

---

### 高质量处理（较慢）

修改脚本，降低 CRF 值：

```python
# 在 to_portrait.py 中修改
'-crf', '20',  # 原为 '23'
```

然后运行：
```bash
python to_portrait.py video.mp4
```

**效果：** 画质提升，文件增大 20-30%

---

## 故障排查示例

### 问题：模糊效果不明显

**尝试：**
```bash
# 大幅增加模糊值
python to_portrait.py video.mp4 -b 30
```

---

### 问题：前景视频太小

**原因：** 原视频宽高比与 9:16 差异大

**解决：** 这是正常现象，保证了内容完整性

---

### 问题：输出文件很大

**解决：**
```bash
# 使用较低分辨率
python to_portrait.py video.mp4 -r 720x1280
```

或修改脚本提高压缩率：
```python
'-crf', '26',  # 增大 CRF 值
```

---

## 实际项目示例

### 项目：批量转换旅行 Vlog

**需求：**
- 30个横屏 Vlog 片段
- 转为竖屏发抖音
- 统一 1080x1920
- 中等模糊效果

**方案：**

```bash
#!/bin/bash

INPUT="./travel_vlogs"
OUTPUT="./douyin_ready"

mkdir -p "$OUTPUT"

for video in "$INPUT"/*.mp4; do
    filename=$(basename "$video" .mp4)
    python to_portrait.py "$video" \
        -o "$OUTPUT/${filename}_douyin.mp4" \
        -r 1080x1920 \
        -b 16
done
```

**结果：** 30个视频自动转换，直接可发布

---

### 项目：教程系列转竖屏

**需求：**
- 保留背景可见性
- 720p 节省空间
- 轻度模糊

**方案：**

```bash
python to_portrait.py tutorial_*.mp4 -r 720x1280 -b 10
```

---

## 进阶技巧

### 技巧 1：自定义输出文件命名

使用脚本循环自定义文件名：

```bash
#!/bin/bash

counter=1
for video in *.mp4; do
    python to_portrait.py "$video" \
        -o "vertical_$(printf "%03d" $counter).mp4" \
        -r 1080x1920
    ((counter++))
done
```

输出：`vertical_001.mp4`, `vertical_002.mp4`, ...

---

### 技巧 2：并行处理多个视频

```bash
#!/bin/bash

# 使用 GNU parallel 并行处理（需先安装）
ls *.mp4 | parallel -j 4 \
    python to_portrait.py {} -r 1080x1920 -b 15
```

**效果：** 同时处理 4 个视频，充分利用 CPU

---

### 技巧 3：根据视频内容调整参数

```bash
#!/bin/bash

for video in *.mp4; do
    # 获取视频分辨率
    resolution=$(ffprobe -v error -select_streams v:0 \
        -show_entries stream=width,height -of csv=p=0 "$video")

    width=$(echo $resolution | cut -d',' -f1)
    height=$(echo $resolution | cut -d',' -f2)

    # 根据宽高比选择模糊强度
    if (( width > height * 2 )); then
        # 超宽屏，增加模糊
        blur=25
    else
        # 普通宽屏，标准模糊
        blur=15
    fi

    python to_portrait.py "$video" -b $blur
done
```

---

## 总结

本示例集涵盖了：

- ✓ 基础用法
- ✓ 平台优化
- ✓ 批量处理
- ✓ 模糊效果调节
- ✓ 特殊场景应用
- ✓ 性能优化
- ✓ 实际项目案例
- ✓ 进阶技巧

根据你的具体需求选择合适的示例，开始创作精彩的竖屏内容！
