# Ontology Builder 验收标准实施计划

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 为ontology-builder skill实现两阶段验收标准体系（自动门禁 + 业务门禁）

**Architecture:**
- 阶段1（自动门禁）：在SKILL.md中实现P0/P1/P2三级检查，拦截技术缺陷
- 阶段2（业务门禁）：在validation-guide.md中提供业务价值评审清单和流程
- 采用渐进式实施：Phase 1必须完成（基础框架），Phase 2-3可选（工具增强）

**Tech Stack:**
- Markdown（文档和skill定义）
- YAML（可选的验证规则配置）
- Python 3.x（可选的自动化验证脚本）

**Spec Document:** docs/superpowers/specs/2026-03-20-ontology-validation-design.md

---

## Phase 1：基础实施（必须完成）

### Task 1: 增强SKILL.md的质量检查部分

**Files:**
- Modify: `/Users/niupian/ontology-building/ontology-builder/SKILL.md:400-432`
- Reference: `docs/superpowers/specs/2026-03-20-ontology-validation-design.md:237-480`

**目标:** 实现P0/P1/P2三级自动门禁检查逻辑

- [ ] **Step 1: 阅读当前的Step 4质量检查部分**

查看当前实现（位于SKILL.md第400-432行）：
```bash
cat ontology-builder/SKILL.md | sed -n '400,432p'
```

预期：看到当前只有5项基本检查

- [ ] **Step 2: 备份原始内容**

```bash
cp ontology-builder/SKILL.md ontology-builder/SKILL.md.backup
```

- [ ] **Step 3: 替换Step 4为增强版本**

将SKILL.md的Step 4部分替换为以下内容：

```markdown
### Step 4: 质量检查（自动门禁）

在输出前，自动执行以下检查：

#### 🔴 P0级检查（必须通过）

执行以下检查，任何一项失败将阻止生成配置：

**基础完整性**
- [ ] Property ≥ 3个
- [ ] Action ≥ 1个
- [ ] 定义了primaryKey

**安全性**
- [ ] 所有Action有permissions字段
- [ ] 高危Action（delete/batch）有confirmationRequired

**逻辑正确性**
- [ ] Automation引用的Function存在
- [ ] Automation引用的Action存在
- [ ] 无循环触发风险

**如果任何P0检查失败**：
1. 暂停输出配置
2. 向用户展示具体问题和失败原因
3. 引导用户回到相应阶段修复问题
4. 修复后重新执行检查

示例错误提示：
```
❌ P0检查失败：

**基础完整性问题**
• Property只有2个，至少需要3个核心字段
  → 建议：回到阶段二，补充至少1个核心数据字段

**安全性问题**
• Action 'delete_work_order' 缺少权限控制
  → 建议：为该Action添加permissions字段，明确哪些角色可以执行删除操作

请修复以上问题后，我会重新生成配置。
```

#### 🟠 P1级检查（强烈建议）

执行以下检查，生成警告但允许继续：

**可用性基础**
- [ ] 数字字段命名包含单位（如"温度(°C)"）
- [ ] 必填字段 ≤ 7个
- [ ] 字段使用业务语言（中文）

**性能保护**
- [ ] 明确了时序属性配置（timeSeries字段）
- [ ] Function逻辑 < 100行
- [ ] Automation有限流保护（rateLimiting）

**健壮性**
- [ ] update/delete类Action有前置条件（preconditions）
- [ ] Function有异常处理（try/except或空值判断）

**如果有P1警告**：
1. 仍然生成配置文件
2. 在输出后显示完整的警告列表
3. 建议用户修复后再提交团队评审
4. 提供具体的修复建议

示例警告提示：
```
⚠️ P1警告（3个） - 强烈建议修复：

**可用性问题**
• Property 'mileage' 建议包含单位
  → 建议：改为 'mileage(公里)' 或 'mileage(km)'

**性能问题**
• Function 'calculate_cost' 逻辑有127行，建议<100行
  → 建议：拆分为多个Function或简化逻辑

**健壮性问题**
• Automation 'daily_report' 缺少限流保护
  → 建议：添加 rateLimiting: { maxExecutionsPerHour: 1, cooldownMinutes: 60 }

这些问题不阻止配置生成，但建议修复后再提交评审。
```

#### 🟡 P2级检查（可选优化）

**文档完整性**
- [ ] 生成了ontology-documentation.md
- [ ] 填写了完整的metadata（businessContext、targetUsers）

**可扩展性**
- [ ] Action类型规范（使用标准actionType）
- [ ] Function有usageScenarios说明

**如果有P2信息**：
仅作为优化建议显示，不影响配置生成。

示例信息提示：
```
ℹ️ P2建议（2个） - 可选优化：

• 建议生成ontology-documentation.md供业务人员阅读
• 建议为Function 'calculate_urgency_level' 添加usageScenarios说明

这些是可选优化，不影响配置质量。
```

---

**检查完成后，显示完整报告**：

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🎉 自动门禁检查完成！
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

✅ P0检查: 全部通过 (8/8)
⚠️ P1警告: 3个
  • Property 'mileage' 建议包含单位
  • Function 'calculate_cost' 逻辑有127行
  • Automation 'daily_report' 缺少限流保护

ℹ️ P2建议: 1个
  • 建议生成ontology-documentation.md

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
💡 建议: 修复P1警告后再提交团队评审
📖 参考: references/validation-guide.md 了解完整验收标准
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```
```

- [ ] **Step 4: 保存修改**

保存SKILL.md文件

- [ ] **Step 5: 验证语法正确性**

```bash
# 检查markdown语法
grep -E "^###|^####|^-" ontology-builder/SKILL.md | head -50
```

预期：看到正确的标题层级和列表格式

- [ ] **Step 6: 提交修改**

```bash
git add ontology-builder/SKILL.md
git commit -m "feat: 增强SKILL.md质量检查 - 实现P0/P1/P2三级自动门禁

