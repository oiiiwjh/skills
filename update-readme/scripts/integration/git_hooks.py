#!/usr/bin/env python3
"""
Git Hooks Integration Script for update-readme skill

This script provides git hooks that automatically update documentation
when code changes are committed.

Usage:
    python git_hooks.py install    # Install git hooks
    python git_hooks.py uninstall  # Remove git hooks
    python git_hooks.py run --hook=pre-commit  # Run specific hook
"""

import os
import sys
import argparse
import subprocess
from pathlib import Path
from typing import Dict, List, Optional

# Add parent directory to path to import utils
sys.path.insert(0, str(Path(__file__).parent.parent))
from utils import logger, run_command


class GitHooksManager:
    """Manage git hooks for automatic documentation updates"""
    
    def __init__(self, repo_path: Optional[Path] = None):
        self.repo_path = repo_path or Path.cwd()
        self.hooks_dir = self.repo_path / ".git" / "hooks"
        self.script_dir = Path(__file__).parent
        
    def install(self, force: bool = False) -> bool:
        """Install git hooks"""
        try:
            # Check if we're in a git repository
            check_result = run_command(['git', 'rev-parse', '--is-inside-work-tree'], 
                                      cwd=str(self.repo_path))
            if not check_result['success']:
                logger.error("Not a git repository")
                return False
            
            # Create hooks directory if it doesn't exist
            self.hooks_dir.mkdir(parents=True, exist_ok=True)
            
            # Install hooks
            hooks_installed = 0
            hooks = self._get_hook_templates()
            
            for hook_name, hook_content in hooks.items():
                hook_path = self.hooks_dir / hook_name
                
                # Skip if hook exists and not forcing
                if hook_path.exists() and not force:
                    logger.info(f"Hook {hook_name} already exists. Use --force to overwrite.")
                    continue
                
                # Write hook
                with open(hook_path, 'w', encoding='utf-8') as f:
                    f.write(hook_content)
                
                # Make executable
                hook_path.chmod(0o755)
                hooks_installed += 1
                logger.info(f"Installed {hook_name} hook")
            
            logger.info(f"Successfully installed {hooks_installed} git hooks")
            return True
            
        except Exception as e:
            logger.error(f"Failed to install git hooks: {e}")
            return False
    
    def uninstall(self) -> bool:
        """Remove installed git hooks"""
        try:
            hooks = self._get_hook_templates()
            hooks_removed = 0
            
            for hook_name in hooks.keys():
                hook_path = self.hooks_dir / hook_name
                if hook_path.exists():
                    hook_path.unlink()
                    hooks_removed += 1
                    logger.info(f"Removed {hook_name} hook")
            
            logger.info(f"Successfully removed {hooks_removed} git hooks")
            return True
            
        except Exception as e:
            logger.error(f"Failed to uninstall git hooks: {e}")
            return False
    
    def run_hook(self, hook_name: str, hook_args: List[str]) -> int:
        """Run a specific git hook"""
        try:
            hook_script = self._get_hook_script(hook_name)
            if not hook_script:
                logger.error(f"Unknown hook: {hook_name}")
                return 1
            
            # Execute hook script
            result = run_command(['bash', '-c', hook_script] + hook_args)
            if not result['success']:
                logger.error(f"Hook {hook_name} failed: {result.get('error', 'Unknown error')}")
                return 1
            
            logger.info(f"Hook {hook_name} completed successfully")
            return 0
            
        except Exception as e:
            logger.error(f"Error running hook {hook_name}: {e}")
            return 1
    
    def _get_hook_templates(self) -> Dict[str, str]:
        """Get hook template scripts"""
        return {
            'pre-commit': self._get_pre_commit_hook(),
            'post-commit': self._get_post_commit_hook(),
            'post-checkout': self._get_post_checkout_hook(),
            'post-merge': self._get_post_merge_hook(),
        }
    
    def _get_hook_script(self, hook_name: str) -> Optional[str]:
        """Get script for a specific hook"""
        hooks = self._get_hook_templates()
        return hooks.get(hook_name)
    
    def _get_pre_commit_hook(self) -> str:
        """Generate pre-commit hook script"""
        return '''#!/bin/bash
# pre-commit hook for update-readme skill
# Automatically updates documentation before commit

set -e

echo "🔍 Checking for documentation updates..."

# Get changed files
CHANGED_FILES=$(git diff --cached --name-only --diff-filter=ACM)

# Check if any documentation-related files changed
DOC_FILES=$(echo "$CHANGED_FILES" | grep -E '\.(md|txt|rst|yml|yaml|json)$' || true)
CODE_FILES=$(echo "$CHANGED_FILES" | grep -E '\.(js|jsx|ts|tsx|py|java|cpp|c|go|rs)$' || true)

if [ -n "$CODE_FILES" ] && [ -z "$DOC_FILES" ]; then
    echo "⚠️  Code files changed but documentation not updated."
    echo "   Consider running: python -m scripts.generate_readme"
    echo "   Or add --no-verify to skip this check"
    # Uncomment to make it blocking:
    # exit 1
fi

# Run documentation check if README.md exists
if [ -f "README.md" ]; then
    echo "📝 Checking README freshness..."
    python -m scripts.analyze_project --check-only
fi

echo "✅ Documentation check passed"
exit 0
'''
    
    def _get_post_commit_hook(self) -> str:
        """Generate post-commit hook script"""
        return '''#!/bin/bash
# post-commit hook for update-readme skill
# Updates documentation after successful commit

set -e

echo "📝 Updating documentation after commit..."

# Check if we should update documentation
SKIP_UPDATE=${UPDATE_README_SKIP:-0}
if [ "$SKIP_UPDATE" = "1" ]; then
    echo "⏭️  Skipping documentation update (UPDATE_README_SKIP=1)"
    exit 0
fi

# Run in background to not block commit
(
    sleep 1  # Small delay to ensure commit is complete
    
    # Update README if it exists
    if [ -f "README.md" ]; then
        echo "🔄 Updating README.md..."
        python -m scripts.generate_readme --quiet
        
        # Stage updated README if changed
        if git diff --quiet README.md; then
            echo "✅ README.md is up to date"
        else
            git add README.md
            echo "📄 README.md updated and staged"
        fi
    fi
    
    # Update AGENTS.md if it exists
    if [ -f "AGENTS.md" ]; then
        echo "🔄 Updating AGENTS.md..."
        python -m scripts.update_agents --quiet
        
        if git diff --quiet AGENTS.md; then
            echo "✅ AGENTS.md is up to date"
        else
            git add AGENTS.md
            echo "📄 AGENTS.md updated and staged"
        fi
    fi
    
    # Commit documentation updates if any
    if ! git diff --cached --quiet; then
        git commit --amend --no-edit --no-verify
        echo "📝 Documentation updates committed"
    fi
    
) > /tmp/update-readme.log 2>&1 &

echo "🔧 Documentation update started in background"
echo "   Check /tmp/update-readme.log for details"
exit 0
'''
    
    def _get_post_checkout_hook(self) -> str:
        """Generate post-checkout hook script"""
        return '''#!/bin/bash
# post-checkout hook for update-readme skill
# Updates documentation after branch checkout

set -e

echo "🌿 Branch checkout detected..."

# Only run on branch changes (not file checkouts)
if [ "$3" = "1" ]; then
    echo "🔄 Checking documentation consistency..."
    
    # Wait a moment for git operations to complete
    sleep 0.5
    
    # Run documentation check
    if [ -f "scripts/generate_readme.py" ]; then
        python scripts/generate_readme.py --check-only
    fi
    
    echo "✅ Documentation check completed"
fi

exit 0
'''
    
    def _get_post_merge_hook(self) -> str:
        """Generate post-merge hook script"""
        return '''#!/bin/bash
# post-merge hook for update-readme skill
# Updates documentation after merge

set -e

echo "🔄 Merge completed, updating documentation..."

# Check if documentation needs update
if [ -f "scripts/generate_readme.py" ]; then
    echo "📝 Generating updated documentation..."
    
    # Update README
    python scripts/generate_readme.py --quiet
    
    # Update AGENTS if exists
    if [ -f "scripts/update_agents.py" ]; then
        python scripts/update_agents.py --quiet
    fi
    
    # Stage changes
    if [ -f "README.md" ] && ! git diff --quiet README.md; then
        git add README.md
    fi
    
    if [ -f "AGENTS.md" ] && ! git diff --quiet AGENTS.md; then
        git add AGENTS.md
    fi
    
    # Commit if changes were staged
    if ! git diff --cached --quiet; then
        git commit -m "docs: update documentation after merge" --no-verify
        echo "📄 Documentation updated and committed"
    else
        echo "✅ Documentation is already up to date"
    fi
fi

exit 0
'''


