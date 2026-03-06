---
name: update-readme
description: 根据当前目录内容、git提交记录和现有文档，自动更新README.md和AGENTS.md文件。当需要维护项目文档、同步最新项目状态、或基于代码库变化更新文档时使用此技能。适用于：1) 项目初始化后创建文档，2) 代码变更后更新文档，3) 定期维护项目文档，4) 同步团队协作信息到文档。
---

# Update Readme Skill

## 概述

自动分析和更新项目的README.md和AGENTS.md文档。扫描目录结构、分析git历史、检查现有文档，生成或更新项目文档以反映最新状态。

## 核心工作流程

### 1. 环境评估
- 检查git仓库状态
- 识别项目类型（前端、后端、全栈、工具库等）
- 检查现有文档文件
- 分析目录结构和关键文件

### 2. 数据收集
- **目录结构**：使用`glob`工具扫描
- **Git历史**：使用`git log`获取提交记录
- **包管理器**：检查package.json、requirements.txt等
- **配置文件**：识别.eslintrc、tsconfig.json、Dockerfile等
- **现有文档**：读取当前README.md和AGENTS.md

### 3. 文档生成策略
基于项目类型选择适当模板：
- **前端项目**：React/Vue/Angular/Svelte
- **后端项目**：Node.js/Python/Go/Rust
- **全栈项目**：包含前后端的完整应用
- **工具库**：npm包/Python库/Rust crate
- **配置项目**：Docker配置、部署脚本

### 4. 模板选择
- **新项目**：创建完整文档结构
- **现有项目**：更新特定章节，保持现有格式
- **AGENTS.md**：记录AI代理配置和使用说明

> **详细模板和示例**：参见 [references/README_templates.md](references/README_templates.md) 和 [references/AGENTS_template.md](references/AGENTS_template.md)

## 操作指南

### 更新现有README.md
1. 读取当前README.md，识别现有章节
2. 更新项目信息（版本、依赖、git历史）
3. 保持原有格式和风格
4. 智能添加缺失章节

### 创建新README.md
1. 分析项目类型
2. 选择适当模板
3. 填充具体内容（名称、描述、结构图）
4. 添加许可证信息

### 更新AGENTS.md
1. 读取当前AGENTS.md
2. 扫描代理配置文件（.agentrc、agent.config.js等）
3. 更新代理列表和配置
4. 添加使用示例

> **详细操作指南**：参见 [references/best_practices.md](references/best_practices.md)

## 工具使用指南

### 必需工具
- `bash`：执行git命令
- `read`：读取文档和配置
- `glob`：扫描目录结构
- `grep`：搜索内容
- `write`：写入文档

### 推荐工作流
```bash
# 1. 检查git状态
bash: git status
bash: git log --oneline -10

# 2. 扫描目录
glob: "**/*.json"
glob: "**/*.py"
glob: "**/*.js"

# 3. 读取关键文件
read: package.json
read: requirements.txt
read: Cargo.toml

# 4. 检查现有文档
read: README.md
read: AGENTS.md
```

## CLI Contract

`update-readme/scripts` 下核心脚本已统一支持标准 CLI：

- `python update-readme/scripts/analyze_project.py <path> [--json] [--output <file>]`
- `python update-readme/scripts/generate_readme.py --project-data <analysis.json> [--output README.md] [--update] [--json]`
- `python update-readme/scripts/update_agents.py [--project-data <analysis.json>] [--output AGENTS.md] [--update] [--json]`

退出码约定：
- `0`: 成功
- `1`: 运行时错误
- `2`: 参数错误

## 最佳实践

### 文档更新时机
1. 代码重大变更后
2. 版本发布前
3. 定期维护（每月）
4. 新功能添加后

### 保持文档质量
1. **准确性**：测试所有命令和示例
2. **完整性**：覆盖主要功能
3. **一致性**：统一格式和风格
4. **可读性**：清晰标题和代码块

### 避免的问题
1. 不要删除用户自定义内容
2. 不要过度格式化
3. 基于实际扫描结果
4. 使用相对路径

> **完整最佳实践指南**：参见 [references/best_practices.md](references/best_practices.md)

## 示例用例

### 用例1：初始化新项目文档
用户：请为我的新React项目创建README.md
技能：扫描目录 → 识别React项目 → 生成模板 → 填充信息 → 创建结构图

### 用例2：更新现有项目文档
用户：我刚添加了Docker支持，请更新README.md
技能：读取现有README → 检查Dockerfile → 添加Docker章节 → 更新说明

### 用例3：同步AGENTS.md
用户：我们新增了oracle代理配置，请更新AGENTS.md
技能：读取现有AGENTS.md → 检查.agentrc → 添加配置 → 更新列表

## 故障排除

### 常见问题
1. git仓库不存在：提示初始化或跳过
2. 配置文件缺失：使用默认值
3. 文档格式混乱：标准化格式
4. 权限问题：检查读写权限

### 错误处理
- 无法读取文件：记录警告并继续
- git命令失败：跳过git部分
- 写入失败：提供错误信息

## 资源

### 脚本
- `scripts/analyze_project.py`：项目分析
- `scripts/generate_readme.py`：README生成
- `scripts/update_agents.py`：AGENTS.md更新

### 参考文件
- `references/README_templates.md`：README模板
- `references/AGENTS_template.md`：AGENTS.md模板
- `references/best_practices.md`：最佳实践

### 资产文件
- `assets/project_structure_diagram.txt`：结构图模板
- `assets/example_asset.txt`：示例资产

> **完整资源列表**：查看各目录内容

## User-Learned Best Practices & Constraints

> **Auto-Generated Section**: This section is maintained by `skill-evolution-manager`. Do not edit manually.

### User Preferences
- 主README.md应作为多语言索引页面
- 详细文档放在语言特定文件中(README_cn.md, README_en.md)
- 使用清晰的技能分类表格展示所有技能

### Known Fixes & Workarounds
- 确保所有README文件保持同步更新
- 项目结构图应包含所有技能目录

### Custom Instruction Injection

更新README时：1) 检查技能总数和分类 2) 更新项目结构图 3) 确保多语言文档一致性 4) 添加新技能的详细描述和使用场景