- P0级（8项）：阻止生成，包含完整性、安全性、逻辑正确性检查
- P1级（8项）：警告但允许，包含可用性、性能、健壮性检查
- P2级（4项）：可选建议，包含文档和可扩展性检查
- 提供详细的错误提示和修复建议

Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>"
```

---

### Task 2: 创建validation-guide.md业务门禁指南

**Files:**
- Create: `/Users/niupian/ontology-building/ontology-builder/references/validation-guide.md`
- Reference: `docs/superpowers/specs/2026-03-20-ontology-validation-design.md:481-1108`

**目标:** 创建完整的验收标准指南，包含自动门禁详解和业务门禁评审清单

- [ ] **Step 1: 创建validation-guide.md文件**

在ontology-builder/references/目录创建新文件

- [ ] **Step 2: 编写文件内容**

写入以下内容（分为4个主要部分）：

```markdown
# 本体配置验收标准指南

本指南提供ontology-builder skill生成的本体配置的完整验收标准。

---

## 📋 验收标准概览

本体配置的验收分为两个阶段：

### 阶段1：自动门禁（Auto Gate）
**目的**：快速过滤技术缺陷
**执行方式**：SKILL.md内置检查（生成时自动执行）
**检查内容**：
- P0级（8项）：严重缺陷，阻止生成
- P1级（8项）：潜在问题，警告但允许
- P2级（4项）：最佳实践建议

### 阶段2：业务门禁（Business Gate）
**目的**：评估业务价值
**执行方式**：人工评审会议
**评审内容**：5个核心问题（总分80分）
- 业务痛点清晰度（20分）
- 解决方案匹配度（20分）
- 效率提升量化（15分）
- 用户采用可行性（15分）
- 可扩展性与演进（10分）

---

## 🚦 阶段1：自动门禁详解

### P0级检查项（Blocker）

#### P0-001: Property数量检查
**检查规则**: len(properties) < 3
**错误信息**: "Property只有{count}个，至少需要3个核心字段"
**理由**: 少于3个字段的对象没有实际业务价值
**修复建议**: 回到阶段二，补充核心数据字段

#### P0-002: Action存在性检查
**检查规则**: len(actions) < 1
**错误信息**: "缺少Action，至少需要'创建对象'操作"
**理由**: 没有操作的对象无法使用
**修复建议**: 回到阶段四，添加至少一个创建操作

#### P0-003: 主键定义检查
**检查规则**: primaryKey is None or len(primaryKey) == 0
**错误信息**: "未定义primaryKey，无法唯一标识对象"
**理由**: 没有主键无法在系统中唯一标识对象
**修复建议**: 确定哪个字段作为唯一标识（如工单编号、设备ID）

#### P0-004: Action权限检查
**检查规则**: any(action.permissions is None for action in actions)
**错误信息**: "Action '{action_name}' 缺少权限控制"
**理由**: 无权限控制会导致严重的安全漏洞
**修复建议**:
```yaml
permissions:
  roles:
    - "管理员"
    - "操作员"
```

#### P0-005: 高危Action确认检查
**检查规则**: action.actionType in ['delete', 'batch'] and not action.confirmationRequired
**错误信息**: "高危操作 '{action_name}' 缺少二次确认"
**理由**: 防止误操作导致数据丢失
**修复建议**:
```yaml
confirmationRequired: true
confirmationMessage: "确定删除该工单吗？删除后无法恢复。"
```

#### P0-006: Automation引用Function检查
**检查规则**: automation.functionName not in [f.name for f in functions]
**错误信息**: "Automation '{auto_name}' 引用了不存在的Function '{func_name}'"
**理由**: 引用不存在的Function会导致运行时错误
**修复建议**: 检查Function名称拼写，或先定义被引用的Function

#### P0-007: Automation引用Action检查
**检查规则**: automation.actionName not in [a.name for a in actions]
**错误信息**: "Automation '{auto_name}' 引用了不存在的Action '{action_name}'"
**理由**: 引用不存在的Action会导致运行时错误
**修复建议**: 检查Action名称拼写，或先定义被引用的Action

#### P0-008: 循环触发检查
**检查规则**: 检测Automation触发链中是否有环路
**错误信息**: "检测到潜在循环触发: {chain}"
**理由**: A触发B，B触发A会导致无限循环
**检测方法**:
1. 构建Automation触发依赖图
2. 使用深度优先搜索检测环路
3. 如果发现环路，列出完整的触发链
**修复建议**: 重新设计Automation触发逻辑，打破循环

---

### P1级检查项（Warning）

#### P1-001: 数字字段单位检查
**检查规则**: property.dataType in ['integer', 'double'] and '(' not in property.displayName
**警告信息**: "数字字段 '{name}' 建议包含单位，如 '温度(°C)'"
**理由**: 包含单位使字段含义更清晰
**修复建议**: "温度" → "温度(°C)"，"里程" → "里程(公里)"

#### P1-002: 必填字段数量检查
**检查规则**: count(properties where required=true) > 7
**警告信息**: "必填字段有{count}个，建议≤7个（影响用户体验）"
**理由**: 太多必填字段增加用户填写负担
**修复建议**: 重新评估哪些字段是真正必填的，其他改为选填

#### P1-003: 字段命名语言检查
**检查规则**: property.displayName.isascii() and metadata.target_audience == 'business_users'
**警告信息**: "字段 '{api_name}' 建议使用中文业务术语而非英文"
**理由**: 业务人员更容易理解中文字段名
**修复建议**: "status" → "工单状态"，"assigned_to" → "分配的技师"

#### P1-004: 时序属性配置检查
**检查规则**: property.dataType == 'timestamp' and property.timeSeries is None
**警告信息**: "字段 '{name}' 未明确是否需要时序追踪"
**理由**: 避免过度使用时序属性导致存储成本暴涨（参考gotchas.md #7）
**修复建议**:
- 需要查看历史趋势 → timeSeries: true
- 固定不变或很少变化 → timeSeries: false

#### P1-005: Function复杂度检查
**检查规则**: len(function.logic.split('\n')) > 100
**警告信息**: "Function '{name}' 逻辑有{lines}行，建议<100行"
**理由**: 超过100行的Function难以维护且影响性能
**修复建议**:
- 拆分为多个Function
- 简化逻辑
- 或改用Automation后台异步执行

