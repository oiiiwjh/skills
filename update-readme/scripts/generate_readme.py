#!/usr/bin/env python3
"""
README.md 生成器
基于项目分析结果生成或更新README.md文件
"""

import os
import json
from pathlib import Path
from typing import Dict, Any, Optional, List
from datetime import datetime
import re

class ReadmeGenerator:
    """README.md生成器"""
    
    def __init__(self, project_data: Dict[str, Any], output_dir: str = "."):
        self.project_data = project_data
        self.output_dir = Path(output_dir).resolve()
        self.templates = self._load_templates()
    
    def _load_templates(self) -> Dict[str, str]:
        """加载模板"""
        templates = {
            "frontend": self._get_frontend_template(),
            "backend": self._get_backend_template(),
            "fullstack": self._get_fullstack_template(),
            "library": self._get_library_template(),
            "tool": self._get_tool_template(),
            "default": self._get_default_template()
        }
        return templates
    
    def generate(self) -> str:
        """生成README.md内容"""
        project_type = self.project_data.get("project_type", "default")
        template = self.templates.get(project_type, self.templates["default"])
        
        # 替换模板变量
        content = self._replace_template_variables(template)
        
        # 格式化内容
        content = self._format_content(content)
        
        return content
    
    def _replace_template_variables(self, template: str) -> str:
        """替换模板变量"""
        variables = {
            "project_name": self._get_project_name(),
            "project_description": self._get_project_description(),
            "current_date": datetime.now().strftime("%Y-%m-%d"),
            "year": datetime.now().strftime("%Y"),
            "features": self._generate_features(),
            "installation": self._generate_installation(),
            "usage": self._generate_usage(),
            "project_structure": self._generate_project_structure(),
            "configuration": self._generate_configuration(),
            "development": self._generate_development(),
            "contributing": self._generate_contributing(),
            "license": self._generate_license(),
            "badges": self._generate_badges(),
            "api_reference": self._generate_api_reference(),
            "tests": self._generate_tests(),
            "deployment": self._generate_deployment()
        }
        
        content = template
        for key, value in variables.items():
            placeholder = f"{{{{{key}}}}}"
            content = content.replace(placeholder, value)
        
        return content
    
    def _get_project_name(self) -> str:
        """获取项目名称"""
        # 尝试从package.json获取
        if "package.json" in str(self.output_dir):
            try:
                package_path = self.output_dir / "package.json"
                if package_path.exists():
                    with open(package_path, 'r') as f:
                        package_data = json.load(f)
                    return package_data.get("name", self.output_dir.name)
            except:
                pass
        
        # 使用目录名
        return self.output_dir.name
    
    def _get_project_description(self) -> str:
        """获取项目描述"""
        # 尝试从package.json获取
        if "package.json" in str(self.output_dir):
            try:
                package_path = self.output_dir / "package.json"
                if package_path.exists():
                    with open(package_path, 'r') as f:
                        package_data = json.load(f)
                    description = package_data.get("description", "")
                    if description:
                        return description
            except:
                pass
        
        # 根据项目类型生成默认描述
        project_type = self.project_data.get("project_type", "default")
        descriptions = {
            "frontend": "现代化的前端应用",
            "backend": "高性能的后端服务",
            "fullstack": "完整的全栈应用",
            "library": "实用的工具库",
            "tool": "便捷的开发工具"
        }
        
        return descriptions.get(project_type, "一个优秀的项目")
    
    def _generate_features(self) -> str:
        """生成功能特性"""
        features = []
        project_type = self.project_data.get("project_type", "")
        
        if project_type == "frontend":
            features = [
                "现代化的前端框架",
                "响应式设计",
                "组件化开发",
                "状态管理",
                "路由管理"
            ]
        elif project_type == "backend":
            features = [
                "RESTful API设计",
                "数据库集成",
                "身份验证和授权",
                "错误处理中间件",
                "日志记录"
            ]
        elif project_type == "fullstack":
            features = [
                "前后端分离架构",
                "API接口文档",
                "用户认证系统",
                "数据持久化",
                "部署配置"
            ]
        elif project_type == "library":
            features = [
                "简洁的API设计",
                "完整的类型定义",
                "详细的文档",
                "单元测试覆盖",
                "持续集成"
            ]
        else:
            features = [
                "易于使用",
                "良好文档",
                "持续维护",
                "社区支持"
            ]
        
        if self.project_data.get("has_frontend"):
            features.append("前端界面")
        if self.project_data.get("has_backend"):
            features.append("后端服务")
        if self.project_data.get("test_dirs"):
            features.append("测试套件")
        if self.project_data.get("docker_files"):
            features.append("容器化支持")
        
        limited_features = features[:8]
        features_list = "\n".join([f"- **{feature}**" for feature in limited_features])
        return features_list
    
    def _generate_installation(self) -> str:
        """生成安装说明"""
        package_manager = self.project_data.get("package_manager", "")
        language = self.project_data.get("language", "")
        
        installation = "## 📦 安装\n\n"
        
        if package_manager == "npm":
            installation += """### 前提条件
- Node.js 16+
- npm 7+ 或 yarn 1.22+

### 安装依赖
```bash
npm install
# 或
yarn install
# 或
pnpm install
```"""
        elif package_manager == "pip":
            installation += """### 前提条件
- Python 3.8+
- pip 20+

### 创建虚拟环境（推荐）
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\\Scripts\\activate  # Windows
```

### 安装依赖
```bash
pip install -r requirements.txt
```"""
        elif package_manager == "cargo":
            installation += """### 前提条件
- Rust 1.60+
- Cargo

### 安装
```bash
cargo build
```"""
        else:
            installation += """### 克隆仓库
```bash
git clone [仓库地址]
cd [项目目录]
```"""
        
        return installation
    
    def _generate_usage(self) -> str:
        """生成使用说明"""
        project_type = self.project_data.get("project_type", "")
        
        usage = "## 🚀 使用\n\n"
        
        if project_type == "frontend":
            usage += """### 开发模式
```bash
npm run dev
```

### 构建生产版本
```bash
npm run build
```

### 预览构建结果
```bash
npm run preview
```"""
        elif project_type == "backend":
            usage += """### 开发模式
```bash
npm run dev
# 或
python app.py
```

### 生产模式
```bash
npm start
# 或
gunicorn app:app
```"""
        elif project_type == "fullstack":
            usage += """### 启动后端服务
```bash
cd server
npm run dev
```

### 启动前端应用
```bash
cd client
npm run dev
```"""
        else:
            usage += """### 基本使用
```bash
# 运行项目
./start.sh

# 或直接执行
python main.py
```"""
        
        return usage
    
    def _generate_project_structure(self) -> str:
        """生成项目结构"""
        structure = self.project_data.get("directory_structure", {})
        
        if not structure:
            return ""
        
        def format_structure(data: Dict, indent: int = 0) -> List[str]:
            lines = []
            prefix = "    " * indent
            
            for key, value in data.items():
                if value is None:
                    lines.append(f"{prefix}{key}")
                else:
                    lines.append(f"{prefix}{key}")
                    lines.extend(format_structure(value, indent + 1))
            
            return lines
        
        structure_lines = format_structure(structure)
        structure_text = "\n".join(structure_lines)
        
        return f"""## 📁 项目结构

```
{structure_text}
```"""
    
    def _generate_configuration(self) -> str:
        """生成配置说明"""
        config_files = self.project_data.get("config_files", [])
        
        if not config_files:
            return ""
        
        config_examples = []
        for config_file in config_files[:3]:  # 只显示前3个配置文件
            if config_file.endswith('.env'):
                config_examples.append(f"""### 环境变量 ({config_file})
创建 `.env` 文件：
```env
API_URL=http://localhost:3000
DATABASE_URL=postgresql://user:password@localhost:5432/dbname
SECRET_KEY=your-secret-key
```""")
            elif config_file == 'docker-compose.yml':
                config_examples.append(f"""### Docker Compose 配置
使用 Docker Compose 启动所有服务：
```bash
docker-compose up -d
```""")
        
        if config_examples:
            return "## ⚙️ 配置\n\n" + "\n\n".join(config_examples)
        
        return ""
    
    def _generate_development(self) -> str:
        """生成开发指南"""
        test_dirs = self.project_data.get("test_dirs", [])
        
        development = "## 🛠️ 开发\n\n"
        
        if test_dirs:
            development += """### 运行测试
```bash
npm test
# 或
pytest
```

### 代码检查
```bash
npm run lint
# 或
flake8 .
```"""
        else:
            development += """### 代码规范
请遵循项目的代码规范：
- 使用一致的缩进
- 添加适当的注释
- 编写清晰的提交信息"""
        
        return development
    
    def _generate_contributing(self) -> str:
        """生成贡献指南"""
        return """## 🤝 贡献

欢迎贡献！请阅读以下指南：

### 开发流程
1. Fork 本仓库
2. 创建功能分支 (`git checkout -b feature/amazing-feature`)
3. 提交更改 (`git commit -m 'Add amazing feature'`)
4. 推送到分支 (`git push origin feature/amazing-feature`)
5. 创建 Pull Request

### 代码规范
- 遵循项目现有的代码风格
- 添加适当的注释
- 编写单元测试
- 更新相关文档

### 提交信息规范
使用约定式提交：
- `feat:` 新功能
- `fix:` 修复bug
- `docs:` 文档更新
- `style:` 代码格式调整
- `refactor:` 代码重构
- `test:` 测试相关
- `chore:` 构建过程或辅助工具变动"""
    
    def _generate_license(self) -> str:
        """生成许可证信息"""
        has_license = self.project_data.get("license_exists", False)
        
        if has_license:
            return """## 📄 许可证

本项目基于 MIT 许可证发布 - 查看 [LICENSE](LICENSE) 文件了解详情。"""
        else:
            return """## 📄 许可证

版权所有 © {year} 项目作者。保留所有权利。"""
    
    def _generate_badges(self) -> str:
        """生成徽章"""
        badges = []
        
        # 版本徽章
        badges.append("![版本](https://img.shields.io/badge/version-1.0.0-blue)")
        
        # 构建状态
        badges.append("![构建状态](https://img.shields.io/badge/build-passing-green)")
        
        # 许可证
        if self.project_data.get("license_exists"):
            badges.append("![许可证](https://img.shields.io/badge/license-MIT-blue)")
        
        # 语言
        language = self.project_data.get("language", "").lower()
        if language:
            badges.append(f"![语言](https://img.shields.io/badge/language-{language}-orange)")
        
        return "\n".join(badges)
    
    def _generate_api_reference(self) -> str:
        """生成API参考"""
        project_type = self.project_data.get("project_type", "")
        
        if project_type in ["backend", "library"]:
            return """## 🔧 API参考

### 主要接口
- `GET /api/resource` - 获取资源列表
- `POST /api/resource` - 创建新资源
- `GET /api/resource/:id` - 获取单个资源
- `PUT /api/resource/:id` - 更新资源
- `DELETE /api/resource/:id` - 删除资源

### 使用示例
```javascript
// JavaScript示例
fetch('/api/resource')
  .then(response => response.json())
  .then(data => console.log(data));
```"""
        return ""
    
    def _generate_tests(self) -> str:
        """生成测试说明"""
        test_dirs = self.project_data.get("test_dirs", [])
        
        if test_dirs:
            return """## 🧪 测试

### 运行测试
```bash
npm test
```

### 测试覆盖率
```bash
npm run test:coverage
```

### 测试报告
测试报告将生成在 `coverage/` 目录中。"""
        return ""
    
    def _generate_deployment(self) -> str:
        """生成部署说明"""
        docker_files = self.project_data.get("docker_files", [])
        
        if docker_files:
            return """## 🚀 部署

### Docker部署
```bash
# 构建镜像
docker build -t myapp:latest .

# 运行容器
docker run -d -p 3000:3000 myapp:latest
```

### Docker Compose
```bash
docker-compose up -d
```"""
        return ""
    
    def _format_content(self, content: str) -> str:
        """格式化内容"""
        # 移除空章节
        sections = content.split('\n## ')
        formatted_sections = []
        
        for section in sections:
            if section.strip() and not section.startswith('## '):
                # 检查章节是否有实际内容（不只是标题）
                lines = section.split('\n')
                if len(lines) > 1 or (len(lines) == 1 and lines[0].strip() and not lines[0].startswith('#')):
                    formatted_sections.append(section)
        
        # 重新组合
        formatted_content = '\n## '.join(formatted_sections)
        
        # 确保以标题开头
        if not formatted_content.startswith('# '):
            formatted_content = f"# {self._get_project_name()}\n\n{formatted_content}"
        
        badges = self._generate_badges()
        if badges:
            lines = formatted_content.split('\n')
            if len(lines) > 1:
                # Workaround for type checker: insert badges between first and second lines
                lines_with_badges = [lines[0], '', badges, ''] + lines[1:]
                formatted_content = '\n'.join(lines_with_badges)
        
        return formatted_content.strip() + '\n'
    
    def _get_frontend_template(self) -> str:
        """前端项目模板"""
        return """{badges}

{project_description}

## 🚀 功能特性
{features}

{installation}

{usage}

{project_structure}

{configuration}

{api_reference}

{tests}

{development}

{deployment}

{contributing}

{license}

---
*最后更新：{current_date}*"""

    def _get_backend_template(self) -> str:
        """后端项目模板"""
        return """{badges}

{project_description}

## 🚀 功能特性
{features}

{installation}

{usage}

{project_structure}

{configuration}

{api_reference}

{tests}

{development}

{deployment}

{contributing}

{license}

---
*最后更新：{current_date}*"""

    def _get_fullstack_template(self) -> str:
        """全栈项目模板"""
        return """{badges}

{project_description}

## 🚀 功能特性
{features}

{installation}

{usage}

{project_structure}

{configuration}

{api_reference}

{tests}

{development}

{deployment}

{contributing}

{license}

---
*最后更新：{current_date}*"""

    def _get_library_template(self) -> str:
        """库项目模板"""
        return """{badges}

{project_description}

## 🚀 功能特性
{features}

{installation}

{usage}

{api_reference}

{tests}

{development}

{contributing}

{license}

---
*最后更新：{current_date}*"""

    def _get_tool_template(self) -> str:
        """工具项目模板"""
        return """{badges}

{project_description}

## 🚀 功能特性
{features}

{installation}

{usage}

{configuration}

{development}

{contributing}

{license}

---
*最后更新：{current_date}*"""

    def _get_default_template(self) -> str:
        """默认模板"""
        return """{badges}

{project_description}

## 🚀 功能特性
{features}

{installation}

{usage}

{project_structure}

{configuration}

{development}

{contributing}

{license}

---
*最后更新：{current_date}*"""

