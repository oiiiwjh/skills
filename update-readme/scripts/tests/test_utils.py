#!/usr/bin/env python3
"""
Unit tests for utils module
"""

import os
import sys
import tempfile
import json
from pathlib import Path
from unittest.mock import patch, MagicMock

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from utils import (
    logger, run_command, safe_read_file, safe_write_file,
    get_git_info, format_file_size, validate_project_data
)


class TestUtils:
    """Test suite for utils module"""
    
    def test_run_command_success(self):
        """Test run_command with successful command"""
        result = run_command(['echo', 'hello'])
        assert result['success'] is True
        assert result['stdout'].strip() == 'hello'
        assert result['stderr'] == ''
        assert result['returncode'] == 0
    
    def test_run_command_failure(self):
        """Test run_command with failing command"""
        result = run_command(['false'])
        assert result['success'] is False
        assert result['returncode'] != 0
    
    def test_run_command_with_cwd(self):
        """Test run_command with working directory"""
        with tempfile.TemporaryDirectory() as tmpdir:
            result = run_command(['pwd'], cwd=tmpdir)
            assert result['success'] is True
            assert tmpdir in result['stdout']
    
    def test_safe_read_file_exists(self):
        """Test safe_read_file with existing file"""
        with tempfile.NamedTemporaryFile(mode='w', delete=False) as f:
            f.write('test content')
            temp_path = f.name
        
        try:
            content = safe_read_file(temp_path)
            assert content == 'test content'
        finally:
            os.unlink(temp_path)
    
    def test_safe_read_file_not_exists(self):
        """Test safe_read_file with non-existent file"""
        content = safe_read_file('/non/existent/path')
        assert content is None
    
    def test_safe_write_file(self):
        """Test safe_write_file"""
        with tempfile.NamedTemporaryFile(mode='w', delete=False) as f:
            temp_path = f.name
        
        try:
            success = safe_write_file(temp_path, 'new content')
            assert success is True
            
            with open(temp_path, 'r') as f:
                assert f.read() == 'new content'
        finally:
            os.unlink(temp_path)
    
    def test_safe_write_file_directory_error(self):
        """Test safe_write_file with directory error"""
        # Try to write to a directory (should fail)
        with tempfile.TemporaryDirectory() as tmpdir:
            success = safe_write_file(tmpdir, 'content')
            assert success is False
    
    def test_format_file_size(self):
        """Test format_file_size"""
        assert format_file_size(0) == '0.0 B'
        assert format_file_size(1023) == '1023.0 B'
        assert format_file_size(1024) == '1.0 KB'
        assert format_file_size(1024 * 1024) == '1.0 MB'
        assert format_file_size(1024 * 1024 * 1024) == '1.0 GB'
        assert format_file_size(1024 * 1024 * 1024 * 1024) == '1.0 TB'
    
    def test_validate_project_data_valid(self):
        """Test validate_project_data with valid data"""
        valid_data = {
            'project_type': 'library',
            'language': 'python',
            'directory_structure': {'src': [], 'tests': []}
        }
        assert validate_project_data(valid_data) is True
    
    def test_validate_project_data_invalid(self):
        """Test validate_project_data with invalid data"""
        # Missing required field
        invalid_data = {
            'project_type': 'library',
            'language': 'python'
            # Missing directory_structure
        }
        assert validate_project_data(invalid_data) is False
    
    @patch('utils.run_command')
    def test_get_git_info_git_repo(self, mock_run_command):
        """Test get_git_info with git repository"""
        # Mock git commands
        mock_run_command.side_effect = [
            {'success': True, 'stdout': 'true\n', 'stderr': '', 'exit_code': 0},  # rev-parse
            {'success': True, 'stdout': 'main\n', 'stderr': '', 'exit_code': 0},  # branch
            {'success': True, 'stdout': 'abc123 feat: test\n', 'stderr': '', 'exit_code': 0},  # log
            {'success': True, 'stdout': 'origin\thttps://github.com/test/repo.git\n', 'stderr': '', 'exit_code': 0},  # remote
            {'success': True, 'stdout': 'M README.md\n', 'stderr': '', 'exit_code': 0},  # status
        ]
        
        with tempfile.TemporaryDirectory() as tmpdir:
            git_info = get_git_info(tmpdir)
            
            assert git_info['is_git_repo'] is True
            assert git_info['current_branch'] == 'main'
            assert git_info['recent_commits'] == ['abc123 feat: test']
            assert git_info['remotes'] == {'origin': 'https://github.com/test/repo.git'}
            assert git_info['status'] == 'M README.md'
    
    @patch('utils.run_command')
    def test_get_git_info_not_git_repo(self, mock_run_command):
        """Test get_git_info with non-git directory"""
        mock_run_command.return_value = {
            'success': False,
            'stdout': '',
            'stderr': 'fatal: not a git repository',
            'exit_code': 128
        }
        
        with tempfile.TemporaryDirectory() as tmpdir:
            git_info = get_git_info(tmpdir)
            
            assert git_info['is_git_repo'] is False
            assert git_info['current_branch'] is None
            assert git_info['recent_commits'] == []
            assert git_info['remotes'] == {}
            assert git_info['status'] is None


def run_tests():
    """Run all tests"""
    test_cases = [
        ('run_command_success', TestUtils().test_run_command_success),
        ('run_command_failure', TestUtils().test_run_command_failure),
        ('run_command_with_cwd', TestUtils().test_run_command_with_cwd),
        ('safe_read_file_exists', TestUtils().test_safe_read_file_exists),
        ('safe_read_file_not_exists', TestUtils().test_safe_read_file_not_exists),
        ('safe_write_file', TestUtils().test_safe_write_file),
        ('safe_write_file_directory_error', TestUtils().test_safe_write_file_directory_error),
        ('format_file_size', TestUtils().test_format_file_size),
        ('validate_project_data_valid', TestUtils().test_validate_project_data_valid),
        ('validate_project_data_invalid', TestUtils().test_validate_project_data_invalid),
        ('get_git_info_git_repo', TestUtils().test_get_git_info_git_repo),
        ('get_git_info_not_git_repo', TestUtils().test_get_git_info_not_git_repo),
    ]
    
    passed = 0
    failed = 0
    
    for test_name, test_func in test_cases:
        try:
            test_func()
            print(f'✅ {test_name}')
            passed += 1
        except Exception as e:
            print(f'❌ {test_name}: {e}')
            failed += 1
    
    print(f'\n{"="*50}')
    print(f'Results: {passed} passed, {failed} failed')
    
    return failed == 0


if __name__ == '__main__':
    success = run_tests()
    sys.exit(0 if success else 1)