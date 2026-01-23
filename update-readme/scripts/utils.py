#!/usr/bin/env python3

import os
import sys
import json
import yaml
import toml
import logging
from pathlib import Path
from typing import Dict, Any, Optional, List, Union
from datetime import datetime
import subprocess
import traceback

def setup_logging(level=logging.INFO, log_file=None):
    log_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    
    handlers = [logging.StreamHandler(sys.stdout)]
    if log_file:
        handlers.append(logging.FileHandler(log_file))
    
    logging.basicConfig(
        level=level,
        format=log_format,
        handlers=handlers
    )
    
    return logging.getLogger(__name__)

logger = setup_logging()

class SkillError(Exception):
    pass

class FileReadError(SkillError):
    pass

class ConfigParseError(SkillError):
    pass

class GitError(SkillError):
    pass

def safe_read_file(file_path: Union[str, Path], encoding='utf-8') -> Optional[str]:
    try:
        with open(file_path, 'r', encoding=encoding) as f:
            return f.read()
    except (FileNotFoundError, PermissionError, UnicodeDecodeError) as e:
        logger.warning(f"无法读取文件 {file_path}: {e}")
        return None

def safe_write_file(file_path: Union[str, Path], content: str, encoding='utf-8') -> bool:
    try:
        file_path = Path(file_path)
        file_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(file_path, 'w', encoding=encoding) as f:
            f.write(content)
        
        logger.info(f"文件已写入: {file_path}")
        return True
    except (PermissionError, UnicodeEncodeError, OSError) as e:
        logger.error(f"无法写入文件 {file_path}: {e}")
        return False

def parse_config_file(file_path: Union[str, Path]) -> Optional[Dict[str, Any]]:
    file_path = Path(file_path)
    
    if not file_path.exists():
        logger.warning(f"配置文件不存在: {file_path}")
        return None
    
    content = safe_read_file(file_path)
    if content is None:
        return None
    
    suffix = file_path.suffix.lower()
    
    try:
        if suffix == '.json':
            return json.loads(content)
        elif suffix in ['.yml', '.yaml']:
            return yaml.safe_load(content)
        elif suffix == '.toml':
            return toml.loads(content)
        else:
            logger.warning(f"不支持的配置文件格式: {suffix}")
            return None
    except (json.JSONDecodeError, yaml.YAMLError, toml.TomlDecodeError) as e:
        logger.error(f"配置文件解析错误 {file_path}: {e}")
        return None

def run_command(cmd: List[str], cwd: Optional[str] = None, timeout: int = 30) -> Dict[str, Any]:
    result = {
        'success': False,
        'stdout': '',
        'stderr': '',
        'returncode': -1,
        'error': None
    }
    
    try:
        logger.debug(f"运行命令: {' '.join(cmd)}")
        process = subprocess.run(
            cmd,
            cwd=cwd,
            capture_output=True,
            text=True,
            timeout=timeout,
            encoding='utf-8'
        )
        
        result.update({
            'success': process.returncode == 0,
            'stdout': process.stdout,
            'stderr': process.stderr,
            'returncode': process.returncode
        })
        
        if process.returncode != 0:
            logger.warning(f"命令执行失败: {' '.join(cmd)}")
            logger.warning(f"错误输出: {process.stderr}")
        
    except subprocess.TimeoutExpired as e:
        result['error'] = f"命令超时: {e}"
        logger.error(f"命令超时: {' '.join(cmd)}")
    except FileNotFoundError as e:
        result['error'] = f"命令未找到: {e}"
        logger.error(f"命令未找到: {' '.join(cmd)}")
    except Exception as e:
        result['error'] = f"命令执行错误: {e}"
        logger.error(f"命令执行错误: {' '.join(cmd)} - {e}")
    
    return result

def get_git_info(repo_path: Union[str, Path]) -> Dict[str, Any]:
    repo_path = Path(repo_path)
    git_info = {
        'is_git_repo': False,
        'current_branch': None,
        'recent_commits': [],
        'remotes': {},
        'status': None
    }
    
    # Convert Path to string for cwd parameter
    repo_path_str = str(repo_path)
    
    check_result = run_command(['git', 'rev-parse', '--is-inside-work-tree'], cwd=repo_path_str)
    if not check_result['success']:
        logger.info(f"不是Git仓库: {repo_path}")
        return git_info
    
    git_info['is_git_repo'] = True
    
    branch_result = run_command(['git', 'branch', '--show-current'], cwd=repo_path_str)
    if branch_result['success']:
        git_info['current_branch'] = branch_result['stdout'].strip()
    
    log_result = run_command(['git', 'log', '--oneline', '-10'], cwd=repo_path_str)
    if log_result['success']:
        git_info['recent_commits'] = [line.strip() for line in log_result['stdout'].split('\n') if line.strip()]
    
    remote_result = run_command(['git', 'remote', '-v'], cwd=repo_path_str)
    if remote_result['success']:
        remotes = {}
        for line in remote_result['stdout'].split('\n'):
            if line:
                parts = line.split()
                if len(parts) >= 2:
                    remotes[parts[0]] = parts[1]
        git_info['remotes'] = remotes
    
    status_result = run_command(['git', 'status', '--short'], cwd=repo_path_str)
    if status_result['success']:
        git_info['status'] = status_result['stdout'].strip()
    
    return git_info

