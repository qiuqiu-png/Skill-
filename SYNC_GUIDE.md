# Skills Git 同步指南

本仓库使用 Git 管理所有 Claude Code Skills，方便在多台电脑间同步。

## 📦 当前状态

✅ Git 仓库已初始化
✅ 所有 Skills 已提交（321 个文件，21 个 Skills）
⏳ 待配置远程仓库

## 🚀 快速开始

### 1. 配置远程仓库（首次）

**方法 A：使用 GitHub**

```bash
# 在 GitHub 创建私有仓库（推荐私有，因为包含个人配置）
# 仓库名建议：claude-skills

# 添加远程仓库
cd ~/.claude/skills
git remote add origin https://github.com/你的用户名/claude-skills.git

# 推送到 GitHub
git branch -M main
git push -u origin main
```

**方法 B：使用 GitLab**

```bash
# 在 GitLab 创建私有仓库

# 添加远程仓库
cd ~/.claude/skills
git remote add origin https://gitlab.com/你的用户名/claude-skills.git

# 推送
git branch -M main
git push -u origin main
```

**方法 C：使用 Gitee（国内）**

```bash
# 在 Gitee 创建私有仓库

# 添加远程仓库
cd ~/.claude/skills
git remote add origin https://gitee.com/你的用户名/claude-skills.git

# 推送
git branch -M main
git push -u origin main
```

---

### 2. 在新电脑上克隆

```bash
# 克隆仓库到全局 Skills 目录
git clone https://github.com/你的用户名/claude-skills.git ~/.claude/skills

# 安装依赖
cd ~/.claude/skills

# Python Skills 依赖
pip install openpyxl pandas Pillow

# 系统工具（视频处理需要）
brew install ffmpeg  # macOS
```

---

## 📝 日常使用

### 更新 Skills（在电脑 A 上修改后）

```bash
cd ~/.claude/skills

# 1. 查看修改
git status

# 2. 添加修改
git add .

# 3. 提交
git commit -m "描述你的修改"

# 4. 推送到远程
git push
```

### 同步 Skills（在电脑 B 上）

```bash
cd ~/.claude/skills

# 拉取最新更新
git pull
```

---

## 🔄 常用命令

### 查看状态

```bash
cd ~/.claude/skills
git status              # 查看当前状态
git log --oneline -10   # 查看最近 10 次提交
```

### 提交更新

```bash
cd ~/.claude/skills
git add .
git commit -m "更新描述"
git push
```

### 拉取更新

```bash
cd ~/.claude/skills
git pull
```

### 查看远程仓库

```bash
cd ~/.claude/skills
git remote -v
```

---

## 📋 自动化脚本

### 创建快速同步脚本

创建 `~/.claude/skills/sync.sh`：

```bash
#!/bin/bash
cd ~/.claude/skills

echo "=== Skills 同步 ==="
echo ""

# 检查是否有修改
if [[ -n $(git status -s) ]]; then
    echo "发现修改，准备提交..."
    git add .

    # 自动生成提交信息
    TIMESTAMP=$(date "+%Y-%m-%d %H:%M:%S")
    git commit -m "Auto sync: $TIMESTAMP"

    echo "推送到远程..."
    git push
    echo "✓ 同步完成"
else
    echo "没有修改，拉取远程更新..."
    git pull
    echo "✓ 已是最新版本"
fi
```

使用：
```bash
chmod +x ~/.claude/skills/sync.sh
~/.claude/skills/sync.sh
```

---

## 🔐 SSH 密钥配置（推荐）

使用 SSH 密钥可以避免每次输入密码。

### 1. 生成 SSH 密钥

```bash
ssh-keygen -t ed25519 -C "your_email@example.com"
```

### 2. 添加到 GitHub/GitLab

```bash
# 复制公钥
cat ~/.ssh/id_ed25519.pub

# 在 GitHub: Settings → SSH and GPG keys → New SSH key
# 粘贴公钥内容
```

### 3. 修改远程 URL 为 SSH

```bash
cd ~/.claude/skills
git remote set-url origin git@github.com:你的用户名/claude-skills.git
```

---

## 🆘 常见问题

### 问题 1：推送被拒绝

**错误：**
```
! [rejected]        main -> main (fetch first)
```

**解决：**
```bash
# 先拉取，再推送
git pull --rebase
git push
```

### 问题 2：合并冲突

**解决：**
```bash
# 查看冲突文件
git status

# 手动编辑冲突文件，然后
git add .
git commit -m "解决冲突"
git push
```

### 问题 3：忘记提交就修改了

**解决：**
```bash
# 暂存当前修改
git stash

# 拉取远程更新
git pull

# 恢复暂存的修改
git stash pop
```

### 问题 4：需要回退到之前的版本

**解决：**
```bash
# 查看提交历史
git log --oneline

# 回退到指定提交（不删除后续提交）
git revert <commit-hash>

# 或者硬重置（慎用）
git reset --hard <commit-hash>
```

---

## 📊 最佳实践

### ✅ 推荐做法

1. **定期同步**：每次使用前先 `git pull`
2. **及时提交**：修改后及时 `git commit`
3. **清晰的提交信息**：描述清楚修改了什么
4. **使用 SSH**：避免频繁输入密码
5. **备份重要修改**：重大修改前先创建分支

### ❌ 避免做法

1. **不要**提交大文件（视频、大图片等）
2. **不要**提交敏感信息（密码、API 密钥）
3. **不要**直接在 main 分支做实验
4. **不要**强制推送 `git push -f`（除非你知道在做什么）

---

## 🌿 进阶：使用分支

### 创建实验分支

```bash
# 创建并切换到新分支
git checkout -b experimental

# 进行实验性修改
git add .
git commit -m "实验性功能"

# 切换回主分支
git checkout main

# 如果实验成功，合并分支
git merge experimental

# 删除实验分支
git branch -d experimental
```

---

## 📈 监控和维护

### 查看仓库大小

```bash
cd ~/.claude/skills
du -sh .git
```

### 清理历史（如果仓库过大）

```bash
# 清理未追踪的文件
git clean -fd

# 压缩仓库
git gc --aggressive --prune=now
```

---

## 🎯 推荐工作流

### 单人使用

```
修改 Skills → git add . → git commit -m "..." → git push
                                                    ↓
                                                  GitHub
                                                    ↑
在新电脑上 ← git pull ← git clone（首次）
```

### 多人协作（团队）

```
创建分支 → 修改 → 提交 → Push → 创建 PR → 代码审查 → 合并
```

---

## 🔗 相关资源

- [Git 官方文档](https://git-scm.com/doc)
- [GitHub 使用指南](https://docs.github.com/)
- [Git 可视化学习](https://learngitbranching.js.org/)

---

**最后更新：** 2025-12-01
**仓库状态：** ✅ 已初始化，待配置远程仓库
