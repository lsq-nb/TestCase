"""
示例数据生成器 - 预置演示项目
"""

from __future__ import annotations

from datetime import datetime

from .models import TestProject, ParameterRule, TestScenario


def create_demo_project() -> TestProject:
    """创建一个包含完整示例数据的演示项目"""
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    project = TestProject(
        name="电商用户系统测试",
        description="某电商平台用户管理模块的自动化测试用例生成项目",
        version="1.0",
        target_framework="pytest",
        created_at=now,
        updated_at=now,
    )

    # 场景1: 用户注册
    reg_scenario = TestScenario(
        name="用户注册",
        description="测试用户注册功能的完整流程",
        method="边界值分析",
        priority="高",
        tags="注册,安全",
        parameters=[
            ParameterRule(
                name="用户名",
                description="用户注册时的登录名",
                param_type="字符串",
                required=True,
                min_value="3",
                max_value="20",
                default_value="testuser",
            ),
            ParameterRule(
                name="密码",
                description="用户设置的登录密码",
                param_type="字符串",
                required=True,
                min_value="6",
                max_value="32",
                default_value="password123",
            ),
            ParameterRule(
                name="邮箱",
                description="用于接收验证邮件的邮箱地址",
                param_type="邮箱",
                required=True,
                default_value="user@example.com",
            ),
            ParameterRule(
                name="手机号",
                description="绑定手机号码",
                param_type="手机号",
                required=False,
                default_value="13800138000",
            ),
        ],
    )

    # 场景2: 用户登录
    login_scenario = TestScenario(
        name="用户登录",
        description="测试用户登录功能的各种场景",
        method="等价类划分",
        priority="高",
        tags="登录,安全",
        parameters=[
            ParameterRule(
                name="用户名",
                description="登录用户名",
                param_type="字符串",
                required=True,
                min_value="3",
                max_value="20",
                default_value="testuser",
            ),
            ParameterRule(
                name="密码",
                description="登录密码",
                param_type="字符串",
                required=True,
                min_value="6",
                max_value="32",
                default_value="password123",
            ),
            ParameterRule(
                name="验证码",
                description="图形验证码",
                param_type="字符串",
                required=True,
                min_value="4",
                max_value="6",
                default_value="ABCD",
            ),
        ],
    )

    # 场景3: 订单状态管理
    order_scenario = TestScenario(
        name="订单状态管理",
        description="测试订单在不同状态间的转换",
        method="状态转换测试",
        priority="高",
        tags="订单,状态机",
        parameters=[
            ParameterRule(
                name="订单状态",
                description="当前订单状态",
                param_type="枚举",
                required=True,
                enum_values="待支付,已支付,发货中,已发货,已完成,已取消,已退款",
                default_value="待支付",
            ),
            ParameterRule(
                name="操作类型",
                description="对订单执行的操作",
                param_type="枚举",
                required=True,
                enum_values="支付,发货,签收,取消,申请退款",
                default_value="支付",
            ),
        ],
    )

    # 场景4: 商品搜索
    search_scenario = TestScenario(
        name="商品搜索",
        description="测试商品搜索功能的排序和筛选",
        method="正交试验法",
        priority="中",
        tags="搜索,性能",
        parameters=[
            ParameterRule(
                name="关键词",
                description="搜索关键词",
                param_type="字符串",
                required=True,
                min_value="1",
                max_value="50",
                default_value="手机",
            ),
            ParameterRule(
                name="排序方式",
                description="搜索结果排序方式",
                param_type="枚举",
                required=False,
                enum_values="综合,销量,价格,好评率",
                default_value="综合",
            ),
            ParameterRule(
                name="价格区间",
                description="价格范围过滤",
                param_type="整数",
                required=False,
                min_value="0",
                max_value="99999",
                default_value="0",
            ),
            ParameterRule(
                name="页码",
                description="分页页码",
                param_type="整数",
                required=False,
                min_value="1",
                max_value="1000",
                default_value="1",
            ),
        ],
    )

    # 场景5: 用户评价
    review_scenario = TestScenario(
        name="用户评价",
        description="测试商品评价功能的完整性",
        method="判定表驱动",
        priority="中",
        tags="评价,社交",
        parameters=[
            ParameterRule(
                name="评分",
                description="用户对商品的评分",
                param_type="整数",
                required=True,
                min_value="1",
                max_value="5",
                default_value="5",
            ),
            ParameterRule(
                name="评价内容",
                description="用户填写的评价文字",
                param_type="字符串",
                required=False,
                min_value="0",
                max_value="1000",
                default_value="很好用",
            ),
            ParameterRule(
                name="是否匿名",
                description="匿名评价开关",
                param_type="布尔值",
                required=False,
                default_value="false",
            ),
            ParameterRule(
                name="是否上传图片",
                description="评价附带图片",
                param_type="布尔值",
                required=False,
                default_value="false",
            ),
        ],
    )

    project.scenarios = [
        reg_scenario,
        login_scenario,
        order_scenario,
        search_scenario,
        review_scenario,
    ]

    return project