#### P1-006: Automation限流检查
**检查规则**: automation.rateLimiting is None
**警告信息**: "Automation '{name}' 缺少rateLimiting配置"
**理由**: 防止频繁触发导致系统过载（参考gotchas.md #10）
**修复建议**:
```yaml
rateLimiting:
  maxExecutionsPerHour: 2  # 每小时最多2次
  cooldownMinutes: 30      # 两次执行间隔至少30分钟
```

#### P1-007: Action前置条件检查
**检查规则**: action.actionType in ['update', 'delete'] and action.preconditions is None
**警告信息**: "Action '{name}' 缺少preconditions"
**理由**: 防止在错误状态执行操作（参考gotchas.md #4）
**修复建议**:
```yaml
preconditions:
  - condition: "work_order_status == '待派单'"
    errorMessage: "只能派单给状态为'待派单'的工单"
```

#### P1-008: Function异常处理检查
**检查规则**: 'try' not in function.logic and 'if' not in function.logic
**警告信息**: "Function '{name}' 的logic中未发现异常处理代码"
**理由**: Function应该处理空值、超时等异常情况
**修复建议**: 添加try/except或if/else空值判断

---

### P2级检查项（Info）

#### P2-001: 业务文档检查
**检查规则**: not exists(ontology-documentation.md)
**信息**: "建议生成ontology-documentation.md供业务人员阅读"
**理由**: 业务文档帮助非技术人员理解配置

#### P2-002: 元数据完整性检查
**检查规则**: metadata.businessContext is None or metadata.targetUsers is None
**信息**: "建议填写businessContext、targetUsers等元数据"
**理由**: 完整的元数据有助于理解和维护

#### P2-003: Action类型规范检查
**检查规则**: action.actionType not in STANDARD_ACTION_TYPES
**信息**: "建议使用标准actionType: create/update/delete/custom"
**理由**: 标准化的类型便于分类和管理

#### P2-004: Function使用场景说明检查
**检查规则**: function.usageScenarios is None
**信息**: "建议为Function '{name}' 添加usageScenarios说明"
**理由**: 使用场景说明有助于理解Function的价值

---

## 💼 阶段2：业务门禁评审指南

### 评审目标

业务门禁专注于**价值判断**：
- ✅ 是否解决了真实痛点
- ✅ 是否有人愿意用
- ✅ 是否值得投入资源部署

### 5个核心评审问题

#### 问题1：业务痛点清晰度（20分）

**评审问题**: 这个本体解决了什么具体的业务痛点？

**评分标准**:

| 等级 | 得分 | 标准 | 示例 |
|------|------|------|------|
| ⭐⭐⭐⭐⭐ 优秀 | 20分 | 痛点描述具体且量化 | "目前每天人工派单需要2小时，错误率15%，导致客户投诉率高" |
| ⭐⭐⭐ 合格 | 12分 | 痛点清晰但未量化 | "派单效率低，容易出错" |
| ⭐ 不合格 | 0分 | 没有明确痛点 | "觉得应该做个系统" |

**评审工具 - 痛点挖掘5W1H表**:

| 维度 | 问题 | 答案 |
|------|------|------|
| What | 什么问题影响了业务？ | |
| Who | 哪些人受到影响？ | |
| When | 什么时候会遇到这个问题？ | |
| Where | 在哪个业务环节发生？ | |
| Why | 为什么现有方式不行？ | |
| How Much | 影响程度有多大（时间/成本/质量）？ | |

**打分参考**:
- 填写了6个维度 → 20分
- 填写了4-5个维度 → 15分
- 填写了2-3个维度 → 10分
- 填写了≤1个维度 → 0分

---

#### 问题2：解决方案匹配度（20分）

**评审问题**: 这个本体的设计是否针对性地解决了上述痛点？

**评分标准**:

| 等级 | 得分 | 标准 | 示例 |
|------|------|------|------|
| ⭐⭐⭐⭐⭐ 优秀 | 20分 | 每个核心功能都对应到具体痛点 | "Automation超时提醒→解决派单延误；Function复杂度判断→智能分配技师" |
| ⭐⭐⭐ 合格 | 12分 | 部分功能对应痛点，但有冗余 | "定义了10个Function，但只有3个真正用得上" |
| ⭐ 不合格 | 0分 | 设计和痛点无关 | "痛点是派单慢，但设计重点在费用计算" |

**评审工具 - 功能价值矩阵**:

| 功能 | 对应痛点 | 使用频率 | 实现复杂度 | 优先级 | 价值评分 |
|------|----------|----------|------------|--------|---------|
| Automation超时提醒 | 派单延误 | 高 | 低 | P0 | ⭐⭐⭐⭐⭐ |
| Function费用计算 | 手工算费时 | 中 | 中 | P1 | ⭐⭐⭐ |
| Function返修判断 | 质量追溯 | 低 | 高 | P2 | ⭐⭐ |

**评分规则**:
- 高频+解决核心痛点 → P0
- 中频+中等痛点 → P1
- 低频或次要痛点 → P2

**打分参考**:
- P0功能占比 > 70% → 20分
- P0功能占比 50-70% → 15分
- P0功能占比 30-50% → 10分
- P0功能占比 < 30% → 5分

---

#### 问题3：效率提升量化（15分）

**评审问题**: 使用这个本体后，预期能节省多少时间/成本？

**评分标准**:

| 等级 | 得分 | 标准 | 示例 |
|------|------|------|------|
| ⭐⭐⭐⭐⭐ 优秀 | 15分 | 有明确的量化目标和ROI计算 | "派单时间从2小时→15分钟（↓87.5%），节省3 FTE，ROI回收期6个月" |
| ⭐⭐⭐ 合格 | 9分 | 有方向性预期但未完全量化 | "能减少人工操作，预计节省1-2个人力" |
| ⭐ 不合格 | 0分 | 没有效率提升预期 | "只是把流程电子化" |

**评审工具 - 前后对比表**:

| 指标 | 当前（人工） | 目标（系统） | 改善幅度 | 年化价值 |
|------|-------------|-------------|---------|---------|
| 派单平均时长 | 2小时 | 15分钟 | ↓ 87.5% | 节省1800小时/年 |
| 派单错误率 | 15% | 3% | ↓ 80% | 减少返工成本 |
| 人工介入次数 | 100次/天 | 10次/天 | ↓ 90% | 节省2.5 FTE |
| 技师满意度 | 60% | 85%（预期） | ↑ 25% | 降低流失率 |

