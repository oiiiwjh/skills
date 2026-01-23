# Git 提交约定规范

## 概述

良好的提交约定有助于：
- 生成清晰的变更日志
- 自动化版本管理
- 提高代码审查效率
- 便于问题追踪

## 提交消息格式

### 标准格式
```
<类型>(<范围>): <主题>

<正文>

<页脚>
```

### 各部分说明

#### 1. 类型（Type）
必填项，表示提交的性质：

| 类型 | 说明 | 示例 |
|------|------|------|
| `feat` | 新功能 | `feat(auth): 添加用户注册功能` |
| `fix` | 修复 bug | `fix(api): 修复用户查询接口500错误` |
| `docs` | 文档更新 | `docs(readme): 更新安装说明` |
| `style` | 代码格式（不影响功能） | `style(button): 调整按钮样式` |
| `refactor` | 重构代码 | `refactor(utils): 重构日期处理函数` |
| `test` | 测试相关 | `test(auth): 添加登录测试用例` |
| `chore` | 构建过程或辅助工具 | `chore(deps): 更新依赖包版本` |
| `perf` | 性能优化 | `perf(db): 优化数据库查询性能` |
| `ci` | CI/CD 相关 | `ci(github): 添加自动化测试工作流` |
| `build` | 构建系统 | `build(webpack): 优化打包配置` |
| `revert` | 回滚提交 | `revert: 回滚错误的合并提交` |

#### 2. 范围（Scope）
可选项，表示影响的范围：
- 模块名：`auth`, `api`, `ui`, `db`
- 文件名：`UserService.ts`, `login.vue`
- 功能区域：`authentication`, `payment`, `notification`

#### 3. 主题（Subject）
必填项，简洁的描述：
- 使用祈使句，现在时态
- 首字母小写
- 不要以句号结尾
- 长度不超过50个字符

#### 4. 正文（Body）
可选项，详细说明：
- 解释"为什么"而不是"做了什么"
- 每行不超过72个字符
- 使用空行分隔段落
- 使用列表说明多个更改

#### 5. 页脚（Footer）
可选项，引用信息：
- 关闭的问题：`Closes #123`, `Fixes #45`
- 重大变更：`BREAKING CHANGE: 移除旧API`
- 关联PR：`Related to PR #78`

## 示例

### 示例1：新功能
```
feat(auth): 实现OAuth2.0登录

- 添加Google OAuth2.0支持
- 实现JWT令牌生成和验证
- 添加用户信息存储

Closes #123
```

### 示例2：Bug修复
```
fix(api): 修复用户列表分页错误

当查询参数包含特殊字符时，分页逻辑会出错。
现在对参数进行URL编码处理。

Fixes #45
```

### 示例3：重构
```
refactor(utils): 重构日期处理函数

将分散的日期处理逻辑集中到DateUtils类中：
- 添加日期格式化方法
- 添加日期计算工具
- 统一时区处理

提高了代码的可维护性和复用性。
```

### 示例4：文档更新
```
docs(readme): 更新项目文档

- 添加快速开始指南
- 更新API文档链接
- 添加贡献指南
- 修复错别字
```

### 示例5：重大变更
```
feat(api): 重构用户认证接口

BREAKING CHANGE: 移除旧的Basic认证方式
- 新的认证接口使用Bearer Token
- 需要更新客户端代码
- 迁移指南见MIGRATION.md

Closes #89
```

## 分支命名约定

### 功能分支
```
feature/<类型>/<简短描述>
```
示例：
- `feature/auth/oauth-login`
- `feature/ui/dark-mode`
- `feature/api/user-profile`

### 修复分支
```
fix/<类型>/<问题描述>
```
示例：
- `fix/bug/login-error`
- `fix/security/xss-vulnerability`
- `fix/performance/db-query`

### 发布分支
```
release/<版本号>
```
示例：
- `release/v1.0.0`
- `release/v2.1.3`

### 热修复分支
```
hotfix/<问题描述>
```
示例：
- `hotfix/critical-security-fix`
- `hotfix/production-bug`

## 版本管理

### 语义化版本（SemVer）
格式：`主版本号.次版本号.修订号`

- **主版本号**：不兼容的API修改
- **次版本号**：向下兼容的功能性新增
- **修订号**：向下兼容的问题修正

### 版本标签
```bash
# 创建版本标签
git tag -a v1.0.0 -m "版本1.0.0：稳定发布"

# 推送标签
git push origin v1.0.0
```

## 自动化工具

### 1. Commitizen
交互式提交工具：
```bash
# 安装
npm install -g commitizen

# 使用
git cz
```

### 2. Commitlint
提交消息校验：
```bash
# 安装
npm install @commitlint/cli @commitlint/config-conventional

# 配置
echo "module.exports = {extends: ['@commitlint/config-conventional']}" > commitlint.config.js
```

### 3. Husky
Git钩子管理：
```bash
# 安装
npm install husky --save-dev

# 初始化
npx husky install

# 添加提交消息钩子
npx husky add .husky/commit-msg 'npx --no -- commitlint --edit "$1"'
```

### 4. Conventional Changelog
自动生成变更日志：
```bash
# 安装
npm install conventional-changelog-cli --save-dev

# 生成变更日志
npx conventional-changelog -p angular -i CHANGELOG.md -s
```

## 团队协作规范

### 1. 代码审查
- 每个PR至少需要1人审查
- 使用有意义的PR标题和描述
- 关联相关issue
- 确保所有测试通过

### 2. 合并策略
- 使用Squash Merge保持提交历史整洁
- 删除已合并的分支
- 更新本地仓库：`git fetch --prune`

### 3. 冲突解决
1. 定期从主分支拉取更新
2. 及时解决冲突
3. 避免长时间存在的分支

## 最佳实践

### 1. 提交频率
- 小步提交，每次提交一个逻辑单元
- 避免大而全的提交
- 提交前运行测试

### 2. 消息质量
- 使用英文提交消息（国际化团队）
- 保持主题简洁明了
- 在正文中解释变更原因

### 3. 工具集成
- 配置IDE的Git插件
- 使用Git GUI工具辅助
- 集成到CI/CD流程中

### 4. 培训和维护
- 新成员入职培训
- 定期回顾和改进规范
- 文档及时更新