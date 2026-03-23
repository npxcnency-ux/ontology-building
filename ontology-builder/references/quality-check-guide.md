# 质量检查指南

本指南详细说明ontology-builder skill在生成配置前执行的三级自动门禁质量检查。

---

## 📋 三级门禁概述

质量检查分为三个级别：

| 级别 | 名称 | 检查项数 | 行为 |
|------|------|---------|------|
| P0 | 阻断级 (Blocker) | 9项 | 必须全部通过才能生成配置 |
| P1 | 警告级 (Warning) | 12项 | 警告但允许继续，强烈建议修复 |
| P2 | 建议级 (Info) | 4项 | 仅提示优化建议 |

**执行方式**: Agent应该自动对用户在五个阶段提供的配置运行所有检查项，无需用户干预。检查完成后，向用户报告发现的问题。

---

## 🚫 P0级检查项（阻断级）

### [P0-1] Property数量不足

**检查内容**: 是否定义了至少3个Property？

**说明**: 少于3个Property意味着对象建模过于简单，无法支撑业务需求

**修复建议**: 回到阶段二，补充基础信息字段（如编号、名称、状态等）

---

### [P0-2] 缺少Action定义

**检查内容**: 是否定义了至少1个Action？

**说明**: 没有Action意味着用户无法对对象进行任何操作

**修复建议**: 回到阶段四，至少添加一个"创建对象"操作

---

### [P0-3] 未定义主键

**检查内容**: 是否定义了primaryKey？

**说明**: 没有主键无法在系统中唯一标识对象

**修复建议**: 确定哪个字段作为唯一标识（如工单编号、设备ID）

---

### [P0-4] Action缺少权限控制

**检查内容**: 每个Action是否都明确了谁可以执行？

**说明**: 没有权限控制会导致权限混乱和安全问题

**修复建议**: 为每个Action添加角色限制

**示例**:
```yaml
permissions:
  roles:
    - "管理员"
    - "操作员"
```

---

### [P0-5] 高危Action缺少二次确认

**检查内容**: 删除、批量操作等高危Action是否需要用户二次确认？

**说明**: 防止误操作导致数据丢失

**修复建议**: 为高危Action添加确认配置

**示例**:
```yaml
confirmationRequired: true
confirmationMessage: "确定删除该工单吗？删除后无法恢复。"
```

---

### [P0-6] Automation引用了不存在的Function

**检查内容**: Automation引用的Function是否存在？需检查两处引用位置：
1. **trigger 中的 `functionName`**（条件触发时调用的Function）
2. **workflow 步骤中 `type: callFunction` 的 function 引用**

**说明**: 引用不存在的Function会导致运行时错误。

**高频出错场景——定时类 Automation 的幽灵引用**：
定时 Automation（如每日统计、每周报表）的 workflow 常需要 "查询数据→计算→通知" 多个步骤。这里的**数据查询和聚合操作不是 Function**——Function 是阶段三定义的只读计算规则（如风险评估、综合评分）。如果 workflow 步骤的目的是查询、筛选、统计数据，应使用 `type: query`，而不是 `type: callFunction`。

**检测方法**:
1. 从 functions 段收集所有已定义的 Function apiName，形成 **已定义 Function 清单**
2. 遍历每个 Automation 的 trigger，检查 functionName 是否在清单中
3. 遍历每个 Automation 的 workflow 步骤，找到所有 `type: callFunction` 的步骤，检查其引用的 function 名是否在清单中
4. 如有不匹配，先判断该步骤的真实意图：
   - 如果是数据查询/聚合 → 将 `type` 改为 `query`（不需要引用 Function）
   - 如果确实需要计算规则 → 在 functions 段补充该 Function 定义

**常见幽灵引用模式**（一旦看到就要警觉）：
- `aggregateQuery` — 不是 Function，应改为 `type: query`
- 临时查询类名称（如 `queryBookings`、`fetchRecords`）— 应改为 `type: query`
- 对已有 Function 的描述性步骤（描述中提到 Function 名但 type 不是 callFunction）— 这种是正确的

**修复建议**: 数据查询步骤改用 `type: query`；真正需要的计算规则补充到 functions 段

---

### [P0-7] Automation引用了不存在的Action

**检查内容**: 如果定义了Automation，它引用的Action是否存在？

**说明**: 引用不存在的Action会导致运行时错误

**修复建议**: 检查Action名称拼写，或先定义被引用的Action