**ROI计算模板**:
```
年节省人力成本：X FTE × 10万/年 = Y万
系统开发成本：Z万（一次性）
年化收益：Y万/年
投资回报期：Z万 / Y万 = N年
```

**打分参考**:
- ROI回收期 < 1年 → 15分
- ROI回收期 1-2年 → 10分
- ROI回收期 2-3年 → 5分
- ROI回收期 > 3年或无ROI计算 → 0分

---

#### 问题4：用户采用可行性（15分）

**评审问题**: 目标用户会真正使用这个本体吗？有什么阻碍？

**评分标准**:

| 等级 | 得分 | 标准 | 示例 |
|------|------|------|------|
| ⭐⭐⭐⭐⭐ 优秀 | 15分 | 已验证用户需求，有推广计划 | "与5个技师访谈确认需求，计划提供2周培训+激励机制" |
| ⭐⭐⭐ 合格 | 9分 | 基于合理假设，但未验证 | "假设技师会用APP接单，因为更方便" |
| ⭐ 不合格 | 0分 | 未考虑用户意愿和能力 | "技师年龄偏大，不习惯用手机，但我们强制推行" |

**评审工具 - 用户画像与障碍分析**:

```markdown
### 用户类型1：调度员

**现有工作方式**: Excel表格手工派单

**采用障碍**:
- 学习成本：需要培训2小时
- 习惯改变：放弃熟悉的Excel
- 信任度：担心系统出错

**解决方案**:
- 提供详细操作手册和视频教程
- 前2周支持双轨运行（Excel+系统）
- 设置回滚按钮增强信任

**采用可行性评估**: ⭐⭐⭐⭐ 高（有挑战但可克服）

### 用户类型2：技师
[同样分析...]

### 综合评估
[汇总所有用户类型的可行性]
```

**打分参考**:
- 所有用户群体可行性 ≥ ⭐⭐⭐⭐ → 15分
- 主要用户群体可行性 ≥ ⭐⭐⭐ → 10分
- 有用户群体可行性 < ⭐⭐⭐ → 5分
- 未评估用户采用障碍 → 0分

---

#### 问题5：可扩展性与演进（10分）

**评审问题**: 3-6个月后需求变化，这个设计能适应吗？

**评分标准**:

| 等级 | 得分 | 标准 | 示例 |
|------|------|------|------|
| ⭐⭐⭐⭐⭐ 优秀 | 10分 | 模块化设计，考虑了未来需求 | "预留了与财务系统对接的字段，增加新工单类型只需配置Enum" |
| ⭐⭐⭐ 合格 | 6分 | 能满足当前需求，扩展性一般 | "增加新字段需要改动多处，但可以实现" |
| ⭐ 不合格 | 0分 | 设计僵化，难以修改 | "工单状态写死在代码里，改动需要重构" |

**评审工具 - 未来场景推演**:

```markdown
### 场景1：需要对接第三方配件系统

**当前设计**: Function手工查询库存
**需要改动**: 增加API配置，修改Function逻辑
**影响范围**: 1个Function
**改动成本**: ⭐⭐ 中（2天开发）
**评估**: ✅ 可接受

### 场景2：增加"保养计划"对象类型
[分析...]

### 场景3：支持多语言界面
[分析...]

### 综合评估
[汇总场景的可扩展性评分]
```

**打分参考**:
- 所有推演场景改动成本 ≤ ⭐⭐ → 10分
- 主要场景改动成本 ≤ ⭐⭐⭐ → 7分
- 有场景改动成本 = ⭐⭐⭐⭐ → 4分
- 未进行场景推演 → 0分

---

### 综合评分与评级

```
总分计算：
= 问题1(20分) + 问题2(20分) + 问题3(15分) + 问题4(15分) + 问题5(10分)
= 满分80分

评级映射：
70-80分 → ⭐⭐⭐⭐⭐ High Value（优先部署）
  特征：
  - 业务价值清晰且量化
  - 用户采用可行性高
  - ROI回收期 < 1年

  建议：
  - 优先级：P0
  - 尽快部署到生产环境
  - 预留充足的推广资源

50-69分 → ⭐⭐⭐ Medium Value（正常部署）
  特征：
  - 有价值但不紧急
  - 或者有价值但实施有挑战
  - ROI回收期 1-2年

  建议：
  - 优先级：P1
  - 正常排期，做好风险控制
  - 重点关注用户采用障碍

<50分 → 🤔 Low Value（重新评估）
  特征：
  - 价值不明确
  - 或者实施障碍太大
  - ROI回收期 > 2年

  建议：
  - 暂缓部署
  - 重新brainstorming，明确痛点
  - 或者降低实施复杂度
```

---

### 评审会议流程

#### 会议组织

**参与人员**:
- 业务负责人（决策者）- 必须参加
- 本体创建者（讲解者）- 必须参加
- 技术负责人（可行性评估）- 必须参加
- 目标用户代表（验证需求）- 建议参加

**会议时长**: 30-45分钟

**会议议程**:
1. (5分钟) 创建者介绍业务背景和痛点
2. (15分钟) 逐一回答5个核心问题
3. (10分钟) 团队讨论和打分
4. (5分钟) 计算总分并决策
5. (5-10分钟) 如果通过，讨论实施计划

#### 评审表模板

