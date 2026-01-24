---
name: github-to-skills
description: Automated factory for converting GitHub repositories into specialized AI skills. Use this skill when the user provides a GitHub URL and wants to "package", "wrap", or "create a skill" from it. It automatically fetches repository details, latest commit hashes, and generates a standardized skill structure with enhanced metadata suitable for lifecycle management.
license: MIT
---

# GitHub to Skills Factory

This skill automates the conversion of GitHub repositories into fully functional AI skills.

## Core Functionality

1. **Analysis**: Fetches repository metadata (Description, README, Latest Commit Hash).
2. **Scaffolding**: Creates a standardized skill directory structure.
3. **Metadata Injection**: Generates `SKILL.md` with extended frontmatter (tracking source, version, hash) for future automated management.
4. **Wrapper Generation**: Creates a `scripts/wrapper.py` (or similar) to interface with the tool.

## Usage

**Trigger**: `/GitHub-to-skills <github_url>` or "Package this repo into a skill: <url>"

### Required Metadata Schema

Every skill created by this factory MUST include the following extended YAML frontmatter in its `SKILL.md`. This is critical for the `skill-manager` to function later.

```yaml
---
name: <kebab-case-repo-name>
description: <concise-description-for-agent-triggering>
# EXTENDED METADATA (MANDATORY)
github_url: <original-repo-url>
github_hash: <latest-commit-hash-at-time-of-creation>
version: <tag-or-0.1.0>
created_at: <ISO-8601-date>
entry_point: scripts/wrapper.py # or main script
dependencies: # List main dependencies if known, e.g., ["yt-dlp", "ffmpeg"]
---
```

## Workflow

1. **Fetch Info**: The agent first runs `scripts/fetch_github_info.py` to get the raw data from the repo.
2. **Plan**: The agent analyzes the README to understand how to invoke the tool (CLI args, Python API, etc.).
3. **Generate**: The agent uses the `skill-creator` patterns to write the `SKILL.md` and wrapper scripts, ensuring the **extended metadata** is present.
4. **Verify**: Checks if the commit hash was correctly captured.

## Resources

- `scripts/fetch_github_info.py`: Utility to scrape/API fetch repo details (README, Hash, Tags).
- `scripts/create_github_skill.py`: Orchestrator to scaffold the folder and write the initial files.

## Best Practices for Generated Skills

- **Isolation**: The generated skill should install its own dependencies (e.g., in a venv or via `uv`/`pip`) if possible, or clearly state them.
- **Progressive Disclosure**: Do not dump the entire repo into the skill. Only include the necessary wrapper code and reference the original repo for deep dives.
- **Idempotency**: The `github_hash` field allows the future `skill-manager` to check `if remote_hash != local_hash` to trigger updates.

## Skill Synergy Examples

### Integration with skill-manager
```bash
# After creating a skill, register it with skill-manager
python github-to-skills/scripts/fetch_github_info.py https://github.com/username/repo.git
python skill-manager/scripts/scan_and_check.py .
```

### Integration with skill-creator
```bash
# Use skill-creator patterns for standardization
python skill-creator/scripts/init_skill.py new-skill --path .
# Then enhance with github-to-skills metadata
```

### Complete workflow example
```bash
# 1. Create skill from GitHub
python github-to-skills/scripts/fetch_github_info.py https://github.com/username/tool.git

# 2. Standardize with skill-creator
python skill-creator/scripts/init_skill.py tool-wrapper --path .

# 3. Register with skill-manager
python skill-manager/scripts/scan_and_check.py .

# 4. Update documentation
python update-readme/scripts/analyze_project.py .
```

## 使用示例

### 示例1：将GitHub工具转换为技能
```bash
# 获取GitHub仓库信息
python scripts/fetch_github_info.py https://github.com/yt-dlp/yt-dlp.git

# 输出示例：
# {
#   "name": "yt-dlp",
#   "url": "https://github.com/yt-dlp/yt-dlp.git",
#   "latest_hash": "abc123def456",
#   "readme": "# yt-dlp - A youtube-dl fork with additional features..."
# }

# 基于获取的信息创建技能目录结构
mkdir yt-dlp-skill
# 创建SKILL.md包含必要的元数据
```

### 示例2：创建Python库的技能包装器
```bash
# 获取Python库信息
python scripts/fetch_github_info.py https://github.com/psf/requests.git

# 创建技能包装器，包含：
# 1. SKILL.md - 技能描述和元数据
# 2. scripts/wrapper.py - 调用requests库的包装器
# 3. references/ - API文档和示例
# 4. assets/ - 示例请求模板
```

### 示例3：创建CLI工具的技能包装器
```bash
# 获取CLI工具信息
python scripts/fetch_github_info.py https://github.com/BurntSushi/ripgrep.git

# 创建技能包装器，包含：
# 1. SKILL.md - 技能描述和安装说明
# 2. scripts/wrapper.py - 封装rg命令的Python脚本
# 3. references/ - 模式示例和用例
# 4. assets/ - 常用搜索模式模板
```

### 示例4：验证技能创建结果
```bash
# 验证创建的技能结构
python skill-creator/scripts/quick_validate.py yt-dlp-skill

# 检查元数据完整性
grep -E "github_url|github_hash" yt-dlp-skill/SKILL.md

# 注册到技能管理器
python skill-manager/scripts/scan_and_check.py .
```