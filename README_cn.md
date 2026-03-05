# OpenCode 技能仓库

一个模块化、自包含的技能集合，用于扩展 Claude 的能力，提供专业化的知识、工作流程和工具集成。

## 概述

本仓库包含用于 OpenCode 代理的技能。技能是针对特定领域或任务的"入职指南"——它们将 Claude 从一个通用代理转变为具备程序化知识的专业化代理，这些知识是任何模型都无法完全掌握的。

技能目录策略：真实技能统一维护在 `~/.agents/skills`，其他工具目录通过软链接使用这些技能。

## 可用技能

### 📄 **paper-detailed-analysis** (论文深度分析)
**描述**: 深度论文分析技能，专注于从PDF学术论文中提取关键信息，生成连贯、详实、富有洞察力的研究笔记。适用于计算机图形学、AI、机器学习等领域的学术论文分析。

**使用场景**:
- 分析PDF学术论文或arXiv链接
- 生成结构化、详细的研究笔记
- 结合论文分析与代码仓库检查
- 进行研究背景调查

### 📚 **paper-depth-reading** (论文深度阅读)
**描述**: 针对计算机图形学和AI研究论文的综合性学术论文分析技能。提供结构化框架，用于提取研究背景、方法、实验，并将论文概念与代码实现连接起来。

**使用场景**:
- 对带有代码实现的学术论文进行深度结构化分析
- 理解复杂的研究方法
- 将理论概念与实际代码实现连接
- 分析计算机图形学、计算机视觉和AI研究论文

### ✨ **humanizer** (文本人性化)
**描述**: AI文本人性化技能，用于去除文本中的AI生成痕迹。基于维基百科的"AI写作迹象"综合指南。检测并修复24种常见的AI写作模式。

**使用场景**:
- 人性化AI生成的文本，使其听起来更自然
- 去除重复的AI写作模式
- 提高文本可读性和真实性
- 使用 `/humanizer [文本]` 命令处理文本

### ✨ **humanizer-zh** (中文文本人性化)
**描述**: 专门针对中文文本的AI写作痕迹去除技能。基于维基百科的"AI写作特征"综合指南，检测并修复夸大的象征意义、宣传性语言、肤浅分析、模糊归因、破折号过度使用、三段式法则、AI词汇、否定式排比、过多连接性短语等模式。

**使用场景**:
- 去除中文文本中的AI生成痕迹
- 编辑或审阅中文文本，使其更自然
- 修复中文AI写作的特定模式
- 提升中文文本的人性化和可读性

### 🛠️ **skill-creator** (技能创建器)
**描述**: 创建有效技能的指南。当用户想要创建新技能（或更新现有技能）以扩展Claude的专业知识、工作流程或工具集成能力时，应使用此技能。

**使用场景**:
- 创建新的OpenCode技能
- 修改现有技能
- 理解技能开发模式
- 生成 OpenAI 技能元数据

### 📚 **latex-lite-template-builder** (LaTeX 轻量模板构建器)
**描述**: 从已有 LaTeX 模板目录构建可复用的轻量论文模板，支持脚本化生成与可选 Overleaf 打包输出。

**使用场景**:
- 将已有论文样式迁移为可复用模板
- 生成精简的论文骨架项目
- 输出便于 Overleaf 使用的模板包

### 📥 **skill-installer** (技能安装器)
**描述**: 将 Codex 技能安装到 `$CODEX_HOME/skills`，支持从预置列表或 GitHub 仓库路径安装。

**使用场景**:
- 查看可安装的预置技能
- 快速安装预置技能
- 从 GitHub 仓库路径安装技能

### 📝 **update-readme** (README更新器)
**描述**: 根据当前目录内容、git提交记录和现有文档，自动更新README.md和AGENTS.md文件。当需要维护项目文档、同步最新项目状态、或基于代码库变化更新文档时使用此技能。

**使用场景**:
- 项目初始化和文档创建
- 代码变更后更新文档
- 定期维护项目文档
- 将团队协作信息同步到文档

### 🔧 **github-commit** (GitHub提交管理)
**描述**: GitHub仓库提交管理技能，用于检查、验证和提交代码到GitHub仓库。确保代码正确提交到指定的GitHub仓库。

**使用场景**:
- 检查当前Git仓库状态和远程链接
- 验证或更新GitHub远程仓库链接
- 审核代码更改并生成提交消息
- 创建提交并可选推送到远程仓库