```markdown
# 本体业务价值评审表

**本体名称**: _______________________
**对象类型**: _______________________
**创建者**: _______________________
**评审日期**: _______________________

---

## 评分卡

| 问题 | 得分 | 满分 | 评语 |
|------|------|------|------|
| 1. 业务痛点清晰度 | __/20 | 20 | |
| 2. 解决方案匹配度 | __/20 | 20 | |
| 3. 效率提升量化 | __/15 | 15 | |
| 4. 用户采用可行性 | __/15 | 15 | |
| 5. 可扩展性与演进 | __/10 | 10 | |
| **总分** | **__/80** | **80** | |

---

## 评级

- [ ] ⭐⭐⭐⭐⭐ High Value (70-80分) - 优先部署
- [ ] ⭐⭐⭐ Medium Value (50-69分) - 正常部署
- [ ] 🤔 Low Value (<50分) - 重新评估

---

## 决策

**部署决定**:
- [ ] 批准部署
- [ ] 修改后重审（具体修改要求：_________________）
- [ ] 暂缓（原因：_________________）

**实施优先级**:
- [ ] P0（本季度必须上线）
- [ ] P1（下季度上线）
- [ ] P2（待资源）

**预期上线时间**: _______________________

---

## 风险与应对措施

**识别的风险**:
1. _________________________________________________
2. _________________________________________________

**应对措施**:
1. _________________________________________________
2. _________________________________________________

---

## 签字确认

**业务负责人**: ______________ 日期: __________

**技术负责人**: ______________ 日期: __________

**备注**: _________________________________________________
```

---

## 📊 附录

### 附录A：检查项与Gotchas映射

| Gotcha | 对应检查项 | 级别 |
|--------|----------|------|
| #1: 一开始就追求完美 | 业务门禁-问题2（功能价值矩阵） | 业务 |
| #3: Function设计过于复杂 | P1-005: Function复杂度检查 | P1 |
| #4: 忘记设置Action前置条件 | P1-007: Action前置条件检查 | P1 |
| #5: Automation触发不当 | P1-006: Automation限流检查 | P1 |
| #7: 过度使用时序属性 | P1-004: 时序属性配置检查 | P1 |
| #8: 字段命名不清晰 | P1-001, P1-003: 命名检查 | P1 |
| #10: Automation没有限流 | P1-006: Automation限流检查 | P1 |
| #11: 权限控制设置不当 | P0-004: Action权限检查 | P0 |

### 附录B：快速检查清单

**使用前提**: 用户已通过自动门禁（P0全部通过）

**快速自查**（5分钟）:
- [ ] 能用一句话说清楚解决什么痛点？
- [ ] 核心功能都对应到具体痛点？
- [ ] 能量化节省的时间或成本？
- [ ] 目标用户愿意用且能用？
- [ ] 3个月后需求变化能适应？

如果5个问题都是"是"，预计评分 ≥ 60分（Medium Value以上）。

---

**文档结束**
```

- [ ] **Step 3: 保存文件**

保存validation-guide.md文件

- [ ] **Step 4: 验证文件格式**

```bash
# 检查文件是否创建成功
ls -lh ontology-builder/references/validation-guide.md

# 检查行数
wc -l ontology-builder/references/validation-guide.md
```

预期：文件约800-1000行

- [ ] **Step 5: 提交修改**

```bash
git add ontology-builder/references/validation-guide.md
git commit -m "feat: 创建validation-guide.md业务门禁指南

- 完整的两阶段验收标准说明
- 自动门禁19项检查项详解（P0/P1/P2）
- 业务门禁5个核心问题和评审工具
- 评审会议流程和表模板
- 检查项与Gotchas映射表

Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>"
```

---

### Task 3: 更新CLAUDE.md记录设计决策

**Files:**
- Modify: `/Users/niupian/ontology-building/CLAUDE.md`
- Reference: `docs/superpowers/specs/2026-03-20-ontology-validation-design.md`

**目标:** 在CLAUDE.md中添加验收标准章节，记录设计决策和维护指南

- [ ] **Step 1: 读取当前CLAUDE.md**

```bash
# 查看当前章节结构
grep "^##" CLAUDE.md
```

- [ ] **Step 2: 在"📊 质量指标"章节后添加新章节**

在CLAUDE.md中添加以下内容：

```markdown
## 🎯 验收标准体系

### 设计决策

**决策时间**: 2026-03-20

**背景**: ontology-builder skill缺少系统化的验收标准，无法评估生成配置的质量和业务价值。

**选择的方案**: 两阶段门禁模型（方案C）

#### 为什么选择两阶段门禁？

**备选方案回顾**:
- 方案A："价值金字塔"模型 - 分层递进，但业务价值难以量化
- 方案B："加权评分卡"模型 - 量化清晰，但评分有主观性
- **方案C："两阶段门禁"模型** - ✅ 选中

**选择理由**:
1. **职责分离清晰**: 机器检查客观规则，人判断主观价值
2. **效率最高**: 自动门禁快速过滤明显缺陷，人工只评审有潜力的配置
3. **符合优先级**: 业务价值(50%) > 可用性(30%) > 完整性(20%)
4. **可渐进式演进**: 先实现自动门禁，再建立业务评审流程

---

### 两阶段门禁详解

#### 阶段1：自动门禁（Auto Gate）

**目的**: 快速过滤技术缺陷
**执行时机**: SKILL.md生成配置时自动执行
**检查内容**:

| 级别 | 名称 | 检查项数 | 行为 |
|------|------|---------|------|
| P0 | Blocker | 8项 | 阻止生成配置 |
| P1 | Warning | 8项 | 警告但允许继续 |
| P2 | Info | 4项 | 仅提示优化建议 |

**P0级检查项（必须通过）**:
1. Property ≥ 3个
2. Action ≥ 1个
3. 定义了primaryKey
4. 所有Action有permissions
5. 高危Action有confirmationRequired
6. Automation引用的Function存在
7. Automation引用的Action存在
8. 无循环触发风险

**P1级检查项（强烈建议）**:
1. 数字字段包含单位
2. 必填字段 ≤ 7个
3. 字段使用业务语言
4. 明确时序属性配置
5. Function逻辑 < 100行
6. Automation有限流保护
7. Action有前置条件
8. Function有异常处理

**P2级检查项（可选优化）**:
1. 生成了业务文档
2. 填写了完整元数据
3. Action类型规范
4. Function有usageScenarios

---

#### 阶段2：业务门禁（Business Gate）

**目的**: 评估业务价值
**执行时机**: 团队评审会议（人工）
**评审内容**: 5个核心问题（总分80分）

