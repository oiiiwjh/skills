# OpenCode Skills Repository

A collection of modular, self-contained skills that extend Claude's capabilities with specialized knowledge, workflows, and tool integrations.

## 📚 Language Versions

- **English**: [README_en.md](./README_en.md) - Complete English documentation
- **中文**: [README_cn.md](./README_cn.md) - 完整中文文档

## 🚀 Quick Overview

This repository contains skills for OpenCode agents. Skills are "onboarding guides" for specific domains or tasks—they transform Claude from a general-purpose agent into a specialized agent equipped with procedural knowledge that no model can fully possess.

### 🔥 New Skills Added (from Khazix-Skills)

We've recently integrated three powerful skill management tools from [Khazix-Skills](https://github.com/KKKKhazix/Khaziz-Skills.git):

1. **🔄 github-to-skills** - Automated factory for converting GitHub repositories into AI skills
2. **📋 skill-manager** - Lifecycle manager for GitHub-based skills
3. **🚀 skill-evolution-manager** - Continuously improves skills based on user feedback

These form a complete skill lifecycle management system:
- **Create** → **Maintain** → **Evolve**

### 📊 Complete Skill List

| Skill | Category | Description |
|-------|----------|-------------|
| 📄 **paper-detailed-analysis** | Research | Deep academic paper analysis from PDFs |
| 📚 **paper-depth-reading** | Research | Comprehensive paper analysis with code connections |
| ✨ **humanizer** | Text Processing | Removes AI writing patterns from text |
| ✨ **humanizer-zh** | Text Processing | Chinese text humanization, removes AI writing traces |
| 🛠️ **skill-creator** | Development | Guide for creating effective skills |
| 📝 **update-readme** | Documentation | Automatically updates README/AGENTS files |
| 🔧 **github-commit** | Version Control | GitHub repository commit management |
| 📊 **pdf** | Document Processing | Comprehensive PDF manipulation toolkit |
| 🔄 **github-to-skills** | Skill Management | Converts GitHub repos to AI skills |
| 📋 **skill-manager** | Skill Management | Lifecycle manager for GitHub-based skills |
| 🚀 **skill-evolution-manager** | Skill Management | Evolves skills based on user feedback |

## 🏗️ Project Structure

```
./
├── README.md                    # This index file
├── README_cn.md                 # Chinese documentation
├── README_en.md                 # English documentation
├── AGENTS.md                    # Agent guidelines
├── .vscode/                     # Development environment settings
├── .git/                        # Git repository
├── skill-creator/              # Skill creation framework
├── github-commit/              # GitHub commit management
├── update-readme/              # README/AGENTS updater
├── paper-detailed-analysis/    # Academic paper analysis
├── paper-depth-reading/        # Deep paper reading
├── humanizer/                  # AI text humanization
├── humanizer-zh/               # Chinese text humanization
├── pdf/                        # PDF processing toolkit
├── github-to-skills/           # GitHub to skills converter
├── skill-manager/              # Skill lifecycle manager
└── skill-evolution-manager/    # Skill evolution manager
```

## ⚡ Quick Start

### For Skill Development
```bash
# Initialize a new skill
python skill-creator/scripts/init_skill.py my-new-skill --path .

# Validate a skill
python skill-creator/scripts/quick_validate.py my-new-skill

# Package a skill for distribution
python skill-creator/scripts/package_skill.py my-new-skill
```

### For Skill Management
```bash
# Check for skill updates
python skill-manager/scripts/scan_and_check.py .

# List all installed skills
python skill-manager/scripts/list_skills.py .

# Convert a GitHub repo to a skill
python github-to-skills/scripts/fetch_github_info.py <github_url>

# Evolve skills based on user feedback
python skill-evolution-manager/scripts/merge_evolution.py <skill_name> '{"preferences": ["user preferences"], "fixes": ["known fixes"], "custom_prompts": "custom instructions"}'
python skill-evolution-manager/scripts/smart_stitch.py <skill_name>
```

## 📖 Detailed Documentation

For comprehensive information, please refer to the appropriate language version:

- **[README_en.md](./README_en.md)** - Complete English documentation with detailed skill descriptions, usage examples, and development guidelines
- **[README_cn.md](./README_cn.md)** - 完整中文文档，包含详细的技能描述、使用示例和开发指南

## 🔗 Resources

- [AGENTS.md](./AGENTS.md) - Comprehensive guidelines for agentic coding agents
- [skill-creator/SKILL.md](./skill-creator/SKILL.md) - Detailed skill creation guide
- [.vscode/settings.json](./.vscode/settings.json) - Development environment settings
- [skill-manager/SKILL.md](./skill-manager/SKILL.md) - Skill lifecycle management guide
- [skill-evolution-manager/SKILL.md](./skill-evolution-manager/SKILL.md) - Skill evolution management guide

## 📄 License

Each skill includes its own license information. See individual skill directories for details.

---

*This repository provides specialized skills for OpenCode agents. Follow the patterns and conventions established in existing skills when creating or modifying skills.*