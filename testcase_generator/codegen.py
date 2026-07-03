"""
代码生成器 - 将测试用例导出为各种测试框架的代码
"""

from __future__ import annotations

from .models import TestProject, TestCase, Framework


def generate_pytest(project: TestProject) -> str:
    """生成 pytest 风格测试代码"""
    lines = [
        '"""',
        f"Auto-generated test code by TestCraft",
        f"Project: {project.name}",
        f"Framework: pytest",
        f"Generated: ",
        '"""',
        "",
        "import pytest",
        "",
    ]

    for scenario in project.scenarios:
        if not scenario.test_cases:
            continue

        lines.append("")
        lines.append(f"# {'=' * 60}")
        lines.append(f"# Module: {scenario.name}")
        lines.append(f"# Method: {scenario.method}")
        lines.append(f"# {'=' * 60}")

        # 生成 fixture
        if scenario.parameters:
            lines.append("")
            lines.append(f"@pytest.fixture")
            lines.append(f"def {scenario.name.replace(' ', '_').lower()}_params():")
            lines.append(f'    """测试参数配置"""')
            lines.append(f"    return {{")
            for param in scenario.parameters:
                val = repr(param.default_value or "")
                lines.append(f'        "{param.name}": {val},')
            lines.append(f"    }}")

        # 生成测试函数
        for tc in scenario.test_cases:
            func_name = f"test_{tc.id.replace('-', '_')}_{tc.title[:30].replace(':', '').replace(' ', '_').replace('(', '').replace(')', '')}"
            # 确保函数名合法
            func_name = "".join(c if c.isalnum() or c == '_' else '_' for c in func_name)

            lines.append("")
            lines.append(f"@pytest.mark.{tc.test_type.lower().replace('测试', '')}")
            if tc.priority == "高":
                lines.append("@pytest.mark.slow")
            lines.append(f"def test_{func_name}({scenario.name.replace(' ', '_').lower()}_params):")
            lines.append(f'    """{tc.title}"""')
            lines.append(f'    # 前置条件: {tc.precondition}')
            lines.append(f'    # 步骤: {tc.steps}')
            lines.append(f'    # 预期结果: {tc.expected_result}')
            lines.append(f"    # TODO: 实现测试逻辑")
            lines.append(f"    params = {scenario.name.replace(' ', '_').lower()}_params")
            lines.append(f"    # assert some_function(params) == expected")

    lines.append("")
    lines.append("")
    lines.append('if __name__ == "__main__":')
    lines.append('    pytest.main([__file__, "-v"])')
    lines.append("")

    return "\n".join(lines)


def generate_unittest(project: TestProject) -> str:
    """生成 unittest 风格测试代码"""
    lines = [
        '"""',
        f"Auto-generated test code by TestCraft",
        f"Project: {project.name}",
        f"Framework: unittest",
        f"Generated: ",
        '"""',
        "",
        "import unittest",
        "",
    ]

    for scenario in project.scenarios:
        if not scenario.test_cases:
            continue

        class_name = f"Test{scenario.name.replace(' ', '').title()}"
        class_name = "".join(c if c.isalnum() else '_' for c in class_name)

        lines.append("")
        lines.append(f"class {class_name}(unittest.TestCase):")
        lines.append(f'    """{scenario.description or scenario.name}"""')
        lines.append("")

        for tc in scenario.test_cases:
            method_name = f"test_{tc.id.replace('-', '_')}_{tc.title[:30].replace(':', '').replace(' ', '_')}"
            method_name = "".join(c if c.isalnum() or c == '_' else '_' for c in method_name)

            lines.append(f"    def {method_name}(self):")
            lines.append(f'        """{tc.title}"""')
            lines.append(f'        # 前置条件: {tc.precondition}')
            lines.append(f'        # 步骤: {tc.steps}')
            lines.append(f'        # 预期结果: {tc.expected_result}')
            lines.append(f"        # TODO: 实现测试逻辑")
            lines.append(f"        self.skipTest('待实现')")
            lines.append("")

    lines.append("")
    lines.append("")
    lines.append('if __name__ == "__main__":')
    lines.append("    unittest.main()")
    lines.append("")

    return "\n".join(lines)


