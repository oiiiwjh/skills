# Humanizer Skill - 快速开始

## 已成功安装！

Humanizer skill 已安装到：`~/.config/opencode/skills/humanizer/`

## 立即使用

在 OpenCode 中直接使用：

### 方法1：命令方式
```
/humanizer [你的文本]
```

示例：
```
/humanizer 这个软件更新证明了公司对创新的承诺。此外，它提供了无缝、直观且强大的用户体验。
```

### 方法2：自然语言方式
```
请帮我人化这段文本：[你的文本]
```

示例：
```
请帮我人化这段文本：这项研究深入探讨了量子计算和机器学习之间复杂的相互作用。
```

## 测试示例

尝试这些测试命令：

1. **基础测试**：
```
/humanizer test: 这个应用程序展示了令人惊叹的功能，体现了创新精神。
```

2. **学术文本**：
```
/humanizer 这篇论文深入探讨了神经网络的复杂结构，强调了它们在人工智能发展中的关键作用。
```

3. **商务沟通**：
```
/humanizer 嗨团队！希望这能帮到你！😊 我们突破性的解决方案确保了最高效率和生产力。
```

## 高级选项

### 调整严格度
```
/humanizer --strictness high [文本]
```
- `low`: 宽松检测
- `medium`: 中等检测（默认）
- `high`: 严格检测

### 指定目标读者
```
/humanizer --audience business [文本]
```
- `general`: 通用（默认）
- `academic`: 学术
- `business`: 商务
- `casual`: 休闲
- `technical`: 技术

### 获取统计信息
```
/humanizer --stats [文本]
```

## 故障排除

### 如果skill不工作：
1. 确保文件在正确位置：`~/.config/opencode/skills/humanizer/skill.md`
2. 重启 OpenCode 会话
3. 检查是否有其他同名skill冲突

### 如果输出不满意：
尝试增加严格度：
```
/humanizer --strictness high [文本]
```

## 文件位置
- 主skill文件：`~/.config/opencode/skills/humanizer/skill.md`
- 实现代码：`~/.config/opencode/skills/humanizer/humanizer-implementation.js`
- 文档：`~/.config/opencode/skills/humanizer/README.md`

## 立即测试
运行测试验证安装：
```bash
cd ~/.config/opencode/skills/humanizer && node test.js
```

现在就可以开始使用了！🎉