def update_existing_readme(readme_path: Path, new_content: str) -> str:
    """更新现有的README.md文件"""
    if not readme_path.exists():
        return new_content
    
    try:
        with open(readme_path, 'r', encoding='utf-8') as f:
            existing_content = f.read()
        
        # 保留用户自定义的内容
        # 这里可以添加更智能的合并逻辑
        # 目前简单返回新内容，实际使用时应该更智能
        
        return new_content
    except:
        return new_content

def main():
    """主函数"""
    import argparse
    
    parser = argparse.ArgumentParser(description='生成README.md文件')
    parser.add_argument('--project-data', required=True, help='项目分析数据JSON文件')
    parser.add_argument('--output', default='README.md', help='输出文件路径')
    parser.add_argument('--update', action='store_true', help='更新现有README.md')
    
    args = parser.parse_args()
    
    # 加载项目数据
    try:
        with open(args.project_data, 'r', encoding='utf-8') as f:
            project_data = json.load(f)
    except FileNotFoundError:
        print(f"❌ 找不到项目数据文件: {args.project_data}")
        return
    except json.JSONDecodeError:
        print(f"❌ 项目数据文件格式错误: {args.project_data}")
        return
    
    # 生成README
    output_dir = Path(args.output).parent
    generator = ReadmeGenerator(project_data, str(output_dir))
    new_content = generator.generate()
    
    # 处理输出
    output_path = Path(args.output)
    
    if args.update and output_path.exists():
        final_content = update_existing_readme(output_path, new_content)
    else:
        final_content = new_content
    
    # 写入文件
    try:
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(final_content)
        
        print(f"✅ README.md 已生成: {output_path}")
        print(f"📏 文件大小: {len(final_content)} 字符")
        
    except Exception as e:
        print(f"❌ 写入文件失败: {e}")

if __name__ == '__main__':
    main()