def generate_junit(project: TestProject) -> str:
    """生成 JUnit 5 风格测试代码"""
    lines = [
        "package test;",
        "",
        "import org.junit.jupiter.api.Test;",
        "import org.junit.jupiter.api.DisplayName;",
        "import org.junit.jupiter.api.BeforeEach;",
        "import static org.junit.jupiter.api.Assertions.*;",
        "",
    ]

    for scenario in project.scenarios:
        if not scenario.test_cases:
            continue

        class_name = f"{scenario.name.replace(' ', '').title()}Test"
        class_name = "".join(c if c.isalnum() else '_' for c in class_name)

        lines.append("")
        lines.append(f"@DisplayName(\"{scenario.name}\")")
        lines.append(f"class {class_name} {{")

        for tc in scenario.test_cases:
            method_name = f"{tc.id.replace('-', '_')}_{tc.title[:30].replace(':', '').replace(' ', '_')}"
            method_name = "".join(c if c.isalnum() or c == '_' else '_' for c in method_name)

            lines.append("")
            lines.append(f'    @Test')
            lines.append(f'    @DisplayName("{tc.title}")')
            lines.append(f"    void {method_name}() {{")
            lines.append(f'        // 前置条件: {tc.precondition}')
            lines.append(f'        // 步骤: {tc.steps}')
            lines.append(f'        // 预期结果: {tc.expected_result}')
            lines.append(f"        // TODO: 实现测试逻辑")
            lines.append(f"        assertTrue(true);")
            lines.append(f"    }}")

        lines.append("")
        lines.append("}")

    lines.append("")
    return "\n".join(lines)


def generate_testng(project: TestProject) -> str:
    """生成 TestNG 风格测试代码"""
    lines = [
        "package test;",
        "",
        "import org.testng.annotations.Test;",
        "import org.testng.annotations.BeforeMethod;",
        "import org.testng.Assert;",
        "",
    ]

    for scenario in project.scenarios:
        if not scenario.test_cases:
            continue

        class_name = f"{scenario.name.replace(' ', '').title()}Test"
        class_name = "".join(c if c.isalnum() else '_' for c in class_name)

        lines.append("")
        lines.append(f"class {class_name} {{")

        for tc in scenario.test_cases:
            method_name = f"{tc.id.replace('-', '_')}_{tc.title[:30].replace(':', '').replace(' ', '_')}"
            method_name = "".join(c if c.isalnum() or c == '_' else '_' for c in method_name)

            lines.append("")
            lines.append(f'    @Test(description = "{tc.title}", groups = {{{repr(tc.test_type)}}})')
            lines.append(f"    public void {method_name}() {{")
            lines.append(f'        // 前置条件: {tc.precondition}')
            lines.append(f'        // 步骤: {tc.steps}')
            lines.append(f'        // 预期结果: {tc.expected_result}')
            lines.append(f"        // TODO: 实现测试逻辑")
            lines.append(f"        Assert.assertTrue(true);")
            lines.append(f"    }}")

        lines.append("")
        lines.append("}")

    lines.append("")
    return "\n".join(lines)


FRAMEWORK_GENERATORS = {
    Framework.PYTEST.value: generate_pytest,
    Framework.UNITTEST.value: generate_unittest,
    Framework.JUNIT.value: generate_junit,
    Framework.TESTNG.value: generate_testng,
}


def generate_code(project: TestProject, framework: str = "pytest") -> str:
    """根据框架生成测试代码"""
    generator = FRAMEWORK_GENERATORS.get(framework)
    if generator:
        return generator(project)
    return generate_pytest(project)
