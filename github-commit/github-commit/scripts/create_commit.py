#!/usr/bin/env python3
"""
创建Git提交的脚本
"""

import subprocess
import sys
import os
import re

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

def validate_commit_message(message):
    """验证提交消息格式"""
    if not message or not message.strip():
        return False, "提交消息不能为空"
    
    if len(message.strip()) < 10:
        return False, "提交消息太短，请提供更详细的描述"
    
    if len(message.strip()) > 200:
        return False, "提交消息太长，请精简到200字符以内"
    
    return True, ""

def generate_commit_message(changes):
    """根据更改生成提交消息"""
    if not changes:
        return "更新代码"
    
    change_types = {}
    for change in changes:
        status = change['status'][0] if change['status'] else '?'
        if status in change_types:
            change_types[status] += 1
        else:
            change_types[status] = 1
    
    # 分析更改类型
    actions = []
    if 'M' in change_types:
        actions.append(f"修改{change_types['M']}个文件")
    if 'A' in change_types:
        actions.append(f"新增{change_types['A']}个文件")
    if 'D' in change_types:
        actions.append(f"删除{change_types['D']}个文件")
    if 'R' in change_types:
        actions.append(f"重命名{change_types['R']}个文件")
    
    if actions:
        return f"{'、'.join(actions)}"
    else:
        return "代码更新"

def get_changes_summary(cwd=None):
    """获取更改摘要"""
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

def add_all_changes(cwd=None):
    """添加所有更改到暂存区"""
    return run_git_command("git add .", cwd)

def create_commit(message, cwd=None):
    """创建提交"""
    return run_git_command(f'git commit -m "{message}"', cwd)

def push_to_remote(remote="origin", branch=None, cwd=None):
    """推送到远程仓库"""
    if not branch:
        return_code, stdout, stderr = run_git_command("git branch --show-current", cwd)
        if return_code == 0:
            branch = stdout.strip()
        else:
            return return_code, stdout, stderr
    
    if branch:
        return run_git_command(f"git push {remote} {branch}", cwd)
    else:
        return 1, "", "无法确定当前分支"

def main():
    """主函数"""
    if len(sys.argv) < 3:
        print("用法: python create_commit.py <目录> <提交消息> [--push]")
        return 1
    
    cwd = sys.argv[1]
    commit_message = sys.argv[2]
    should_push = len(sys.argv) > 3 and sys.argv[3] == "--push"
    
    if not os.path.exists(cwd):
        print(f"❌ 目录不存在: {cwd}")
        return 1
    
    # 验证提交消息
    is_valid, error_msg = validate_commit_message(commit_message)
    if not is_valid:
        print(f"❌ 提交消息无效: {error_msg}")
        return 1
    
    # 获取更改
    changes = get_changes_summary(cwd)
    if not changes:
        print("⚠️  没有检测到更改，跳过提交")
        return 0
    
    print(f"📝 检测到 {len(changes)} 个更改")
    
    # 添加所有更改
    print("📦 添加更改到暂存区...")
    return_code, stdout, stderr = add_all_changes(cwd)
    if return_code != 0:
        print(f"❌ 添加更改失败: {stderr}")
        return return_code
    
    # 创建提交
    print(f"💾 创建提交: {commit_message}")
    return_code, stdout, stderr = create_commit(commit_message, cwd)
    if return_code != 0:
        print(f"❌ 创建提交失败: {stderr}")
        return return_code
    
    print(f"✅ 提交成功: {stdout}")
    
    # 如果需要推送
    if should_push:
        print("🚀 推送到远程仓库...")
        return_code, stdout, stderr = push_to_remote(cwd=cwd)
        if return_code != 0:
            print(f"❌ 推送失败: {stderr}")
            return return_code
        print(f"✅ 推送成功: {stdout}")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())