---

### [P0-8] 检测到循环触发风险

**检查内容**: Automation触发链中是否有环路？

**说明**: A触发B，B触发A会导致无限循环

**检测方法**:
1. 构建Automation触发依赖图
2. 使用深度优先搜索检测环路
3. 如果发现环路，列出完整的触发链

**修复建议**: 重新设计Automation触发逻辑，打破循环

---

### [P0-9] Precondition引用了不存在的字段

**检查内容**: Action的precondition表达式中引用的字段名是否在Properties中定义过？

**说明**: Precondition中引用不存在的字段（如 `activePurchaseOrderCount == 0` 但该字段未在Properties中声明）会导致运行时错误。这是一个常见错误——编写precondition时容易"发明"一个听起来合理但实际未定义的字段。

**检测方法**:
1. 从所有Properties中提取apiName列表
2. 解析每个Action的preconditions表达式，提取引用的变量名
3. 检查每个变量名是否在apiName列表中

**修复建议**:
- 如果该字段确实需要：回到阶段二补充该Property定义
- 如果该字段是关联对象的聚合值：改为Function计算（如 `countActiveOrders()` 函数），在precondition中引用Function结果
- 如果该字段是由其他检查项推导：明确数据来源

**示例**:
```yaml
# ❌ 引用了不存在的字段
preconditions:
  - condition: "activePurchaseOrderCount == 0"
    errorMessage: "还有进行中的采购订单"

# ✅ 方案A：补充Property定义
properties:
  - apiName: "activePurchaseOrderCount"
    displayName: "进行中采购订单数"
    dataType: "integer"
    source: "系统计算"

# ✅ 方案B：改用Function
functions:
  countActiveOrders:
    description: "计算进行中的采购订单数量"
    returnType: "integer"
preconditions:
  - condition: "countActiveOrders() == 0"
    errorMessage: "还有进行中的采购订单"
```

---

## ⚠️ P1级检查项（警告级）

### [P1-1] 数字字段缺少单位

**检查内容**: 数字类型的Property名称中是否包含单位？

**说明**: 包含单位使字段含义更清晰

**修复建议**:
- "温度" → "温度(°C)"
- "里程" → "里程(公里)"
- "重量" → "重量(kg)"

---

### [P1-2] 必填字段过多

**检查内容**: 必填字段是否≤7个？

**说明**: 太多必填字段增加用户填写负担，影响用户体验

**修复建议**: 重新评估哪些字段是真正必填的，其他改为选填

---

### [P1-3] 字段使用英文命名

**检查内容**: Property名称是否使用中文业务术语而非英文？

**说明**: 业务人员更容易理解中文字段名

**修复建议**:
- "status" → "工单状态"
- "assigned_to" → "分配的技师"
- "priority" → "优先级"

---

### [P1-4] 未明确时序属性配置

**检查内容**: 对于会变化的字段，是否明确了是否需要时序追踪？

**说明**: 避免过度使用时序属性导致存储成本暴涨（存储量是普通属性的100倍以上）

**修复建议**:
- 需要查看历史趋势 → 启用"历史追踪"（如设备温度、状态变化历史）
- 固定不变或很少变化 → 不启用"历史追踪"（如编号、名称）

> 技术配置中对应 `timeSeries: true / false`

**参考**: 详见 `gotchas.md` 的 Gotcha #3

---

### [P1-5] Function逻辑过于复杂

**检查内容**: Function的逻辑代码行数是否<100行？

**说明**: 超过100行的Function难以维护且影响性能

**修复建议**:
- 拆分为多个Function
- 简化逻辑
- 或改用Automation后台异步执行

---

### [P1-6] Automation缺少限流配置

**检查内容**: Automation是否配置了频率限制（如maxExecutionsPerHour）？

**说明**: 没有限流会导致通知/操作过于频繁，用户被打扰

**修复建议**: 添加限流配置

**示例**:
```yaml
rateLimiting:
  maxExecutionsPerHour: 1  # 每小时最多1次
  cooldownMinutes: 60      # 两次执行间隔至少60分钟
```

**参考**: 详见 `gotchas.md` 的 Gotcha #10

---

### [P1-7] Action缺少前置条件

**检查内容**: 关键Action（如删除、停机）是否设置了前置条件？

**说明**: 没有前置条件会导致误操作（如已报废的设备还能启动）

**修复建议**: 为关键Action添加状态检查

