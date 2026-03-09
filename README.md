# Skills Repository

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
| 📄 **paper-detailed-analysis** | Research & Analysis | Deep academic paper analysis from PDFs |
| 📚 **paper-depth-reading** | Research & Analysis | Comprehensive paper analysis with code connections |
| ✨ **humanizer** | Text Processing | Removes AI writing patterns from text |
| ✨ **humanizer-zh** | Text Processing | Chinese text humanization, removes AI writing traces |
| 🛠️ **skill-creator** | Development Tools | Guide for creating effective skills |
| 📝 **update-readme** | Documentation | Automatically updates README/AGENTS files |
| 🔧 **github-commit** | Version Control | GitHub repository commit management |
| 📊 **pdf** | Document Processing | Comprehensive PDF manipulation toolkit |
| 📚 **latex-lite-template-builder** | Document Processing | Build reusable lite LaTeX paper templates |
| 🔄 **github-to-skills** | Skill Management | Converts GitHub repos to AI skills |
| 📋 **skill-manager** | Skill Management | Lifecycle manager for GitHub-based skills |
| 🚀 **skill-evolution-manager** | Skill Management | Evolves skills based on user feedback |
| 📥 **skill-installer** | Skill Management | Install Codex skills from curated list or GitHub repos |
| 🌐 **baoyu-url-to-markdown** | Web & Content | Fetch URLs and convert to markdown using Chrome CDP |
| 🎞️ **frontend-slides** | Presentation & Design | Wrapper skill to install/update animation-rich HTML slide generation from upstream GitHub repo |

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
├── skill-evolution-manager/    # Skill evolution manager
├── skill-installer/            # Skill installer
├── frontend-slides/            # Frontend slides wrapper skill
├── latex-lite-template-builder/# LaTeX lite template builder
└── baoyu-url-to-markdown/      # URL to markdown converter
```

## ⚡ Quick Start

### For Skill Development
```bash
# Initialize a new skill
python skill-creator/scripts/init_skill.py my-new-skill --path .

# Validate a skill
python skill-creator/scripts/quick_validate.py my-new-skill

# Generate OpenAI skill metadata
python skill-creator/scripts/generate_openai_yaml.py my-new-skill
```

### For Skill Management
```bash
# Check for skill updates
python skill-manager/scripts/scan_and_check.py .

# List all installed skills
python skill-manager/scripts/list_skills.py .

# Convert a GitHub repo to a skill
python github-to-skills/scripts/fetch_github_info.py <github_url>

# List installable curated skills
python skill-installer/scripts/list-skills.py

# Install skill from GitHub
python skill-installer/scripts/install-skill-from-github.py https://github.com/owner/repo.git

# Evolve skills based on user feedback
python skill-evolution-manager/scripts/merge_evolution.py <skill_name> '{"preferences": ["user preferences"], "fixes": ["known fixes"], "custom_prompts": "custom instructions"}'
python skill-evolution-manager/scripts/smart_stitch.py <skill_name>
```

## ⚠️ Breaking CLI Changes (2026-03)

| Script | Old | New |
|-------|-----|-----|
| `skill-evolution-manager/scripts/align_all.py` | default `~/.claude/skills` | default inferred repo root, or explicit `[skills_root]` |
| `github-commit/scripts/update_remote.py` | interactive confirm | non-interactive upsert + optional `--json` |
| `github-commit/scripts/check_git_status.py` | plain text only | supports `--history-limit` and `--json` |
| `github-commit/scripts/create_commit.py` | `--push` only | supports `--push --remote <name> --json` |
| `update-readme/scripts/*` | mixed return behavior | unified exit codes: `0` success, `1` runtime, `2` argument |

## 🧭 Skill Directory Policy

- Canonical source directory for real skills: `~/.agents/skills`
- Other tool-specific skill directories should consume these skills via symlinks.

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
- [frontend-slides/SKILL.md](./frontend-slides/SKILL.md) - Frontend slides wrapper skill guide

## 📄 License

Each skill includes its own license information. See individual skill directories for details.

---

*This repository provides specialized skills for OpenCode agents. Follow the patterns and conventions established in existing skills when creating or modifying skills.*
