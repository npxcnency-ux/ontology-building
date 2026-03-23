# 【对象名称】本体配置说明

> **生成时间**: {{generated_time}}
> **业务场景**: {{business_scenario}}
> **使用人员**: {{target_users}}

---

## 📋 配置概览

| 配置项 | 数量 | 说明 |
|--------|------|------|
| 数据字段（Property） | {{property_count}} | {{property_summary}} |
| 计算规则（Function） | {{function_count}} | {{function_summary}} |
| 操作按钮（Action） | {{action_count}} | {{action_summary}} |
| 自动化规则（Automation） | {{automation_count}} | {{automation_summary}} |

---

## 1. 数据字段（Property）

### 1.1 固定信息字段
这些字段通常在对象创建时设置,后续很少变化。

{{#each fixed_properties}}
#### {{name}}
- **类型**: {{type}}
- **说明**: {{description}}
- **示例**: {{example}}
{{#if constraints}}
- **约束**: {{constraints}}
{{/if}}

{{/each}}

### 1.2 变化信息字段
这些字段会根据业务情况更新。

{{#each dynamic_properties}}
#### {{name}}
- **类型**: {{type}}
- **说明**: {{description}}
- **示例**: {{example}}
{{#if update_frequency}}
- **更新频率**: {{update_frequency}}
{{/if}}

{{/each}}

### 1.3 时序追踪字段
这些字段会记录历史变化,可以查看趋势。

{{#each timeseries_properties}}
#### {{name}}
- **类型**: {{type}} (时序)
- **说明**: {{description}}
- **示例**: {{example}}
- **历史保留**: {{retention_period}}
- **为什么需要历史**: {{history_reason}}

{{/each}}

---

## 2. 计算规则（Function）

计算规则会根据数据字段自动计算结果,不需要人工输入。

{{#each functions}}
### 2.{{@index}}. {{name}}

**业务目的**: {{business_purpose}}

**计算逻辑**:
{{logic_description}}

**输入数据**:
{{#each inputs}}
- {{this}}
{{/each}}

**输出结果**: {{output}}

**使用场景**:
{{#each use_cases}}
- {{this}}
{{/each}}

**示例**:
```
{{example_calculation}}
```

---
{{/each}}

## 3. 操作按钮（Action）

操作按钮是用户与系统交互的入口,每个按钮对应一个业务操作。

{{#each actions}}
### 3.{{@index}}. {{name}}

**操作类型**: {{action_type}} (创建/更新/删除/业务操作)

**业务场景**: {{business_scenario}}

{{#if input_fields}}
**需要填写的信息**:
{{#each input_fields}}
- **{{name}}** ({{type}}{{#if required}}, 必填{{/if}}): {{description}}
{{/each}}
{{/if}}

{{#if preconditions}}
**前置条件**:
{{#each preconditions}}
- {{this}}
{{/each}}
{{/if}}

{{#if execution_effects}}
**执行后会发生什么**:
{{#each execution_effects}}
{{@index}}. {{this}}
{{/each}}
{{/if}}

{{#if permissions}}
**谁可以执行**:
{{#each permissions}}
- {{role}}: {{description}}
{{/each}}
{{/if}}

{{#if confirmation_required}}
⚠️ **需要二次确认**: {{confirmation_message}}
{{/if}}

---
{{/each}}

## 4. 自动化规则（Automation）

自动化规则在后台运行,当满足特定条件时自动执行操作。

{{#each automations}}
### 4.{{@index}}. {{name}}

**自动化类型**: {{automation_type}} (异常响应/流程编排/定时任务)

**业务价值**: {{business_value}}

{{#if trigger_condition}}
**触发条件**:
{{trigger_condition}}
{{/if}}

{{#if trigger_schedule}}
**定时执行**: {{trigger_schedule}}
{{/if}}

**自动执行流程**:
{{#each workflow_steps}}
{{@index}}. {{this}}
{{/each}}

{{#if notifications}}
**通知方式**:
{{#each notifications}}
- {{channel}}: {{recipients}} - "{{message}}"
{{/each}}
{{/if}}

{{#if safety_notes}}
⚠️ **安全提示**: {{safety_notes}}
{{/if}}

---
{{/each}}

## 5. 对象关联关系（Links）

本对象与其他业务对象的关联关系。

{{#each links}}
### 5.{{@index}}. {{display_name}}
- **关联对象**: {{target_object_type}}
- **关系类型**: {{link_type}}（一对一/一对多/多对多）
- **业务含义**: {{description}}
{{#if cascading_behavior}}
- **级联行为**: {{cascading_behavior}}
{{/if}}

{{/each}}

---

## 6. 业务流程示意图

{{flow_diagram}}

---

## 7. 典型使用场景

{{#each use_case_scenarios}}
### 7.{{@index}}. {{scenario_name}}

**情况**: {{situation}}

**系统响应**:
{{#each system_responses}}
{{@index}}. {{this}}
{{/each}}

**最终结果**: {{outcome}}

---
{{/each}}

## 8. 部署检查清单

在将此配置部署到理想连山平台前,请确认以下事项:

- [ ] 所有Property的类型和约束已正确配置
- [ ] 所有Function的计算逻辑已验证正确
- [ ] 所有Action的权限规则已设置
- [ ] 所有Automation的触发条件已测试
- [ ] 相关人员已收到培训(如何使用新的操作按钮)
- [ ] 已在测试环境验证完整流程
- [ ] 已准备回滚方案(如果上线后发现问题)

---

## 9. 后续优化建议

{{#if optimization_suggestions}}
{{#each optimization_suggestions}}
- {{this}}
{{/each}}
{{else}}
当前配置已经较为完整。建议在使用过程中收集用户反馈,持续优化。
{{/if}}

---

## 附录: 相关文档

- 技术配置文件: `ontology-config.yaml`
- 平台部署文档: [链接]
- 用户操作手册: [待编写]

---

**文档版本**: 1.0
**最后更新**: {{generated_time}}
**维护负责人**: {{maintainer}}
