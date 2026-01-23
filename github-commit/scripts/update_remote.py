#!/usr/bin/env python3
"""
更新Git远程仓库链接的脚本
"""

import subprocess
import sys
import os
import re
from typing import Dict, List, Tuple, Any

def run_git_command(command, cwd=None):
    """运行git命令并返回输出"""
    try:
        result = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True,
            cwd=cwd,
            env={**os.environ, 'GIT_TERMINAL_PROMPT': '0'}
        )
        return result.returncode, result.stdout.strip(), result.stderr.strip()
    except Exception as e:
        return 1, "", str(e)

def validate_github_url(url):
    """验证GitHub URL格式"""
    if not url:
        return False, "URL不能为空"
    
    # 检查是否是有效的GitHub URL
    github_patterns = [
        r'^https://github\.com/[\w\-]+/[\w\-]+(\.git)?$',
        r'^git@github\.com:[\w\-]+/[\w\-]+(\.git)?$'
    ]
    
    for pattern in github_patterns:
        if re.match(pattern, url):
            return True, ""
    
    return False, "无效的GitHub URL格式。支持格式：\n- https://github.com/用户名/仓库名.git\n- git@github.com:用户名/仓库名.git"

def get_remotes(cwd=None) -> Dict[str, List[Dict[str, str]]]:
    """获取所有远程仓库"""
    return_code, stdout, stderr = run_git_command("git remote -v", cwd)
    if return_code != 0:
        return {}
    
    remotes: Dict[str, List[Dict[str, str]]] = {}
    for line in stdout.split('\n'):
        if line:
            parts = line.split()
            if len(parts) >= 2:
                remote_name = parts[0]
                remote_url = parts[1]
                remote_type = parts[2] if len(parts) > 2 else 'unknown'
                
                if remote_name not in remotes:
                    remotes[remote_name] = []
                remotes[remote_name].append({
                    'url': remote_url,
                    'type': remote_type
                })
    
    return remotes

def add_remote(name, url, cwd=None):
    """添加远程仓库"""
    return run_git_command(f"git remote add {name} {url}", cwd)

def update_remote(name, url, cwd=None):
    """更新远程仓库URL"""
    # 先删除旧的远程仓库
    return_code, stdout, stderr = run_git_command(f"git remote remove {name}", cwd)
    if return_code != 0:
        return return_code, stdout, stderr
    
    # 添加新的远程仓库
    return add_remote(name, url, cwd)

def remove_remote(name, cwd=None):
    """删除远程仓库"""
    return run_git_command(f"git remote remove {name}", cwd)

def test_remote_connection(name, cwd=None):
    """测试远程仓库连接"""
    return run_git_command(f"git ls-remote {name}", cwd)

def main():
    """主函数"""
    if len(sys.argv) < 4:
        print("用法: python update_remote.py <目录> <远程名称> <GitHub URL>")
        print("示例: python update_remote.py . origin https://github.com/username/repo.git")
        return 1
    
    cwd = sys.argv[1]
    remote_name = sys.argv[2]
    github_url = sys.argv[3]
    
    if not os.path.exists(cwd):
        print(f"❌ 目录不存在: {cwd}")
        return 1
    
    # 验证GitHub URL
    is_valid, error_msg = validate_github_url(github_url)
    if not is_valid:
        print(f"❌ {error_msg}")
        return 1
    
    # 检查是否是Git仓库
    return_code, stdout, stderr = run_git_command("git rev-parse --is-inside-work-tree", cwd)
    if return_code != 0:
        print("❌ 不是Git仓库")
        return 1
    
    # 获取当前远程仓库
    remotes = get_remotes(cwd)
    
    if remote_name in remotes:
        print(f"⚠️  远程仓库 '{remote_name}' 已存在")
        current_urls = [r['url'] for r in remotes[remote_name]]
        if current_urls:
            print(f"   当前URL: {current_urls[0]}")
        print(f"   新URL: {github_url}")
        
        confirm = input("是否更新？(y/N): ").strip().lower()
        if confirm != 'y':
            print("❌ 操作取消")
            return 0
        
        # 更新远程仓库
        print(f"🔄 更新远程仓库 '{remote_name}'...")
        return_code, stdout, stderr = update_remote(remote_name, github_url, cwd)
    else:
        # 添加新的远程仓库
        print(f"➕ 添加远程仓库 '{remote_name}'...")
        return_code, stdout, stderr = add_remote(remote_name, github_url, cwd)
    
    if return_code != 0:
        print(f"❌ 操作失败: {stderr}")
        return return_code
    
    print(f"✅ 操作成功: {stdout}")
    
    # 测试连接
    print(f"🔗 测试远程连接...")
    return_code, stdout, stderr = test_remote_connection(remote_name, cwd)
    if return_code == 0:
        print("✅ 远程连接测试成功")
    else:
        print(f"⚠️  远程连接测试失败: {stderr}")
        print("提示: 请检查URL是否正确，以及是否有访问权限")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())