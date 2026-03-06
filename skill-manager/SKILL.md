---
name: skill-manager
description: Lifecycle manager for GitHub-based skills. Use this to batch scan your skills directory, check for updates on GitHub, and perform guided upgrades of your skill wrappers.
license: MIT
---

# Skill Lifecycle Manager

This skill helps you maintain your library of GitHub-wrapped skills by automating the detection of updates and assisting in the refactoring process.

## Core Capabilities

1.  **Audit**: Scans your local skills folder for skills with `github_url` metadata.
2.  **Check**: Queries GitHub (via `git ls-remote`) to compare local commit hashes against the latest remote HEAD.
3.  **Report**: Generates a status report identifying which skills are "Stale" or "Current".
4.  **Update Workflow**: Provides a structured process for the Agent to upgrade a skill.
5.  **Inventory Management**: Lists all local skills and provides deletion capabilities.

## Usage

**Trigger**: `/skill-manager check` or "Scan my skills for updates"
**Trigger**: `/skill-manager list` or "List my skills"
**Trigger**: `/skill-manager delete <skill_name>` or "Delete skill <skill_name>"

### Workflow 1: Check for Updates

1.  **Run Scanner**: The agent runs `scripts/scan_and_check.py` to analyze all skills.
2.  **Review Report**: The script outputs a JSON summary. The Agent presents this to the user.
    *   Example: "Found 3 outdated skills: `yt-dlp` (behind 50 commits), `ffmpeg-tool` (behind 2 commits)..."

### Workflow 2: Update a Skill

**Trigger**: "Update [Skill Name]" (after a check)

1.  **Fetch New Context**: The agent fetches the *new* README from the remote repo.
2.  **Diff Analysis**:
    *   The agent compares the new README with the old `SKILL.md`.
    *   Identifies new features, deprecated flags, or usage changes.
3.  **Refactor**:
    *   The agent rewrites `SKILL.md` to reflect the new capabilities.
    *   The agent updates the `github_hash` in the frontmatter.
    *   The agent (optionally) attempts to update the `wrapper.py` if CLI args have changed.
4.  **Verify**: Runs a quick validation (if available).

## Scripts

- `scripts/scan_and_check.py`: The workhorse. Scans directories, parses Frontmatter, fetches remote tags, returns status.
- `scripts/update_helper.py`: (Optional) Helper to backup files before update.
- `scripts/list_skills.py`: Lists all installed skills with type and version.
- `scripts/delete_skill.py`: Permanently removes a skill folder.

## Metadata Requirements

This manager relies on the `github-to-skills` metadata standard:
- `github_url`: Source of truth.
- `github_hash`: State of truth.

## Skill Synergy Examples

### Working with github-to-skills
```bash
# After creating a skill with github-to-skills, register it with skill-manager
python github-to-skills/scripts/fetch_github_info.py https://github.com/username/repo.git
python skill-manager/scripts/scan_and_check.py .
```

### Working with skill-evolution-manager
```bash
# After skill-manager updates a skill, restore evolution data
python skill-manager/scripts/scan_and_check.py .
python skill-evolution-manager/scripts/smart_stitch.py updated-skill-name
```

### Working with update-readme
```bash
# After adding new skills, update documentation
python skill-manager/scripts/list_skills.py .
python update-readme/scripts/analyze_project.py .
```

## 使用示例

### 示例1：列出所有技能
```bash
# 列出所有已安装技能
python scripts/list_skills.py .

# 输出示例：
# Skill Name           | Type         | Description                              | Ver     
# -----------------------------------------------------------------------------------------
# github-to-skills     | Standard     | Automated factory for converting GitH... | 0.1.0   
# skill-manager        | Standard     | Lifecycle manager for GitHub-based sk... | 0.1.0   
# paper-detailed-analysis | Standard     | 深度论文分析技能... | 0.1.0
```

### 示例2：检查技能更新
```bash
# 扫描所有技能检查GitHub更新
python scripts/scan_and_check.py .

# 输出示例：
# [{
#   "skill": "github-to-skills",
#   "local_hash": "abc123",
#   "remote_hash": "def456",
#   "needs_update": true,
#   "update_url": "https://github.com/KKKKhazix/Khaziz-Skills.git"
# }]
```

### 示例3：删除不需要的技能
```bash
# 删除指定技能
python scripts/delete_skill.py old-skill-name

# 确认删除
python scripts/list_skills.py .
```

### 示例4：批量管理技能
```bash
# 1. 列出所有技能
python scripts/list_skills.py . --detailed

# 2. 检查所有GitHub技能的更新
python scripts/scan_and_check.py . --verbose

# 3. 更新需要升级的技能
# (根据scan_and_check的输出手动更新)

# 4. 验证更新结果
python scripts/list_skills.py .
```

### 示例5：与其他技能协同工作
```bash
# 与github-to-skills协同
python github-to-skills/scripts/fetch_github_info.py https://github.com/new/tool.git
python scripts/scan_and_check.py .

# 与skill-evolution-manager协同
python scripts/scan_and_check.py .
python skill-evolution-manager/scripts/align_all.py

# 与update-readme协同
python scripts/list_skills.py .
python update-readme/scripts/analyze_project.py .
```

## User-Learned Best Practices & Constraints

> **Auto-Generated Section**: This section is maintained by `skill-evolution-manager`. Do not edit manually.

### User Preferences
- 技能应按照功能分类展示
- 建立完整的技能生命周期管理系统
- 新技能集成后需要更新所有相关文档

### Known Fixes & Workarounds
- 技能总数统计需要实时更新
- 项目结构图必须包含所有技能目录

### Custom Instruction Injection

管理技能时：1) 维护技能分类系统 2) 跟踪技能总数变化 3) 确保文档同步 4) 验证技能生态系统完整性
