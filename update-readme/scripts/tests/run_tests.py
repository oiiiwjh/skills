#!/usr/bin/env python3
"""
Test runner for update-readme skill scripts
"""

import os
import sys
import subprocess
from pathlib import Path


def run_test_module(module_path: Path) -> bool:
    """Run a test module and return success status"""
    try:
        print(f"\n{'='*60}")
        print(f"Running tests: {module_path.name}")
        print('='*60)
        
        result = subprocess.run(
            [sys.executable, str(module_path)],
            cwd=module_path.parent,
            capture_output=True,
            text=True
        )
        
        if result.returncode == 0:
            print("✅ All tests passed!")
            return True
        else:
            print("❌ Tests failed!")
            if result.stdout:
                print("\nStdout:")
                print(result.stdout)
            if result.stderr:
                print("\nStderr:")
                print(result.stderr)
            return False
            
    except Exception as e:
        print(f"❌ Error running tests: {e}")
        return False


def main():
    """Run all test suites"""
    tests_dir = Path(__file__).parent
    test_modules = [
        tests_dir / 'test_utils.py',
        tests_dir.parent / 'integration' / 'test_integration.py',
    ]
    
    print("🚀 Running test suite for update-readme skill")
    print(f"Python: {sys.version}")
    print(f"Working directory: {Path.cwd()}")
    
    passed = 0
    failed = 0
    
    for test_module in test_modules:
        if test_module.exists():
            if run_test_module(test_module):
                passed += 1
            else:
                failed += 1
        else:
            print(f"⚠️  Test module not found: {test_module}")
    
    print(f"\n{'='*60}")
    print("📊 Test Summary")
    print('='*60)
    print(f"Total tests run: {passed + failed}")
    print(f"✅ Passed: {passed}")
    print(f"❌ Failed: {failed}")
    
    if failed == 0:
        print("\n🎉 All tests passed!")
        return 0
    else:
        print(f"\n💥 {failed} test suite(s) failed")
        return 1


if __name__ == '__main__':
    sys.exit(main())