# AGENTS.md - Skills Repository Guidelines

Comprehensive guidelines for agentic coding agents working with this skills repository.

## Overview

This document provides guidelines, conventions, and best practices for agents working with skills in this repository. Skills are modular packages that extend agent capabilities with specialized knowledge, workflows, and tool integrations.

## How to Use These Skills

- Canonical source directory: `~/.agents/skills`
- Codex and similar agents can discover skills directly from that directory.
- For OpenCode, keep this repository in `~/.agents/skills` and symlink the skill directories into `~/.config/opencode/skill`.

Example:
```bash
git clone <repo-url> ~/.agents/skills
mkdir -p ~/.config/opencode/skill
ln -s ~/.agents/skills/* ~/.config/opencode/skill/
```

## Available Skills

Canonical source directory for real skills: `~/.agents/skills`

Current skill set (14):
- `baoyu-url-to-markdown`
- `github-commit`
- `github-to-skills`
- `humanizer`
- `humanizer-zh`
- `latex-lite-template-builder`
- `paper-depth-reading`
- `paper-detailed-analysis`
- `pdf`
- `skill-creator`
- `skill-evolution-manager`
- `skill-installer`
- `skill-manager`
- `update-readme`

Other tool-specific skill directories should consume these skills through symlinks.

## Skill Development Guidelines

### Skill Structure

Each skill must follow this structure:
```
skill-name/
├── SKILL.md (required)           # YAML frontmatter + instructions
├── scripts/ (optional)           # Executable code for deterministic tasks
├── references/ (optional)        # Documentation loaded as needed
└── assets/ (optional)            # Files used in output (templates, etc.)
```

### SKILL.md Requirements

Every SKILL.md must include YAML frontmatter:
```yaml
---
name: skill-name
description: Clear description of when to use this skill
---
```

The body should include:
- **Overview**: What the skill does and when to use it
- **Workflow**: Step-by-step instructions
- **Examples**: Concrete usage examples
- **References**: Links to bundled resources

### Code Style Guidelines

#### Python Skills
- **Indentation**: 4 spaces (PEP 8)
- **Naming**: snake_case for functions/variables, PascalCase for classes
- **Imports**: Group imports (standard library, third-party, local)
- **Error Handling**: Use try-except with meaningful error messages
- **Type Hints**: Include type hints for function signatures

Example:
```python
def validate_skill(skill_path: str) -> dict:
    """Validate a skill directory structure.
    
    Args:
        skill_path: Path to skill directory
        
    Returns:
        Dictionary with validation results
        
    Raises:
        FileNotFoundError: If skill directory doesn't exist
    """
    try:
        # Implementation
        pass
    except Exception as e:
        raise ValueError(f"Validation failed: {e}")
```

#### JavaScript/Node.js Skills
- **Indentation**: 2 spaces
- **Naming**: camelCase for functions/variables, PascalCase for classes
- **Imports**: CommonJS (`require`) for Node.js skills
- **Error Handling**: Use try-catch with descriptive error messages
- **Async/Await**: Prefer async/await over callbacks

Example:
```javascript
function humanizeText(text, options = {}) {
  try {
    // Implementation
    return humanizedText;
  } catch (error) {
    throw new Error(`Humanization failed: ${error.message}`);
  }
}
```

## Build and Test Commands

### Python-based Skills
```bash
# Run validation script
python skill-creator/scripts/quick_validate.py skill-directory

# Run tests (if available)
cd skill-directory
python -m pytest tests/  # or specific test file
```

### Node.js Skills
```bash
# Install dependencies
cd skill-directory
npm install

# Run tests
npm test

# Run specific test file
node test.js
```

### Generic Commands
```bash
# Check syntax
python -m py_compile script.py  # Python
node -c script.js              # JavaScript

# Lint code
python -m pylint script.py     # Python (if pylint installed)
npx eslint script.js           # JavaScript (if eslint configured)
```

## File Organization Standards

### Directory Naming
- Use kebab-case for skill directories (e.g., `skill-creator`, `github-commit`)
- Use descriptive names that indicate the skill's purpose

### Required Files
- **SKILL.md** (or **skill.md**): Main skill documentation (required)
- **LICENSE.txt**: License information (recommended)

### Files to Avoid
- README.md (use SKILL.md instead)
- INSTALLATION_GUIDE.md (include in SKILL.md)
- CHANGELOG.md (use git history)
- Unnecessary configuration files

### Script Organization
- Place executable scripts in `scripts/` directory
- Use descriptive names (e.g., `validate_skill.py`, `humanize_text.js`)
- Include shebang lines for executable scripts
- Add proper error handling and logging

## Development Environment Setup

### VS Code Settings
The repository includes `.vscode/settings.json` with recommended settings:
- Python path configuration
- Formatting rules
- Linting preferences

### Git Configuration
- Commit messages should follow conventional commits
- Use meaningful commit descriptions
- Include references to issues when applicable

### Testing Strategy
1. **Unit Tests**: Test individual functions/components
2. **Integration Tests**: Test skill workflows end-to-end
3. **Validation Tests**: Verify skill structure and requirements

## Skill Development Patterns

### Progressive Disclosure Pattern
Skills should use a three-level loading system:
1. **Metadata** (name + description): Always in context (~100 words)
2. **SKILL.md body**: Loaded when skill triggers (<5k words)
3. **Bundled resources**: Loaded as needed by Claude