### 📊 **pdf** (PDF处理工具包)
**描述**: 综合性PDF操作工具包，用于提取文本和表格、创建新PDF、合并/拆分文档和处理表单。当Claude需要填写PDF表单或以编程方式处理、生成或分析PDF文档时使用。

**使用场景**:
- 从PDF中提取文本和表格数据
- 创建新的PDF文档
- 合并或拆分PDF文件
- 处理PDF表单填写
- 批量处理PDF文档

### 🔄 **github-to-skills** (GitHub到技能转换器)
**描述**: 将GitHub仓库转换为专业化AI技能的自动化工厂。当用户提供GitHub URL并想要"打包"、"包装"或从中"创建技能"时使用此技能。它会自动获取仓库详细信息、最新提交哈希，并生成具有增强元数据的标准化技能结构，适合生命周期管理。

**使用场景**:
- 将GitHub仓库转换为AI技能
- 为开源工具创建技能包装器
- 自动化技能创建流程
- 管理技能版本和更新

### 📋 **skill-manager** (技能管理器)
**描述**: GitHub基础技能的生命周期管理器。用于批量扫描技能目录、检查GitHub更新，并执行技能包装器的引导式升级。

**使用场景**:
- 扫描本地技能目录查找GitHub基础技能
- 检查GitHub仓库的更新
- 管理技能库存和版本
- 删除不需要的技能
- 执行技能升级工作流程

### 🚀 **skill-evolution-manager** (技能进化管理器)
**描述**: 专门用于在对话结束时，根据用户反馈和对话内容总结优化并迭代现有Skills的核心工具。它通过吸取对话中的"精华"（如成功的解决方案、失败的教训、特定的代码规范）来持续演进Skills库。

**使用场景**:
- 对话结束后复盘技能表现
- 根据用户反馈改进技能
- 保存最佳实践和约束条件
- 跨技能版本保持经验不丢失
- 批量对齐所有技能的经验数据

### 🌐 **baoyu-url-to-markdown** (URL转Markdown)
**描述**: 使用Chrome CDP获取任何URL并将其转换为markdown。支持两种模式 - 页面加载时自动捕获，或等待用户信号（对于需要登录的页面）。当用户想要将网页保存为markdown时使用此技能。

**使用场景**:
- 将网页转换为markdown格式
- 保存在线内容以供离线阅读
- 捕获需要登录的网页内容
- 以完整格式存档网页

## 快速开始

### 对于代理化编码代理
- `opencode stats --models --days 7` 可以使用这个命令来查看最近7天内可用的模型列表和统计信息。

参考 [AGENTS.md](./AGENTS.md) 获取全面的指南：
- 每个技能的构建/测试命令
- 代码风格指南和约定
- 技能开发模式
- 文件组织标准
- 开发环境设置

### 对于技能开发
```bash
# 初始化新技能
python skill-creator/scripts/init_skill.py my-new-skill --path .

# 验证技能
python skill-creator/scripts/quick_validate.py my-new-skill

# 生成 OpenAI 技能元数据
python skill-creator/scripts/generate_openai_yaml.py my-new-skill
```

### 对于技能使用
```bash
# 测试Node.js技能（例如humanizer）
cd humanizer/
npm test

# 运行特定测试文件
node test.js

# 测试Python基础技能
python skill-creator/scripts/quick_validate.py skill-directory

# 列出所有已安装技能
python skill-manager/scripts/list_skills.py .

# 检查技能更新
python skill-manager/scripts/scan_and_check.py .

# 将GitHub仓库转换为技能
python github-to-skills/scripts/fetch_github_info.py https://github.com/username/repo.git

# 列出可安装的预置技能
python skill-installer/scripts/list-skills.py

# 从 GitHub 安装技能
python skill-installer/scripts/install-skill-from-github.py https://github.com/owner/repo.git

# 基于反馈进化技能
python skill-evolution-manager/scripts/merge_evolution.py skill-name '{"preferences": ["用户偏好"], "fixes": ["已知修复"], "custom_prompts": "自定义指令"}'
python skill-evolution-manager/scripts/smart_stitch.py skill-name
```

## 技能结构