def format_file_size(size_bytes: int) -> str:
    size_float = float(size_bytes)
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size_float < 1024.0:
            return f"{size_float:.1f} {unit}"
        size_float /= 1024.0
    return f"{size_float:.1f} TB"

def validate_project_data(project_data: Dict[str, Any]) -> bool:
    required_fields = ['project_type', 'language', 'directory_structure']
    
    for field in required_fields:
        if field not in project_data:
            logger.error(f"项目数据缺少必需字段: {field}")
            return False
    
    return True

def create_backup(file_path: Union[str, Path]) -> Optional[Path]:
    file_path = Path(file_path)
    
    if not file_path.exists():
        logger.warning(f"无法备份不存在的文件: {file_path}")
        return None
    
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    backup_path = file_path.with_suffix(f'.{timestamp}.bak')
    
    try:
        import shutil
        shutil.copy2(file_path, backup_path)
        logger.info(f"文件备份已创建: {backup_path}")
        return backup_path
    except Exception as e:
        logger.error(f"创建备份失败 {file_path}: {e}")
        return None

def restore_backup(backup_path: Union[str, Path], original_path: Union[str, Path]) -> bool:
    backup_path = Path(backup_path)
    original_path = Path(original_path)
    
    if not backup_path.exists():
        logger.error(f"备份文件不存在: {backup_path}")
        return False
    
    try:
        import shutil
        shutil.copy2(backup_path, original_path)
        logger.info(f"文件已从备份恢复: {original_path}")
        return True
    except Exception as e:
        logger.error(f"恢复备份失败 {backup_path}: {e}")
        return False

def get_directory_structure(root_dir: Union[str, Path], max_depth: int = 3) -> Dict[str, Any]:
    root_dir = Path(root_dir).resolve()
    
    ignore_patterns = {
        '.git', 'node_modules', '__pycache__', '.venv', 'venv',
        'dist', 'build', '.next', '.nuxt', '.svelte-kit',
        'target', '.idea', '.vscode', '.DS_Store'
    }
    
    def scan_dir(path: Path, depth: int = 0) -> Dict:
        if depth > max_depth:
            return {}
        
        structure = {}
        try:
            for item in sorted(path.iterdir()):
                if item.name in ignore_patterns:
                    continue
                
                if item.is_dir():
                    structure[f"{item.name}/"] = scan_dir(item, depth + 1)
                else:
                    if item.suffix in ['.js', '.ts', '.jsx', '.tsx', '.py', '.rs', '.go', '.java', '.md']:
                        structure[item.name] = None
                    elif item.name in ['package.json', 'Dockerfile', 'docker-compose.yml', '.env']:
                        structure[item.name] = None
        except PermissionError:
            logger.warning(f"无权限访问目录: {path}")
        
        return structure
    
    return scan_dir(root_dir)

def generate_summary_report(project_data: Dict[str, Any]) -> str:
    summary = [
        "📊 项目分析摘要",
        "=" * 40,
        f"项目: {project_data.get('project_name', '未知')}",
        f"类型: {project_data.get('project_type', '未知')}",
        f"语言: {project_data.get('language', '未知')}",
        f"框架: {project_data.get('framework', '未知')}",
        "",
        "📁 目录结构",
        f"源代码目录: {len(project_data.get('source_dirs', []))} 个",
        f"测试目录: {len(project_data.get('test_dirs', []))} 个",
        f"配置文件: {len(project_data.get('config_files', []))} 个",
        "",
        "📦 依赖信息",
        f"依赖数量: {len(project_data.get('dependencies', []))}",
        f"开发依赖: {len(project_data.get('dev_dependencies', []))}",
        "",
        "📄 文档状态",
        f"README.md: {'✅ 存在' if project_data.get('readme_exists') else '❌ 缺失'}",
        f"许可证文件: {'✅ 存在' if project_data.get('license_exists') else '❌ 缺失'}",
        "",
        "🐙 Git信息",
        f"Git仓库: {'✅ 是' if project_data.get('git_info', {}).get('is_git_repo') else '❌ 否'}",
        f"当前分支: {project_data.get('git_info', {}).get('current_branch', '未知')}",
        f"最近提交: {len(project_data.get('git_info', {}).get('recent_commits', []))} 个",
        "=" * 40
    ]
    
    return '\n'.join(summary)

if __name__ == '__main__':
    print("🔧 工具函数模块测试")
    print("-" * 40)
    
    test_content = "测试内容"
    test_file = Path("test_file.txt")
    
    if safe_write_file(test_file, test_content):
        print(f"✅ 文件写入测试通过: {test_file}")
        
        read_content = safe_read_file(test_file)
        if read_content == test_content:
            print(f"✅ 文件读取测试通过")
        else:
            print(f"❌ 文件读取测试失败")
        
        test_file.unlink(missing_ok=True)
    else:
        print(f"❌ 文件写入测试失败")
    
    cmd_result = run_command(['echo', '测试命令'])
    if cmd_result['success']:
        print(f"✅ 命令运行测试通过")
    else:
        print(f"❌ 命令运行测试失败")
    
    print("-" * 40)
    print("测试完成")