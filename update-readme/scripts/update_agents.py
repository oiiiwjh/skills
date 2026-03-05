#!/usr/bin/env python3
"""
AGENTS.md 更新工具
更新或创建AGENTS.md文档
"""

import os
import json
import sys
import yaml
import re
from pathlib import Path
from typing import Dict, List, Optional, Any
from datetime import datetime

class AgentsUpdater:
    """AGENTS.md更新器"""
    
    def __init__(self, project_data: Dict[str, Any], output_dir: str = "."):
        self.project_data = project_data
        self.output_dir = Path(output_dir).resolve()
        self.agent_configs = self._detect_agent_configs()
    
    def _detect_agent_configs(self) -> Dict[str, Any]:
        """检测代理配置"""
        configs = {
            "agents": {},
            "global": {},
            "files": []
        }
        
        # 查找代理配置文件
        agent_config_patterns = [
            ".agentrc",
            "agent.config.*",
            ".agents",
            "agents.json",
            "agents.yml",
            "agents.yaml"
        ]
        
        for pattern in agent_config_patterns:
            for file_path in self.output_dir.glob(pattern):
                if file_path.is_file():
                    configs["files"].append(str(file_path.relative_to(self.output_dir)))
                    
                    # 尝试读取配置
                    try:
                        content = self._read_config_file(file_path)
                        if content:
                            configs["agents"].update(self._extract_agent_info(content, file_path.suffix))
                    except:
                        pass
        
        # 检查package.json中的代理配置
        package_json_path = self.output_dir / "package.json"
        if package_json_path.exists():
            try:
                with open(package_json_path, 'r') as f:
                    package_data = json.load(f)
                
                # 检查scripts中的代理命令
                scripts = package_data.get("scripts", {})
                agent_scripts = {k: v for k, v in scripts.items() if "agent" in k.lower()}
                if agent_scripts:
                    configs["agents"]["npm_scripts"] = agent_scripts
                    
            except (json.JSONDecodeError, FileNotFoundError):
                pass
        
        return configs
    
    def _read_config_file(self, file_path: Path) -> Optional[Dict]:
        """读取配置文件"""
        suffix = file_path.suffix.lower()
        
        try:
            if suffix == '.json':
                with open(file_path, 'r') as f:
                    return json.load(f)
            elif suffix in ['.yml', '.yaml']:
                with open(file_path, 'r') as f:
                    return yaml.safe_load(f)
            elif suffix == '.js':
                # 简单解析JavaScript配置文件
                with open(file_path, 'r') as f:
                    content = f.read()
                
                # 提取module.exports的内容
                match = re.search(r'module\.exports\s*=\s*({[^}]+})', content, re.DOTALL)
                if match:
                    # 简单转换，实际应该使用更复杂的解析
                    config_str = match.group(1)
                    config_str = config_str.replace("'", '"')
                    try:
                        return json.loads(config_str)
                    except:
                        pass
        except:
            pass
        
        return None
    
    def _extract_agent_info(self, config: Dict, file_type: str) -> Dict:
        """从配置中提取代理信息"""
        agents = {}
        
        if isinstance(config, dict):
            # 检查常见的代理配置结构
            if "agents" in config:
                agents.update(config["agents"])
            
            # 检查顶层代理配置
            agent_keys = [k for k in config.keys() if "agent" in k.lower()]
            for key in agent_keys:
                if isinstance(config[key], dict):
                    agents[key] = config[key]
        
        return agents
    
    def generate(self) -> str:
        """生成AGENTS.md内容"""
        template = self._get_template()
        content = self._populate_template(template)
        return content
    
    def _get_template(self) -> str:
        """获取模板"""
        return """# AI 代理配置文档

## 概述

本文档记录项目中使用的AI代理配置、使用方法和最佳实践。

{badges}

## 可用代理

{agents_list}

## 配置说明

{configuration}

## 使用示例

{usage_examples}

## 最佳实践

{best_practices}

## 故障排除

{troubleshooting}

## 更新和维护

{maintenance}

---
*本文档最后更新于：{current_date}*  
*基于项目分析和实际配置生成*"""
    
    def _populate_template(self, template: str) -> str:
        """填充模板"""
        variables = {
            "badges": self._generate_badges(),
            "agents_list": self._generate_agents_list(),
            "configuration": self._generate_configuration(),
            "usage_examples": self._generate_usage_examples(),
            "best_practices": self._generate_best_practices(),
            "troubleshooting": self._generate_troubleshooting(),
            "maintenance": self._generate_maintenance(),
            "current_date": datetime.now().strftime("%Y-%m-%d")
        }
        
        content = template
        for key, value in variables.items():
            placeholder = f"{{{key}}}"
            content = content.replace(placeholder, value)
        
        return content
    
    def _generate_badges(self) -> str:
        """生成徽章"""
        badges = [
            "![文档状态](https://img.shields.io/badge/文档-已配置-green)",
            "![代理数量](https://img.shields.io/badge/代理-{count}-blue)".format(
                count=len(self.agent_configs.get("agents", {}))
            )
        ]
        
        if self.agent_configs["files"]:
            badges.append("![配置文件](https://img.shields.io/badge/配置文件-{count}-orange)".format(
                count=len(self.agent_configs["files"])
            ))
        
        return "\n".join(badges) + "\n"
    
    def _generate_agents_list(self) -> str:
        """生成代理列表"""
        agents = self.agent_configs.get("agents", {})
        
        if not agents:
            return "当前项目中没有检测到特定的AI代理配置。\n\n如需配置代理，请参考项目文档。"
        
        agent_list = []
        
        # 标准代理
        standard_agents = {
            "explore": "代码库探索专家 - 快速探索代码库结构、查找模式",
            "librarian": "文档搜索专家 - 搜索外部文档、库文档、最佳实践",
            "oracle": "架构设计和调试专家 - 复杂问题解决、架构设计",
            "frontend-ui-ux-engineer": "前端UI/UX专家 - 界面设计、用户体验优化",
            "document-writer": "技术文档编写专家 - 编写技术文档、API文档"
        }
        
        # 添加标准代理
        for agent_id, description in standard_agents.items():
            if agent_id in agents or any(agent_id in key.lower() for key in agents.keys()):
                status = "✅ 已配置"
            else:
                status = "⚪ 可用"
            
            agent_list.append(f"- **{agent_id}** - {description} ({status})")
        
        # 添加自定义代理
        custom_agents = {}
        for agent_key, config in agents.items():
            if agent_key not in standard_agents and not agent_key.startswith("_"):
                if isinstance(config, dict):
                    description = config.get("description", "自定义代理")
                else:
                    description = "自定义代理"
                
                custom_agents[agent_key] = description
        
        if custom_agents:
            agent_list.append("\n### 自定义代理")
            for agent_id, description in custom_agents.items():
                agent_list.append(f"- **{agent_id}** - {description}")
        
        return "\n".join(agent_list)
    
    def _generate_configuration(self) -> str:
        """生成配置说明"""
        config_files = self.agent_configs.get("files", [])
        
        if not config_files:
            return """### 基础配置

项目当前没有检测到特定的代理配置文件。您可以创建以下配置文件：

#### .agentrc (JSON格式)
```json
{
  "agents": {
    "explore": {
      "enabled": true,
      "timeout": 180000
    },
    "librarian": {
      "enabled": true,
      "sources": ["official_docs", "github"]
    }
  }
}
```

#### agent.config.js (JavaScript格式)
```javascript
module.exports = {
  agents: {
    explore: {
      enabled: true,
      filePatterns: ['**/*.{js,ts,jsx,tsx}']
    }
  }
};
```"""
        
        config_sections = []
        
        for config_file in config_files:
            file_path = self.output_dir / config_file
            if file_path.exists():
                try:
                    content = file_path.read_text(encoding='utf-8')
                    
                    # 根据文件类型格式化
                    if config_file.endswith('.json'):
                        config_sections.append(f"""### {config_file}

```json
{content}
```""")
                    elif config_file.endswith(('.yml', '.yaml')):
                        config_sections.append(f"""### {config_file}

```yaml
{content}
```""")
                    elif config_file.endswith('.js'):
                        config_sections.append(f"""### {config_file}

```javascript
{content}
```""")
                    else:
                        config_sections.append(f"""### {config_file}

```
{content}
```""")
                        
                except:
                    config_sections.append(f"""### {config_file}

*(无法读取文件内容)*""")
        
        return "### 配置文件\n\n" + "\n\n".join(config_sections)
    
    def _generate_usage_examples(self) -> str:
        """生成使用示例"""
        agents = self.agent_configs.get("agents", {})
        
        examples = []
        
        # 根据检测到的代理生成示例
        if any("explore" in key.lower() for key in agents.keys()):
            examples.append("""### 代码库探索
```bash
# 探索项目结构
/explore "分析项目的目录结构"

# 查找特定代码模式
/explore "查找所有使用React hooks的组件"

# 分析设计模式
/explore "检查项目的错误处理模式"
```""")
        
        if any("librarian" in key.lower() for key in agents.keys()):
            examples.append("""### 文档搜索
```bash
# 搜索库文档
/librarian "查找Express.js中间件的最佳实践"

# 搜索API文档
/librarian "React useEffect的完整API文档"

# 解决技术问题
/librarian "如何优化大型React应用的性能"
```""")
        
        if any("oracle" in key.lower() for key in agents.keys()):
            examples.append("""### 复杂问题解决
```bash
# 架构设计
/oracle "设计一个可扩展的微服务架构"

# 问题调试
/oracle "分析这个内存泄漏问题"

# 性能优化
/oracle "优化数据库查询性能"
```""")
        
        if not examples:
            examples.append("""### 基本使用示例
```bash
# 使用explore代理探索代码
/explore "显示项目的主要模块"

# 使用librarian搜索文档
/librarian "查找项目相关的最佳实践"

# 使用oracle解决复杂问题
/oracle "分析项目的架构设计"
```""")
        
        return "\n\n".join(examples)
    
    def _generate_best_practices(self) -> str:
        """生成最佳实践"""
        return """### 代理选择指南

| 任务类型 | 推荐代理 | 说明 |
|---------|----------|------|
| 代码探索 | `explore` | 快速了解代码结构、查找模式 |
| 文档搜索 | `librarian` | 搜索外部文档、API参考、最佳实践 |
| 复杂问题 | `oracle` | 架构设计、深度调试、性能优化 |
| 界面设计 | `frontend-ui-ux-engineer` | UI/UX优化、样式调整、响应式设计 |
| 文档编写 | `document-writer` | 技术文档、API文档、用户指南 |

### 性能优化建议

1. **缓存结果**：代理结果可以缓存以提高性能
2. **批量请求**：将多个相关请求合并处理
3. **明确查询**：提供具体的查询条件以获得更准确的结果
4. **限制范围**：指定搜索范围以减少处理时间

### 安全考虑

- 避免在查询中包含敏感信息（API密钥、密码等）
- 验证代理返回的结果
- 定期更新代理配置和知识库"""
    
    def _generate_troubleshooting(self) -> str:
        """生成故障排除"""
        return """### 常见问题

#### 1. 代理无响应
**症状**：代理调用超时或无响应
**解决方案**：
```bash
# 检查代理状态
检查网络连接和代理服务状态

# 减少查询复杂度
简化查询语句，提供更具体的上下文
```

#### 2. 结果不准确
**症状**：代理返回的结果不相关或不准确
**解决方案**：
```bash
# 优化查询
# 不好：模糊查询
/explore "代码"

# 好：具体查询
/explore "查找用户认证相关的React组件"

# 添加更多上下文
提供项目类型、技术栈等背景信息
```

#### 3. 性能问题
**症状**：代理响应慢
**解决方案**：
- 启用缓存机制
- 减少并发请求数量
- 优化查询语句

### 调试方法

```bash
# 查看代理日志（如果可用）
检查代理服务的日志输出

# 简化测试
使用最简单的查询测试代理功能

# 逐步排查
从基础功能开始，逐步增加复杂度
```"""
    
    def _generate_maintenance(self) -> str:
        """生成维护指南"""
        config_files = self.agent_configs.get("files", [])
        
        maintenance = """### 定期维护任务

1. **每月检查**：验证代理配置的准确性
2. **季度更新**：更新代理知识和最佳实践
3. **版本同步**：确保代理版本与项目需求匹配

### 配置备份

```bash
# 备份配置文件
cp .agentrc .agentrc.backup
cp agent.config.js agent.config.js.backup

# 恢复配置
cp .agentrc.backup .agentrc
```"""
        
        if config_files:
            file_list = "\n".join([f"- `{file}`" for file in config_files])
            maintenance += f"""

### 当前配置文件
{file_list}

请定期检查这些文件的更新和维护。"""
        
        return maintenance
    
    def update_existing(self, existing_content: str) -> str:
        """更新现有内容"""
        # 简单的更新策略：替换整个文档
        # 实际使用时可以实现更智能的合并
        
        new_content = self.generate()
        
        # 检查是否需要保留某些用户自定义内容
        # 这里可以添加更复杂的合并逻辑
        
        return new_content

