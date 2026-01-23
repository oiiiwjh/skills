# Git 工作流程指南

## 基本 Git 工作流

### 1. 初始化仓库
```bash
# 初始化新的 Git 仓库
git init

# 克隆现有仓库
git clone <repository-url>
```

### 2. 配置 Git
```bash
# 设置用户名和邮箱
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"

# 设置默认编辑器
git config --global core.editor "code --wait"

# 查看配置
git config --list
```

### 3. 基本操作
```bash
# 检查状态
git status

# 添加文件到暂存区
git add <file>          # 添加特定文件
git add .               # 添加所有更改
git add -A              # 添加所有文件（包括删除的）

# 提交更改
git commit -m "提交消息"

# 查看提交历史
git log
git log --oneline       # 简洁格式
git log --graph         # 图形化显示分支
```

## GitHub 集成

### 1. 连接远程仓库
```bash
# 添加远程仓库
git remote add origin https://github.com/username/repository.git

# 查看远程仓库
git remote -v

# 修改远程仓库
git remote set-url origin <new-url>

# 删除远程仓库
git remote remove origin
```

### 2. 推送和拉取
```bash
# 推送到远程仓库
git push origin main

# 强制推送（谨慎使用）
git push -f origin main

# 拉取远程更改
git pull origin main

# 获取远程更改但不合并
git fetch origin
```

## 分支管理

### 1. 分支操作
```bash
# 创建分支
git branch <branch-name>

# 切换到分支
git checkout <branch-name>
git switch <branch-name>  # Git 2.23+

# 创建并切换到新分支
git checkout -b <branch-name>
git switch -c <branch-name>

# 查看分支
git branch              # 本地分支
git branch -a           # 所有分支（包括远程）
git branch -r           # 远程分支

# 删除分支
git branch -d <branch-name>     # 安全删除
git branch -D <branch-name>     # 强制删除
```

### 2. 合并分支
```bash
# 合并分支到当前分支
git merge <branch-name>

# 变基（重写历史）
git rebase <branch-name>

# 解决冲突后继续变基
git rebase --continue

# 中止变基
git rebase --abort
```

## 提交规范

### 1. 提交消息格式
```
<类型>(<范围>): <主题>

<正文>

<页脚>
```

### 2. 提交类型
- **feat**: 新功能
- **fix**: 修复 bug
- **docs**: 文档更新
- **style**: 代码格式（不影响功能）
- **refactor**: 重构代码
- **test**: 测试相关
- **chore**: 构建过程或辅助工具

### 3. 示例
```
feat(auth): 添加用户登录功能

- 实现 JWT 认证
- 添加登录页面
- 添加错误处理

Closes #123
```

## 高级操作

### 1. 撤销更改
```bash
# 撤销工作区更改
git checkout -- <file>

# 撤销暂存区更改
git reset HEAD <file>

# 撤销提交（保留更改）
git reset --soft HEAD~1

# 撤销提交（丢弃更改）
git reset --hard HEAD~1

# 修改上次提交
git commit --amend
```

### 2. 暂存更改
```bash
# 暂存当前工作
git stash

# 查看暂存列表
git stash list

# 恢复暂存
git stash pop

# 应用暂存但不删除
git stash apply

# 删除暂存
git stash drop
```

### 3. 标签管理
```bash
# 创建标签
git tag v1.0.0

# 创建带注释的标签
git tag -a v1.0.0 -m "版本 1.0.0"

# 推送标签
git push origin v1.0.0
git push origin --tags

# 删除标签
git tag -d v1.0.0
git push origin --delete v1.0.0
```

## 故障排除

### 1. 常见问题
```bash
# 修复损坏的仓库
git fsck

# 清理未跟踪文件
git clean -fd

# 重置到远程状态
git fetch origin
git reset --hard origin/main
```

### 2. 冲突解决
1. 查找冲突文件：`git status`
2. 编辑冲突文件（查找 `<<<<<<<`, `=======`, `>>>>>>>`）
3. 解决冲突后：`git add <file>`
4. 继续操作：`git commit` 或 `git rebase --continue`

## 最佳实践

### 1. 提交频率
- 小步提交，每次提交一个逻辑更改
- 提交前运行测试
- 编写有意义的提交消息

### 2. 分支策略
- `main`/`master`: 生产代码
- `develop`: 开发分支
- `feature/*`: 功能分支
- `hotfix/*`: 热修复分支
- `release/*`: 发布分支

### 3. 代码审查
- 使用 Pull Request 进行代码审查
- 确保代码通过所有测试
- 遵循代码规范
- 添加适当的文档

## 工具集成

### 1. Git GUI 工具
- GitHub Desktop
- GitKraken
- SourceTree
- VS Code Git 集成

### 2. CI/CD 集成
- GitHub Actions
- GitLab CI
- Jenkins
- CircleCI

### 3. 代码质量工具
- ESLint (JavaScript)
- Prettier (代码格式化)
- SonarQube (代码质量)
- CodeClimate (代码质量)