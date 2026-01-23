# Git 快速参考手册

## 基础命令

### 配置
```bash
# 设置用户信息
git config --global user.name "Your Name"
git config --global user.email "email@example.com"

# 查看配置
git config --list
git config user.name

# 设置别名
git config --global alias.co checkout
git config --global alias.br branch
git config --global alias.ci commit
git config --global alias.st status
```

### 创建仓库
```bash
# 初始化新仓库
git init

# 克隆现有仓库
git clone <url>
git clone <url> <directory>
git clone --depth 1 <url>    # 浅克隆
```

### 基本工作流
```bash
# 检查状态
git status
git status -s               # 简短格式

# 添加文件
git add <file>
git add .                   # 所有文件
git add -A                  # 包括删除的文件
git add -p                  # 交互式添加

# 提交更改
git commit -m "message"
git commit -am "message"    # 添加并提交
git commit --amend          # 修改上次提交
```

## 分支管理

### 分支操作
```bash
# 查看分支
git branch                  # 本地分支
git branch -a               # 所有分支
git branch -r               # 远程分支
git branch -v               # 带最后提交

# 创建分支
git branch <name>
git checkout -b <name>      # 创建并切换
git switch -c <name>        # Git 2.23+

# 切换分支
git checkout <name>
git switch <name>           # Git 2.23+

# 删除分支
git branch -d <name>        # 安全删除
git branch -D <name>        # 强制删除

# 重命名分支
git branch -m <old> <new>
git branch -m <new>         # 当前分支
```

### 合并与变基
```bash
# 合并分支
git merge <branch>
git merge --no-ff <branch>  # 禁用快进合并

# 变基
git rebase <branch>
git rebase --continue       # 冲突解决后继续
git rebase --abort          # 中止变基
git rebase --skip           # 跳过当前提交

# 交互式变基
git rebase -i HEAD~3
```

## 远程操作

### 远程仓库
```bash
# 查看远程
git remote
git remote -v

# 添加远程
git remote add <name> <url>

# 修改远程
git remote set-url <name> <newurl>

# 删除远程
git remote remove <name>

# 重命名远程
git remote rename <old> <new>
```

### 推送与拉取
```bash
# 推送
git push <remote> <branch>
git push -u <remote> <branch>  # 设置上游
git push --force              # 强制推送（谨慎！）

# 拉取
git pull <remote> <branch>
git pull --rebase             # 变基方式拉取

# 获取
git fetch <remote>
git fetch --all
git fetch --prune             # 清理已删除的远程分支
```

## 查看历史

### 日志查看
```bash
# 基本日志
git log
git log --oneline            # 单行显示
git log --graph              # 图形化
git log --stat               # 显示文件统计
git log -p                   # 显示差异

# 过滤日志
git log -n 5                 # 最近5条
git log --since="2024-01-01"
git log --until="2024-12-31"
git log --author="name"
git log --grep="pattern"
git log <file>               # 文件历史

# 搜索提交
git log -S "function_name"   # 搜索代码
git log -G "regex"           # 正则搜索
```

### 差异比较
```bash
# 工作区差异
git diff                     # 未暂存的更改
git diff --staged            # 已暂存的更改
git diff HEAD                # 所有更改

# 提交间差异
git diff <commit1> <commit2>
git diff <branch1>..<branch2>
git diff <branch1>...<branch2>  # 共同祖先后的差异

# 文件差异
git diff -- <file>
git diff HEAD~1 -- <file>    # 与上次提交比较
```

## 撤销操作

### 撤销更改
```bash
# 撤销工作区更改
git checkout -- <file>
git restore <file>           # Git 2.23+

# 撤销暂存区更改
git reset HEAD <file>
git restore --staged <file>  # Git 2.23+

# 撤销提交
git reset --soft HEAD~1      # 保留更改到暂存区
git reset --mixed HEAD~1     # 保留更改到工作区（默认）
git reset --hard HEAD~1      # 丢弃所有更改（谨慎！）

# 恢复删除的文件
git checkout HEAD -- <file>
```

### 恢复提交
```bash
# 恢复特定提交
git revert <commit>          # 创建新提交撤销

# 恢复文件到特定版本
git checkout <commit> -- <file>

# 查找丢失的提交
git reflog                   # 查看所有操作历史
git fsck --lost-found        # 查找悬空对象
```

## 暂存与清理

### 暂存更改
```bash
# 基本暂存
git stash                    # 暂存当前更改
git stash save "message"     # 带消息暂存
git stash -u                 # 包括未跟踪文件

# 查看暂存
git stash list
git stash show stash@{0}     # 显示差异
git stash show -p stash@{0}  # 显示详细差异

# 恢复暂存
git stash pop                # 恢复并删除
git stash apply stash@{0}    # 恢复但不删除
git stash apply              # 恢复最新

# 删除暂存
git stash drop stash@{0}
git stash clear              # 清除所有
```