**示例**:
```yaml
preconditions:
  - condition: "设备状态 = '停机'"
    errorMessage: "只有停机状态才能启动设备"
```

**参考**: 详见 `gotchas.md` 的 Gotcha #4

---

### [P1-8] Function缺少异常处理

**检查内容**: Function的计算逻辑是否考虑了空值情况？

**说明**: 没有异常处理会导致计算失败

**修复建议**: 添加"如果字段为空，返回默认值"的逻辑

**示例**:
```python
# ❌ 没有异常处理
@function
def calculate_utilization(device: Device) -> float:
    return device.running_time / device.total_time

# ✅ 有异常处理
@function
def calculate_utilization(device: Device) -> float:
    if device.total_time is None or device.total_time == 0:
        return 0.0
    return device.running_time / device.total_time
```

---

### [P1-11] Function描述包含写操作

**检查内容**: Function的描述是否为纯只读逻辑（判断/计算/推断）？

**说明**: Function是"只读的大脑"，只能读取数据并返回计算结果，不能修改数据或触发外部操作。如果Function描述中包含"发送通知"、"修改状态"、"创建工单"等写操作，说明该逻辑应归入Action（单次操作）或Automation（自动触发）。

**识别关键词**:
- ❌ 写操作词汇：发送、通知、修改、更新、创建、删除、执行、触发、停机
- ✅ 只读词汇：判断、计算、评估、检查、返回、推断、比较

**修复建议**: 将写操作部分拆分到Action或Automation，Function只保留判断/计算逻辑

**示例**:
```yaml
# ❌ 混淆了Function和Automation
Function: "当温度超标时，发送邮件给经理"

# ✅ 正确拆分
Function: "判断温度是否超标" → 返回"超标"/"正常"
Automation: 当Function返回"超标"时 → 触发Action"发送告警通知"
```

---

### [P1-12] Automation缺少错误处理配置

**检查内容**: 涉及外部系统调用（回写、发送通知、Webhook）的Automation是否配置了errorHandling？

**说明**: 调用外部系统的Automation可能因网络故障、目标系统宕机等原因失败。没有错误处理会导致操作静默丢失，用户不知道自动化没有执行成功。

**修复建议**: 为涉及外部调用的Automation添加错误处理策略

**示例**:
```yaml
# ❌ 调用外部系统但没有错误处理
automations:
  auto_writeback_erp:
    workflow:
      - step: 0
        type: "callAction"
        action: "sync_to_erp"
    # 缺少 errorHandling

# ✅ 配置了错误处理
automations:
  auto_writeback_erp:
    workflow:
      - step: 0
        type: "callAction"
        action: "sync_to_erp"
    errorHandling:
      strategy: "retry"
      retryConfig:
        maxAttempts: 3
        backoffSeconds: 60
      notifyOnFailure:
        - "系统管理员"
```

**参考**: 详见 `automation-guide.md` 的失败处理策略

---

### [P1-9] Links目标对象类型不存在

**检查内容**: 如果定义了Links，目标对象类型是否在对象全景图中？

**说明**: 引用不存在的对象类型会导致关联关系无效

**修复建议**: 检查目标对象类型名称，确认它在阶段一的对象全景图中已识别

**示例**:
```yaml
# ❌ 目标对象"配件"不在全景图中
links:
  - targetObjectType: "配件"
    relationship: "使用"

# ✅ 修复：先在全景图中确认"配件"是否属于该场景
# 如果属于 → 添加到对象全景图，标记"待建模"
# 如果不属于 → 移除该Link
```

---

### [P1-10] 核心对象缺少关联关系

**检查内容**: 核心对象是否定义了至少1个Link？

**说明**: 核心对象通常是业务场景的中心节点，至少应与一个其他对象有关联关系。缺少Link意味着对象是"孤岛"，无法支撑跨对象的业务查询和分析。

**修复建议**: 回到阶段二的Q8，根据对象全景图确认核心对象与其他对象的关联关系

**示例**:
```yaml
# ❌ 设备对象没有任何Link
links: []

# ✅ 设备对象至少关联车间和工单
links:
  - targetObjectType: "车间"
    relationship: "属于"
    cardinality: "manyToOne"
  - targetObjectType: "工单"
    relationship: "产生"
    cardinality: "oneToMany"
```

---

## 💡 P2级检查项（建议级）

### [P2-1] 对象命名不友好