def main():
    """主函数"""
    import argparse
    
    parser = argparse.ArgumentParser(description='更新AGENTS.md文档')
    parser.add_argument('--project-data', help='项目分析数据JSON文件')
    parser.add_argument('--output', default='AGENTS.md', help='输出文件路径')
    parser.add_argument('--update', action='store_true', help='更新现有文件')
    parser.add_argument('--json', action='store_true', help='以JSON输出执行结果')
    
    try:
        args = parser.parse_args()
    except SystemExit as exc:
        code = int(str(exc) or 0)
        return 2 if code != 0 else 0
    
    # 加载项目数据
    project_data = {}
    if args.project_data:
        try:
            with open(args.project_data, 'r', encoding='utf-8') as f:
                project_data = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            if args.json:
                print(
                    json.dumps(
                        {"status": "warning", "warning": "无法加载项目数据，使用默认配置"},
                        ensure_ascii=False,
                    ),
                    file=sys.stderr,
                )
            else:
                print(f"⚠️  无法加载项目数据，使用默认配置")
    
    # 创建更新器
    output_dir = Path(args.output).parent
    updater = AgentsUpdater(project_data, str(output_dir))
    
    # 生成内容
    output_path = Path(args.output)
    
    if args.update and output_path.exists():
        try:
            with open(output_path, 'r', encoding='utf-8') as f:
                existing_content = f.read()
            
            new_content = updater.update_existing(existing_content)
        except:
            new_content = updater.generate()
    else:
        new_content = updater.generate()
    
    # 写入文件
    try:
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(new_content)

        agent_count = len(updater.agent_configs.get("agents", {}))
        config_count = len(updater.agent_configs.get("files", []))

        result = {
            "status": "ok",
            "output": str(output_path),
            "agent_count": agent_count,
            "config_count": config_count,
        }
        if args.json:
            print(json.dumps(result, ensure_ascii=False))
        else:
            print(f"✅ AGENTS.md 已更新: {output_path}")
            print(f"📊 统计:")
            print(f"   检测到代理配置: {agent_count} 个")
            print(f"   配置文件: {config_count} 个")
        return 0
    except Exception as e:
        if args.json:
            print(json.dumps({"status": "error", "error": str(e)}, ensure_ascii=False), file=sys.stderr)
        else:
            print(f"❌ 写入文件失败: {e}", file=sys.stderr)
        return 1

if __name__ == '__main__':
    sys.exit(main())