### 清理工作区
```bash
# 清理未跟踪文件
git clean -n                 # 预览要删除的文件
git clean -f                 # 强制删除
git clean -fd                # 包括目录
git clean -fx                # 包括.gitignore中的文件

# 重置工作区
git checkout -- .            # 撤销所有更改
git reset --hard HEAD        # 重置到最新提交
```

## 标签管理

### 创建标签
```bash
# 轻量标签
git tag v1.0.0

# 附注标签
git tag -a v1.0.0 -m "版本1.0.0"

# 特定提交打标签
git tag -a v1.0.0 <commit> -m "消息"

# 签名标签
git tag -s v1.0.0 -m "签名版本"
```

### 管理标签
```bash
# 查看标签
git tag
git tag -l "v1.*"           # 过滤标签
git show v1.0.0             # 查看标签详情

# 推送标签
git push origin v1.0.0
git push origin --tags      # 推送所有标签
git push origin --delete v1.0.0  # 删除远程标签

# 删除标签
git tag -d v1.0.0
```

## 高级操作

### 二分查找
```bash
# 开始二分查找
git bisect start
git bisect bad               # 标记当前为坏提交
git bisect good <commit>     # 标记已知好提交

# 测试当前提交
# 运行测试，然后标记结果
git bisect good              # 测试通过
git bisect bad               # 测试失败

# 结束二分查找
git bisect reset
```

### 子模块
```bash
# 添加子模块
git submodule add <url> <path>

# 初始化子模块
git submodule init
git submodule update

# 更新子模块
git submodule update --remote

# 删除子模块
git submodule deinit <path>
git rm <path>
```

### 补丁
```bash
# 创建补丁
git format-patch HEAD~3      # 最近3个提交
git format-patch -1 <commit> # 单个提交

# 应用补丁
git apply <patch>
git am <patch>               # 应用并提交
```

## 配置优化

### 常用配置
```bash
# 提高命令输出可读性
git config --global color.ui auto

# 设置默认编辑器
git config --global core.editor "code --wait"

# 设置差异工具
git config --global diff.tool vscode
git config --global difftool.vscode.cmd "code --wait --diff \$LOCAL \$REMOTE"

# 设置合并工具
git config --global merge.tool vscode
git config --global mergetool.vscode.cmd "code --wait \$MERGED"

# 自动修正命令
git config --global help.autocorrect 1

# 设置行尾处理
git config --global core.autocrlf input  # Linux/Mac
git config --global core.autocrlf true   # Windows
```

### 别名配置
```bash
# 添加到 ~/.gitconfig
[alias]
    co = checkout
    br = branch
    ci = commit
    st = status
    unstage = reset HEAD --
    last = log -1 HEAD
    lg = log --color --graph --pretty=format:'%Cred%h%Creset -%C(yellow)%d%Creset %s %Cgreen(%cr) %C(bold blue)<%an>%Creset' --abbrev-commit
    lol = log --graph --decorate --pretty=oneline --abbrev-commit
    lola = log --graph --decorate --pretty=oneline --abbrev-commit --all
    hist = log --pretty=format:'%h %ad | %s%d [%an]' --graph --date=short
    type = cat-file -t
    dump = cat-file -p
```

## 故障排除

### 常见问题
```bash
# 权限被拒绝
chmod 600 ~/.ssh/id_rsa

# 大文件问题
git filter-branch --tree-filter 'rm -f large_file' HEAD
git push origin --force

# 修复损坏的仓库
git fsck --full
git reflog expire --expire=now --all
git gc --prune=now --aggressive

# 撤销错误的合并
git reset --hard ORIG_HEAD
```

### 性能优化
```bash
# 清理仓库
git gc --aggressive --prune=now

# 压缩仓库
git repack -a -d --depth=250 --window=250

# 检查大文件
git verify-pack -v .git/objects/pack/*.idx | sort -k 3 -n | tail -10
```

## 最佳实践提示

### 日常使用
1. **小步提交**：每次提交一个逻辑单元
2. **有意义的消息**：使用约定式提交
3. **定期推送**：避免本地积压太多提交
4. **保持同步**：经常拉取远程更新

### 团队协作
1. **分支策略**：使用功能分支工作流
2. **代码审查**：所有更改通过PR合并
3. **解决冲突**：及时处理，避免积累
4. **清理分支**：合并后删除功能分支

### 安全注意事项
1. **不要强制推送**到共享分支
2. **备份重要更改**：使用stash或分支
3. **验证远程URL**：避免推送到错误仓库
4. **保护敏感信息**：不要提交密码、密钥等