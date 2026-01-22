#!/usr/bin/env python3
"""
检查Git仓库状态的脚本
"""

import subprocess
import sys
import os

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

def check_git_repo(cwd=None):
    """检查是否是Git仓库"""
    return_code, stdout, stderr = run_git_command("git rev-parse --is-inside-work-tree", cwd)
    return return_code == 0

def get_remote_urls(cwd=None):
    """获取远程仓库URL"""
    return_code, stdout, stderr = run_git_command("git remote -v", cwd)
    if return_code != 0:
        return []
    
    remotes = []
    for line in stdout.split('\n'):
        if line:
            parts = line.split()
            if len(parts) >= 2:
                remotes.append({
                    'name': parts[0],
                    'url': parts[1],
                    'type': parts[2] if len(parts) > 2 else 'unknown'
                })
    return remotes

def get_current_branch(cwd=None):
    """获取当前分支"""
    return_code, stdout, stderr = run_git_command("git branch --show-current", cwd)
    if return_code == 0:
        return stdout.strip()
    return None

def get_status_summary(cwd=None):
    """获取状态摘要"""
    return_code, stdout, stderr = run_git_command("git status --porcelain", cwd)
    if return_code != 0:
        return []
    
    changes = []
    for line in stdout.split('\n'):
        if line:
            status = line[:2].strip()
            file_path = line[3:]
            changes.append({
                'status': status,
                'file': file_path
            })
    return changes

def get_commit_history(cwd=None, limit=5):
    """获取提交历史"""
    return_code, stdout, stderr = run_git_command(f"git log --oneline -{limit}", cwd)
    if return_code != 0:
        return []
    
    commits = []
    for line in stdout.split('\n'):
        if line:
            parts = line.split(' ', 1)
            if len(parts) == 2:
                commits.append({
                    'hash': parts[0],
                    'message': parts[1]
                })
    return commits

def main():
    """主函数"""
    cwd = sys.argv[1] if len(sys.argv) > 1 else os.getcwd()
    
    print(f"检查目录: {cwd}")
    
    if not check_git_repo(cwd):
        print("❌ 不是Git仓库")
        return 1
    
    print("✅ 是Git仓库")
    
    # 获取远程信息
    remotes = get_remote_urls(cwd)
    if remotes:
        print("\n📡 远程仓库:")
        for remote in remotes:
            print(f"  {remote['name']}: {remote['url']} ({remote['type']})")
    else:
        print("\n⚠️  没有配置远程仓库")
    
    # 获取当前分支
    branch = get_current_branch(cwd)
    if branch:
        print(f"\n🌿 当前分支: {branch}")
    
    # 获取状态
    changes = get_status_summary(cwd)
    if changes:
        print(f"\n📝 未提交的更改 ({len(changes)}个):")
        for change in changes:
            status_symbol = {
                'M': '📄',
                'A': '🆕',
                'D': '🗑️',
                'R': '🔄',
                'C': '📋',
                'U': '❓'
            }.get(change['status'][0], '📝')
            print(f"  {status_symbol} {change['status']} {change['file']}")
    else:
        print("\n✅ 工作区干净，没有未提交的更改")
    
    # 获取提交历史
    commits = get_commit_history(cwd)
    if commits:
        print(f"\n📜 最近提交 ({len(commits)}个):")
        for commit in commits:
            print(f"  {commit['hash'][:8]} {commit['message']}")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())