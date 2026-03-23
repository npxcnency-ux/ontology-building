# Ontology Building Project

## 项目概述

本项目包含一个 Claude Code Skill（`ontology-builder`），用于通过交互式对话引导用户构建 Palantir 本体配置。

## 项目结构

```
ontology-building/
├── ontology-builder/          # Skill 源码（生产版本）
│   ├── SKILL.md               # Skill 主文件（~355行）
│   ├── references/            # 参考指南（8个）
│   ├── assets/                # 模板资源
│   ├── examples/              # 完整示例
│   └── evals/                 # 评估用例
├── references/                # 学习资料（ADK设计模式、最佳实践）
├── docs/superpowers/          # 历史设计文档（specs/plans）
├── README.md                  # 项目 README
└── CLAUDE.md                  # 本文件
```

## 部署位置

- **Skill 源码**: `ontology-building/ontology-builder/`
- **Skill 部署**: `~/.claude/skills/ontology-builder/`（从源码复制）
- **评估工作区**: `~/.claude/skills/ontology-builder-workspace/`（不在 git 中）

修改 skill 时，编辑 `~/.claude/skills/ontology-builder/` 中的文件，测试通过后用 `cp` 同步回 repo。

## Skill 核心设计

### 五阶段引导流程
1. 理解业务场景与对象全景
2. 定义数据字段（Property）与对象关联（Link）
3. 定义计算规则（Function）
4. 定义操作按钮（Action）
5. 定义自动化规则（Automation）

### 质量门禁
- P0（阻断级）: 9项，必须全部通过
- P1（警告级）: 12项，强烈建议修复
- P2（建议级）: 4项，可选优化
- 总计 25 项检查

### 关键设计决策

- **workflow 步骤类型区分**: `callFunction` 仅用于调用已定义的 Function；数据查询/聚合使用 `type: query`。这是 v1.3.0 的核心修复，防止定时 Automation 生成幽灵函数引用
- **交叉引用完整性**: 生成 YAML 前构建三张清单（Property/Action/Function apiName），逐条比对确保无悬空引用
- **多对象支持**: 核心对象完整配置 + 关联对象骨架配置，YAML 使用 `objectTypes:` 数组格式

## Benchmark 评估

使用 skill-creator 框架进行迭代评估，当前 3 个测试场景（会议室管理、供应商管理、设备巡检），共 57 个 assertions。

### 当前结果（iteration-5, v1.3.0）
- meeting-room-simple: 18/18 (100%)
- supplier-management: 19/19 (100%)
- equipment-inspection: 20/20 (100%)

## 编码规范

- YAML 中所有 `apiName` 使用 camelCase
- 中文 `displayName` 使用业务术语
- 对话中使用业务语言替代技术术语（Property→数据字段, Function→计算规则 等）