def main():
    parser = argparse.ArgumentParser(
        description="Git Hooks Integration for update-readme skill"
    )
    subparsers = parser.add_subparsers(dest='command', help='Command to execute')
    
    # Install command
    install_parser = subparsers.add_parser('install', help='Install git hooks')
    install_parser.add_argument('--force', action='store_true', 
                               help='Overwrite existing hooks')
    
    # Uninstall command
    subparsers.add_parser('uninstall', help='Remove git hooks')
    
    # Run command
    run_parser = subparsers.add_parser('run', help='Run a git hook')
    run_parser.add_argument('--hook', required=True, 
                           choices=['pre-commit', 'post-commit', 'post-checkout', 'post-merge'],
                           help='Hook to run')
    run_parser.add_argument('args', nargs=argparse.REMAINDER, 
                           help='Arguments to pass to hook')
    
    # List command
    subparsers.add_parser('list', help='List available hooks')
    
    args = parser.parse_args()
    
    manager = GitHooksManager()
    
    if args.command == 'install':
        success = manager.install(force=args.force)
        sys.exit(0 if success else 1)
        
    elif args.command == 'uninstall':
        success = manager.uninstall()
        sys.exit(0 if success else 1)
        
    elif args.command == 'run':
        exit_code = manager.run_hook(args.hook, args.args)
        sys.exit(exit_code)
        
    elif args.command == 'list':
        hooks = manager._get_hook_templates()
        print("Available hooks:")
        for hook_name in hooks.keys():
            print(f"  - {hook_name}")
        sys.exit(0)
        
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == '__main__':
    main()