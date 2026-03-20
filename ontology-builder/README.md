# Ontology Builder - 企业本体构建助手

一个面向企业白领的交互式本体构建skill,帮助非技术人员通过友好的对话,将业务概念转化为Palantir平台可用的本体配置。

## ✨ 核心特点

- **🗣️ 对话式交互**: 通过逐步提问引导用户,无需技术背景
- **📚 渐进式引导**: 分5个阶段收集信息,每阶段都有检查点
- **🎯 业务语言**: 避免技术术语,使用"数据字段"、"计算规则"、"操作按钮"等易懂的表达
- **🔍 三级质量门禁**: P0/P1/P2三级自动检查（20项），确保配置质量 ← 新增 v1.1.0
- **📋 完整输出**: 生成YAML技术配置 + Markdown业务文档
- **💡 内置示例**: 包含设备监控等真实业务场景的完整示例

## 📂 Skill 结构

```
ontology-builder/
├── SKILL.md                          # 主skill文件 (交互式引导逻辑)
├── references/                       # 参考指南目录
│   ├── property-guide.md             # 数据字段类型指南
│   ├── function-guide.md             # 计算规则指南
│   ├── action-guide.md               # 操作按钮指南
│   ├── automation-guide.md           # 自动化规则指南
│   ├── quality-check-guide.md        # 质量检查指南 ← 新增 v1.1.0
│   └── gotchas.md                    # 常见问题与陷阱
├── assets/                           # 模板资源目录
│   ├── ontology-template.yaml        # YAML配置模板
│   └── documentation-template.md     # 文档模板
└── examples/                         # 完整示例目录
    └── equipment-monitoring-example.md  # 设备监控完整示例
```

## 🎯 设计原则

基于三个行业最佳实践:

1. **Palantir本体四要素**: Property → Function → Action → Automation
2. **Claude Code Skill最佳实践**: 渐进式资料加载、Gotchas驱动、内置例子
3. **ADK设计模式**: Inversion (先理解需求) + Pipeline (强制完整流程)

## 🚀 使用场景

适合以下情况:
- ✅ 企业白领需要为业务对象建模 (设备、供应商、订单等)
- ✅ 需要配置自动化业务流程 (异常响应、审批流程、定时任务)
- ✅ 希望通过对话式交互而非填写复杂表单
- ✅ 需要生成符合Palantir标准的配置文件

## 📖 五阶段构建流程

### 阶段一: 理解业务对象 (5分钟)
- 识别要管理的业务对象
- 理解业务场景和使用人员
- 🚫 用户确认前不进入下一阶段

### 阶段二: 定义数据字段 (10分钟)
- 确定需要记录的信息
- 分类: 固定信息、变化信息、历史追踪
- 自动推荐字段类型 (String/Integer/Date/Enum等)
- 🚫 用户确认前不进入下一阶段

### 阶段三: 定义计算规则 (10分钟)
- 确定自动判断逻辑 (风险判断、状态推断)
- 设计业务计算公式 (利用率、评分等)
- 提供常见模式参考
- 🚫 用户确认前不进入下一阶段

### 阶段四: 定义操作按钮 (10分钟)
- 设计用户可执行的操作
- 设置前置条件和权限控制
- 明确执行效果和二次确认
- 🚫 用户确认前不进入下一阶段

### 阶段五: 定义自动化规则 (15分钟)
- 设置异常响应规则
- 编排业务流程
- 配置定时任务
- 🚫 用户确认前不生成配置

### 输出阶段: 生成配置文件
- 生成 `ontology-config.yaml` (技术配置)
- 生成 `ontology-documentation.md` (业务说明)
- **自动质量检查**: 三级门禁（P0/P1/P2，20项检查） ← 新增 v1.1.0
  - **P0阻断级**: 8项必须通过（如权限控制、引用完整性）
  - **P1警告级**: 8项强烈建议（如限流配置、前置条件）
  - **P2建议级**: 4项可选优化（如元数据完整性）
- 提供部署检查清单

## 📝 生成的配置示例

**输入** (用户回答5个阶段的问题):
```
对象: 生产设备
场景: 实时监控设备温度,自动保护
关键字段: 设备编号、温度、状态
计算规则: 温度风险判断
操作: 紧急停机
自动化: 高温自动停机
```

**输出**:
1. **ontology-config.yaml** (200+ 行标准YAML)
2. **ontology-documentation.md** (包含配置说明、流程图、使用场景)

## 🎓 学习资源

### 新手入门
1. 先阅读 `examples/equipment-monitoring-example.md` 了解完整示例
2. 再阅读 `references/property-guide.md` 理解数据字段概念
3. 然后阅读 `references/gotchas.md` 避免常见错误

