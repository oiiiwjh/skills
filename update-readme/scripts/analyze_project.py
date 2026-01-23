#!/usr/bin/env python3
"""
项目分析工具
用于分析项目结构、类型和配置，为文档生成提供数据
"""

import os
import json
import yaml
import toml
import re
from pathlib import Path
from typing import Dict, List, Optional, Any
import subprocess
import sys

class ProjectAnalyzer:
    """项目分析器"""
    
    def __init__(self, root_dir: str = "."):
        self.root_dir = Path(root_dir).resolve()
        self.analysis_result = {
            "project_type": "unknown",
            "language": "unknown",
            "framework": "unknown",
            "has_frontend": False,
            "has_backend": False,
            "is_fullstack": False,
            "is_library": False,
            "is_tool": False,
            "package_manager": "unknown",
            "dependencies": [],
            "dev_dependencies": [],
            "config_files": [],
            "source_dirs": [],
            "test_dirs": [],
            "build_files": [],
            "docker_files": [],
            "readme_exists": False,
            "license_exists": False,
            "git_info": {},
            "directory_structure": {}
        }
    
    def analyze(self) -> Dict[str, Any]:
        """执行完整分析"""
        print(f"🔍 分析项目: {self.root_dir}")
        
        # 检查基本文件
        self._check_basic_files()
        
        # 分析项目类型
        self._analyze_project_type()
        
        # 分析依赖和配置
        self._analyze_dependencies()
        
        # 分析目录结构
        self._analyze_directory_structure()
        
        # 获取Git信息
        self._get_git_info()
        
        # 生成摘要
        self._generate_summary()
        
        return self.analysis_result
    
    def _check_basic_files(self):
        """检查基本文件"""
        basic_files = {
            "README.md": "readme_exists",
            "LICENSE": "license_exists",
            "LICENSE.txt": "license_exists",
            "LICENSE.md": "license_exists"
        }
        
        for file_name, key in basic_files.items():
            if (self.root_dir / file_name).exists():
                self.analysis_result[key] = True
    
    def _analyze_project_type(self):
        """分析项目类型"""
        files = list(self.root_dir.iterdir())
        
        # 检查前端文件
        frontend_indicators = [
            "package.json",
            "package-lock.json",
            "yarn.lock",
            "pnpm-lock.yaml",
            "index.html",
            "vite.config.js",
            "vite.config.ts",
            "webpack.config.js",
            "next.config.js",
            "nuxt.config.js"
        ]
        
        # 检查后端文件
        backend_indicators = [
            "requirements.txt",
            "Pipfile",
            "pyproject.toml",
            "go.mod",
            "Cargo.toml",
            "composer.json",
            "pom.xml",
            "build.gradle",
            "build.gradle.kts"
        ]
        
        # 检查配置文件
        config_indicators = [
            "docker-compose.yml",
            "docker-compose.yaml",
            "Dockerfile",
            ".env",
            ".env.example",
            "docker-compose.prod.yml"
        ]
        
        # 分析文件类型
        has_frontend = any((self.root_dir / f).exists() for f in frontend_indicators)
        has_backend = any((self.root_dir / f).exists() for f in backend_indicators)
        has_config = any((self.root_dir / f).exists() for f in config_indicators)
        
        # 确定项目类型
        if has_frontend and has_backend:
            self.analysis_result["project_type"] = "fullstack"
            self.analysis_result["is_fullstack"] = True
            self.analysis_result["has_frontend"] = True
            self.analysis_result["has_backend"] = True
        elif has_frontend:
            self.analysis_result["project_type"] = "frontend"
            self.analysis_result["has_frontend"] = True
        elif has_backend:
            self.analysis_result["project_type"] = "backend"
            self.analysis_result["has_backend"] = True
        elif has_config:
            self.analysis_result["project_type"] = "tool"
            self.analysis_result["is_tool"] = True
        else:
            # 检查是否是库项目
            lib_files = list(self.root_dir.glob("*.py")) + list(self.root_dir.glob("*.js"))
            if lib_files:
                self.analysis_result["project_type"] = "library"
                self.analysis_result["is_library"] = True
        
        # 确定语言和框架
        self._detect_language_and_framework()
    
    def _detect_language_and_framework(self):
        """检测编程语言和框架"""
        # 检查JavaScript/TypeScript项目
        if (self.root_dir / "package.json").exists():
            try:
                with open(self.root_dir / "package.json", 'r') as f:
                    package_data = json.load(f)
                
                dependencies = package_data.get("dependencies", {})
                dev_dependencies = package_data.get("devDependencies", {})
                
                # 检测框架
                if "react" in dependencies or "react" in dev_dependencies:
                    self.analysis_result["framework"] = "react"
                    self.analysis_result["language"] = "javascript"
                elif "vue" in dependencies or "vue" in dev_dependencies:
                    self.analysis_result["framework"] = "vue"
                    self.analysis_result["language"] = "javascript"
                elif "angular" in dependencies or "@angular/core" in dependencies:
                    self.analysis_result["framework"] = "angular"
                    self.analysis_result["language"] = "typescript"
                elif "next" in dependencies:
                    self.analysis_result["framework"] = "nextjs"
                    self.analysis_result["language"] = "javascript"
                elif "nuxt" in dependencies:
                    self.analysis_result["framework"] = "nuxtjs"
                    self.analysis_result["language"] = "javascript"
                elif "svelte" in dependencies or "svelte" in dev_dependencies:
                    self.analysis_result["framework"] = "svelte"
                    self.analysis_result["language"] = "javascript"
                else:
                    self.analysis_result["framework"] = "nodejs"
                    self.analysis_result["language"] = "javascript"
                
                # 检查TypeScript
                if "typescript" in dev_dependencies or (self.root_dir / "tsconfig.json").exists():
                    self.analysis_result["language"] = "typescript"
                
            except (json.JSONDecodeError, FileNotFoundError):
                pass
        
        # 检查Python项目
        elif (self.root_dir / "requirements.txt").exists() or (self.root_dir / "pyproject.toml").exists():
            self.analysis_result["language"] = "python"
            
            # 检查框架
            if (self.root_dir / "requirements.txt").exists():
                try:
                    with open(self.root_dir / "requirements.txt", 'r') as f:
                        content = f.read().lower()
                    
                    if "django" in content:
                        self.analysis_result["framework"] = "django"
                    elif "flask" in content:
                        self.analysis_result["framework"] = "flask"
                    elif "fastapi" in content:
                        self.analysis_result["framework"] = "fastapi"
                except FileNotFoundError:
                    pass
        
        # 检查Rust项目
        elif (self.root_dir / "Cargo.toml").exists():
            self.analysis_result["language"] = "rust"
            self.analysis_result["framework"] = "rust"
        
        # 检查Go项目
        elif (self.root_dir / "go.mod").exists():
            self.analysis_result["language"] = "go"
            self.analysis_result["framework"] = "go"
    
    def _analyze_dependencies(self):
        """分析依赖关系"""
        # JavaScript/TypeScript项目
        if (self.root_dir / "package.json").exists():
            try:
                with open(self.root_dir / "package.json", 'r') as f:
                    package_data = json.load(f)
                
                self.analysis_result["package_manager"] = "npm"
                self.analysis_result["dependencies"] = list(package_data.get("dependencies", {}).keys())
                self.analysis_result["dev_dependencies"] = list(package_data.get("devDependencies", {}).keys())
                
                # 检查其他包管理器
                if (self.root_dir / "yarn.lock").exists():
                    self.analysis_result["package_manager"] = "yarn"
                elif (self.root_dir / "pnpm-lock.yaml").exists():
                    self.analysis_result["package_manager"] = "pnpm"
                    
            except (json.JSONDecodeError, FileNotFoundError):
                pass
        
        # Python项目
        elif (self.root_dir / "requirements.txt").exists():
            try:
                with open(self.root_dir / "requirements.txt", 'r') as f:
                    lines = f.readlines()
                
                dependencies = []
                for line in lines:
                    line = line.strip()
                    if line and not line.startswith('#') and not line.startswith('-'):
                        # 提取包名（去除版本号）
                        match = re.match(r'^([a-zA-Z0-9_-]+)', line)
                        if match:
                            dependencies.append(match.group(1))
                
                self.analysis_result["package_manager"] = "pip"
                self.analysis_result["dependencies"] = dependencies
                
            except FileNotFoundError:
                pass
        
        # Rust项目
        elif (self.root_dir / "Cargo.toml").exists():
            try:
                with open(self.root_dir / "Cargo.toml", 'r') as f:
                    cargo_data = toml.load(f)
                
                dependencies = []
                if "dependencies" in cargo_data:
                    dependencies = list(cargo_data["dependencies"].keys())
                
                self.analysis_result["package_manager"] = "cargo"
                self.analysis_result["dependencies"] = dependencies
                
            except (toml.TomlDecodeError, FileNotFoundError):
                pass
    
    def _analyze_directory_structure(self):
        """分析目录结构"""
        ignore_patterns = {
            '.git', 'node_modules', '__pycache__', '.venv', 'venv',
            'dist', 'build', '.next', '.nuxt', '.svelte-kit',
            'target', '.idea', '.vscode', '.DS_Store'
        }
        
        def scan_dir(path: Path, depth: int = 0, max_depth: int = 3) -> Dict:
            """递归扫描目录"""
            if depth > max_depth:
                return {}
            
            structure = {}
            try:
                for item in path.iterdir():
                    if item.name in ignore_patterns:
                        continue
                    
                    if item.is_dir():
                        structure[item.name + '/'] = scan_dir(item, depth + 1, max_depth)
                    else:
                        # 只记录重要文件
                        if item.suffix in ['.js', '.ts', '.jsx', '.tsx', '.py', '.rs', '.go', '.java', '.md']:
                            structure[item.name] = None
                        elif item.name in ['package.json', 'Dockerfile', 'docker-compose.yml', '.env']:
                            structure[item.name] = None
            except PermissionError:
                pass
            
            return structure
        
        self.analysis_result["directory_structure"] = scan_dir(self.root_dir)
        
        # 收集配置文件和构建文件
        config_patterns = [
            "*.json", "*.yml", "*.yaml", "*.toml", "*.config.*",
            "Dockerfile*", "docker-compose*", ".env*", "*.env"
        ]
        
        for pattern in config_patterns:
            for file in self.root_dir.glob(pattern):
                if file.is_file():
                    self.analysis_result["config_files"].append(str(file.relative_to(self.root_dir)))
        
        # 收集源代码目录
        source_dirs = ["src", "lib", "app", "server", "client", "components", "pages"]
        for dir_name in source_dirs:
            dir_path = self.root_dir / dir_name
            if dir_path.exists() and dir_path.is_dir():
                self.analysis_result["source_dirs"].append(dir_name)
        
        # 收集测试目录
        test_dirs = ["tests", "test", "__tests__", "spec", "cypress", "e2e"]
        for dir_name in test_dirs:
            dir_path = self.root_dir / dir_name
            if dir_path.exists() and dir_path.is_dir():
                self.analysis_result["test_dirs"].append(dir_name)
    
    def _get_git_info(self):
        """获取Git信息"""
        try:
            # 检查是否是git仓库
            result = subprocess.run(
                ["git", "rev-parse", "--is-inside-work-tree"],
                cwd=self.root_dir,
                capture_output=True,
                text=True
            )
            
            if result.returncode != 0:
                return
            
            # 获取最近提交
            log_result = subprocess.run(
                ["git", "log", "--oneline", "-5"],
                cwd=self.root_dir,
                capture_output=True,
                text=True
            )
            
            if log_result.returncode == 0:
                self.analysis_result["git_info"]["recent_commits"] = log_result.stdout.strip().split('\n')
            
            # 获取分支信息
            branch_result = subprocess.run(
                ["git", "branch", "--show-current"],
                cwd=self.root_dir,
                capture_output=True,
                text=True
            )
            
            if branch_result.returncode == 0:
                self.analysis_result["git_info"]["current_branch"] = branch_result.stdout.strip()
            
            # 获取远程仓库
            remote_result = subprocess.run(
                ["git", "remote", "-v"],
                cwd=self.root_dir,
                capture_output=True,
                text=True
            )
            
            if remote_result.returncode == 0:
                remotes = {}
                for line in remote_result.stdout.strip().split('\n'):
                    if line:
                        parts = line.split()
                        if len(parts) >= 2:
                            remotes[parts[0]] = parts[1]
                self.analysis_result["git_info"]["remotes"] = remotes
                
        except (subprocess.SubprocessError, FileNotFoundError):
            pass
    
    def _generate_summary(self):
        """生成分析摘要"""
        summary = {
            "project": str(self.root_dir.name),
            "type": self.analysis_result["project_type"],
            "language": self.analysis_result["language"],
            "framework": self.analysis_result["framework"],
            "has_documentation": self.analysis_result["readme_exists"],
            "has_license": self.analysis_result["license_exists"],
            "source_directories": len(self.analysis_result["source_dirs"]),
            "test_directories": len(self.analysis_result["test_dirs"]),
            "dependencies_count": len(self.analysis_result["dependencies"]),
            "has_git": bool(self.analysis_result["git_info"])
        }
        
        self.analysis_result["summary"] = summary
    
    def print_report(self):
        """打印分析报告"""
        result = self.analysis_result
        
        print("\n" + "="*60)
        print("📊 项目分析报告")
        print("="*60)
        
        print(f"\n📁 项目: {self.root_dir.name}")
        print(f"📍 路径: {self.root_dir}")
        
        print(f"\n🔧 项目类型: {result['project_type'].upper()}")
        print(f"💻 编程语言: {result['language'].upper()}")
        if result['framework'] != 'unknown':
            print(f"🏗️  框架: {result['framework'].upper()}")
        
        print(f"\n📦 包管理器: {result['package_manager'].upper()}")
        print(f"📚 依赖数量: {len(result['dependencies'])}")
        if result['dependencies']:
            print(f"   主要依赖: {', '.join(result['dependencies'][:5])}")
            if len(result['dependencies']) > 5:
                print(f"   ... 还有 {len(result['dependencies']) - 5} 个依赖")
        
        print(f"\n📄 文档状态:")
        print(f"   README.md: {'✅ 存在' if result['readme_exists'] else '❌ 缺失'}")
        print(f"   许可证文件: {'✅ 存在' if result['license_exists'] else '❌ 缺失'}")
        
        print(f"\n📁 目录结构:")
        if result['source_dirs']:
            print(f"   源代码目录: {', '.join(result['source_dirs'])}")
        if result['test_dirs']:
            print(f"   测试目录: {', '.join(result['test_dirs'])}")
        
        print(f"\n🔧 配置文件:")
        if result['config_files']:
            for config in result['config_files'][:5]:
                print(f"   - {config}")
            if len(result['config_files']) > 5:
                print(f"   ... 还有 {len(result['config_files']) - 5} 个配置文件")
        else:
            print("   未找到配置文件")
        
        print(f"\n🐙 Git信息:")
        if result['git_info']:
            if 'current_branch' in result['git_info']:
                print(f"   当前分支: {result['git_info']['current_branch']}")
            if 'remotes' in result['git_info']:
                print(f"   远程仓库: {len(result['git_info']['remotes'])} 个")
            if 'recent_commits' in result['git_info']:
                print(f"   最近提交: {len(result['git_info']['recent_commits'])} 个")
        else:
            print("   不是Git仓库或Git不可用")
        
        print("\n" + "="*60)
        print("✅ 分析完成")
        print("="*60)

def main():
    """主函数"""
    import argparse
    
    parser = argparse.ArgumentParser(description='分析项目结构')
    parser.add_argument('path', nargs='?', default='.', help='项目路径（默认当前目录）')
    parser.add_argument('--json', action='store_true', help='输出JSON格式')
    parser.add_argument('--output', help='输出到文件')
    
    args = parser.parse_args()
    
    analyzer = ProjectAnalyzer(args.path)
    result = analyzer.analyze()
    
    if args.json:
        output = json.dumps(result, indent=2, ensure_ascii=False)
    else:
        analyzer.print_report()
        output = None
    
    if args.output and output:
        with open(args.output, 'w', encoding='utf-8') as f:
            f.write(output)
        print(f"\n📄 结果已保存到: {args.output}")
    elif args.output and not output:
        # 保存非JSON格式的报告
        import io
        from contextlib import redirect_stdout
        
        f = io.StringIO()
        with redirect_stdout(f):
            analyzer.print_report()
        
        with open(args.output, 'w', encoding='utf-8') as out_file:
            out_file.write(f.getvalue())
        
        print(f"\n📄 报告已保存到: {args.output}")

if __name__ == '__main__':
    main()