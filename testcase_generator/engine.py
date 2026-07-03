"""
测试方法论引擎 - 根据输入参数自动生成测试用例
"""

from __future__ import annotations

import random
import re
from datetime import datetime
from typing import Optional

from .models import (
    ParameterRule,
    ParameterType,
    TestCase,
    TestScenario,
    TestProject,
)


def generate_case_id(scenario_index: int, case_index: int) -> str:
    """生成测试用例ID"""
    return f"TC-{scenario_index + 1:02d}-{case_index + 1:03d}"


class BoundaryValueEngine:
    """边界值分析引擎"""

    METHOD_NAME = "边界值分析"

    @staticmethod
    def analyze(rule: ParameterRule) -> list[dict]:
        """对单个参数进行边界值分析"""
        ptype = rule.param_type
        values = []

        if ptype in ("整数", "浮点数"):
            try:
                if ptype == "整数":
                    min_v = int(rule.min_value) if rule.min_value else None
                    max_v = int(rule.max_value) if rule.max_value else None
                else:
                    min_v = float(rule.min_value) if rule.min_value else None
                    max_v = float(rule.max_value) if rule.max_value else None

                if min_v is not None and max_v is not None:
                    step = 1 if ptype == "整数" else 0.1
                    # 标准边界值：最小、略高于最小、中间、略低于最大、最大
                    near_min = min_v + step
                    mid = min_v + (max_v - min_v) / 2
                    near_max = max_v - step

                    values.append({"value": min_v, "type": "最小值"})
                    values.append({"value": near_min, "type": "略高于最小值"})
                    values.append({"value": mid, "type": "中间值"})
                    values.append({"value": near_max, "type": "略低于最大值"})
                    values.append({"value": max_v, "type": "最大值"})

                    # 越界值
                    values.append({"value": min_v - step, "type": "低于最小值(无效)"})
                    values.append({"value": max_v + step, "type": "高于最大值(无效)"})
                elif min_v is not None:
                    values.append({"value": min_v, "type": "最小值"})
                    values.append({"value": min_v + 1, "type": "略高于最小值"})
                    values.append({"value": min_v - 1, "type": "低于最小值(无效)"})
                elif max_v is not None:
                    values.append({"value": max_v, "type": "最大值"})
                    values.append({"value": max_v - 1, "type": "略低于最大值"})
                    values.append({"value": max_v + 1, "type": "高于最大值(无效)"})
            except (ValueError, TypeError, ZeroDivisionError):
                pass

        elif ptype == "字符串":
            try:
                min_len = int(rule.min_value) if rule.min_value else 0
                max_len = int(rule.max_value) if rule.max_value else 50
                prefix = rule.default_value[:min_len] if rule.default_value else "test"

                values.append({"value": prefix[:min_len], "type": f"最小长度({min_len})"})
                values.append({"value": prefix[:min_len + 1] if min_len > 0 else "a", "type": f"略大于最小长度"})
                values.append({"value": prefix[:max_len], "type": f"最大长度({max_len})"})
                values.append({"value": prefix[:max_len - 1] + "x", "type": f"略小于最大长度"})
                values.append({"value": prefix[:max_len + 1] if max_len > 0 else "abc", "type": f"超过最大长度(无效)"})
                values.append({"value": "", "type": "空字符串(无效)"})
            except (ValueError, TypeError):
                values.append({"value": "normal_text", "type": "正常文本"})
                values.append({"value": "", "type": "空字符串(无效)"})

        elif ptype == "邮箱":
            values.extend([
                {"value": "a@b.com", "type": "最短邮箱格式"},
                {"value": "test@example.com", "type": "正常邮箱"},
                {"value": "user.name+tag@example.co.jp", "type": "复杂邮箱格式"},
                {"value": "@example.com", "type": "缺少用户名(无效)"},
                {"value": "test@", "type": "缺少域名(无效)"},
                {"value": "test@.com", "type": "无效域名(无效)"},
            ])

        elif ptype == "手机号":
            values.extend([
                {"value": "13800138000", "type": "正常手机号"},
                {"value": "13999999999", "type": "最大手机号段"},
                {"value": "13000000000", "type": "最小编号段"},
                {"value": "12800138000", "type": "无效号段(无效)"},
                {"value": "1380013800", "type": "少一位(无效)"},
                {"value": "138001380001", "type": "多一位(无效)"},
            ])

        elif ptype == "日期":
            values.extend([
                {"value": "2020-01-01", "type": "早期日期"},
                {"value": "2024-06-15", "type": "正常日期"},
                {"value": "2099-12-31", "type": "晚期日期"},
                {"value": "invalid", "type": "无效格式(无效)"},
                {"value": "2024-13-01", "type": "无效月份(无效)"},
            ])

        elif ptype == "枚举":
            if rule.enum_values:
                enums = [e.strip() for e in rule.enum_values.split(",") if e.strip()]
                if len(enums) >= 2:
                    values.append({"value": enums[0], "type": "第一个枚举值"})
                    values.append({"value": enums[-1], "type": "最后一个枚举值"})
                    if len(enums) > 2:
                        values.append({"value": enums[len(enums) // 2], "type": "中间枚举值"})
                    values.append({"value": "__invalid__", "type": "不在枚举列表中(无效)"})

        elif ptype == "布尔值":
            values.extend([
                {"value": "true", "type": "真值"},
                {"value": "false", "type": "假值"},
            ])

        if not values:
            values.append({"value": "default", "type": "默认值"})

        return values

    @staticmethod
    def generate(scenario: TestScenario) -> list[TestCase]:
        """根据场景生成边界值测试用例"""
        cases = []
        params = scenario.parameters

        if not params:
            return cases

        # 为每个参数生成边界值组合
        param_values_map = {}
        for i, rule in enumerate(params):
            keys = BoundaryValueEngine.analyze(rule)
            param_values_map[i] = keys

        # 单因子边界值测试：每次只变一个参数
        for pi, pv_list in param_values_map.items():
            for pv in pv_list:
                case = TestCase()
                case.id = generate_case_id(
                    list(param_values_map.keys()).index(pi),
                    list(pv_list).index(pv),
                )
                case.module = scenario.name
                case.title = f"{params[pi].name}: {pv['type']}"
                case.precondition = scenario.description
                steps_parts = []
                for i, rule in enumerate(params):
                    if i == pi:
                        val = pv["value"]
                    else:
                        # 其他参数取默认值
                        val = rule.default_value or "默认值"
                    steps_parts.append(f"输入 {rule.name} = {val}")
                case.steps = "；".join(steps_parts)
                case.expected_result = f"系统正确处理 {params[pi].name} 的 {pv['type']} 情况"
                case.test_type = scenario.method
                case.priority = scenario.priority
                case.tags = scenario.tags
                cases.append(case)

        return cases


class EquivalenceClassEngine:
    """等价类划分引擎"""

    METHOD_NAME = "等价类划分"

    @staticmethod
    def analyze(rule: ParameterRule) -> list[dict]:
        """划分等价类"""
        partitions = []
        ptype = rule.param_type

        if ptype in ("整数", "浮点数"):
            try:
                min_v = rule.min_value
                max_v = rule.max_value
                if min_v and max_v:
                    partitions.extend([
                        {"value": min_v, "class": "有效等价类", "desc": f"等于最小值({min_v})"},
                        {"value": f"({min_v}+{max_v})/2", "class": "有效等价类", "desc": "范围内任意值"},
                        {"value": max_v, "class": "有效等价类", "desc": f"等于最大值({max_v})"},
                        {"value": f"({int(min_v)-1 if min_v.isdigit() else 'min-1'})", "class": "无效等价类", "desc": "小于最小值"},
                        {"value": f"({int(max_v)+1 if max_v.isdigit() else 'max+1'})", "class": "无效等价类", "desc": "大于最大值"},
                    ])
                else:
                    partitions.append({"value": "0", "class": "有效等价类", "desc": "默认值"})
            except Exception:
                partitions.append({"value": "0", "class": "有效等价类", "desc": "默认值"})

        elif ptype == "字符串":
            try:
                min_len = int(rule.min_value) if rule.min_value else 0
                max_len = int(rule.max_value) if rule.max_value else 50
                sample = rule.default_value or "test"
                partitions.extend([
                    {"value": sample[:max_len] if max_len > 0 else "", "class": "有效等价类", f"长度在[{min_len},{max_len}]之间"},
                    {"value": "", "class": "无效等价类", "desc": "空字符串"},
                    {"value": sample + "x" * (max_len + 10), "class": "无效等价类", "desc": f"超过最大长度({max_len})"},
                ])
            except ValueError:
                partitions.append({"value": "test", "class": "有效等价类", "desc": "有效字符串"})

        elif ptype == "邮箱":
            partitions.extend([
                {"value": "valid@email.com", "class": "有效等价类", "desc": "符合格式的邮箱"},
                {"value": "invalid", "class": "无效等价类", "desc": "缺少@符号"},
                {"value": "@email.com", "class": "无效等价类", "desc": "缺少用户名"},
            ])

        elif ptype == "枚举":
            if rule.enum_values:
                enums = [e.strip() for e in rule.enum_values.split(",") if e.strip()]
                for e in enums:
                    partitions.append({"value": e, "class": "有效等价类", "desc": f"枚举值: {e}"})
                partitions.append({"value": "unknown", "class": "无效等价类", "desc": "不在枚举列表中"})

        else:
            partitions.append({"value": rule.default_value or "default", "class": "有效等价类", "desc": "默认值"})

        return partitions

    @staticmethod
    def generate(scenario: TestScenario) -> list[TestCase]:
        """生成等价类测试用例"""
        cases = []
        params = scenario.parameters
        if not params:
            return cases

        partitions_map = {}
        for i, rule in enumerate(params):
            partitions_map[i] = EquivalenceClassEngine.analyze(rule)

        # 有效等价类交叉测试
        valid_partitions = {}
        for i, parts in partitions_map.items():
            valid_partitions[i] = [p for p in parts if p["class"] == "有效等价类"]

        if valid_partitions:
            # 取每个参数的第一个有效等价类组成一条用例
            steps_parts = []
            values = []
            for i, rule in enumerate(params):
                if i in valid_partitions and valid_partitions[i]:
                    val = valid_partitions[i][0]["value"]
                    desc = valid_partitions[i][0]["desc"]
                else:
                    val = rule.default_value or "默认值"
                    desc = "默认值"
                steps_parts.append(f"输入 {rule.name} = {val}")
                values.append(val)

            case = TestCase()
            case.id = generate_case_id(0, len(cases))
            case.module = scenario.name
            case.title = "有效等价类交叉测试"
            case.precondition = scenario.description
            case.steps = "；".join(steps_parts)
            case.expected_result = "所有参数均被正确接受和处理"
            case.test_type = scenario.method
            case.priority = scenario.priority
            case.tags = scenario.tags
            cases.append(case)

        # 无效等价类逐个测试
        invalid_idx = 0
        for i, parts in partitions_map.items():
            for part in parts:
                if part["class"] == "无效等价类":
                    case = TestCase()
                    case.id = generate_case_id(invalid_idx, invalid_idx)
                    case.module = scenario.name
                    case.title = f"无效等价类: {part['desc']}"
                    case.precondition = scenario.description
                    steps_parts = []
                    for j, rule in enumerate(params):
                        if j == i:
                            steps_parts.append(f"输入 {rule.name} = {part['value']}")
                        else:
                            steps_parts.append(f"输入 {rule.name} = {rule.default_value or '默认值'}")
                    case.steps = "；".join(steps_parts)
                    case.expected_result = f"系统应拒绝该输入并提示: {part['desc']}"
                    case.test_type = scenario.method
                    case.priority = scenario.priority
                    case.tags = scenario.tags
                    cases.append(case)
                    invalid_idx += 1

        return cases


class DecisionTableEngine:
    """判定表驱动引擎"""

    METHOD_NAME = "判定表驱动"

    @staticmethod
    def generate(scenario: TestScenario) -> list[TestCase]:
        """根据布尔条件生成判定表用例"""
        cases = []
        params = scenario.parameters
        if len(params) < 2:
            return cases

        # 将参数视为条件（布尔化）
        conditions = []
        for rule in params:
            if rule.param_type in ("整数", "浮点数"):
                try:
                    threshold = float(rule.min_value or "0")
                    conditions.append({
                        "name": rule.name,
                        "condition": f">={threshold}",
                        "true_val": threshold + 1,
                        "false_val": threshold - 1,
                    })
                except (ValueError, TypeError):
                    conditions.append({
                        "name": rule.name,
                        "condition": ">0",
                        "true_val": 1,
                        "false_val": -1,
                    })
            elif rule.param_type == "布尔值":
                conditions.append({
                    "name": rule.name,
                    "condition": "is_true",
                    "true_val": "true",
                    "false_val": "false",
                })
            else:
                conditions.append({
                    "name": rule.name,
                    "condition": "non_empty",
                    "true_val": rule.default_value or "value",
                    "false_val": "",
                })

        # 生成所有组合 (最多16种，超过则采样)
        n = len(conditions)
        max_combinations = min(n, 4)  # 最多4个条件
        total = 2 ** max_combinations
        if total > 16:
            sampled_indices = random.sample(range(total), 16)
        else:
            sampled_indices = list(range(total))

        for idx in sampled_indices:
            case = TestCase()
            case.id = generate_case_id(len(cases) // 4 + 1, len(cases))
            case.module = scenario.name
            case.title = f"判定表组合 #{idx + 1}"

            steps_parts = []
            condition_results = []
            for ci in range(max_combinations):
                bit = (idx >> ci) & 1
                cond = conditions[ci]
                val = cond["true_val"] if bit else cond["false_val"]
                steps_parts.append(f"{cond['name']} {cond['condition']} → {val}")
                condition_results.append(f"C{ci + 1}={'T' if bit else 'F'}")

            case.steps = "；".join(steps_parts)
            case.expected_result = f"根据判定表条件 [{'/'.join(condition_results)}]，系统应执行对应分支"
            case.test_type = scenario.method
            case.priority = scenario.priority
            case.tags = scenario.tags
            cases.append(case)

        return cases


class StateTransitionEngine:
    """状态转换测试引擎"""

    METHOD_NAME = "状态转换测试"

    @staticmethod
    def generate(scenario: TestScenario) -> list[TestCase]:
        """生成状态转换测试用例"""
        cases = []
        params = scenario.parameters

        # 寻找可能的"状态"参数
        state_param = None
        for rule in params:
            if rule.param_type == "枚举" and rule.enum_values:
                enums = [e.strip() for e in rule.enum_values.split(",") if e.strip()]
                if len(enums) >= 2:
                    state_param = rule
                    break

        if not state_param:
            # 退化为场景法
            return ScenarioEngine.generate(scenario)

        states = [e.strip() for e in state_param.enum_values.split(",") if e.strip()]

        # 生成状态间转换的用例
        for i, from_state in enumerate(states):
            for j, to_state in enumerate(states):
                if i == j:
                    continue  # 跳过自转换

                case = TestCase()
                case.id = generate_case_id(i, j)
                case.module = scenario.name
                case.title = f"状态转换: {from_state} → {to_state}"
                case.precondition = f"当前状态: {from_state}"

                steps_parts = []
                for rule in params:
                    if rule == state_param:
                        steps_parts.append(f"设置 {rule.name} = {to_state}")
                    else:
                        steps_parts.append(f"设置 {rule.name} = {rule.default_value or '默认值'}")
                case.steps = "；".join(steps_parts)
                case.expected_result = f"状态应从 '{from_state}' 成功转换为 '{to_state}'"
                case.test_type = scenario.method
                case.priority = scenario.priority
                case.tags = scenario.tags
                cases.append(case)

        # 非法状态转换
        for i, state in enumerate(states):
            case = TestCase()
            case.id = generate_case_id(len(states), i)
            case.module = scenario.name
            case.title = f"非法状态转换测试: {state}"
            case.precondition = f"当前处于非{state}状态"
            case.steps = f"直接设置 {state_param.name} = {state}"
            case.expected_result = "系统应拒绝非法状态转换并给出提示"
            case.test_type = scenario.method
            case.priority = "高"
            case.tags = scenario.tags
            cases.append(case)

        return cases


class ScenarioEngine:
    """场景法测试引擎"""

    METHOD_NAME = "场景法"

    @staticmethod
    def generate(scenario: TestScenario) -> list[TestCase]:
        """根据场景法生成测试用例"""
        cases = []
        params = scenario.parameters

        if not params:
            return cases

        # 基本流（正常场景）
        case = TestCase()
        case.id = generate_case_id(0, 0)
        case.module = scenario.name
        case.title = "基本流程测试"
        case.precondition = scenario.description
        steps_parts = []
        for rule in params:
            steps_parts.append(f"输入 {rule.name} = {rule.default_value or '默认值'}")
        case.steps = "；".join(steps_parts)
        case.expected_result = "业务流程顺利完成"
        case.test_type = scenario.method
        case.priority = "高"
        case.tags = scenario.tags
        cases.append(case)

        # 备选流（异常场景）
        for i, rule in enumerate(params):
            case = TestCase()
            case.id = generate_case_id(1, i)
            case.module = scenario.name
            case.title = f"异常场景: {rule.name}缺失或无效"
            case.precondition = scenario.description
            steps_parts = []
            for j, r in enumerate(params):
                if j == i:
                    if r.required:
                        steps_parts.append(f"不输入 {r.name}（必填项缺失）")
                    else:
                        steps_parts.append(f"输入 {r.name} = 无效值")
                else:
                    steps_parts.append(f"输入 {r.name} = {r.default_value or '默认值'}")
            case.steps = "；".join(steps_parts)
            case.expected_result = f"系统应对 {rule.name} 异常情况进行适当处理并提示用户"
            case.test_type = scenario.method
            case.priority = "中"
            case.tags = scenario.tags
            cases.append(case)

        return cases


class OrthogonalEngine:
    """正交试验法引擎"""

    METHOD_NAME = "正交试验法"

    @staticmethod
    def generate(scenario: TestScenario) -> list[TestCase]:
        """使用正交试验法生成测试用例"""
        cases = []
        params = scenario.parameters
        if len(params) < 2:
            return ScenarioEngine.generate(scenario)

        # 为每个参数确定水平（取值）
        levels = []
        for rule in params:
            if rule.param_type == "枚举" and rule.enum_values:
                enums = [e.strip() for e in rule.enum_values.split(",") if e.strip()]
                levels.append(enums[:5])  # 最多5个水平
            elif rule.param_type in ("整数", "浮点数"):
                try:
                    min_v = float(rule.min_value or "0")
                    max_v = float(rule.max_value or "100")
                    levels.append([min_v, (min_v + max_v) / 2, max_v])
                except (ValueError, TypeError):
                    levels.append(["low", "medium", "high"])
            elif rule.param_type == "布尔值":
                levels.append(["true", "false"])
            elif rule.param_type == "字符串":
                levels.append(["正常文本", "空字符串", "超长文本"])
            else:
                levels.append(["默认值"])

        # 使用简化正交表 L9(3^4) 或更小
        # 根据参数数量选择正交表
        n_params = len(levels)
        if n_params <= 2:
            orthogonal_table = [[0, 0], [0, 1], [0, 2], [1, 0], [1, 1], [1, 2], [2, 0], [2, 1], [2, 2]]
        elif n_params <= 3:
            orthogonal_table = [
                [0, 0, 0], [0, 1, 1], [0, 2, 2],
                [1, 0, 1], [1, 1, 2], [1, 2, 0],
                [2, 0, 2], [2, 1, 0], [2, 2, 1],
            ]
        elif n_params <= 4:
            orthogonal_table = [
                [0, 0, 0, 0], [0, 1, 1, 1], [0, 2, 2, 2],
                [1, 0, 1, 2], [1, 1, 2, 0], [1, 2, 0, 1],
                [2, 0, 2, 1], [2, 1, 0, 2], [2, 2, 1, 0],
            ]
        else:
            # 参数多时取前4个做正交
            orthogonal_table = [
                [0, 0, 0, 0], [0, 1, 1, 1], [0, 2, 2, 2],
                [1, 0, 1, 2], [1, 1, 2, 0], [1, 2, 0, 1],
                [2, 0, 2, 1], [2, 1, 0, 2], [2, 2, 1, 0],
            ]

        for row_idx, row in enumerate(orthogonal_table):
            case = TestCase()
            case.id = generate_case_id(row_idx // 3 + 1, row_idx)
            case.module = scenario.name
            case.title = f"正交组合 #{row_idx + 1}"
            case.precondition = scenario.description

            steps_parts = []
            for pi, level_idx in enumerate(row):
                if pi < len(params):
                    param = params[pi]
                    if level_idx < len(levels[pi]):
                        val = levels[pi][level_idx]
                    else:
                        val = levels[pi][0] if levels[pi] else "默认"
                    steps_parts.append(f"设置 {param.name} = {val}")

            case.steps = "；".join(steps_parts)
            case.expected_result = "系统正确处理该参数组合"
            case.test_type = scenario.method
            case.priority = scenario.priority
            case.tags = scenario.tags
            cases.append(case)

        return cases


# 注册所有引擎
ENGINES = {
    BoundaryValueEngine.METHOD_NAME: BoundaryValueEngine,
    EquivalenceClassEngine.METHOD_NAME: EquivalenceClassEngine,
    DecisionTableEngine.METHOD_NAME: DecisionTableEngine,
    StateTransitionEngine.METHOD_NAME: StateTransitionEngine,
    ScenarioEngine.METHOD_NAME: ScenarioEngine,
    OrthogonalEngine.METHOD_NAME: OrthogonalEngine,
}


def generate_test_cases(scenario: TestScenario) -> list[TestCase]:
    """根据场景自动生成测试用例"""
    method = scenario.method
    engine_class = ENGINES.get(method)
    if engine_class:
        return engine_class.generate(scenario)
    return ScenarioEngine.generate(scenario)


def generate_for_project(project: TestProject) -> TestProject:
    """为项目中所有场景生成测试用例"""
    result = project.duplicate()
    for scenario in result.scenarios:
        scenario.test_cases = generate_test_cases(scenario)
    return result
