---
name: skill-evolution-manager
description: 专门用于在对话结束时，根据用户反馈和对话内容总结优化并迭代现有 Skills 的核心工具。它通过吸取对话中的"精华"（如成功的解决方案、失败的教训、特定的代码规范）来持续演进 Skills 库。
license: MIT
---

# Skill Evolution Manager

这是整个 AI 技能系统的"进化中枢"。它不仅负责优化单个 Skill，还负责跨 Skill 的经验复盘和沉淀。

## 核心职责

1.  **复盘诊断 (Session Review)**：在对话结束时，分析所有被调用的 Skill 的表现。
2.  **经验提取 (Experience Extraction)**：将非结构化的用户反馈转化为结构化的 JSON 数据（`evolution.json`）。
3.  **智能缝合 (Smart Stitching)**：将沉淀的经验自动写入 `SKILL.md`，确保持久化且不被版本更新覆盖。

## 使用场景

**Trigger**: 
- `/evolve`
- "复盘一下刚才的对话"
- "我觉得刚才那个工具不太好用，记录一下"
- "把这个经验保存到 Skill 里"

## 工作流 (The Evolution Workflow)

### 1. 经验复盘 (Review & Extract)
当用户触发复盘时，Agent 必须执行：
1.  **扫描上下文**：找出用户不满意的点（报错、风格不对、参数错误）或满意的点（特定 Prompt 效果好）。
2.  **定位 Skill**：确定是哪个 Skill 需要进化（例如 `yt-dlp` 或 `baoyu-comic`）。
3.  **生成 JSON**：在内存中构建如下 JSON 结构：
    ```json
    {
      "preferences": ["用户希望下载默认静音"],
      "fixes": ["Windows 下 ffmpeg 路径需转义"],
      "custom_prompts": "在执行前总是先打印预估耗时"
    }
    ```

### 2. 经验持久化 (Persist)
Agent 调用 `scripts/merge_evolution.py`，将上述 JSON 增量写入目标 Skill 的 `evolution.json` 文件中。
- **命令**: `python skill-evolution-manager/scripts/merge_evolution.py <skill_path> <json_string> [--json]`

### 3. 文档缝合 (Stitch)
Agent 调用 `scripts/smart_stitch.py`，将 `evolution.json` 的内容转化为 Markdown 并追加到 `SKILL.md` 末尾。
- **命令**: `python skill-evolution-manager/scripts/smart_stitch.py <skill_path> [--json]`

### 4. 跨版本对齐 (Align)
当 `skill-manager` 更新了某个 Skill 后，Agent 应主动运行 `smart_stitch.py`，将之前保存的经验"重新缝合"到新版文档中。

## 核心脚本

- `scripts/merge_evolution.py`: **增量合并工具**。负责读取旧 JSON，去重合并新 List，保存。
- `scripts/smart_stitch.py`: **文档生成工具**。负责读取 JSON，在 `SKILL.md` 末尾生成或更新 `## User-Learned Best Practices & Constraints` 章节。
- `scripts/align_all.py`: **全量对齐工具**。一键遍历技能根目录（默认自动推断为当前仓库根目录）并缝合所有存在 `evolution.json` 的技能。

### CLI Contract

- `python skill-evolution-manager/scripts/merge_evolution.py <skill_path> <json_string> [--json]`
- `python skill-evolution-manager/scripts/smart_stitch.py <skill_path> [--json]`
- `python skill-evolution-manager/scripts/align_all.py [skills_root] [--json]`

退出码约定：
- `0`: 成功
- `1`: 运行时错误
- `2`: 参数错误

## 最佳实践

- **不要直接修改 SKILL.md 的正文**：除非是明显的拼写错误。所有的经验修正应通过 `evolution.json` 通道进行，这样可以保证在 Skill 升级时经验不丢失。
- **多 Skill 协同**：如果一次对话涉及多个 Skill，请依次为每个 Skill 执行上述流程。

## 使用示例

### 示例1：记录单个技能的经验
```bash
# 记录用户对github-commit技能的偏好
python skill-evolution-manager/scripts/merge_evolution.py github-commit '{
  "preferences": ["提交前总是检查git状态", "使用语义化版本提交消息"],
  "fixes": ["修复子模块处理问题"],
  "custom_prompts": "在提交前运行git status和git diff确认更改"
}'

# 将经验缝合到技能文档
python skill-evolution-manager/scripts/smart_stitch.py github-commit
```

### 示例2：批量处理多个技能
```bash
# 记录paper-detailed-analysis技能的经验
python skill-evolution-manager/scripts/merge_evolution.py paper-detailed-analysis '{
  "preferences": ["优先分析论文的方法论部分", "提取关键算法伪代码"],
  "fixes": ["修复PDF解析中的编码问题"],
  "custom_prompts": "为每篇论文生成执行摘要和技术要点"
}'

# 记录humanizer技能的经验
python skill-evolution-manager/scripts/merge_evolution.py humanizer '{
  "preferences": ["保留专业术语", "调整语气为学术风格"],
  "fixes": ["修复过度人性化导致的语义丢失"],
  "custom_prompts": "针对学术文本使用更保守的人性化策略"
}'

# 批量缝合所有技能的经验
python skill-evolution-manager/scripts/align_all.py .
```

### 示例3：技能更新后的经验恢复
```bash
# 当skill-manager更新技能后，恢复进化数据
python skill-manager/scripts/scan_and_check.py .
python skill-evolution-manager/scripts/align_all.py .

# 验证经验恢复结果
grep -r "User-Learned" . --include="SKILL.md"
```

### 示例4：与其他技能协同工作
```bash
# 与skill-manager协同
python skill-manager/scripts/scan_and_check.py .
python skill-evolution-manager/scripts/align_all.py .

# 与update-readme协同
python scripts/align_all.py
python update-readme/scripts/analyze_project.py .

# 与github-commit协同
python skill-evolution-manager/scripts/merge_evolution.py github-commit '{"preferences": ["自动生成有意义的提交消息"]}'
python skill-evolution-manager/scripts/smart_stitch.py github-commit
python github-commit/scripts/create_commit.py . "feat: 添加技能进化经验"
```

### 示例5：查看进化数据
```bash
# 查看特定技能的进化数据
cat github-commit/evolution.json | python -m json.tool

# 查看所有技能的进化章节
find . -name "SKILL.md" -exec grep -l "User-Learned" {} \;

# 统计进化数据
find . -name "evolution.json" | wc -l
```

## Overview

This skill is used when its `description` in frontmatter matches the user request. Prefer existing scripts under `scripts/` over ad-hoc rewrites.

## References

- `scripts/`: executable helpers for deterministic steps
- `references/`: additional docs loaded on demand
- `assets/`: templates or static files used by the skill

## Trigger Conditions

- User explicitly names this skill
- User intent clearly matches this skill description
- The task needs this skill's scripts/resources

## Applicable Scope

- Requests covered by this skill's frontmatter `description`
- Tasks that benefit from the bundled workflow and scripts

## Out of Scope

- Requests that conflict with repository safety rules
- Tasks unrelated to this skill's declared purpose
- Destructive changes without explicit user permission
