"""
数据模型定义
"""

from __future__ import annotations

from dataclasses import dataclass, field, asdict
from enum import Enum
from typing import Optional
import json
from copy import deepcopy


class TestCaseType(Enum):
    """测试用例类型"""
    FUNCTIONAL = "功能测试"
    BOUNDARY = "边界值测试"
    EQUIVALENCE = "等价类测试"
    DECISION_TABLE = "判定表测试"
    STATE_TRANSITION = "状态转换测试"
    SCENARIO = "场景测试"
    ORTHOGONAL = "正交试验测试"


class Framework(Enum):
    """测试框架"""
    PYTEST = "pytest"
    UNITTEST = "unittest"
    JUNIT = "JUnit"
    TESTNG = "TestNG"


class ParameterType(Enum):
    """参数数据类型"""
    STRING = "字符串"
    INTEGER = "整数"
    FLOAT = "浮点数"
    BOOLEAN = "布尔值"
    EMAIL = "邮箱"
    PHONE = "手机号"
    DATE = "日期"
    ENUM = "枚举"


@dataclass
class ParameterRule:
    """参数规则定义"""
    name: str = ""
    description: str = ""
    param_type: str = "字符串"
    required: bool = True
    min_value: Optional[str] = None
    max_value: Optional[str] = None
    enum_values: str = ""  # 逗号分隔
    regex_pattern: str = ""
    default_value: str = ""
    valid_range_desc: str = ""  # 有效范围描述
    invalid_range_desc: str = ""  # 无效范围描述

    def to_dict(self) -> dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict) -> ParameterRule:
        return cls(**data)


@dataclass
class TestCase:
    """单个测试用例"""
    id: str = ""
    module: str = ""
    title: str = ""
    precondition: str = ""
    steps: str = ""
    expected_result: str = ""
    priority: str = "中"  # 高/中/低
    test_type: str = "功能测试"
    tags: str = ""
    notes: str = ""

    def to_dict(self) -> dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict) -> TestCase:
        return cls(**data)


@dataclass
class TestScenario:
    """测试场景（对应一个功能模块）"""
    name: str = ""
    description: str = ""
    parameters: list[ParameterRule] = field(default_factory=list)
    test_cases: list[TestCase] = field(default_factory=list)
    method: str = "边界值分析"  # 使用的测试方法
    priority: str = "中"
    tags: str = ""

    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "description": self.description,
            "parameters": [p.to_dict() for p in self.parameters],
            "test_cases": [tc.to_dict() for tc in self.test_cases],
            "method": self.method,
            "priority": self.priority,
            "tags": self.tags,
        }

    @classmethod
    def from_dict(cls, data: dict) -> TestScenario:
        return cls(
            name=data.get("name", ""),
            description=data.get("description", ""),
            parameters=[ParameterRule.from_dict(p) for p in data.get("parameters", [])],
            test_cases=[TestCase.from_dict(tc) for tc in data.get("test_cases", [])],
            method=data.get("method", "边界值分析"),
            priority=data.get("priority", "中"),
            tags=data.get("tags", ""),
        )


@dataclass
class TestProject:
    """测试项目"""
    name: str = ""
    description: str = ""
    version: str = "1.0"
    scenarios: list[TestScenario] = field(default_factory=list)
    target_framework: str = "pytest"
    created_at: str = ""
    updated_at: str = ""

    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "description": self.description,
            "version": self.version,
            "scenarios": [s.to_dict() for s in self.scenarios],
            "target_framework": self.target_framework,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }

    @classmethod
    def from_dict(cls, data: dict) -> TestProject:
        return cls(
            name=data.get("name", ""),
            description=data.get("description", ""),
            version=data.get("version", "1.0"),
            scenarios=[TestScenario.from_dict(s) for s in data.get("scenarios", [])],
            target_framework=data.get("target_framework", "pytest"),
            created_at=data.get("created_at", ""),
            updated_at=data.get("updated_at", ""),
        )

    @property
    def total_test_cases(self) -> int:
        return sum(len(s.test_cases) for s in self.scenarios)

    @property
    def total_scenarios(self) -> int:
        return len(self.scenarios)

    def duplicate(self) -> TestProject:
        return TestProject.from_dict(deepcopy(self.to_dict()))
