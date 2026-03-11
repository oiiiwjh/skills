# Skills Repository

A collection of modular, self-contained skills that extend coding agents with specialized knowledge, workflows, and tool integrations.

## Overview

This repository contains reusable skills for coding agents. Skills are task-specific onboarding guides that package domain knowledge, workflows, and reusable tooling into a format agents can discover and apply.

Canonical source path policy: keep real skills in `~/.agents/skills`, and let other tool-specific directories use symlinks.

## Available Skills

### 📄 **paper-detailed-analysis**
**Description**: Deep academic paper analysis skill focused on extracting key information from PDF academic papers and generating coherent, detailed, insightful research notes. Suitable for academic paper analysis in computer graphics, AI, machine learning, and related fields.

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

### ✨ **humanizer-zh** (Chinese Text Humanizer)
**Description**: Specialized AI writing trace removal skill for Chinese text. Based on Wikipedia's "AI Writing Features" comprehensive guide, detects and fixes patterns such as exaggerated symbolism, promotional language, superficial analysis, vague attribution, excessive dash usage, three-part rule, AI vocabulary, negative parallelism, and excessive connective phrases.

**Use when**:
- Removing AI generation traces from Chinese text
- Editing or reviewing Chinese text to make it more natural
- Fixing specific patterns in Chinese AI writing
- Enhancing the humanization and readability of Chinese text

### 🛠️ **skill-creator**
**Description**: Guide for creating effective skills. This skill should be used when users want to create a new skill (or update an existing skill) that extends an agent's capabilities with specialized knowledge, workflows, or tool integrations.

**Use when**:
- Creating new skills
- Modifying existing skills
- Understanding skill development patterns
- Generating OpenAI skill metadata

### 📚 **latex-lite-template-builder**
**Description**: Build reusable lite LaTeX paper templates from a source template directory. Supports script-based generation and optional Overleaf bundle output.

**Use when**:
- Migrating an existing LaTeX paper style into a reusable template
- Creating compact paper skeletons for repeated use
- Preparing Overleaf-friendly template bundles

### 📥 **skill-installer**
**Description**: Install Codex skills into `$CODEX_HOME/skills` from a curated list or a GitHub repo path.

**Use when**:
- Listing installable curated skills
- Installing a curated skill quickly
- Installing a skill directly from a GitHub repository path

### 🎞️ **frontend-slides**
**Description**: Wrapper skill for installing and updating the upstream `frontend-slides` presentation skill from GitHub.

**Use when**:
- Adding high-quality HTML slide generation capability to local agents
- Updating local copies of `frontend-slides` from upstream
- Managing a tracked wrapper with pinned hash/version metadata

### 📝 **update-readme**
**Description**: Automatically updates README.md and AGENTS.md files based on current directory contents, git commit history, and existing documentation. Use this skill when maintaining project documentation, synchronizing the latest project status, or updating documentation based on codebase changes.

**Use when**:
- Project initialization and documentation creation
- Updating documentation after code changes
- Regular maintenance of project documentation
- Synchronizing team collaboration information to documentation

### 🔧 **github-commit**
**Description**: GitHub repository commit management skill for checking, validating, and committing code to GitHub repositories. Ensures code is correctly committed to the specified GitHub repository.

**Use when**:
- Checking current Git repository status and remote links
- Verifying or updating GitHub remote repository links
- Reviewing code changes and generating commit messages
- Creating commits and optionally pushing to remote repositories

### 📊 **pdf**
**Description**: Comprehensive PDF manipulation toolkit for extracting text and tables, creating new PDFs, merging/splitting documents, and handling forms. When Claude needs to fill in a PDF form or programmatically process, generate, or analyze PDF documents at scale.

**Use when**:
- Extracting text and table data from PDFs
- Creating new PDF documents
- Merging or splitting PDF files
- Handling PDF form filling
- Batch processing PDF documents

### 🔄 **github-to-skills**
**Description**: Automated factory for converting GitHub repositories into specialized AI skills. Use this skill when the user provides a GitHub URL and wants to "package", "wrap", or "create a skill" from it. It automatically fetches repository details, latest commit hashes, and generates a standardized skill structure with enhanced metadata suitable for lifecycle management.

**Use when**:
- Converting GitHub repositories into AI skills
- Creating skill wrappers for open-source tools
- Automating skill creation workflows
- Managing skill versions and updates

### 📋 **skill-manager**
**Description**: Lifecycle manager for GitHub-based skills. Use this to batch scan your skills directory, check for updates on GitHub, and perform guided upgrades of your skill wrappers.

**Use when**:
- Scanning local skills directory for GitHub-based skills
- Checking for updates from GitHub repositories
- Managing skill inventory and versions
- Deleting unwanted skills
- Performing skill upgrade workflows

### 🚀 **skill-evolution-manager**
**Description**: Core tool for summarizing, optimizing, and iterating existing skills based on user feedback and conversation content at the end of dialogues. It continuously evolves the skills library by absorbing the "essence" from conversations (such as successful solutions, failure lessons, specific code specifications).

**Use when**:
- Reviewing skill performance after conversations
- Improving skills based on user feedback
- Saving best practices and constraints
- Preserving experience across skill versions
- Batch aligning experience data for all skills

### 🌐 **baoyu-url-to-markdown**
**Description**: Fetch any URL and convert to markdown using Chrome CDP. Supports two modes - auto-capture on page load, or wait for user signal (for pages requiring login). Use when user wants to save a webpage as markdown.