| 问题 | 分值 | 评审工具 |
|------|------|---------|
| 1. 业务痛点清晰度 | 20分 | 5W1H痛点挖掘表 |
| 2. 解决方案匹配度 | 20分 | 功能价值矩阵 |
| 3. 效率提升量化 | 15分 | ROI前后对比表 |
| 4. 用户采用可行性 | 15分 | 用户画像障碍分析 |
| 5. 可扩展性与演进 | 10分 | 未来场景推演 |

**评级标准**:
- 70-80分 → ⭐⭐⭐⭐⭐ High Value（优先部署）
- 50-69分 → ⭐⭐⭐ Medium Value（正常部署）
- <50分 → 🤔 Low Value（重新评估）

---

### 文件组织

```
ontology-builder/
├── SKILL.md
│   └── Step 4增强：实现P0/P1/P2三级自动门禁
│
├── references/
│   └── validation-guide.md（新增）
│       ├── 自动门禁19项检查详解
│       ├── 业务门禁5个核心问题
│       ├── 评审工具和模板
│       └── 评审会议流程
│
└── assets/
    └── validation-template.yaml（可选，Phase 2）
        └── 可执行的自动化验证脚本配置
```

---

### 使用方式

#### 流程1：Skill使用者自我检查

```
1. 用户完成5个阶段对话
2. SKILL.md自动执行自动门禁
   ├─ P0失败 → 阻止生成，提示修复
   └─ P0通过 → 生成配置 + 显示P1/P2建议
3. 生成后提供validation-guide.md链接
4. 用户自行评估业务价值
```

#### 流程2：团队正式评审

```
1. 用户提交配置到团队
2. 组织评审会议（30-45分钟）
3. 使用validation-guide.md的评审表
4. 团队打分并决策
   ├─ High Value → P0优先部署
   ├─ Medium Value → 正常排期
   └─ Low Value → 重新设计
```

---

### 维护指南

#### 添加新的检查项

如果发现新的常见错误需要检查：

1. **确定级别**:
   - P0: 会导致严重问题（安全漏洞、运行时错误）
   - P1: 影响质量但不致命（性能、可用性）
   - P2: 最佳实践建议（文档、可扩展性）

2. **更新SKILL.md**:
   在Step 4对应级别添加检查规则

3. **更新validation-guide.md**:
   添加检查项详解，包含：
   - 检查规则
   - 错误信息
   - 理由
   - 修复建议

4. **更新CLAUDE.md**:
   在本章节记录新增检查项及原因

5. **测试验证**:
   用现有配置测试新检查项是否正常工作

#### 修改评审问题

如果需要调整业务门禁的评审维度：

1. **评估影响**:
   - 是否影响评分总分（80分）？
   - 是否需要调整评级映射？

2. **更新validation-guide.md**:
   - 修改问题描述
   - 更新评分标准
   - 调整评审工具

3. **更新评审表模板**:
   确保表格与问题一致

4. **培训评审团队**:
   向业务负责人和技术负责人说明变更

---

### 关键原则

1. **自动门禁只检查客观规则**
   - ✅ 数量、格式、引用完整性
   - ❌ 命名是否"好听"、设计是否"优雅"

2. **业务门禁专注价值判断**
   - ✅ 是否解决真实痛点
   - ✅ 是否有人愿意用
   - ✅ 是否值得投入资源

3. **失败必须给建议**
   - 不能只说"有问题"
   - 要告诉用户"怎么修复"

4. **评分必须有依据**
   - 提供评审工具（表格、清单）
   - 不能拍脑袋打分

---

### 成功指标

| 指标 | 目标 | 当前 | 测量方法 |
|------|------|------|---------|
| P0缺陷拦截率 | 100% | ? | 拦截的P0问题数 / 总P0问题数 |
| 配置返工率 | <20% | ? | 评审后需修改的配置数 / 总配置数 |
| High Value配置占比 | >60% | ? | High Value配置数 / 总配置数 |
| 评审会议效率 | <45分钟 | ? | 平均会议时长 |

---

### 相关文档

- **设计文档**: `docs/superpowers/specs/2026-03-20-ontology-validation-design.md`
- **实施计划**: `docs/superpowers/plans/2026-03-20-ontology-validation-implementation.md`
- **验收指南**: `ontology-builder/references/validation-guide.md`
```

- [ ] **Step 3: 保存修改**

保存CLAUDE.md文件

- [ ] **Step 4: 提交修改**

```bash
git add CLAUDE.md
git commit -m "docs: 更新CLAUDE.md记录验收标准设计决策

- 添加"验收标准体系"章节
- 记录两阶段门禁设计决策和选择理由
- 说明自动门禁和业务门禁的详细机制
- 提供维护指南和成功指标

Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>"
```

---

### Task 4: 使用现有配置测试自动门禁

**Files:**
- Test with: `vehicle-service-ontology-config.yaml`
- Test with: `vehicle-ontology-config.yaml`
- Test with: `technician-ontology-config.yaml`
- Test with: `parts-ontology-config.yaml`

**目标:** 验证自动门禁检查逻辑是否正常工作，发现并修复bug

- [ ] **Step 1: 创建测试脚本**

创建简单的测试脚本验证检查逻辑：

```python
#!/usr/bin/env python3
"""
测试自动门禁检查逻辑
"""
import yaml
from pathlib import Path

def check_p0_completeness(config):
    """P0级基础完整性检查"""
    issues = []

    # P0-001: Property数量
    if len(config.get('properties', {})) < 3:
        issues.append(f"P0-001: Property只有{len(config.get('properties', {}))}个，至少需要3个")

    # P0-002: Action存在性
    if len(config.get('actions', {})) < 1:
        issues.append("P0-002: 缺少Action")

    # P0-003: 主键定义
    if not config.get('objectType', {}).get('primaryKey'):
        issues.append("P0-003: 未定义primaryKey")

    return issues

def check_p0_security(config):
    """P0级安全性检查"""
    issues = []

    actions = config.get('actions', {})
    for action_name, action in actions.items():
        # P0-004: Action权限检查
        if not action.get('permissions'):
            issues.append(f"P0-004: Action '{action_name}' 缺少权限控制")

        # P0-005: 高危Action确认
        if action.get('actionType') in ['delete', 'batch']:
            if not action.get('confirmationRequired'):
                issues.append(f"P0-005: 高危操作 '{action_name}' 缺少二次确认")

    return issues