### Resource Management
- **References**: For documentation Claude should reference while working
- **Scripts**: For deterministic tasks that are repeatedly rewritten
- **Assets**: For files used in output (templates, images, etc.)

### Error Handling Patterns
- Provide clear error messages
- Include recovery suggestions
- Log errors appropriately
- Validate inputs before processing

## Agent Workflow Guidelines

### When Working with Skills
1. **Identify the right skill**: Check skill descriptions for matches
2. **Load the skill**: Use the skill tool with the skill name
3. **Follow instructions**: Execute the skill's workflow
4. **Use bundled resources**: Reference scripts and documentation as needed
5. **Validate results**: Run tests and verify outputs

### Skill Selection Criteria
- **Exact match**: Use when skill description exactly matches the task
- **Partial match**: Use when skill covers part of the task
- **No match**: Consider creating a new skill or adapting existing ones

### Quality Assurance
- **Before committing**: Run validation scripts
- **After changes**: Test affected functionality
- **Regular maintenance**: Update documentation and dependencies

## Common Tasks and Commands

### Skill Creation and Management
```bash
# Initialize new skill
python skill-creator/scripts/init_skill.py my-new-skill --path .

# Validate skill structure
python skill-creator/scripts/quick_validate.py my-new-skill

# Generate OpenAI skill metadata
python skill-creator/scripts/generate_openai_yaml.py my-new-skill

# List all installed skills
python skill-manager/scripts/list_skills.py .

# Check for skill updates
python skill-manager/scripts/scan_and_check.py .

# Convert GitHub repo to skill
python github-to-skills/scripts/fetch_github_info.py https://github.com/username/repo.git

# List installable curated skills
python skill-installer/scripts/list-skills.py

# Evolve skills based on feedback
python skill-evolution-manager/scripts/merge_evolution.py skill-name '{"preferences": ["user preferences"], "fixes": ["known fixes"], "custom_prompts": "custom instructions"}'
python skill-evolution-manager/scripts/smart_stitch.py skill-name
```

### Documentation Updates
```bash
# Update README.md based on current structure
# (Use update-readme skill)

# Check git status
git status

# View recent commits
git log --oneline -10
```

### Refactored CLI Contracts (2026-03)
```bash
# skill-evolution-manager
python skill-evolution-manager/scripts/merge_evolution.py <skill_path> <json_string> [--json]
python skill-evolution-manager/scripts/smart_stitch.py <skill_path> [--json]
python skill-evolution-manager/scripts/align_all.py [skills_root] [--json]

# github-commit
python github-commit/scripts/check_git_status.py [path] [--history-limit N] [--json]
python github-commit/scripts/update_remote.py <path> <remote> <url> [--json]
python github-commit/scripts/create_commit.py <path> <message> [--push] [--remote origin] [--json]

# update-readme
python update-readme/scripts/analyze_project.py [path] [--json] [--output <file>]
python update-readme/scripts/generate_readme.py --project-data <analysis.json> [--output README.md] [--update] [--json]
python update-readme/scripts/update_agents.py [--project-data <analysis.json>] [--output AGENTS.md] [--update] [--json]
```

Exit code contract for refactored Python CLIs:
- `0`: success
- `1`: runtime error
- `2`: argument/usage error

### Code Quality
```bash
# Check Python syntax
python -m py_compile script.py

# Check JavaScript syntax
node -c script.js

# Run linters (if configured)
pylint script.py
eslint script.js
```

## Troubleshooting

### Common Issues

#### Skill Not Loading
- Verify skill name matches directory name
- Check SKILL.md frontmatter format
- Ensure skill is in the correct location

#### Script Execution Errors
- Check file permissions (`chmod +x script.py`)
- Verify Python/Node.js version compatibility
- Check for missing dependencies

#### Validation Failures
- Review skill structure requirements
- Check for missing required files
- Verify file naming conventions

### Debugging Tips
1. **Start simple**: Test basic functionality first
2. **Check logs**: Look for error messages and warnings
3. **Isolate issues**: Test components independently
4. **Consult references**: Check skill documentation and examples

## Best Practices

### For Skill Developers
1. **Keep it concise**: Only include essential information
2. **Provide examples**: Show concrete usage scenarios
3. **Include error handling**: Anticipate and handle common errors
4. **Test thoroughly**: Verify all functionality works as expected
5. **Document clearly**: Write clear, actionable instructions

### For Agents Using Skills
1. **Read skill descriptions**: Choose the right skill for the task
2. **Follow workflows**: Execute steps in the recommended order
3. **Validate inputs**: Check requirements before proceeding
4. **Test outputs**: Verify results meet expectations
5. **Provide feedback**: Report issues or suggest improvements

### For Repository Maintenance
1. **Regular updates**: Keep skills current with best practices
2. **Quality checks**: Run validation scripts regularly
3. **Documentation sync**: Ensure documentation matches code
4. **Dependency management**: Update dependencies as needed
5. **Backward compatibility**: Maintain compatibility when possible

## Resources

- [OpenCode Skills Documentation](https://docs.opencode.ai/skills)
- [Skill Creator Guide](./skill-creator/SKILL.md)
- [GitHub Commit Skill](./github-commit/SKILL.md)
- [Update Readme Skill](./update-readme/SKILL.md)
- [Humanizer Skill](./humanizer/SKILL.md)

## Contributing

See the main [README.md](./README.md) for contribution guidelines and skill development principles.

---

*Last updated: January 22, 2026*