**Use when**:
- Converting web pages to markdown format
- Saving online content for offline reading
- Capturing web content that requires login
- Archiving web pages with full formatting

## How to Use These Skills

For Codex and similar agents that scan `~/.agents/skills`, clone this repository directly there:

```bash
git clone <repo-url> ~/.agents/skills
```

For OpenCode, keep this repository in `~/.agents/skills` as the canonical source, then symlink skills into `~/.config/opencode/skill`:

```bash
mkdir -p ~/.config/opencode/skill
ln -s ~/.agents/skills/* ~/.config/opencode/skill/
```

## Quick Start

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

# Generate OpenAI skill metadata
python skill-creator/scripts/generate_openai_yaml.py my-new-skill
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

# List all installed skills
python skill-manager/scripts/list_skills.py .

# Check for skill updates
python skill-manager/scripts/scan_and_check.py .

# Convert GitHub repo to skill
python github-to-skills/scripts/fetch_github_info.py https://github.com/username/repo.git

# List installable curated skills
python skill-installer/scripts/list-skills.py

# Install skill from GitHub
python skill-installer/scripts/install-skill-from-github.py https://github.com/owner/repo.git

# Evolve skills based on feedback
python skill-evolution-manager/scripts/merge_evolution.py skill-name '{"preferences": ["user preferences"], "fixes": ["known fixes"], "custom_prompts": "custom instructions"}'
python skill-evolution-manager/scripts/smart_stitch.py skill-name
```

## Breaking CLI Changes (2026-03)

| Script | Old behavior | New behavior |
|---|---|---|
| `skill-evolution-manager/scripts/align_all.py` | defaulted to `~/.claude/skills` | infers repository root by default, or accepts explicit `[skills_root]` |
| `github-commit/scripts/update_remote.py` | interactive confirmation | non-interactive remote upsert, supports `--json` |
| `github-commit/scripts/check_git_status.py` | text output only | supports `--history-limit` and `--json` |
| `github-commit/scripts/create_commit.py` | basic `--push` flow | supports `--push --remote <name> --json` |
| `update-readme/scripts/*` | inconsistent exits | unified exits: `0` success, `1` runtime, `2` usage |

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

## Skill Ecosystem

The three new skills form a complete skill lifecycle management system:

1. **Create**: `github-to-skills` creates new skills from GitHub repositories
2. **Maintain**: `skill-manager` checks for updates and manages skill inventory
3. **Evolve**: `skill-evolution-manager` continuously improves skills based on user feedback

## Project Structure

```
./
├── README.md                    # Main README file
├── README_cn.md                 # Chinese README file
├── README_en.md                 # English README file
├── AGENTS.md                    # Agent guidelines
├── baoyu-url-to-markdown/       # URL to markdown converter
├── github-commit/               # GitHub commit management
├── github-to-skills/            # GitHub to skills converter
├── humanizer/                   # AI text humanization
├── humanizer-zh/                # Chinese text humanization
├── latex-lite-template-builder/ # LaTeX lite template builder
├── paper-depth-reading/         # Deep paper reading
├── paper-detailed-analysis/     # Academic paper analysis
├── pdf/                         # PDF processing toolkit
├── skill-creator/               # Skill creation framework
├── skill-evolution-manager/     # Skill evolution manager
├── skill-installer/             # Skill installer
├── frontend-slides/             # Frontend slides wrapper skill
├── skill-manager/               # Skill lifecycle manager
└── update-readme/               # README/AGENTS updater
```

## Contributing

### Adding a New Skill
1. **Understand** the skill with concrete examples
2. **Plan** reusable contents (scripts, references, assets)
3. **Initialize** skill with `init_skill.py`
4. **Edit** the skill - implement resources and write SKILL.md
5. **Generate metadata** with `generate_openai_yaml.py`
6. **Iterate** based on real usage

### Code Style Guidelines
- **JavaScript/Node.js**: CommonJS imports, 2-space indentation, camelCase/PascalCase naming
- **Python**: PEP 8 compliance, 4-space indentation, snake_case naming
- **Error Handling**: Use try-catch/try-except with meaningful error messages

### File Organization
- **Skill directories**: kebab-case (e.g., `skill-creator`)
- **Required files**: Each skill must have `SKILL.md` (or `skill.md`)
- **Avoid**: README.md, INSTALLATION_GUIDE.md, CHANGELOG.md, etc.

## Resources

- [AGENTS.md](./AGENTS.md) - Comprehensive guidelines for agentic coding agents
- [skill-creator/SKILL.md](./skill-creator/SKILL.md) - Detailed skill creation guide
- [skill-manager/SKILL.md](./skill-manager/SKILL.md) - Skill lifecycle management guide
- [skill-evolution-manager/SKILL.md](./skill-evolution-manager/SKILL.md) - Skill evolution management guide
- [github-to-skills/SKILL.md](./github-to-skills/SKILL.md) - GitHub to skills conversion guide
- [latex-lite-template-builder/SKILL.md](./latex-lite-template-builder/SKILL.md) - LaTeX lite template builder guide
- [skill-installer/SKILL.md](./skill-installer/SKILL.md) - Skill installer guide
- [frontend-slides/SKILL.md](./frontend-slides/SKILL.md) - Frontend slides wrapper skill guide
- [.vscode/settings.json](./.vscode/settings.json) - Development environment settings

## License

Each skill includes its own license information. See individual skill directories for details.

---

*This repository provides specialized skills for coding agents. Follow the patterns and conventions established in existing skills when creating or modifying skills.*
