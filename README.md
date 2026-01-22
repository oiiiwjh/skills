# OpenCode Skills Repository

A collection of modular, self-contained skills that extend Claude's capabilities with specialized knowledge, workflows, and tool integrations.

## Overview

This repository contains skills for OpenCode agents. Skills are "onboarding guides" for specific domains or tasks—they transform Claude from a general-purpose agent into a specialized agent equipped with procedural knowledge that no model can fully possess.

## Available Skills

### 📄 **paper-detailed-analysis**
**Description**: 深度论文分析技能，专注于从PDF学术论文中提取关键信息，生成连贯、详实、富有洞察力的研究笔记。适用于计算机图形学、AI、机器学习等领域的学术论文分析。

**Use when**:
- Analyzing PDF academic papers or arXiv links
- Generating structured, detailed research notes
- Combining paper analysis with code repository examination
- Conducting research background investigations

### 📚 **paper-depth-reading**
**Description**: Comprehensive academic paper analysis skill for computer graphics and AI research papers. Provides structured framework for extracting research background, methodology, experiments, and connecting paper concepts to code implementations.

**Use when**:
- Deep, structured analysis of academic papers with code implementation
- Understanding complex research methodologies
- Connecting theoretical concepts with practical code implementations
- Analyzing computer graphics, computer vision, and AI research papers

### ✨ **humanizer**
**Description**: AI text humanization skill that removes signs of AI-generated writing from text. Based on Wikipedia's comprehensive "Signs of AI writing" guide. Detects and fixes 24 common AI writing patterns.

**Use when**:
- Humanizing AI-generated text to sound more natural
- Removing repetitive AI writing patterns
- Improving text readability and authenticity
- Processing text with `/humanizer [text]` command

### 🛠️ **skill-creator**
**Description**: Guide for creating effective skills. This skill should be used when users want to create a new skill (or update an existing skill) that extends Claude's capabilities with specialized knowledge, workflows, or tool integrations.

**Use when**:
- Creating new OpenCode skills
- Modifying existing skills
- Understanding skill development patterns
- Packaging skills for distribution

### 📝 **update-readme**
**Description**: 根据当前目录内容、git提交记录和现有文档，自动更新README.md和AGENTS.md文件。当需要维护项目文档、同步最新项目状态、或基于代码库变化更新文档时使用此技能。

**Use when**:
- Project initialization and documentation creation
- Updating documentation after code changes
- Regular maintenance of project documentation
- Synchronizing team collaboration information to documentation

### 🔧 **github-commit**
**Description**: GitHub仓库提交管理技能，用于检查、验证和提交代码到GitHub仓库。确保代码正确提交到指定的GitHub仓库。

**Use when**:
- Checking current Git repository status and remote links
- Verifying or updating GitHub remote repository links
- Reviewing code changes and generating commit messages
- Creating commits and optionally pushing to remote repositories

## Quick Start

### For Agentic Coding Agents
Refer to [AGENTS.md](./AGENTS.md) for comprehensive guidelines on:
- Build/test commands for each skill
- Code style guidelines and conventions
- Skill development patterns
- File organization standards
- Development environment setup

### For Skill Development
```bash
# Initialize a new skill
python skill-creator/scripts/init_skill.py my-new-skill --path .

# Validate a skill
python skill-creator/scripts/quick_validate.py my-new-skill

# Package a skill for distribution
python skill-creator/scripts/package_skill.py my-new-skill
```

### For Skill Usage
```bash
# Test a Node.js skill (e.g., humanizer)
cd humanizer/
npm test

# Run specific test file
node test.js

# Test Python-based skills
python skill-creator/scripts/quick_validate.py skill-directory
```

## Skill Structure

Each skill follows this structure:
```
skill-name/
├── SKILL.md (required)           # YAML frontmatter + instructions
├── scripts/ (optional)           # Executable code for deterministic tasks
├── references/ (optional)        # Documentation loaded as needed
└── assets/ (optional)            # Files used in output (templates, etc.)
```

### SKILL.md Requirements
Every SKILL.md must include:
```yaml
---
name: skill-name
description: Clear description of when to use this skill
---
```

## Development Principles

### Progressive Disclosure
Skills use a three-level loading system to manage context efficiently:
1. **Metadata** (name + description) - Always in context (~100 words)
2. **SKILL.md body** - When skill triggers (<5k words)
3. **Bundled resources** - As needed by Claude

### Concise is Key
The context window is a public good. Only add context Claude doesn't already have. Challenge each piece of information: "Does Claude really need this explanation?"

### Appropriate Degrees of Freedom
Match specificity to task fragility:
- **High freedom**: Text-based instructions for multiple valid approaches
- **Medium freedom**: Pseudocode/scripts with parameters for preferred patterns
- **Low freedom**: Specific scripts for fragile, error-prone operations

## Contributing

### Adding a New Skill
1. **Understand** the skill with concrete examples
2. **Plan** reusable contents (scripts, references, assets)
3. **Initialize** skill with `init_skill.py`
4. **Edit** the skill - implement resources and write SKILL.md
5. **Package** skill with `package_skill.py`
6. **Iterate** based on real usage

### Code Style Guidelines
- **JavaScript/Node.js**: CommonJS imports, 2-space indentation, camelCase/PascalCase naming
- **Python**: PEP 8 compliance, 4-space indentation, snake_case naming
- **Error Handling**: Use try-catch/try-except with meaningful error messages

### File Organization
- **Skill directories**: kebab-case (e.g., `skill-creator`)
- **Required files**: Each skill must have `SKILL.md` (or `skill.md`)
- **Avoid**: README.md, INSTALLATION_GUIDE.md, CHANGELOG.md, etc.

## Project Structure

```
./
├── README.md                    # This file
├── AGENTS.md                    # Agent guidelines (if exists)
├── skill-creator/              # Skill creation framework
│   ├── SKILL.md
│   ├── scripts/
│   │   ├── init_skill.py
│   │   ├── quick_validate.py
│   │   └── package_skill.py
│   └── references/
│       ├── workflows.md
│       └── output-patterns.md
├── github-commit/              # GitHub commit management
│   ├── SKILL.md
│   ├── scripts/
│   │   ├── check_git_status.py
│   │   ├── create_commit.py
│   │   └── update_remote.py
│   └── references/
│       ├── git_workflow.md
│       └── commit_conventions.md
├── update-readme/              # README/AGENTS.md updater
│   ├── SKILL.md
│   ├── scripts/
│   │   ├── analyze_project.py
│   │   ├── generate_readme.py
│   │   ├── update_agents.py
│   │   └── utils.py
│   └── references/
│       ├── README_templates.md
│       ├── AGENTS_template.md
│       └── best_practices.md
├── paper-detailed-analysis/    # Academic paper analysis
│   └── SKILL.md
├── paper-depth-reading/        # Deep paper reading
│   └── SKILL.md
├── humanizer/                  # AI text humanization
│   ├── SKILL.md
│   ├── package.json
│   ├── humanizer-implementation.js
│   ├── test.js
│   └── README.md
└── .vscode/                    # Development environment
    └── settings.json
```

## Resources

- [AGENTS.md](./AGENTS.md) - Comprehensive guidelines for agentic coding agents
- [skill-creator/SKILL.md](./skill-creator/SKILL.md) - Detailed skill creation guide
- [.vscode/settings.json](./.vscode/settings.json) - Development environment settings

## License

Each skill includes its own license information. See individual skill directories for details.

---

*This repository provides specialized skills for OpenCode agents. Follow the patterns and conventions established in existing skills when creating or modifying skills.*