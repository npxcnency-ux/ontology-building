# Ontology Builder 验收标准设计文档

**创建日期**: 2026-03-20
**设计者**: Ontology Team
**状态**: Draft
**版本**: 1.0.0

---

## 📋 目录

1. [背景与目标](#背景与目标)
2. [设计原则](#设计原则)
3. [整体架构](#整体架构)
4. [阶段1：自动门禁](#阶段1自动门禁)
5. [阶段2：业务门禁](#阶段2业务门禁)
6. [实施计划](#实施计划)
7. [成功指标](#成功指标)

---

## 背景与目标

### 现状问题

ontology-builder skill目前已经实现了交互式本体构建功能，但在验收标准方面存在以下问题：

1. **验收标准不明确**：只有SKILL.md中的5项基本检查，缺少系统化的质量评估体系
2. **业务价值难衡量**：无法判断生成的本体是否真正解决业务问题
3. **缺少分级机制**：无法区分"优秀"、"合格"、"不合格"的本体配置

### 设计目标

创建一个**两阶段验收标准体系**，实现：

- **自动门禁**：快速过滤技术缺陷（完整性、可用性、健壮性）
- **业务门禁**：人工评估业务价值（解决痛点、效率提升、用户采用）
- **分级评定**：明确区分High/Medium/Low Value，指导部署决策

### 优先级排序

基于用户反馈，验收标准的优先级为：

1. **业务价值** (50%) - 是否解决真实问题
2. **可用性** (30%) - 是否易用、易懂
3. **完整性** (20%) - 是否技术完整

---

## 设计原则

### 原则1：职责分离

- **机器检查客观规则**：数量、格式、逻辑错误（自动门禁）
- **人判断主观价值**：业务价值、用户需求、ROI（业务门禁）
- **避免混淆**：不让机器做价值判断，不让人做重复检查

### 原则2：渐进式过滤

```
所有配置
    ↓ 自动门禁（快速、严格）
通过技术检查的配置
    ↓ 业务门禁（深入、权衡）
值得部署的配置
```

### 原则3：可操作性

- **检查项必须明确**：不能有歧义的规则
- **失败必须给建议**：告诉用户怎么修复
- **评分必须有依据**：不能拍脑袋打分

### 原则4：渐进式实施

- **Phase 1**：SKILL.md增强自动门禁（必须）
- **Phase 2**：创建validation-guide.md（必须）
- **Phase 3**：创建validation-template.yaml（可选）
- **Phase 4**：集成到CI/CD（可选）

---

## 整体架构

### 系统架构图

```
┌─────────────────────────────────────────────────────┐
│ 用户使用ontology-builder skill生成配置               │
└────────────────────┬────────────────────────────────┘
                     ↓
┌─────────────────────────────────────────────────────┐
│  阶段1: 自动门禁 (Auto Gate)                         │
│  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━  │
│                                                     │
│  检查内容：完整性 + 可用性 + 健壮性                   │
│  执行方式：                                          │
│  • SKILL.md内置检查（生成时实时执行）                │
│  • validation-template.yaml（CLI/CI可选）           │
│                                                     │
│  检查级别：                                          │
│  • P0 (Blocker) - 阻止生成配置                      │
│  • P1 (Warning) - 允许生成但警告                    │
│  • P2 (Info) - 优化建议                            │
│                                                     │
│  结果：                                              │
│  ✅ Pass → 进入阶段2                                │
│  ❌ Fail → 给出修复建议，重新生成                    │
└────────────────────┬────────────────────────────────┘
                     ↓ (P0全部通过后)
┌─────────────────────────────────────────────────────┐
│  阶段2: 业务门禁 (Business Gate)                     │
│  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━  │
│                                                     │
│  检查内容：业务价值评估                              │
│  执行方式：                                          │
│  • validation-guide.md中的评审清单                   │
│  • 团队评审会议（人工打分）                          │
│                                                     │
│  评审维度（5个核心问题）：                            │
│  1. 业务痛点清晰度 (20分)                            │
│  2. 解决方案匹配度 (20分)                            │
│  3. 效率提升量化 (15分)                              │
│  4. 用户采用可行性 (15分)                            │
│  5. 可扩展性与演进 (10分)                            │
│  ────────────────────                              │
│  总分：80分                                          │
│                                                     │
│  评级标准：                                          │
│  ⭐⭐⭐⭐⭐ High Value (70-80分) → 优先部署          │
│  ⭐⭐⭐ Medium Value (50-69分) → 正常部署            │
│  🤔 Low Value (<50分) → 重新评估                    │
└────────────────────┬────────────────────────────────┘
                     ↓
┌─────────────────────────────────────────────────────┐
│  部署到生产环境                                      │
└─────────────────────────────────────────────────────┘
```

### 文件组织

```
ontology-builder/
├── SKILL.md
│   └── 增强 "Step 4: 质量检查" 部分
│       ├── 实现P0/P1/P2三级检查
│       └── 检查失败时的引导逻辑
│
├── references/
│   └── validation-guide.md (新建)
│       ├── 两阶段验收标准完整说明
│       ├── 自动门禁检查项详解
│       ├── 业务门禁5个核心问题
│       ├── 评审工具（表格、模板）
│       └── 评审会议流程
│
└── assets/
    └── validation-template.yaml (新建)
        ├── P0/P1/P2检查规则（机器可读）
        ├── 评分算法
        └── 可执行脚本的配置文件
```

### 工作流程

#### 流程1：Skill使用者自我检查

```
1. 用户完成5个阶段对话
2. SKILL.md自动执行自动门禁检查
   ├─ P0失败 → 阻止生成，提示修复
   └─ P0通过 → 生成配置 + 显示P1/P2建议
3. 生成配置后，提供validation-guide.md链接
4. 用户阅读业务门禁清单，自我评估价值
```

#### 流程2：团队正式评审

```
1. 用户提交配置到团队
2. 技术人员运行validation-template.yaml（可选）
   └─ 再次验证自动门禁规则
3. 组织评审会议
   ├─ 使用validation-guide.md的评审表
   ├─ 逐一回答5个核心问题
   └─ 团队打分并决策
4. 决策结果
   ├─ High Value → P0优先部署
   ├─ Medium Value → 正常排期
   └─ Low Value → 重新设计或暂缓
```

#### 流程3：CI/CD集成（可选）

```
1. 开发者push配置到Git
2. CI Pipeline触发
   └─ 运行validation-template.yaml脚本
3. 检查结果
   ├─ P0失败 → 阻止合并 + 通知开发者
   └─ P0通过 → 允许合并 + 等待人工评审
```

---

## 阶段1：自动门禁

### 设计理念

自动门禁只检查**客观、可量化、无争议**的规则：
- ✅ 数量、格式、引用完整性
- ❌ 命名是否"好听"、设计是否"优雅"

### 检查级别定义

| 级别 | 名称 | 行为 | 适用场景 |
|------|------|------|---------|
| P0 | Blocker | 阻止配置生成 | 严重缺陷：缺少必须字段、安全漏洞、逻辑错误 |
| P1 | Warning | 允许生成但警告 | 潜在问题：性能风险、可用性问题、缺少保护 |
| P2 | Info | 仅提示优化建议 | 最佳实践：文档完整性、可扩展性建议 |

### P0级检查项（Blocker）

#### 1. 基础完整性

```yaml
P0-001: Property数量检查
  condition: len(properties) < 3
  message: "Property只有{count}个，至少需要3个核心字段"
  理由: 少于3个字段的对象没有实际业务价值

P0-002: Action存在性检查
  condition: len(actions) < 1
  message: "缺少Action，至少需要'创建对象'操作"
  理由: 没有操作的对象无法使用

P0-003: 主键定义检查
  condition: primaryKey is None or len(primaryKey) == 0
  message: "未定义primaryKey，无法唯一标识对象"
  理由: 没有主键无法在系统中唯一标识对象
```

#### 2. 安全性

```yaml
P0-004: Action权限检查
  condition: any(action.permissions is None for action in actions)
  message: "Action '{action_name}' 缺少权限控制"
  理由: 无权限控制会导致严重的安全漏洞

P0-005: 高危Action确认检查
  condition: |
    action.actionType in ['delete', 'batch'] and
    action.confirmationRequired != true
  message: "高危操作 '{action_name}' 缺少二次确认"
  理由: 防止误操作导致数据丢失
```

#### 3. 逻辑正确性

```yaml
P0-006: Automation引用Function检查
  condition: |
    automation.functionName not in [f.name for f in functions]
  message: "Automation '{auto_name}' 引用了不存在的Function '{func_name}'"
  理由: 引用不存在的Function会导致运行时错误

P0-007: Automation引用Action检查
  condition: |
    automation.actionName not in [a.name for a in actions]
  message: "Automation '{auto_name}' 引用了不存在的Action '{action_name}'"
  理由: 引用不存在的Action会导致运行时错误

P0-008: 循环触发检查
  condition: 检测Automation触发链中是否有环路
  message: "检测到潜在循环触发: {chain}"
  理由: A触发B，B触发A会导致无限循环
  检测方法: |
    1. 构建Automation触发依赖图
    2. 使用DFS检测环路
    3. 如果发现环路，列出完整的触发链
```

### P1级检查项（Warning）

#### 4. 可用性基础

```yaml
P1-001: 数字字段单位检查
  condition: |
    property.dataType in ['integer', 'double'] and
    '(' not in property.displayName
  message: "数字字段 '{name}' 建议包含单位，如 '温度(°C)'"
  理由: 包含单位使字段含义更清晰

P1-002: 必填字段数量检查
  condition: count(properties where required=true) > 7
  message: "必填字段有{count}个，建议≤7个（影响用户体验）"
  理由: 太多必填字段增加用户填写负担

P1-003: 字段命名语言检查
  condition: |
    property.displayName.isascii() and
    metadata.target_audience == 'business_users'
  message: "字段 '{api_name}' 建议使用中文业务术语而非英文"
  理由: 业务人员更容易理解中文字段名
```

#### 5. 性能保护

```yaml
P1-004: 时序属性配置检查
  condition: |
    property.dataType == 'timestamp' and
    property.timeSeries is None
  message: "字段 '{name}' 未明确是否需要时序追踪"
  理由: 避免过度使用时序属性导致存储成本暴涨（参考Gotcha #7）

P1-005: Function复杂度检查
  condition: len(function.logic.split('\n')) > 100
  message: "Function '{name}' 逻辑有{lines}行，建议<100行"
  理由: 超过100行的Function难以维护且影响性能

P1-006: Automation限流检查
  condition: automation.rateLimiting is None
  message: "Automation '{name}' 缺少rateLimiting配置"
  理由: 防止频繁触发导致系统过载（参考Gotcha #10）
```

#### 6. 健壮性

```yaml
P1-007: Action前置条件检查
  condition: |
    action.actionType in ['update', 'delete'] and
    action.preconditions is None
  message: "Action '{name}' 缺少preconditions"
  理由: 防止在错误状态执行操作（参考Gotcha #4）

P1-008: Function异常处理检查
  condition: |
    'try' not in function.logic and
    'if' not in function.logic  # 简化检测
  message: "Function '{name}' 的logic中未发现异常处理代码"
  理由: Function应该处理空值、超时等异常情况
  建议: 添加try/except或if/else空值判断
```

### P2级检查项（Info）

#### 7. 文档完整性

```yaml
P2-001: 业务文档检查
  condition: not exists(ontology-documentation.md)
  message: "建议生成ontology-documentation.md供业务人员阅读"
  理由: 业务文档帮助非技术人员理解配置

P2-002: 元数据完整性检查
  condition: |
    metadata.businessContext is None or
    metadata.targetUsers is None
  message: "建议填写businessContext、targetUsers等元数据"
  理由: 完整的元数据有助于理解和维护
```

#### 8. 可扩展性

```yaml
P2-003: Action类型规范检查
  condition: action.actionType not in STANDARD_ACTION_TYPES
  message: "建议使用标准actionType: create/update/delete/custom"
  理由: 标准化的类型便于分类和管理

P2-004: Function使用场景说明检查
  condition: function.usageScenarios is None
  message: "建议为Function '{name}' 添加usageScenarios说明"
  理由: 使用场景说明有助于理解Function的价值
```

### 实现方式

#### 实现1：SKILL.md内置检查

在SKILL.md的"输出阶段 → Step 4: 质量检查"部分增强：

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

#### 🟠 P1级检查（强烈建议）

执行以下检查，生成警告但允许继续：

**可用性基础**
- [ ] 数字字段命名包含单位
- [ ] 必填字段 ≤ 7个
- [ ] 字段使用业务语言（中文）

**性能保护**
- [ ] 明确了时序属性配置
- [ ] Function逻辑 < 100行
- [ ] Automation有限流保护

**健壮性**
- [ ] update/delete类Action有前置条件
- [ ] Function有异常处理

**如果有P1警告**：
1. 仍然生成配置文件
2. 在输出后显示完整的警告列表
3. 建议用户修复后再提交团队评审
4. 提供具体的修复建议

#### 🟡 P2级检查（可选优化）

**文档完整性**
- [ ] 生成了ontology-documentation.md
- [ ] 填写了完整的metadata

**可扩展性**
- [ ] Action类型规范
- [ ] Function有usageScenarios说明

**如果有P2信息**：
仅作为优化建议显示，不影响配置生成。

---

**检查完成后，显示完整报告**：

```
🎉 自动门禁检查完成！

✅ P0检查: 全部通过 (8/8)
⚠️ P1警告: 3个
  • Property 'mileage' 建议包含单位
  • Function 'calculate_cost' 逻辑有127行
  • Automation 'daily_report' 缺少限流保护

ℹ️ P2建议: 1个
  • 建议生成ontology-documentation.md

建议: 修复P1警告后再提交团队评审
参考: references/validation-guide.md 了解完整验收标准
```
```

#### 实现2：validation-template.yaml

供技术团队在CLI或CI/CD中使用：

```yaml
# Ontology配置自动验证规则
# 用法: python validate_ontology.py <config.yaml>

version: "1.0.0"

# P0级检查规则
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

# P1级检查规则
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

# P2级检查规则
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

# 输出格式配置
output:
  format: "console"  # console | json | junit
  colors: true
  show_passed: false
  exit_on_blocker: true
```

配套的Python脚本示例：

```python
#!/usr/bin/env python3
"""
Ontology配置验证脚本
用法: python validate_ontology.py <config.yaml>
"""

import yaml
import sys
from pathlib import Path

def load_config(path):
    """加载配置文件"""
    with open(path) as f:
        return yaml.safe_load(f)

def validate(config, rules):
    """执行验证"""
    results = {
        'blockers': [],
        'warnings': [],
        'infos': []
    }

    # 执行P0检查
    for rule in rules['blockers']:
        if check_condition(config, rule['condition']):
            results['blockers'].append(rule)

    # 执行P1检查
    for rule in rules['warnings']:
        if check_condition(config, rule['condition']):
            results['warnings'].append(rule)

    # 执行P2检查
    for rule in rules['infos']:
        if check_condition(config, rule['condition']):
            results['infos'].append(rule)

    return results

def print_results(results):
    """打印验证结果"""
    print("\n" + "="*60)
    print("Ontology配置验证报告")
    print("="*60 + "\n")

    # P0错误
    if results['blockers']:
        print(f"🔴 P0 错误 ({len(results['blockers'])}个) - 阻止部署")
        for rule in results['blockers']:
            print(f"  ✗ {rule['message']}")
        print()
    else:
        print("✅ P0 检查: 全部通过\n")

    # P1警告
    if results['warnings']:
        print(f"🟠 P1 警告 ({len(results['warnings'])}个) - 强烈建议修复")
        for rule in results['warnings']:
            print(f"  ⚠ {rule['message']}")
        print()

    # P2信息
    if results['infos']:
        print(f"🟡 P2 信息 ({len(results['infos'])}个) - 可选优化")
        for rule in results['infos']:
            print(f"  ℹ {rule['message']}")
        print()

    # 综合评估
    if results['blockers']:
        print("总分: 不及格 (有P0错误)")
        print("建议: 修复所有P0错误后重新检查\n")
        return 1
    elif len(results['warnings']) > 5:
        print("总分: 及格 (P1警告较多)")
        print("建议: 修复P1警告后再提交评审\n")
        return 0
    else:
        print("总分: 良好")
        print("建议: 可以进入业务门禁评审\n")
        return 0

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("用法: python validate_ontology.py <config.yaml>")
        sys.exit(1)

    config_path = sys.argv[1]
    rules_path = Path(__file__).parent / 'validation-template.yaml'

    config = load_config(config_path)
    rules = load_config(rules_path)

    results = validate(config, rules)
    exit_code = print_results(results)

    sys.exit(exit_code)
```

---

## 阶段2：业务门禁

### 设计理念

业务门禁专注于**价值判断**，这是机器无法做的：
- ✅ 是否解决了真实痛点
- ✅ 是否有人愿意用
- ✅ 是否值得投入资源部署

### 5个核心评审问题

#### 问题1：业务痛点清晰度（20分）

**评审问题**：
```
这个本体解决了什么具体的业务痛点？
```

**评分标准**：

| 等级 | 得分 | 标准 | 示例 |
|------|------|------|------|
| ⭐⭐⭐⭐⭐ 优秀 | 20分 | 痛点描述具体且量化 | "目前每天人工派单需要2小时，错误率15%，导致客户投诉率高" |
| ⭐⭐⭐ 合格 | 12分 | 痛点清晰但未量化 | "派单效率低，容易出错" |
| ⭐ 不合格 | 0分 | 没有明确痛点 | "觉得应该做个系统" |

**评审工具 - 痛点挖掘5W1H表**：

```markdown
| 维度 | 问题 | 答案 |
|------|------|------|
| What | 什么问题影响了业务？ | |
| Who | 哪些人受到影响？ | |
| When | 什么时候会遇到这个问题？ | |
| Where | 在哪个业务环节发生？ | |
| Why | 为什么现有方式不行？ | |
| How Much | 影响程度有多大（时间/成本/质量）？ | |
```

**打分参考**：
- 填写了6个维度 → 20分
- 填写了4-5个维度 → 15分
- 填写了2-3个维度 → 10分
- 填写了≤1个维度 → 0分

---

#### 问题2：解决方案匹配度（20分）

**评审问题**：
```
这个本体的设计是否针对性地解决了上述痛点？
```

**评分标准**：

| 等级 | 得分 | 标准 | 示例 |
|------|------|------|------|
| ⭐⭐⭐⭐⭐ 优秀 | 20分 | 每个核心功能都对应到具体痛点 | "Automation超时提醒→解决派单延误；Function复杂度判断→智能分配技师" |
| ⭐⭐⭐ 合格 | 12分 | 部分功能对应痛点，但有冗余 | "定义了10个Function，但只有3个真正用得上" |
| ⭐ 不合格 | 0分 | 设计和痛点无关 | "痛点是派单慢，但设计重点在费用计算" |

**评审工具 - 功能价值矩阵**：

```markdown
| 功能 | 对应痛点 | 使用频率 | 实现复杂度 | 优先级 | 价值评分 |
|------|----------|----------|------------|--------|---------|
| Automation超时提醒 | 派单延误 | 高 | 低 | P0 | ⭐⭐⭐⭐⭐ |
| Function费用计算 | 手工算费时 | 中 | 中 | P1 | ⭐⭐⭐ |
| Function返修判断 | 质量追溯 | 低 | 高 | P2 | ⭐⭐ |

评分规则：
- P0功能（高频+解决核心痛点）占比 > 70% → 20分
- P0功能占比 50-70% → 15分
- P0功能占比 30-50% → 10分
- P0功能占比 < 30% → 5分
```

**打分参考**：
- 核心功能都是P0，无冗余 → 20分
- 核心功能是P0，有少量P1/P2 → 15分
- P0/P1功能混合 → 10分
- 大量P2或冗余功能 → 5分

---

#### 问题3：效率提升量化（15分）

**评审问题**：
```
使用这个本体后，预期能节省多少时间/成本？
```

**评分标准**：

| 等级 | 得分 | 标准 | 示例 |
|------|------|------|------|
| ⭐⭐⭐⭐⭐ 优秀 | 15分 | 有明确的量化目标和ROI计算 | "派单时间从2小时→15分钟（↓87.5%），节省3 FTE，ROI回收期6个月" |
| ⭐⭐⭐ 合格 | 9分 | 有方向性预期但未完全量化 | "能减少人工操作，预计节省1-2个人力" |
| ⭐ 不合格 | 0分 | 没有效率提升预期 | "只是把流程电子化" |

**评审工具 - 前后对比表**：

```markdown
| 指标 | 当前（人工） | 目标（系统） | 改善幅度 | 年化价值 |
|------|-------------|-------------|---------|---------|
| 派单平均时长 | 2小时 | 15分钟 | ↓ 87.5% | 节省1800小时/年 |
| 派单错误率 | 15% | 3% | ↓ 80% | 减少返工成本 |
| 人工介入次数 | 100次/天 | 10次/天 | ↓ 90% | 节省2.5 FTE |
| 技师满意度 | 60% | 85%（预期） | ↑ 25% | 降低流失率 |

ROI计算：
- 年节省人力成本：2.5 FTE × 10万/年 = 25万
- 系统开发成本：15万（一次性）
- 年化收益：25万/年
- 投资回报期：15万 / 25万 = 0.6年（7个月）
```

**打分参考**：
- ROI回收期 < 1年 → 15分
- ROI回收期 1-2年 → 10分
- ROI回收期 2-3年 → 5分
- ROI回收期 > 3年或无ROI计算 → 0分

---

#### 问题4：用户采用可行性（15分）

**评审问题**：
```
目标用户会真正使用这个本体吗？有什么阻碍？
```

**评分标准**：

| 等级 | 得分 | 标准 | 示例 |
|------|------|------|------|
| ⭐⭐⭐⭐⭐ 优秀 | 15分 | 已验证用户需求，有推广计划 | "与5个技师访谈确认需求，计划提供2周培训+激励机制" |
| ⭐⭐⭐ 合格 | 9分 | 基于合理假设，但未验证 | "假设技师会用APP接单，因为更方便" |
| ⭐ 不合格 | 0分 | 未考虑用户意愿和能力 | "技师年龄偏大，不习惯用手机，但我们强制推行" |

**评审工具 - 用户画像与障碍分析**：

```markdown
### 用户类型1：调度员

**现有工作方式**：Excel表格手工派单

**采用障碍**：
- 学习成本：需要培训2小时
- 习惯改变：放弃熟悉的Excel
- 信任度：担心系统出错

**解决方案**：
- 提供详细操作手册和视频教程
- 前2周支持双轨运行（Excel+系统）
- 设置回滚按钮增强信任

**采用可行性评估**：⭐⭐⭐⭐ 高（有挑战但可克服）

### 用户类型2：技师

**现有工作方式**：电话接单，纸质记录

**采用障碍**：
- 年龄偏大（平均45岁），不熟悉智能手机
- 工作环境嘈杂，操作需要简单
- 担心系统复杂影响工作效率

**解决方案**：
- APP界面极简化，大按钮设计
- 支持语音输入和拍照上传
- 提供1对1现场培训

**采用可行性评估**：⭐⭐⭐ 中（需要额外支持）

### 综合评估

| 用户类型 | 占比 | 可行性 | 风险等级 |
|---------|------|--------|---------|
| 调度员 | 10% | ⭐⭐⭐⭐ | 低 |
| 技师 | 70% | ⭐⭐⭐ | 中 |
| 审核人 | 20% | ⭐⭐⭐⭐⭐ | 低 |

整体可行性：⭐⭐⭐⭐ 良好（技师群体需要重点支持）
```

**打分参考**：
- 所有用户群体可行性 ≥ ⭐⭐⭐⭐ → 15分
- 主要用户群体可行性 ≥ ⭐⭐⭐ → 10分
- 有用户群体可行性 < ⭐⭐⭐ → 5分
- 未评估用户采用障碍 → 0分

---

#### 问题5：可扩展性与演进（10分）

**评审问题**：
```
3-6个月后需求变化，这个设计能适应吗？
```

**评分标准**：

| 等级 | 得分 | 标准 | 示例 |
|------|------|------|------|
| ⭐⭐⭐⭐⭐ 优秀 | 10分 | 模块化设计，考虑了未来需求 | "预留了与财务系统对接的字段，增加新工单类型只需配置Enum" |
| ⭐⭐⭐ 合格 | 6分 | 能满足当前需求，扩展性一般 | "增加新字段需要改动多处，但可以实现" |
| ⭐ 不合格 | 0分 | 设计僵化，难以修改 | "工单状态写死在代码里，改动需要重构" |

**评审工具 - 未来场景推演**：

```markdown
### 场景1：需要对接第三方配件系统

**当前设计**：
- Function 'check_parts_inventory' 手工查询库存

**需要改动**：
- 增加API连接配置（新增Property）
- 修改Function的库存查询逻辑
- 影响范围：1个Function

**改动成本**：⭐⭐ 中（2天开发）

**评估**：✅ 可接受

---

### 场景2：增加"保养计划"对象类型

**当前设计**：
- 只有"维修工单"一个对象类型

**需要改动**：
- 创建新的ontology配置文件
- 与现有工单对象建立关联
- 影响范围：新对象，不影响现有配置

**改动成本**：⭐ 低（使用ontology-builder skill生成）

**评估**：✅ 易于扩展

---

### 场景3：支持多语言界面

**当前设计**：
- displayName全部是中文硬编码

**需要改动**：
- 需要改造为i18n key-value映射
- 所有displayName需要重构
- 影响范围：所有Property/Function/Action

**改动成本**：⭐⭐⭐⭐ 高（1周开发 + 翻译）

**评估**：⚠️ 成本较高，如果有多语言需求应提前考虑

---

### 综合评估

| 场景 | 发生概率 | 改动成本 | 风险等级 |
|------|---------|---------|---------|
| 对接配件系统 | 高 | ⭐⭐ | 低 |
| 增加保养计划 | 中 | ⭐ | 低 |
| 支持多语言 | 低 | ⭐⭐⭐⭐ | 中 |

整体可扩展性：⭐⭐⭐⭐ 良好（高概率场景易扩展）
```

**打分参考**：
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

### 评审会议流程

#### 会议组织

**参与人员**：
- 业务负责人（决策者）- 必须参加
- 本体创建者（讲解者）- 必须参加
- 技术负责人（可行性评估）- 必须参加
- 目标用户代表（验证需求）- 建议参加

**会议时长**：30-45分钟

**会议议程**：
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

**部署决定**：
- [ ] 批准部署
- [ ] 修改后重审（具体修改要求：_________________）
- [ ] 暂缓（原因：_________________）

**实施优先级**：
- [ ] P0（本季度必须上线）
- [ ] P1（下季度上线）
- [ ] P2（待资源）

**预期上线时间**: _______________________

---

## 风险与应对措施

**识别的风险**：
1. _________________________________________________
2. _________________________________________________

**应对措施**：
1. _________________________________________________
2. _________________________________________________

---

## 签字确认

**业务负责人**: ______________ 日期: __________

**技术负责人**: ______________ 日期: __________

**备注**: _________________________________________________
```

---

## 实施计划

### Phase 1：基础实施（必须完成）

**目标**：建立自动门禁 + 业务门禁的基础框架

**任务列表**：

1. **增强SKILL.md（2小时）**
   - [ ] 修改"Step 4: 质量检查"部分
   - [ ] 实现P0/P1/P2三级检查逻辑
   - [ ] 添加检查失败的引导逻辑
   - [ ] 生成配置后显示完整检查报告

2. **创建validation-guide.md（3小时）**
   - [ ] 两阶段验收标准完整说明
   - [ ] 自动门禁所有检查项详解
   - [ ] 业务门禁5个核心问题
   - [ ] 评审工具（5W1H表、功能价值矩阵等）
   - [ ] 评审会议流程和表模板

3. **更新CLAUDE.md（1小时）**
   - [ ] 记录验收标准设计决策
   - [ ] 更新"质量指标"部分
   - [ ] 添加"验收标准"章节

4. **测试验证（2小时）**
   - [ ] 用现有的4个本体配置测试自动门禁
   - [ ] 修复发现的bug
   - [ ] 完善检查规则

**预计完成时间**：1个工作日

---

### Phase 2：工具增强（可选）

**目标**：提供自动化验证工具

**任务列表**：

1. **创建validation-template.yaml（2小时）**
   - [ ] 编写所有检查规则的YAML定义
   - [ ] 配置评分算法
   - [ ] 添加输出格式配置

2. **开发验证脚本（4小时）**
   - [ ] Python脚本实现规则引擎
   - [ ] 支持console/json/junit输出格式
   - [ ] 添加单元测试

3. **文档和示例（1小时）**
   - [ ] 编写脚本使用文档
   - [ ] 提供示例配置和预期输出

**预计完成时间**：1个工作日

---

### Phase 3：CI/CD集成（可选）

**目标**：集成到自动化流程

**任务列表**：

1. **GitHub Actions配置（2小时）**
   - [ ] 创建validation workflow
   - [ ] PR时自动运行验证
   - [ ] 失败时阻止合并

2. **通知机制（1小时）**
   - [ ] 验证失败时Slack/Email通知
   - [ ] 生成验证报告并上传到artifact

**预计完成时间**：0.5个工作日

---

## 成功指标

### 定量指标

| 指标 | 当前 | 目标 | 测量方法 |
|------|------|------|---------|
| P0缺陷拦截率 | 0% | 100% | 通过自动门禁拦截的P0问题数 / 总P0问题数 |
| 配置返工率 | ? | <20% | 评审后需要修改的配置数 / 总配置数 |
| High Value配置占比 | ? | >60% | High Value配置数 / 总配置数 |
| 评审会议效率 | ? | <45分钟 | 平均会议时长 |

### 定性指标

- [ ] 用户反馈：自动门禁的检查项清晰实用
- [ ] 技术团队反馈：验证脚本易于集成
- [ ] 业务团队反馈：业务门禁评审表易于使用
- [ ] 减少了"技术完美但无人用"的配置

### 验收标准

Phase 1完成后，必须满足：
- [ ] 用现有4个配置测试，自动门禁正常工作
- [ ] validation-guide.md清晰易懂，评审人员能独立使用
- [ ] 完成至少1次真实的业务门禁评审会议

---

## 附录

### 附录A：检查项完整清单

**P0级检查项（8项）**：
1. P0-001: Property数量检查
2. P0-002: Action存在性检查
3. P0-003: 主键定义检查
4. P0-004: Action权限检查
5. P0-005: 高危Action确认检查
6. P0-006: Automation引用Function检查
7. P0-007: Automation引用Action检查
8. P0-008: 循环触发检查

**P1级检查项（7项）**：
1. P1-001: 数字字段单位检查
2. P1-002: 必填字段数量检查
3. P1-003: 字段命名语言检查
4. P1-004: 时序属性配置检查
5. P1-005: Function复杂度检查
6. P1-006: Automation限流检查
7. P1-007: Action前置条件检查

**P2级检查项（4项）**：
1. P2-001: 业务文档检查
2. P2-002: 元数据完整性检查
3. P2-003: Action类型规范检查
4. P2-004: Function使用场景说明检查

**总计**：19项检查

### 附录B：与Gotchas的映射

| Gotcha | 对应检查项 | 级别 |
|--------|----------|------|
| Gotcha #1: 一开始就追求完美 | 业务门禁-问题2（功能价值矩阵） | 业务 |
| Gotcha #2: 混淆Property和Function | 需要人工判断 | - |
| Gotcha #3: Function设计过于复杂 | P1-005: Function复杂度检查 | P1 |
| Gotcha #4: 忘记设置Action前置条件 | P1-007: Action前置条件检查 | P1 |
| Gotcha #5: Automation触发不当 | P1-006: Automation限流检查 | P1 |
| Gotcha #6: Property字段类型选错 | 需要人工判断 | - |
| Gotcha #7: 过度使用时序属性 | P1-004: 时序属性配置检查 | P1 |
| Gotcha #8: 字段命名不清晰 | P1-001, P1-003: 命名检查 | P1 |
| Gotcha #9: 没有充分测试 | 业务门禁-问题4（用户采用） | 业务 |
| Gotcha #10: Automation没有限流 | P1-006: Automation限流检查 | P1 |
| Gotcha #11: 权限控制设置不当 | P0-004: Action权限检查 | P0 |
| Gotcha #19: 配置文件和文档不一致 | P2-001: 业务文档检查 | P2 |

---

**文档结束**

**版本历史**：
- v1.0.0 (2026-03-20) - 初始版本
