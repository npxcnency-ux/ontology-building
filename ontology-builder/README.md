# Ontology Builder - 企业本体构建助手

一个 Claude Code Skill，帮助非技术人员通过交互式对话将业务概念转化为 Palantir 本体配置。

## 核心特点

- **对话式交互**: 逐步提问引导，无需技术背景
- **5 阶段渐进引导**: 每阶段有检查点，确认后才进入下一阶段
- **业务语言**: 用"数据字段"、"计算规则"、"操作按钮"替代技术术语
- **三级质量门禁**: P0/P1/P2 共 25 项自动检查
- **多对象支持**: 核心对象完整配置 + 关联对象骨架
- **双输出**: YAML 技术配置 + Markdown 业务文档
- **交叉引用完整性**: 生成前自动校验所有 Function/Action/Property 引用

## Skill 结构

```
ontology-builder/
├── SKILL.md                          # 主文件（交互引导逻辑）
├── references/                       # 参考指南
│   ├── property-guide.md             # 数据字段类型
│   ├── function-guide.md             # 计算规则
│   ├── action-guide.md               # 操作按钮
│   ├── automation-guide.md           # 自动化规则
│   ├── links-guide.md                # 对象关联关系
│   ├── stage-guide.md                # 详细引导问题（Q1-Q19b）
│   ├── quality-check-guide.md        # 质量检查（25项）
│   └── gotchas.md                    # 常见陷阱（20个）
├── assets/                           # 模板资源
│   ├── ontology-template.yaml        # YAML 配置模板
│   └── documentation-template.md     # 文档模板
├── examples/                         # 完整示例
│   └── equipment-monitoring-example.md
└── evals/                            # 评估用例
    └── evals.json
```

## 五阶段构建流程

### 阶段一: 理解业务场景与对象全景
- 识别核心业务对象和关联对象
- 绘制对象全景图
- 确定建模优先级

### 阶段二: 定义数据字段与对象关联
- 固定信息、变化信息、历史追踪分类
- 数据来源（人工录入/外部同步/系统生成）
- 对象关联关系和级联行为

### 阶段三: 定义计算规则（Function）
- 风险判断、状态推断、业务计算
- Function 是只读的，不修改数据

### 阶段四: 定义操作按钮（Action）
- 创建/更新/删除/自定义操作
- 权限控制、前置条件、二次确认
- 回写到外部系统

### 阶段五: 定义自动化规则（Automation）
- 异常响应（事件驱动）
- 流程编排（Action 触发链）
- 定时任务（cron 调度）
- 限流保护和错误处理

### 输出阶段
- 交叉引用完整性校验
- 生成 `ontology-config.yaml` + `ontology-documentation.md`
- 三级质量门禁检查

## 使用方法

```bash
# 安装
cp -r ontology-builder ~/.claude/skills/

# 使用：直接描述业务场景
# "我们公司要管理会议室，想建一个系统来跟踪使用情况"
# "我是供应链经理，需要建一个供应商管理的本体"
```

### 触发关键词
本体建模、ontology、object type、业务对象、数据建模、配置生成、建模、Palantir 配置

## 质量检查

### P0（阻断级）- 9 项
- Property 数量 ≥ 3
- 定义了 primaryKey
- 至少 1 个 Action
- 每个 Action 有权限控制
- 高危 Action 有二次确认
- Automation 引用的 Function 存在（含 callFunction 步骤检查）
- Automation 引用的 Action 存在
- 无循环触发风险
- Precondition 引用的字段存在

### P1（警告级）- 12 项
数字字段含单位、必填字段 ≤ 7、业务语言命名、时序属性配置、Function 逻辑简洁、Automation 限流保护、Action 前置条件、Function 异常处理、Links 目标对象存在、核心对象有 Link、Function 只读纯度、外部调用错误处理

### P2（建议级）- 4 项
业务文档完整、元数据完整、Action 类型规范、Function 使用场景标记

## Benchmark

v1.3.0 在 3 个测试场景上达到 100% 通过率（57/57 assertions）：

| 场景 | 通过率 | 关键验证点 |
|------|--------|-----------|
| 会议室管理 | 18/18 | 基础场景，含定时统计报表 |
| 供应商管理 | 19/19 | 复杂场景，含评级 Function 和风险预警 |
| 设备巡检 | 20/20 | 多对象场景，含自动工单和通知 |

## 常见陷阱（Top 5）

1. **一开始就追求完美** → 先做 MVP 再迭代
2. **混淆 Property 和 Function** → 能自动计算的用 Function
3. **Automation 没有限流** → 必须设置冷却期
4. **Action 缺少前置条件** → 每个 Action 都要明确执行条件
5. **定时 Automation 用 callFunction 查询数据** → 数据查询用 `type: query`

详见 `references/gotchas.md`。

## 版本

**当前版本**: v1.3.0 (2026-03-23)

**最后更新**: 2026-03-23