### 进阶指南
- `references/function-guide.md`: 学习三大类计算规则模式
- `references/action-guide.md`: 掌握四大类操作设计
- `references/automation-guide.md`: 理解事件驱动和流程编排
- `references/quality-check-guide.md`: 了解三级质量门禁体系 ← 新增 v1.1.0

## ⚠️ 常见陷阱 (Top 5)

1. **一开始就追求完美** → 应该先做MVP,再迭代
2. **混淆Property和Function** → 能自动计算的用Function
3. **Automation没有限流** → 必须设置冷却期避免频繁触发
4. **Action缺少前置条件** → 每个Action都要明确执行条件
5. **字段命名不清晰** → 使用业务语言,包含单位

详见 `references/gotchas.md` 的完整列表。

## 🧪 测试场景

skill已包含以下测试场景:

1. **设备监控场景** (examples/equipment-monitoring-example.md)
   - 12个Property (3个时序)
   - 3个Function
   - 5个Action
   - 4个Automation

可用于验证:
- ✅ 异常响应 (高温自动停机)
- ✅ 流程编排 (报废审批流程)
- ✅ 定时任务 (每日健康报告)

## 🔧 如何使用

### 在Claude Code中
```bash
# 安装skill
cp -r ontology-builder ~/.claude/skills/

# 使用skill
/ontology-builder
```

### 触发条件
当用户提到以下关键词时,skill会自动触发:
- "构建本体"
- "创建对象类型"
- "设计业务对象"
- "建模业务流程"
- "配置Palantir对象"

## 📊 设计模式

本skill采用 **Inversion + Pipeline** 混合模式:

```
Inversion (倒置模式):
  └─ Agent作为面试官,先收集用户需求
      └─ 避免盲目猜测,理解真实业务场景

Pipeline (流水线模式):
  └─ 强制执行5个阶段,每阶段有检查点
      └─ 确保本体四要素完整构建
          └─ Property → Function → Action → Automation
```

## 🎯 质量检查

输出前自动执行三级门禁检查（v1.1.0新增）:

### P0级（阻断级）- 必须通过
- ✅ 至少定义3个Property
- ✅ 至少定义1个Action
- ✅ 定义了primaryKey
- ✅ 每个Action有明确权限控制
- ✅ 高危Action有二次确认
- ✅ Automation引用的Function存在
- ✅ Automation引用的Action存在
- ✅ 无循环触发风险

### P1级（警告级）- 强烈建议
- ⚠️ 数字字段包含单位
- ⚠️ 必填字段 ≤ 7个
- ⚠️ 字段使用业务语言
- ⚠️ 明确时序属性配置
- ⚠️ Function逻辑 < 100行
- ⚠️ Automation有限流保护
- ⚠️ Action有前置条件
- ⚠️ Function有异常处理

### P2级（建议级）- 可选优化
- 💡 生成了业务文档
- 💡 填写了完整元数据
- 💡 Action类型规范
- 💡 Function有usageScenarios

**测试验证**: 已在4个真实配置上验证，成功拦截10个P0安全漏洞，识别75个P1问题和8个P2建议。

## 🔄 后续迭代建议

1. **优化检查规则** (v1.2.0计划):
   - 优化P1-1: 跳过计数类字段（`_count`、`_number`）
   - 优化P1-4: 跳过审计字段（`created_time`、`updated_time`）
   - 为高频P1问题提供修复模板

2. **增加更多行业示例**:
   - 供应链管理示例
   - 客户关系管理示例
   - 人力资源管理示例

3. **可视化支持**:
   - 生成流程图 (Mermaid格式)
   - 生成本体关系图

4. **验证增强**:
   - 完善循环Automation检测（深度优先搜索）
   - 检测权限冲突
   - 检测孤立的Function (定义了但从未使用)

## 📚 参考资料

- [Palantir Ontology SDK文档](https://www.palantir.com/docs/foundry/ontology/)
- [Claude Code Skills最佳实践](内部文档)
- [ADK设计模式](内部文档)

## 🤝 贡献

如果你发现新的常见错误或有改进建议:
1. 更新 `references/gotchas.md`
2. 在 `examples/` 添加新的业务场景
3. 提交PR并说明改进原因

## 📄 License

Internal Use Only - Anthropic

---

**最后更新**: 2026-03-20
**维护者**: Ontology Team
**版本**: 1.1.0

## 📝 更新日志

### v1.1.0 (2026-03-20)
- ✅ 新增三级自动门禁质量检查（P0/P1/P2，20项）
- ✅ 新增 `references/quality-check-guide.md`
- ✅ SKILL.md精简重构（469行 → 300行，-36%）
- ✅ 完成自动门禁测试验证（4个配置，75%通过率）

### v1.0.0 (2026-03-19)
- ✅ 5阶段交互式引导
- ✅ 完整的参考指南（5个）
- ✅ 设备监控完整示例
- ✅ 19个Gotchas覆盖
- ✅ 双输出（YAML + Markdown）