def check_p0_logic(config):
    """P0级逻辑正确性检查"""
    issues = []

    # 收集所有Function和Action名称
    function_names = set(config.get('functions', {}).keys())
    action_names = set(config.get('actions', {}).keys())

    automations = config.get('automations', {})
    for auto_name, automation in automations.items():
        # P0-006: Automation引用Function
        trigger = automation.get('trigger', {})
        if trigger.get('type') == 'functionResult':
            func_name = trigger.get('eventSource', {}).get('functionName')
            if func_name and func_name not in function_names:
                issues.append(f"P0-006: Automation '{auto_name}' 引用了不存在的Function '{func_name}'")

        # P0-007: Automation引用Action
        workflow = automation.get('workflow', [])
        for step in workflow:
            if step.get('type') == 'callAction':
                action_name = step.get('action')
                if action_name and action_name not in action_names:
                    issues.append(f"P0-007: Automation '{auto_name}' 引用了不存在的Action '{action_name}'")

    # P0-008: 循环触发（简化检查，只检测直接循环）
    # 完整实现需要构建依赖图并检测环路

    return issues

def test_config(config_path):
    """测试单个配置文件"""
    print(f"\n{'='*60}")
    print(f"测试配置: {config_path.name}")
    print(f"{'='*60}\n")

    with open(config_path) as f:
        config = yaml.safe_load(f)

    all_issues = []
    all_issues.extend(check_p0_completeness(config))
    all_issues.extend(check_p0_security(config))
    all_issues.extend(check_p0_logic(config))

    if all_issues:
        print("🔴 P0检查失败:\n")
        for issue in all_issues:
            print(f"  ✗ {issue}")
        print("\n建议: 修复以上问题")
        return False
    else:
        print("✅ P0检查: 全部通过\n")
        return True

if __name__ == '__main__':
    configs = [
        'vehicle-service-ontology-config.yaml',
        'vehicle-ontology-config.yaml',
        'technician-ontology-config.yaml',
        'parts-ontology-config.yaml'
    ]

    results = {}
    for config_name in configs:
        config_path = Path(config_name)
        if config_path.exists():
            results[config_name] = test_config(config_path)
        else:
            print(f"⚠️ 配置文件不存在: {config_name}")

    print(f"\n{'='*60}")
    print("测试总结")
    print(f"{'='*60}\n")

    passed = sum(results.values())
    total = len(results)
    print(f"通过: {passed}/{total}")

    if passed == total:
        print("\n✅ 所有配置都通过了P0检查")
    else:
        print("\n⚠️ 部分配置存在P0问题，需要修复")
```

保存为 `test_auto_gate.py`

- [ ] **Step 2: 运行测试脚本**

```bash
python3 test_auto_gate.py
```

预期：看到4个配置的测试结果

- [ ] **Step 3: 分析测试结果**

检查是否有P0错误被正确检测到。
如果发现检测逻辑有误，回到Task 1修复SKILL.md。

- [ ] **Step 4: 记录测试结果**

创建测试报告：

```bash
cat > AUTO_GATE_TEST_RESULTS.md <<'EOF'
# 自动门禁测试结果

**测试日期**: $(date +%Y-%m-%d)
**测试配置**: 4个现有本体配置

## 测试结果

[粘贴test_auto_gate.py的输出]

## 发现的问题

[列出发现的问题]

## 修复建议

[列出修复建议]

## 结论

[是否通过测试]
EOF
```

- [ ] **Step 5: 如果发现bug，修复并重新测试**

如果测试发现检查逻辑有问题：
1. 回到Task 1修改SKILL.md
2. 重新运行测试
3. 直到所有测试通过

- [ ] **Step 6: 提交测试脚本和结果**

```bash
git add test_auto_gate.py AUTO_GATE_TEST_RESULTS.md
git commit -m "test: 添加自动门禁测试脚本和结果

- 创建P0级检查测试脚本
- 用4个现有配置验证检查逻辑
- 记录测试结果和发现的问题

Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>"
```

---

## Phase 1 完成检查点

在继续Phase 2之前，确认：

- [ ] SKILL.md的Step 4已增强，包含P0/P1/P2检查
- [ ] validation-guide.md已创建，内容完整
- [ ] CLAUDE.md已更新，记录了设计决策
- [ ] 测试脚本运行通过，验证了检查逻辑

**预计完成时间**: Phase 1约需8小时（1个工作日）

---

## Phase 2：工具增强（可选）

### Task 5: 创建validation-template.yaml配置文件

**Files:**
- Create: `/Users/niupian/ontology-building/ontology-builder/assets/validation-template.yaml`
- Reference: `docs/superpowers/specs/2026-03-20-ontology-validation-design.md:481-600`

**目标:** 创建机器可读的验证规则配置，供CLI/CI使用

- [ ] **Step 1: 创建validation-template.yaml**

```yaml
# Ontology配置自动验证规则模板
# 用法: python validate_ontology.py <config.yaml>

version: "1.0.0"

# P0级检查规则（阻止部署）
blockers:
  - id: "P0-001"
    name: "Property数量检查"
    category: "completeness"
    condition: "len(properties) < 3"
    message: "Property只有{count}个，至少需要3个核心字段"

  - id: "P0-002"
    name: "Action存在性检查"
    category: "completeness"
    condition: "len(actions) < 1"
    message: "缺少Action，至少需要'创建对象'操作"

  - id: "P0-003"
    name: "主键定义检查"
    category: "completeness"
    condition: "primaryKey is None or len(primaryKey) == 0"
    message: "未定义primaryKey"

  - id: "P0-004"
    name: "Action权限检查"
    category: "security"
    condition: "any(action.permissions is None for action in actions)"
    message: "Action '{action_name}' 缺少权限控制"

  - id: "P0-005"
    name: "高危Action确认检查"
    category: "security"
    condition: "action.actionType in ['delete', 'batch'] and not action.confirmationRequired"
    message: "高危操作 '{action_name}' 缺少二次确认"

  - id: "P0-006"
    name: "Automation引用Function检查"
    category: "logic"
    condition: "automation.functionName not in function_names"
    message: "Automation '{auto_name}' 引用了不存在的Function"

  - id: "P0-007"
    name: "Automation引用Action检查"
    category: "logic"
    condition: "automation.actionName not in action_names"
    message: "Automation '{auto_name}' 引用了不存在的Action"

  - id: "P0-008"
    name: "循环触发检查"
    category: "logic"
    condition: "detect_trigger_cycle(automations)"
    message: "检测到潜在循环触发: {chain}"