每个技能遵循以下结构：
```
技能名称/
├── SKILL.md (必需)           # YAML前置元数据 + 指令
├── scripts/ (可选)           # 确定性任务的可执行代码
├── references/ (可选)        # 按需加载的文档
└── assets/ (可选)            # 输出中使用的文件（模板等）
```

### SKILL.md 要求
每个SKILL.md必须包含：
```yaml
---
name: 技能名称
description: 何时使用此技能的清晰描述
---
```

## 开发原则

### 渐进式披露
技能使用三级加载系统来有效管理上下文：
1. **元数据**（名称 + 描述）- 始终在上下文中（约100字）
2. **SKILL.md正文** - 技能触发时加载（<5k字）
3. **捆绑资源** - 按Claude需要加载

### 简洁是关键
上下文窗口是公共资源。只添加Claude尚未拥有的上下文。质疑每条信息："Claude真的需要这个解释吗？"

### 适当的自由度
根据任务脆弱性匹配特异性：
- **高自由度**：基于文本的指令，允许多种有效方法
- **中自由度**：带有参数的伪代码/脚本，用于首选模式
- **低自由度**：针对脆弱、易出错操作的具体脚本

## 技能生态系统

三个新技能形成了一个完整的技能生命周期管理系统：

1. **创建**: `github-to-skills` 从GitHub仓库创建新技能
2. **维护**: `skill-manager` 检查更新和管理技能库存
3. **进化**: `skill-evolution-manager` 基于用户反馈持续改进技能

## 项目结构

```
./
├── README.md                    # 主README文件
├── README_cn.md                 # 中文README文件
├── README_en.md                 # 英文README文件
├── AGENTS.md                    # 代理指南
├── baoyu-url-to-markdown/       # URL 转 Markdown
├── github-commit/               # GitHub 提交管理
├── github-to-skills/            # GitHub 转技能
├── humanizer/                   # 英文文本人性化
├── humanizer-zh/                # 中文文本人性化
├── latex-lite-template-builder/ # LaTeX 轻量模板构建
├── paper-depth-reading/         # 论文深度阅读
├── paper-detailed-analysis/     # 论文深度分析
├── pdf/                         # PDF 处理工具包
├── skill-creator/               # 技能创建框架
├── skill-evolution-manager/     # 技能进化管理
├── skill-installer/             # 技能安装器
├── skill-manager/               # 技能生命周期管理
└── update-readme/               # README/AGENTS 更新器
```

## 贡献

### 添加新技能
1. **理解** 技能的具体示例
2. **规划** 可重用内容（脚本、参考资料、资源）
3. **初始化** 技能使用 `init_skill.py`
4. **编辑** 技能 - 实现资源和编写SKILL.md
5. **生成元数据** 使用 `generate_openai_yaml.py`
6. **迭代** 基于实际使用情况

### 代码风格指南
- **JavaScript/Node.js**: CommonJS导入，2空格缩进，camelCase/PascalCase命名
- **Python**: PEP 8合规，4空格缩进，snake_case命名
- **错误处理**: 使用try-catch/try-except并提供有意义的错误消息

### 文件组织
- **技能目录**: kebab-case（例如 `skill-creator`）
- **必需文件**: 每个技能必须有 `SKILL.md`（或 `skill.md`）
- **避免**: README.md、INSTALLATION_GUIDE.md、CHANGELOG.md等

## 资源

- [AGENTS.md](./AGENTS.md) - 代理化编码代理的全面指南
- [skill-creator/SKILL.md](./skill-creator/SKILL.md) - 详细的技能创建指南
- [skill-manager/SKILL.md](./skill-manager/SKILL.md) - 技能生命周期管理指南
- [skill-evolution-manager/SKILL.md](./skill-evolution-manager/SKILL.md) - 技能进化管理指南
- [github-to-skills/SKILL.md](./github-to-skills/SKILL.md) - GitHub到技能转换指南
- [latex-lite-template-builder/SKILL.md](./latex-lite-template-builder/SKILL.md) - LaTeX 轻量模板构建指南
- [skill-installer/SKILL.md](./skill-installer/SKILL.md) - 技能安装器指南
- [.vscode/settings.json](./.vscode/settings.json) - 开发环境设置

## 许可证

每个技能包含自己的许可证信息。有关详细信息，请参阅各个技能目录。

---

*本仓库为OpenCode代理提供专业化技能。创建或修改技能时，请遵循现有技能中建立的模式和约定。*