**检查内容**: 对象类型名称是否使用了业务术语（而非技术术语）？

**说明**: 技术化的名称会降低业务人员的理解度

**优化建议**: 使用业务常用名（如"生产设备"而非"Equipment Entity"）

---

### [P2-2] Property分组不清晰

**检查内容**: 是否将Property按"固定信息"、"变化信息"、"历史追踪"分组？

**说明**: 分组有助于用户快速找到所需字段

**优化建议**: 在documentation中按类别组织字段

---

### [P2-3] 缺少使用场景说明

**检查内容**: documentation是否包含了典型使用场景？

**说明**: 场景说明帮助新用户快速上手

**优化建议**: 添加2-3个典型场景（如"如何查看设备温度趋势"）

---

### [P2-4] 缺少业务价值说明

**检查内容**: documentation是否说明了本体能带来什么业务价值？

**说明**: 价值说明有助于获得管理层支持

**优化建议**: 添加预期收益（如"预计减少30%故障响应时间"）

---

## 📊 检查结果反馈模板

### 发现P0问题时

```
❌ 发现P0阻断级问题，必须修复后才能生成配置文件：

1. [P0-4] Action 'createEquipment' 缺少权限控制
   修复建议：添加permissions配置，指定哪些角色可以执行

2. [P0-6] Automation 'dailyReport' 的 workflow step 2 用 callFunction 引用了 'aggregateQuery'，
   但该 Function 未在 functions 段定义。该步骤实际是数据聚合查询，应改用 type: query
   修复建议：将该 workflow step 的 type 改为 query，移除 function 引用

我们回到相关阶段修复这些问题？
```

### 发现P1问题时

```
⚠️ 发现P1警告级问题，强烈建议修复（可以跳过）：

1. [P1-2] 必填字段有10个，建议≤7个（影响用户体验）
   修复建议：重新评估哪些字段是真正必填的

2. [P1-6] Automation 'temperatureAlert' 缺少rateLimiting配置
   修复建议：添加限流保护，避免频繁通知

你想修复这些问题吗？还是直接继续生成配置？
```

### 发现P2问题时

```
💡 发现P2建议级优化点（可选）：

1. [P2-1] 对象命名"Equipment Entity"建议改用业务术语"生产设备"
   优化建议：使用业务人员熟悉的名称

2. [P2-4] 建议添加业务价值说明，如"预计减少30%故障响应时间"
   优化建议：帮助管理层理解投资回报

你想优化这些部分吗？还是直接继续生成配置？
```

### 全部通过时

```
✅ 质量检查全部通过！可以生成配置文件。
```

---

## 🔍 检查项与Gotchas映射

| Gotcha | 对应检查项 | 级别 |
|--------|----------|------|
| #3: Function设计过于复杂 | P1-5: Function复杂度检查 | P1 |
| #4: 忘记设置Action前置条件 | P1-7: Action前置条件检查 | P1 |
| #5: Automation触发不当 | P0-8: 循环触发检测, P1-6: Automation限流检查 | P0/P1 |
| #6: 数据类型选错 | 阶段二引导预防（自动推荐字段类型） | 引导预防 |
| #7: 过度使用时序属性 | P1-4: 时序属性配置检查 | P1 |
| #8: 字段命名不清晰 | P1-1, P1-3: 命名检查 | P1 |
| #10: Automation没有限流 | P1-6: Automation限流检查 | P1 |
| #11: 权限控制设置不当 | P0-4: Action权限检查 | P0 |
| #20: Link和Property混淆 | P1-9, P1-10: Links检查 | P1 |
| 对象孤岛缺少关联 | P1-9, P1-10: Links检查 | P1 |

---

## 💡 使用技巧

### 技巧1: 优先修复P0问题

P0问题会阻止配置生成，必须优先处理。通常P0问题都有明确的修复方法，按照建议操作即可。

### 技巧2: P1问题可以分批修复

如果P1问题较多，可以：
1. 先修复最常见的（如P1-6 Automation限流）
2. 生成配置后继续优化
3. 在下次迭代时完善

### 技巧3: P2问题可以在部署后优化

P2问题不影响功能，可以在配置部署后根据实际使用反馈再优化。

### 技巧4: 结合CLAUDE.md了解业务门禁

如果需要了解业务价值评审流程（阶段2：业务门禁），请查阅项目 `CLAUDE.md` 的"验收标准体系"章节。

---

**文档结束**
