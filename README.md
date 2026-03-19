# Ontology Building Project

这是一个企业级本体构建工具集项目，专注于帮助非技术人员通过友好的交互式对话，将业务概念转化为结构化的本体配置。

## 📦 项目内容

### Ontology Builder Skill
一个面向企业白领的交互式本体构建 Claude Code Skill，通过5阶段渐进式引导，帮助用户构建完整的 Palantir 本体配置。

**核心特点：**
- 🗣️ 对话式交互，无需技术背景
- 📚 渐进式引导，分5个阶段逐步构建
- 🎯 使用业务语言，避免技术术语
- 📋 双输出：YAML技术配置 + Markdown业务文档
- 💡 内置真实业务场景示例

**详细文档：** 查看 [`ontology-builder/README.md`](./ontology-builder/README.md)

## 🚀 快速开始

### 安装 Skill
```bash
# 复制 skill 到 Claude Code skills 目录
cp -r ontology-builder ~/.claude/skills/

# 使用 skill
/ontology-builder
```

### 适用场景
- ✅ 为业务对象建模（设备、供应商、订单、客户等）
- ✅ 配置自动化业务流程（异常响应、审批流程、定时任务）
- ✅ 生成符合 Palantir 标准的本体配置文件
- ✅ 需要通过对话而非复杂表单完成配置

## 📂 项目结构

```
ontology-building/
│
├── ontology-builder/                  # Ontology Builder Skill（生产就绪）
│   ├── SKILL.md                       # Skill 主文件（294行）
│   ├── README.md                      # Skill 详细文档
│   ├── references/                    # 参考指南（6个）
│   │   ├── property-guide.md          # 数据字段指南（270行）
│   │   ├── function-guide.md          # 计算规则指南（300行）
│   │   ├── action-guide.md            # 操作按钮指南（400行）
│   │   ├── automation-guide.md        # 自动化规则指南（450行）
│   │   ├── gotchas.md                 # 常见陷阱（600行，19个）
│   │   └── stage-guide.md             # 详细引导问题（320行）
│   ├── assets/                        # 模板资源
│   │   ├── ontology-template.yaml     # YAML配置模板
│   │   └── documentation-template.md  # 文档模板
│   └── examples/                      # 完整示例
│       └── equipment-monitoring-example.md  # 设备监控示例（500行）
│
├── docs/                              # 项目文档
│   ├── TESTING.md                     # TDD测试文档（697行）
│   ├── VERIFICATION.md                # 验证清单（240行）
│   └── CLEANUP_REPORT.md              # 目录结构优化报告
│
├── references/                        # 学习资料
│   ├── 内部创建本体最佳实践.md          # 原始需求文档
│   ├── 5 Agent Skill design patterns... # ADK设计模式
│   └── Lessons from Building Claude...  # Anthropic最佳实践
│
├── README.md                          # 项目概览（本文件）
├── CLAUDE.md                          # 项目记忆和设计决策（678行）
├── PROJECT_COMPLETION_REPORT.md       # 项目完成报告
└── .gitignore                         # Git忽略配置
```

## 🎯 设计原则

本项目基于三个最佳实践：

1. **Palantir 本体四要素**
   - Property（数据字段）→ Function（计算规则）→ Action（操作按钮）→ Automation（自动化规则）

2. **Claude Code Skill 最佳实践**
   - 渐进式资料加载
   - Gotchas 驱动（19个常见陷阱预防）
   - 内置完整示例

3. **ADK 设计模式**
   - Inversion（先理解用户需求）+ Pipeline（强制完整流程）

## 📊 项目统计

| 指标 | 数值 |
|------|------|
| 总代码量 | 3,586 行 |
| 核心文件数 | 11 个 |
| 参考指南 | 5 个（1,620 行）|
| 完整示例 | 1 个（设备监控，500 行）|
| 覆盖陷阱 | 19 个 |

## 🎓 学习路径

### 新手入门
1. 阅读本 README 了解项目概览
2. 查看 [`ontology-builder/README.md`](./ontology-builder/README.md) 了解 skill 使用方法
3. 学习 [`ontology-builder/examples/equipment-monitoring-example.md`](./ontology-builder/examples/equipment-monitoring-example.md) 完整示例
4. 阅读 [`ontology-builder/references/gotchas.md`](./ontology-builder/references/gotchas.md) 避免常见错误

### 进阶学习
- 研究 `CLAUDE.md` 了解设计决策和经验教训
- 深入阅读 `ontology-builder/references/` 中的各个指南掌握高级特性
- 查看 `docs/TESTING.md` 了解TDD测试方法论

### 开发者参考
- `docs/` - 项目文档（TDD测试、验证清单、优化报告）
- `references/` - 学习资料（最佳实践、设计模式）
- `PROJECT_COMPLETION_REPORT.md` - 完整的项目总结

## ⚠️ 常见陷阱（Top 5）

1. **一开始就追求完美** → 先做 MVP，再迭代
2. **混淆 Property 和 Function** → 能自动计算的用 Function
3. **Automation 没有限流** → 必须设置冷却期
4. **Action 缺少前置条件** → 每个 Action 都要明确执行条件
5. **字段命名不清晰** → 使用业务语言，包含单位

## 🔄 版本信息

- **当前版本**: 1.0.0
- **最后更新**: 2026-03-19
- **维护团队**: Ontology Team

## 📝 License

Internal Use Only - Anthropic

## 🤝 贡献指南

查看 [`ontology-builder/README.md`](./ontology-builder/README.md) 的贡献部分。

---

**快速链接：**
- [Skill 详细文档](./ontology-builder/README.md)
- [项目设计决策](./CLAUDE.md)
- [项目完成报告](./PROJECT_COMPLETION_REPORT.md)
- [完整示例](./ontology-builder/examples/equipment-monitoring-example.md)
- [常见陷阱](./ontology-builder/references/gotchas.md)
- [TDD测试文档](./docs/TESTING.md)
- [学习资料](./references/)