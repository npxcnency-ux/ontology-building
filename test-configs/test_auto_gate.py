#!/usr/bin/env python3
"""
自动门禁测试脚本
验证P0/P1/P2检查规则是否正确工作
"""

import yaml
import sys
from pathlib import Path
from typing import Dict, List, Tuple

class AutoGateValidator:
    def __init__(self):
        self.p0_issues = []
        self.p1_issues = []
        self.p2_issues = []

    def load_config(self, file_path) -> Dict:
        """加载YAML配置文件"""
        # 支持str和Path对象
        file_path = Path(file_path) if not isinstance(file_path, Path) else file_path
        with open(file_path, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)

    def check_p0(self, config: Dict) -> None:
        """P0级检查（阻断级）"""

        # P0-1: Property数量检查
        properties = config.get('properties', {})
        if len(properties) < 3:
            self.p0_issues.append(
                f"[P0-1] Property数量不足: 只有{len(properties)}个，至少需要3个核心字段"
            )

        # P0-2: Action存在性检查
        actions = config.get('actions', {})
        if len(actions) < 1:
            self.p0_issues.append(
                "[P0-2] 缺少Action: 至少需要'创建对象'操作"
            )

        # P0-3: 主键定义检查
        primary_key = config.get('objectType', {}).get('primaryKey')
        if not primary_key or len(primary_key) == 0:
            self.p0_issues.append(
                "[P0-3] 未定义primaryKey: 无法唯一标识对象"
            )

        # P0-4: Action权限检查
        for action_name, action_def in actions.items():
            permissions = action_def.get('permissions')
            if not permissions:
                self.p0_issues.append(
                    f"[P0-4] Action '{action_name}' 缺少权限控制"
                )

        # P0-5: 高危Action确认检查
        for action_name, action_def in actions.items():
            action_type = action_def.get('actionType', '').lower()
            confirmation_required = action_def.get('confirmationRequired', False)
            if action_type in ['delete', 'batch'] and not confirmation_required:
                self.p0_issues.append(
                    f"[P0-5] 高危操作 '{action_name}' 缺少二次确认"
                )

        # P0-6: Automation引用Function检查
        automations = config.get('automations', {})
        functions = config.get('functions', {})
        function_names = set(functions.keys())

        for auto_name, auto_def in automations.items():
            trigger = auto_def.get('trigger', {})
            function_name = trigger.get('functionName')
            if function_name and function_name not in function_names:
                self.p0_issues.append(
                    f"[P0-6] Automation '{auto_name}' 引用了不存在的Function '{function_name}'"
                )

        # P0-7: Automation引用Action检查
        action_names = set(actions.keys())
        for auto_name, auto_def in automations.items():
            action_list = auto_def.get('action', [])
            if isinstance(action_list, str):
                action_list = [action_list]
            for action_name in action_list:
                if action_name not in action_names:
                    self.p0_issues.append(
                        f"[P0-7] Automation '{auto_name}' 引用了不存在的Action '{action_name}'"
                    )

        # P0-8: 循环触发检查（简化版，检测直接循环）
        # 完整实现需要构建依赖图并进行DFS
        for auto_name, auto_def in automations.items():
            trigger = auto_def.get('trigger', {})
            if trigger.get('type') == 'onActionComplete':
                trigger_action = trigger.get('actionName')
                auto_actions = auto_def.get('action', [])
                if isinstance(auto_actions, str):
                    auto_actions = [auto_actions]
                # 检查是否有直接循环
                if trigger_action in auto_actions:
                    self.p0_issues.append(
                        f"[P0-8] 检测到潜在循环触发: Automation '{auto_name}' 由 '{trigger_action}' 触发，但又执行 '{trigger_action}'"
                    )

    def check_p1(self, config: Dict) -> None:
        """P1级检查（警告级）"""

        properties = config.get('properties', {})
        functions = config.get('functions', {})
        actions = config.get('actions', {})
        automations = config.get('automations', {})

        # P1-1: 数字字段单位检查
        for prop_name, prop_def in properties.items():
            data_type = prop_def.get('dataType', {})
            type_str = data_type.get('type', '') if isinstance(data_type, dict) else str(data_type)
            display_name = prop_def.get('displayName', '')

            if type_str in ['integer', 'double'] and '(' not in display_name:
                self.p1_issues.append(
                    f"[P1-1] 数字字段 '{prop_name}' 建议包含单位，如 '温度(°C)'"
                )

        # P1-2: 必填字段数量检查
        required_count = sum(1 for p in properties.values() if p.get('required', False))
        if required_count > 7:
            self.p1_issues.append(
                f"[P1-2] 必填字段有{required_count}个，建议≤7个（影响用户体验）"
            )

        # P1-3: 字段命名语言检查（简化版，检查是否全是ASCII）
        for prop_name, prop_def in properties.items():
            display_name = prop_def.get('displayName', '')
            if display_name.isascii() and len(display_name) > 0:
                self.p1_issues.append(
                    f"[P1-3] 字段 '{prop_name}' 建议使用中文业务术语而非英文"
                )

        # P1-4: 时序属性配置检查（简化版）
        for prop_name, prop_def in properties.items():
            data_type = prop_def.get('dataType', {})
            type_str = data_type.get('type', '') if isinstance(data_type, dict) else str(data_type)
            time_series = prop_def.get('timeSeries')

            if type_str == 'timestamp' and time_series is None:
                self.p1_issues.append(
                    f"[P1-4] 字段 '{prop_name}' 未明确是否需要时序追踪"
                )

        # P1-5: Function复杂度检查（简化版，检查logic字段）
        for func_name, func_def in functions.items():
            logic = func_def.get('logic', '')
            if isinstance(logic, str):
                line_count = len(logic.split('\n'))
                if line_count > 100:
                    self.p1_issues.append(
                        f"[P1-5] Function '{func_name}' 逻辑有{line_count}行，建议<100行"
                    )

        # P1-6: Automation限流检查
        for auto_name, auto_def in automations.items():
            rate_limiting = auto_def.get('rateLimiting')
            if not rate_limiting:
                self.p1_issues.append(
                    f"[P1-6] Automation '{auto_name}' 缺少rateLimiting配置"
                )

        # P1-7: Action前置条件检查
        for action_name, action_def in actions.items():
            action_type = action_def.get('actionType', '').lower()
            preconditions = action_def.get('preconditions')
            if action_type in ['update', 'delete'] and not preconditions:
                self.p1_issues.append(
                    f"[P1-7] Action '{action_name}' 缺少preconditions"
                )

        # P1-8: Function异常处理检查（简化版）
        for func_name, func_def in functions.items():
            logic = func_def.get('logic', '')
            if isinstance(logic, str) and 'try' not in logic and 'if' not in logic:
                self.p1_issues.append(
                    f"[P1-8] Function '{func_name}' 的logic中未发现异常处理代码"
                )

    def check_p2(self, config: Dict) -> None:
        """P2级检查（建议级）"""

        functions = config.get('functions', {})
        actions = config.get('actions', {})
        metadata = config.get('metadata', {})
        object_type = config.get('objectType', {})

        # P2-1: 业务文档检查（跳过，这是文件级检查）

        # P2-2: 元数据完整性检查
        business_context = metadata.get('businessContext')
        target_users = metadata.get('targetUsers')
        if not business_context or not target_users:
            self.p2_issues.append(
                "[P2-2] 建议填写businessContext、targetUsers等元数据"
            )

        # P2-3: Action类型规范检查
        standard_types = ['create', 'update', 'delete', 'custom']
        for action_name, action_def in actions.items():
            action_type = action_def.get('actionType', '').lower()
            if action_type and action_type not in standard_types:
                self.p2_issues.append(
                    f"[P2-3] 建议使用标准actionType: create/update/delete/custom (当前: {action_type})"
                )

        # P2-4: Function使用场景说明检查
        for func_name, func_def in functions.items():
            usage_scenarios = func_def.get('usageScenarios')
            if not usage_scenarios:
                self.p2_issues.append(
                    f"[P2-4] 建议为Function '{func_name}' 添加usageScenarios说明"
                )

    def validate(self, file_path) -> Tuple[bool, str]:
        """执行完整验证"""
        try:
            # 支持str和Path对象
            file_path = Path(file_path) if not isinstance(file_path, Path) else file_path
            config = self.load_config(file_path)

            # 执行三级检查
            self.check_p0(config)
            self.check_p1(config)
            self.check_p2(config)

            # 生成报告
            report = self.generate_report(file_path)

            # P0问题阻断
            passed = len(self.p0_issues) == 0

            return passed, report

        except Exception as e:
            return False, f"❌ 配置文件解析失败: {str(e)}"

    def generate_report(self, file_path) -> str:
        """生成测试报告"""
        # 支持str和Path对象
        file_path = Path(file_path) if not isinstance(file_path, Path) else file_path
        lines = []
        lines.append("=" * 80)
        lines.append(f"自动门禁测试报告")
        lines.append(f"配置文件: {file_path.name}")
        lines.append("=" * 80)
        lines.append("")

        # P0检查结果
        lines.append("## P0级检查（阻断级）")
        if self.p0_issues:
            lines.append(f"❌ 发现 {len(self.p0_issues)} 个P0问题，必须修复：")
            for issue in self.p0_issues:
                lines.append(f"   {issue}")
        else:
            lines.append("✅ P0检查全部通过")
        lines.append("")

        # P1检查结果
        lines.append("## P1级检查（警告级）")
        if self.p1_issues:
            lines.append(f"⚠️  发现 {len(self.p1_issues)} 个P1问题，强烈建议修复：")
            for issue in self.p1_issues:
                lines.append(f"   {issue}")
        else:
            lines.append("✅ P1检查全部通过")
        lines.append("")

        # P2检查结果
        lines.append("## P2级检查（建议级）")
        if self.p2_issues:
            lines.append(f"💡 发现 {len(self.p2_issues)} 个P2优化建议：")
            for issue in self.p2_issues:
                lines.append(f"   {issue}")
        else:
            lines.append("✅ P2检查全部通过")
        lines.append("")

        # 总结
        lines.append("=" * 80)
        if len(self.p0_issues) == 0:
            lines.append("✅ 配置通过自动门禁，可以生成！")
        else:
            lines.append("❌ 配置未通过自动门禁，请修复P0问题后重试。")
        lines.append("=" * 80)

        return "\n".join(lines)


def main():
    """主函数"""
    # 获取项目根目录（脚本所在目录的上一级）
    script_dir = Path(__file__).parent
    project_root = script_dir.parent

    # 测试4个现有配置文件（使用绝对路径）
    test_files = [
        project_root / "vehicle-service-ontology-config.yaml",
        project_root / "vehicle-ontology-config.yaml",
        project_root / "technician-ontology-config.yaml",
        project_root / "parts-ontology-config.yaml"
    ]

    print("\n🚦 开始自动门禁测试\n")

    results = []
    for file_path in test_files:
        if not Path(file_path).exists():
            print(f"⚠️  文件不存在: {file_path}\n")
            continue

        validator = AutoGateValidator()
        passed, report = validator.validate(file_path)

        print(report)
        print("\n")

        results.append((Path(file_path).name, passed))

    # 汇总报告
    print("=" * 80)
    print("📊 测试汇总")
    print("=" * 80)
    for file_name, passed in results:
        status = "✅ 通过" if passed else "❌ 失败"
        print(f"{status}  {file_name}")
    print("=" * 80)

    # 返回退出码
    all_passed = all(passed for _, passed in results)
    sys.exit(0 if all_passed else 1)


if __name__ == "__main__":
    main()
