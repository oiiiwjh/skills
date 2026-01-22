---
name: update-readme
description: 根据当前目录内容、git提交记录和现有文档，自动更新README.md和AGENTS.md文件。当需要维护项目文档、同步最新项目状态、或基于代码库变化更新文档时使用此技能。适用于：1) 项目初始化后创建文档，2) 代码变更后更新文档，3) 定期维护项目文档，4) 同步团队协作信息到文档。
---

# Update Readme Skill

## 概述

此技能用于自动分析和更新项目的README.md和AGENTS.md文档。它会扫描当前目录结构、分析git提交历史、检查现有文档内容，然后生成或更新项目文档以反映最新状态。

## 核心工作流程

### 1. 环境评估
在开始更新前，技能会评估当前环境：
- 检查当前目录是否为git仓库
- 识别项目类型（前端、后端、全栈、工具库等）
- 检查现有README.md和AGENTS.md文件
- 分析目录结构和关键文件

### 2. 数据收集
技能收集以下信息：
- **目录结构**：使用`bash ls`和`glob`工具扫描文件
- **Git历史**：使用`git log`获取提交记录和贡献者
- **包管理器**：检查package.json、requirements.txt、Cargo.toml等
- **配置文件**：识别.eslintrc、tsconfig.json、Dockerfile等
- **现有文档**：读取当前README.md和AGENTS.md内容

### 3. 文档生成策略
基于项目类型和现有内容，技能选择适当的文档模板：

#### 项目类型识别：
- **前端项目**：React/Vue/Angular/Svelte等
- **后端项目**：Node.js/Python/Go/Rust等
- **全栈项目**：包含前后端的完整应用
- **工具库**：npm包/Python库/Rust crate等
- **配置/脚本项目**：Docker配置、部署脚本等

#### 文档模板选择：
- **新项目**：创建完整的README.md结构
- **现有项目**：更新特定章节，保持现有格式
- **AGENTS.md**：专门记录AI代理配置和使用说明

### 4. README.md结构
标准README.md包含以下章节：

```markdown
# 项目名称

[简短的项目描述]

## 功能特性
- 主要功能1
- 主要功能2
- 主要功能3

## 快速开始

### 安装
```bash
[安装命令]
```

### 使用
```bash
[使用示例]
```

## 项目结构
```
project/
├── src/
├── tests/
├── docs/
└── ...
```

## 配置
[配置说明]

## 开发
[开发指南]

## 贡献
[贡献指南]

## 许可证
[许可证信息]
```

### 5. AGENTS.md结构
AGENTS.md专门记录AI代理配置：

```markdown
# AI代理配置

## 可用代理
- **explore**：代码库探索和模式匹配
- **librarian**：文档搜索和代码实现查找
- **oracle**：架构设计和调试专家
- **frontend-ui-ux-engineer**：前端UI/UX开发专家
- **document-writer**：技术文档编写专家

## 配置说明
[各代理的配置和使用说明]

## 使用示例
[具体使用示例]

## 最佳实践
[使用建议和注意事项]
```

## 具体操作指南

### 更新现有README.md
1. **检查现有结构**：读取当前README.md，识别现有章节
2. **更新项目信息**：
   - 从package.json/requirements.txt更新版本和依赖
   - 从git log更新最近提交和贡献者
   - 扫描目录更新项目结构
3. **保持格式一致**：尽量保持原有格式和风格
4. **添加缺失章节**：如果缺少标准章节，智能添加

### 创建新README.md
1. **分析项目类型**：根据文件结构确定项目类型
2. **生成适当模板**：选择最适合的README模板
3. **填充具体内容**：
   - 从package.json获取项目名称和描述
   - 从目录结构生成项目结构图
   - 从配置文件提取安装和使用说明
4. **添加许可证信息**：检查LICENSE文件或package.json中的许可证

### 更新AGENTS.md
1. **检查现有代理配置**：读取当前AGENTS.md
2. **扫描代理相关文件**：查找.agentrc、agent.config.js等配置文件
3. **更新代理列表**：确保所有可用代理都被记录
4. **添加使用示例**：基于实际使用情况添加示例

## 工具使用指南

### 必需工具
- `bash`：执行git命令和目录扫描
- `read`：读取现有文档和配置文件
- `glob`：扫描目录结构
- `grep`：搜索特定内容
- `write`：写入更新后的文档

### 推荐工具组合
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

## 最佳实践

### 文档更新时机
1. **代码重大变更后**：API变化、架构调整
2. **版本发布前**：确保文档与代码同步
3. **定期维护**：每月检查一次文档准确性
4. **新功能添加后**：及时更新功能说明

### 保持文档质量
1. **准确性**：确保所有命令和示例都能正常工作
2. **完整性**：覆盖所有主要功能和配置选项
3. **一致性**：保持格式和风格统一
4. **可读性**：使用清晰的标题和适当的代码块

### 避免的问题
1. **不要删除用户自定义内容**：保留用户添加的特殊说明
2. **不要过度格式化**：保持简洁实用的风格
3. **不要假设项目结构**：基于实际扫描结果
4. **不要硬编码路径**：使用相对路径和通用命令

## 示例用例

### 用例1：初始化新项目文档
```
用户：请为我的新React项目创建README.md
技能：扫描目录 → 识别React项目 → 生成React专用README模板 → 填充package.json信息 → 创建项目结构图
```

### 用例2：更新现有项目文档
```
用户：我刚添加了Docker支持，请更新README.md
技能：读取现有README → 检查Dockerfile → 添加Docker章节 → 更新安装和使用说明 → 保持原有格式
```

### 用例3：同步AGENTS.md
```
用户：我们新增了oracle代理配置，请更新AGENTS.md
技能：读取现有AGENTS.md → 检查.agentrc文件 → 添加oracle配置说明 → 更新代理列表 → 添加使用示例
```

## 故障排除

### 常见问题
1. **git仓库不存在**：提示用户初始化git仓库或跳过git历史
2. **配置文件缺失**：使用合理的默认值或提示用户提供
3. **文档格式混乱**：尝试标准化格式，保留重要内容
4. **权限问题**：检查文件读写权限

### 错误处理
- 如果无法读取文件，记录警告并继续
- 如果git命令失败，跳过git相关部分
- 如果写入失败，提供错误信息和回退方案

## 资源

### 脚本目录
- `scripts/analyze_project.py`：项目分析工具
- `scripts/generate_readme.py`：README生成器
- `scripts/update_agents.py`：AGENTS.md更新工具

### 参考文件
- `references/README_templates.md`：各种项目类型的README模板
- `references/AGENTS_template.md`：AGENTS.md标准模板
- `references/best_practices.md`：文档最佳实践指南

### 资产文件
- `assets/project_structure_diagram.txt`：项目结构图模板
- `assets/badges.md`：常用徽章（构建状态、版本、许可证等）
- `assets/license_templates/`：各种许可证模板
