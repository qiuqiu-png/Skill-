# My Claude Code Skills

我的 Claude Code 全局 Skills 集合，包含官方 Skills 和自定义 Skills。

## 📦 Skills 列表

### 🎨 官方 Skills（12个）

来自 [anthropics/skills](https://github.com/anthropics/skills) 仓库：

1. **algorithmic-art** - 算法艺术生成
2. **brand-guidelines** - 品牌指南
3. **canvas-design** - Canvas 设计
4. **document-skills** - 文档处理技能
5. **frontend-design** - 前端设计
6. **internal-comms** - 内部沟通
7. **mcp-builder** - MCP 构建器
8. **skill-creator** - Skill 创建器
9. **slack-gif-creator** - Slack GIF 创建器
10. **theme-factory** - 主题工厂
11. **web-artifacts-builder** - Web 工件构建器
12. **webapp-testing** - Web 应用测试

### 🛠️ 自定义 Skills（9个）

#### 📊 Excel 处理

1. **excel-row-copier** - 表格复制行数
   - 批量复制 Excel/WPS 表格的指定行数据
   - 支持自定义列范围和复制次数

2. **excel-insert-images-horizontal** - Excel 横向插图
   - 将图片按行插入 Excel 表格
   - 根据单元格名称自动匹配图片

3. **excel-insert-images-vertical** - Excel 竖向插图
   - 将图片按列插入 Excel 表格
   - 适合产品对比表和横向展示

#### 🎬 视频处理

4. **video-crop-borders** - 视频黑边裁剪
   - 自动检测并裁剪视频黑边
   - 保持原视频质量

5. **video-to-portrait** - 视频转竖屏
   - 将横屏视频转为 9:16 竖屏格式
   - 使用毛玻璃背景填充
   - 适配抖音、TikTok、Instagram Reels

6. **video-random-concatenate** - 视频随机拼接
   - 将视频按时长分段
   - 随机打乱顺序后拼接
   - 适合创建混剪视频

#### 🖼️ 图片处理

7. **image-batch-processor** - 图片批量处理
   - 批量压缩图片到指定大小
   - 转换为 JPG 格式
   - 智能质量调整

## 🚀 快速开始

### 安装到新电脑

```bash
# 克隆仓库到全局 Skills 目录
git clone <你的仓库URL> ~/.claude/skills
```

### 更新 Skills

```bash
cd ~/.claude/skills
git pull
```

### 提交更新

```bash
cd ~/.claude/skills
git add .
git commit -m "Update skills"
git push
```

## 📋 依赖安装

### Python Skills

```bash
# Excel 相关
pip install openpyxl pandas

# 图片处理
pip install Pillow
```

### 系统工具

```bash
# FFmpeg（视频处理必需）
brew install ffmpeg  # macOS
```

## 🔧 Skills 使用指南

### Excel Skills

**表格复制行数：**
```bash
cd ~/.claude/skills/excel-row-copier
python copy_rows.py data.xlsx output.xlsx A:A 22 128
```

**横向插图：**
```bash
cd ~/.claude/skills/excel-insert-images-horizontal
python insert_images_horizontal.py --excel data.xlsx --images photos/
```

**竖向插图：**
```bash
cd ~/.claude/skills/excel-insert-images-vertical
python insert_images_vertical.py --excel data.xlsx --images images/
```

### 视频 Skills

**裁剪黑边：**
```bash
cd ~/.claude/skills/video-crop-borders
python crop_video.py movie.mp4
```

**转竖屏：**
```bash
cd ~/.claude/skills/video-to-portrait
python to_portrait.py video.mp4 -r 1080x1920
```

**随机拼接：**
```bash
cd ~/.claude/skills/video-random-concatenate
python random_concatenate.py video.mp4 -d 5
```

### 图片 Skills

**批量处理：**
```bash
cd ~/.claude/skills/image-batch-processor
python process_images.py *.png --max-size 500
```

## 📝 创建新 Skill

1. 在 `~/.claude/skills/` 创建新目录
2. 添加 `SKILL.md` 文件（包含 YAML front matter）
3. 添加实现脚本
4. 提交到 Git

示例 SKILL.md：
```markdown
---
name: my-skill
description: 简短描述和触发条件
---

# Skill 名称

功能说明...
```

## 🔄 同步到多台电脑

### 方法 1：Git 同步（推荐）

当前方法，所有电脑共享同一个仓库。

### 方法 2：定期备份

```bash
# 备份
cd ~/.claude
tar -czf skills-backup-$(date +%Y%m%d).tar.gz skills/

# 恢复
cd ~/.claude
tar -xzf skills-backup-YYYYMMDD.tar.gz
```

## 🌟 Skills 开发规范

### 文件结构

```
skill-name/
├── SKILL.md          # 必需：Skill 元数据
├── README.md         # 可选：详细文档
├── main_script.py    # 必需：主脚本
├── requirements.txt  # 可选：Python 依赖
└── .gitignore       # 可选：Git 忽略规则
```

### 命名规范

- 目录名：小写字母 + 连字符（如 `excel-row-copier`）
- 脚本名：小写字母 + 下划线（如 `copy_rows.py`）
- Skill name：与目录名一致

### YAML Front Matter

```yaml
---
name: skill-name
description: 功能描述。触发条件说明。
---
```

## 📊 统计信息

- **总 Skills 数量：** 21
- **官方 Skills：** 12
- **自定义 Skills：** 9
- **最后更新：** 2025-12-01

## 📄 许可证

- 官方 Skills：遵循 anthropics/skills 仓库许可证
- 自定义 Skills：个人使用

## 🔗 相关资源

- [Claude Code 文档](https://code.claude.com/docs)
- [官方 Skills 仓库](https://github.com/anthropics/skills)
- [Skills 创建指南](https://code.claude.com/docs/en/skills.md)

---

**注意：** 本仓库包含个人定制的 Skills，仅供个人使用。如需分享，请确保已获得相关许可。
