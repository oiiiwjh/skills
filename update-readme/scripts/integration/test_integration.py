#!/usr/bin/env python3
"""
Test script for integration utilities
"""

import os
import sys
import tempfile
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from utils import logger


def test_git_hooks_import():
    """Test that git_hooks module can be imported"""
    try:
        from integration.git_hooks import GitHooksManager
        logger.info("✓ git_hooks module imports successfully")
        return True
    except Exception as e:
        logger.error(f"✗ Failed to import git_hooks: {e}")
        return False


def test_ci_cd_import():
    """Test that ci_cd module can be imported"""
    try:
        from integration.ci_cd import CICDManager
        logger.info("✓ ci_cd module imports successfully")
        return True
    except Exception as e:
        logger.error(f"✗ Failed to import ci_cd: {e}")
        return False


def test_git_hooks_template_generation():
    """Test git hooks template generation"""
    try:
        from integration.git_hooks import GitHooksManager
        
        with tempfile.TemporaryDirectory() as tmpdir:
            manager = GitHooksManager(Path(tmpdir))
            templates = manager._get_hook_templates()
            
            required_hooks = ['pre-commit', 'post-commit', 'post-checkout', 'post-merge']
            for hook in required_hooks:
                if hook not in templates:
                    logger.error(f"✗ Missing hook template: {hook}")
                    return False
                if not templates[hook].strip():
                    logger.error(f"✗ Empty hook template: {hook}")
                    return False
            
            logger.info("✓ Git hooks templates generated successfully")
            return True
            
    except Exception as e:
        logger.error(f"✗ Git hooks template test failed: {e}")
        return False


def test_ci_cd_template_generation():
    """Test CI/CD template generation"""
    try:
        from integration.ci_cd import CICDManager
        
        manager = CICDManager()
        
        platforms = ['github-actions', 'gitlab-ci', 'azure-pipelines', 'circleci', 'jenkins']
        for platform in platforms:
            template = manager._get_template(platform)
            if not template:
                logger.error(f"✗ No template for platform: {platform}")
                return False
            
            # Check template has content
            if isinstance(template, (dict, str)):
                if isinstance(template, dict):
                    if not template:
                        logger.error(f"✗ Empty dict template for: {platform}")
                        return False
                elif isinstance(template, str):
                    if not template.strip():
                        logger.error(f"✗ Empty string template for: {platform}")
                        return False
            else:
                logger.error(f"✗ Invalid template type for {platform}: {type(template)}")
                return False
        
        logger.info("✓ CI/CD templates generated successfully")
        return True
        
    except Exception as e:
        logger.error(f"✗ CI/CD template test failed: {e}")
        return False


def test_utils_import():
    """Test that utils module can be imported"""
    try:
        from utils import (
            logger, run_command, safe_read_file, safe_write_file,
            get_git_info, format_file_size, validate_project_data
        )
        logger.info("✓ utils module imports successfully")
        return True
    except Exception as e:
        # Use print since logger might not be available
        print(f"✗ Failed to import utils: {e}")
        return False


def main():
    """Run all integration tests"""
    logger.info("Running integration tests...")
    
    tests = [
        ("Utils Import", test_utils_import),
        ("Git Hooks Import", test_git_hooks_import),
        ("CI/CD Import", test_ci_cd_import),
        ("Git Hooks Templates", test_git_hooks_template_generation),
        ("CI/CD Templates", test_ci_cd_template_generation),
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        logger.info(f"\nTesting: {test_name}")
        if test_func():
            passed += 1
        else:
            logger.error(f"Test failed: {test_name}")
    
    logger.info(f"\n{'='*50}")
    logger.info(f"Test Results: {passed}/{total} passed")
    
    if passed == total:
        logger.info("✅ All integration tests passed!")
        return 0
    else:
        logger.error(f"❌ {total - passed} test(s) failed")
        return 1


if __name__ == '__main__':
    sys.exit(main())