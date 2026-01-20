# Java 面试八股 Obsidian 笔记生成器

这是一个本地 Skill 模板，用于生成高质量、结构化的 Obsidian 风格 Java 面试笔记。

## 目录结构
- `skill.yaml`: Skill 元信息与配置
- `prompt/`: 核心 Prompt 模板
  - `system.md`: 系统角色定义
  - `instruction.md`: 输出规则与格式要求
  - `user_input_template.md`: 用户输入模板
  - `output_note_template.md`: 输出 Markdown 骨架
- `examples/`: 示例文件

## 使用方法
1. 打开 `prompt/user_input_template.md`，修改 `{topic}` 等参数。
2. 复制以下三个文件的内容（按顺序）：
   - `prompt/system.md`
   - `prompt/instruction.md`
   - `prompt/user_input_template.md`
3. 发给 AI，获取生成的 Markdown 笔记。
