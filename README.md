# Ontology Building Project

企业级本体构建工具集，帮助非技术人员通过交互式对话将业务概念转化为结构化的 Palantir 本体配置。

## Ontology Builder Skill

一个 Claude Code Skill，通过 5 阶段渐进式引导构建完整的 Palantir 本体配置。

**核心特点：**
- 对话式交互，无需技术背景
- 5 阶段渐进引导，每阶段有检查点
- 使用业务语言，避免技术术语
- 三级质量门禁（P0/P1/P2，25 项检查）
- 双输出：YAML 技术配置 + Markdown 业务文档
- 多对象支持：核心对象完整配置 + 关联对象骨架
- 交叉引用完整性保证：无悬空 Function/Action/Property 引用

**详细文档：** [`ontology-builder/README.md`](./ontology-builder/README.md)

## 快速开始

```bash
# 复制 skill 到 Claude Code skills 目录
cp -r ontology-builder ~/.claude/skills/

# 在 Claude Code 中使用
# 直接描述业务场景即可触发，例如：
# "我们工厂有一套设备巡检流程，帮我建成本体配置"
```

## 适用场景

- 为业务对象建模（设备、供应商、订单、客户等）
- 配置自动化业务流程（异常响应、审批流程、定时任务）
- 生成符合 Palantir 标准的本体配置文件

## 项目结构

```
ontology-building/
├── ontology-builder/              # Skill 源码
│   ├── SKILL.md                   # Skill 主文件
│   ├── references/                # 参考指南（8个）
│   │   ├── property-guide.md      # 数据字段指南
│   │   ├── function-guide.md      # 计算规则指南
│   │   ├── action-guide.md        # 操作按钮指南
│   │   ├── automation-guide.md    # 自动化规则指南
│   │   ├── links-guide.md         # 对象关联关系指南
│   │   ├── stage-guide.md         # 详细引导问题（Q1-Q19b）
│   │   ├── quality-check-guide.md # 质量检查指南（25项）
│   │   └── gotchas.md             # 常见陷阱（20个）
│   ├── assets/                    # 模板资源
│   │   ├── ontology-template.yaml # YAML 配置模板
│   │   └── documentation-template.md
│   └── examples/                  # 完整示例
│       └── equipment-monitoring-example.md
├── references/                    # 学习资料
├── docs/                          # 设计文档
├── CLAUDE.md                      # 项目上下文
└── README.md                      # 本文件
```

## 设计原则

1. **Palantir 本体四要素**: Property → Function → Action → Automation
2. **Claude Code Skill 最佳实践**: 渐进式资料加载、Gotchas 驱动、内置示例
3. **ADK 设计模式**: Inversion（先理解需求）+ Pipeline（强制完整流程）

## 质量保障

### 三级自动门禁

| 级别 | 名称 | 检查项 | 行为 |
|------|------|--------|------|
| P0 | 阻断级 | 9 项 | 必须全部通过才能生成配置 |
| P1 | 警告级 | 12 项 | 警告但允许继续 |
| P2 | 建议级 | 4 项 | 仅提示优化建议 |

### Benchmark 评估结果（v1.3.0）

| 测试场景 | 通过率 | assertions |
|----------|--------|------------|
| 会议室管理 | 100% | 18/18 |
| 供应商管理 | 100% | 19/19 |
| 设备巡检 | 100% | 20/20 |

## 版本信息

### v1.3.0 (2026-03-23) - 当前版本

- 修复定时 Automation 的 callFunction 幽灵引用问题
- 区分 workflow 步骤类型：`callFunction`（调用已定义 Function）vs `query`（数据查询/聚合）
- 强化 P0-6 交叉引用检查，覆盖所有 Automation 类型
- Benchmark 全部 57 个 assertions 通过（3 场景 100%）

### v1.2.0 (2026-03-20)

- 新增 4 个引导问题（Q5b/Q7b/Q15b/Q19b）
- 新增质量检查项，P1 总数 8→12
- 阶段检查点升级为结构化表格
- 核心改进：质量检查"事后拦截"→引导问题"事前收集"

### v1.1.0 (2026-03-20)

- 三级自动门禁质量检查（P0/P1/P2）

### v1.0.0 (2026-03-19)

- 5 阶段交互式引导
- 完整参考指南（5个）
- 设备监控完整示例
- 双输出（YAML + Markdown）