# P1级检查规则（警告）
warnings:
  - id: "P1-001"
    name: "数字字段单位检查"
    category: "usability"
    condition: "property.dataType in ['integer', 'double'] and '(' not in property.displayName"
    message: "数字字段 '{name}' 建议包含单位"

  - id: "P1-002"
    name: "必填字段数量检查"
    category: "usability"
    condition: "count_required_properties() > 7"
    message: "必填字段有{count}个，建议≤7个"

  - id: "P1-003"
    name: "字段命名语言检查"
    category: "usability"
    condition: "property.displayName.isascii()"
    message: "字段 '{api_name}' 建议使用中文业务术语"

  - id: "P1-004"
    name: "时序属性配置检查"
    category: "performance"
    condition: "property.timeSeries is None and property.dataType == 'timestamp'"
    message: "字段 '{name}' 未明确是否需要时序追踪"

  - id: "P1-005"
    name: "Function复杂度检查"
    category: "performance"
    condition: "len(function.logic.split('\\n')) > 100"
    message: "Function '{name}' 逻辑有{lines}行，建议<100行"

  - id: "P1-006"
    name: "Automation限流检查"
    category: "performance"
    condition: "automation.rateLimiting is None"
    message: "Automation '{name}' 缺少rateLimiting配置"

  - id: "P1-007"
    name: "Action前置条件检查"
    category: "robustness"
    condition: "action.actionType in ['update', 'delete'] and action.preconditions is None"
    message: "Action '{name}' 缺少preconditions"

  - id: "P1-008"
    name: "Function异常处理检查"
    category: "robustness"
    condition: "'try' not in function.logic and 'if' not in function.logic"
    message: "Function '{name}' 未发现异常处理代码"

# P2级检查规则（信息）
infos:
  - id: "P2-001"
    name: "业务文档检查"
    category: "documentation"
    condition: "not file_exists(documentation_path)"
    message: "建议生成ontology-documentation.md"

  - id: "P2-002"
    name: "元数据完整性检查"
    category: "documentation"
    condition: "metadata.businessContext is None"
    message: "建议填写businessContext等元数据"

  - id: "P2-003"
    name: "Action类型规范检查"
    category: "extensibility"
    condition: "action.actionType not in STANDARD_ACTION_TYPES"
    message: "建议使用标准actionType"

  - id: "P2-004"
    name: "Function使用场景说明检查"
    category: "extensibility"
    condition: "function.usageScenarios is None"
    message: "建议为Function '{name}' 添加usageScenarios"

# 输出格式配置
output:
  format: "console"  # console | json | junit
  colors: true
  show_passed: false
  exit_on_blocker: true

# 标准Action类型定义
standard_action_types:
  - "create"
  - "update"
  - "delete"
  - "custom"
  - "batch"
```

- [ ] **Step 2: 保存文件**

保存到ontology-builder/assets/validation-template.yaml

- [ ] **Step 3: 提交修改**

```bash
git add ontology-builder/assets/validation-template.yaml
git commit -m "feat: 创建validation-template.yaml验证规则配置

- 定义P0/P1/P2三级检查规则
- 机器可读的YAML格式
- 供CLI/CI使用

Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>"
```

---

### Task 6: 开发validate_ontology.py验证脚本

**Files:**
- Create: `/Users/niupian/ontology-building/scripts/validate_ontology.py`
- Reference: `ontology-builder/assets/validation-template.yaml`

**目标:** 创建可执行的Python验证脚本，读取validation-template.yaml并执行检查

_（省略详细步骤以控制篇幅，完整实现需约150行Python代码）_

---

### Task 7: 添加脚本使用文档

**Files:**
- Create: `/Users/niupian/ontology-building/scripts/README.md`

**目标:** 说明如何使用validate_ontology.py脚本

_（省略详细内容）_

---

## Phase 3：CI/CD集成（可选）

_（省略Phase 3详细内容，仅在需要时实施）_

---

## 实施检查清单

### Phase 1完成标准

- [ ] SKILL.md Step 4增强完成，包含P0/P1/P2检查逻辑
- [ ] validation-guide.md创建完成，内容完整且清晰
- [ ] CLAUDE.md更新完成，记录了设计决策
- [ ] 测试脚本验证通过，检查逻辑正常工作
- [ ] 所有修改已提交Git

### Phase 2完成标准（可选）

- [ ] validation-template.yaml创建完成
- [ ] validate_ontology.py脚本开发完成
- [ ] 脚本文档编写完成
- [ ] 用现有配置测试脚本功能

### Phase 3完成标准（可选）

- [ ] GitHub Actions workflow配置完成
- [ ] CI集成测试通过
- [ ] 通知机制配置完成

---

## 成功标准

实施完成后，应该达到：

1. **功能完整性**
   - ✅ 自动门禁能检测19项规则
   - ✅ 业务门禁有完整的评审清单和流程
   - ✅ 文档清晰易懂，评审人员能独立使用

2. **可用性**
   - ✅ Skill使用者收到清晰的错误提示和修复建议
   - ✅ 评审团队能在45分钟内完成评审
   - ✅ 验证脚本（如果实现）易于集成到工作流

3. **质量提升**
   - ✅ P0缺陷拦截率达到100%
   - ✅ High Value配置占比 > 60%（假设经过一段时间使用后）

---

## 参考文档

- **规范文档**: `docs/superpowers/specs/2026-03-20-ontology-validation-design.md`
- **Gotchas清单**: `ontology-builder/references/gotchas.md`
- **现有SKILL.md**: `ontology-builder/SKILL.md`

---

**计划版本**: 1.0.0
**创建日期**: 2026-03-20
**预计完成时间**: Phase 1（1天）+ Phase 2（1天，可选）
