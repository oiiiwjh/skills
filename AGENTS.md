# OpenCode Skills Repository - Agent Guidelines

This repository contains skills for OpenCode agents. Skills are modular, self-contained packages that extend Claude's capabilities with specialized knowledge, workflows, and tool integrations.

## Project Structure

```
skills/
├── paper-detailed-analysis/    # Academic paper analysis skill
│   └── SKILL.md
├── paper-depth-reading/        # Deep paper reading skill
│   └── SKILL.md
├── humanizer/                  # AI text humanization skill
│   ├── SKILL.md
│   ├── package.json
│   ├── humanizer-implementation.js
│   ├── test.js
│   └── humanizer-openapi-spec.yaml
├── skill-creator/              # Skill creation guidance
│   ├── SKILL.md
│   ├── scripts/
│   │   ├── init_skill.py
│   │   ├── package_skill.py
│   │   └── quick_validate.py
│   └── references/
│       ├── workflows.md
│       └── output-patterns.md
└── .vscode/
    └── settings.json
```

## Build, Test, and Development Commands

### Node.js Skills (e.g., humanizer)
```bash
# Navigate to skill directory
cd humanizer/

# Install dependencies (if any)
npm install

# Run tests
npm test

# Run specific test file
node test.js
```

### Python Scripts
```bash
# Run skill validation
python skill-creator/scripts/quick_validate.py <skill-directory>

# Initialize new skill
python skill-creator/scripts/init_skill.py <skill-name> --path <output-directory>

# Package skill for distribution
python skill-creator/scripts/package_skill.py <skill-directory>
```

### No Global Build System
This repository doesn't have a global build system. Each skill is self-contained. Development happens at the skill level.

## Code Style Guidelines

### JavaScript/Node.js
- **Imports**: Use CommonJS `require()` syntax (not ES6 imports)
- **Formatting**: 2-space indentation
- **Naming**: camelCase for variables/functions, PascalCase for classes
- **Error Handling**: Use try-catch blocks for async operations
- **Example from humanizer-implementation.js**:
```javascript
class Humanizer {
  async humanize(text) {
    try {
      // Implementation
    } catch (error) {
      console.error('Error:', error.message);
    }
  }
}
```

### Python
- **Imports**: Standard Python imports at top of file
- **Formatting**: Follow PEP 8 (4-space indentation)
- **Naming**: snake_case for variables/functions, PascalCase for classes
- **Error Handling**: Use try-except with specific exceptions
- **Example from quick_validate.py**:
```python
def validate_skill(skill_path):
    """Basic validation of a skill"""
    try:
        # Implementation
    except yaml.YAMLError as e:
        return False, f"Invalid YAML in frontmatter: {e}"
```

### Skill Development Patterns
1. **SKILL.md Structure**:
   - Must have YAML frontmatter with `name` and `description`
   - Description should clearly indicate when skill triggers
   - Body contains instructions and references to bundled resources

2. **Bundled Resources**:
   - `scripts/` - Executable code for deterministic tasks
   - `references/` - Documentation loaded as needed
   - `assets/` - Files used in output (templates, images, etc.)

3. **Progressive Disclosure**:
   - Keep SKILL.md body concise (<500 lines)
   - Split detailed content into reference files
   - Load resources only when needed

## Testing Guidelines

### JavaScript Tests
- Test files use simple Node.js assertions
- No test framework required
- Example test pattern from `humanizer/test.js`:
```javascript
async function testHumanizer() {
  const humanizer = new Humanizer();
  const testTexts = [...];
  
  for (let i = 0; i < testTexts.length; i++) {
    console.log(`Test ${i + 1}:`);
    const result = await humanizer.humanize(testTexts[i]);
    console.log('Humanized:', result.humanized);
  }
}
```

### Python Tests
- No formal test framework in use
- Scripts should include validation logic
- Use exit codes to indicate success/failure

## Skill Creation Workflow

When creating or modifying skills:

1. **Understand the skill** with concrete examples
2. **Plan reusable contents** (scripts, references, assets)
3. **Initialize skill** with `init_skill.py`
4. **Edit the skill** - implement resources and write SKILL.md
5. **Package skill** with `package_skill.py`
6. **Iterate** based on real usage

## File Organization Conventions

1. **Skill Directory Naming**: kebab-case (e.g., `skill-creator`)
2. **Required Files**: Each skill must have `SKILL.md`
3. **Optional Directories**:
   - `scripts/` - For executable code
   - `references/` - For documentation
   - `assets/` - For output resources
4. **Avoid**: README.md, INSTALLATION_GUIDE.md, CHANGELOG.md, etc.

## Error Handling Standards

### JavaScript
- Use `try-catch` for async operations
- Log errors with `console.error()`
- Return meaningful error messages

### Python
- Catch specific exceptions
- Return tuples `(success, message)` for validation functions
- Use descriptive error messages

## Documentation Standards

1. **SKILL.md Frontmatter**:
   ```yaml
   ---
   name: skill-name
   description: Clear description of when to use this skill
   ---
   ```

2. **Code Comments**:
   - Use JSDoc-style comments for JavaScript functions
   - Use docstrings for Python functions
   - Explain complex logic, not obvious code

3. **Reference Files**:
   - Include table of contents for files >100 lines
   - Organize by domain or variant
   - Link directly from SKILL.md

## Development Environment

### VS Code Settings
The repository includes `.vscode/settings.json` with custom color theme:
- Active title bar: `#dc93f2`
- Activity bar: `#dc93f2`
- Status bar: `#dc93f2`

### No Linter/Formatter Configuration
No ESLint, Prettier, or other linter configurations found. Code style is maintained through consistency with existing patterns.

## Agent-Specific Notes

1. **When working on skills**:
   - Always validate with `quick_validate.py` before packaging
   - Test scripts by running them
   - Follow progressive disclosure principles

2. **When using skills**:
   - Skills trigger based on frontmatter description
   - Load reference files only when needed
   - Use bundled scripts for deterministic tasks

3. **Code quality checks**:
   - Run `npm test` for Node.js skills
   - Validate skill structure before changes
   - Maintain consistency with existing patterns

## Common Tasks for Agents

### Adding a New Skill
```bash
# 1. Initialize skill structure
python skill-creator/scripts/init_skill.py new-skill-name --path .

# 2. Edit SKILL.md and add resources
# 3. Test the skill
# 4. Package for distribution
python skill-creator/scripts/package_skill.py new-skill-name
```

### Modifying Existing Skill
1. Navigate to skill directory
2. Make changes to SKILL.md or resources
3. Test changes (run tests if available)
4. Validate skill structure
5. Consider impact on existing usage

### Running Tests
```bash
# For Node.js skills
cd skill-directory
npm test

# For Python scripts
python script-name.py
```

## Best Practices

1. **Keep SKILL.md concise** - Under 500 lines, split content into references
2. **Test scripts** - Run them to ensure they work
3. **Follow naming conventions** - kebab-case for directories, camelCase/PascalCase for code
4. **Validate before packaging** - Use `quick_validate.py`
5. **Maintain consistency** - Follow patterns in existing skills
6. **Use progressive disclosure** - Load resources only when needed
7. **Document triggers clearly** - In SKILL.md frontmatter description

## Troubleshooting

### Skill Not Triggering
- Check SKILL.md frontmatter description
- Ensure description clearly indicates when to use skill
- Verify skill is in correct directory structure

### Validation Errors
- Run `quick_validate.py` to identify issues
- Check YAML frontmatter format
- Verify required fields (name, description)

### Test Failures
- Check Node.js version (>=14.0.0 for humanizer)
- Verify dependencies are installed
- Examine error messages for clues

---

*This AGENTS.md file provides guidelines for agentic coding agents working in this repository. Follow existing patterns and conventions when making changes.*