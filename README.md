# 🧪 TestCraft - 智能测试用例生成器

> **基于经典软件测试方法论的桌面端自动化测试用例生成工具** —— 让测试更高效、更专业

[![Python](https://img.shields.io/badge/Python-3.13+-blue.svg)](https://www.python.org/)
[![PyQt6](https://img.shields.io/badge/PyQt6-6.11.0-green.svg)](https://www.riverbankcomputing.com/static/Docs/PyQt6/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Platform](https://img.shields.io/badge/Platform-Windows%20|%20macOS%20|%20Linux-lightgrey.svg)]()

---

## 📖 项目简介

TestCraft 是一款现代化的桌面端测试用例自动生成工具，内置 **6 种经典软件测试方法论引擎**，可根据用户定义的功能场景和参数配置，智能推导出全面的测试用例。支持多格式导出、主题切换、统计分析等功能，并提供一键打包为独立可执行文件的能力。

### 核心亮点

| 特性 | 说明 |
|------|------|
| 🧠 **6大测试引擎** | 边界值分析、等价类划分、判定表驱动、状态转换测试、场景法、正交试验法 |
| 🎨 **现代化UI** | PyQt6 打造，支持深色/浅色主题切换，流畅的侧边栏导航 |
| 📤 **多格式导出** | Excel（带优先级颜色标记）、CSV、JSON、pytest/unittest/JUnit/TestNG 代码 |
| 📊 **统计分析** | 实时展示用例数量、优先级分布、测试类型占比等多维数据 |
| 💾 **项目持久化** | 完整的项目保存/加载机制，支持自定义 `.tcproj` 格式 |
| 📦 **一键打包** | PyInstaller 打包为独立 exe，开箱即用 |

## 🏗️ 项目架构

```
TestCraft/
├── main.py                          # 程序入口
├── testcase_generator/
│   ├── __init__.py                  # 包声明 & 版本信息
│   ├── models.py                    # 数据模型 (Project / Scenario / TestCase / ParameterRule)
│   ├── engine.py                    # 测试方法论引擎 (6大引擎 + 统一调度)
│   ├── codegen.py                   # 代码生成器 (pytest / unittest / JUnit / TestNG)
│   ├── exporter.py                  # 多格式导出器 (Excel / CSV / JSON)
│   ├── theme.py                     # 全局样式表 (浅色/深色主题)
│   ├── ui_mainwindow.py             # 主窗口 (集成所有页面)
│   ├── ui_sidebar.py                # 侧边栏导航
│   ├── ui_dashboard.py              # 工作台仪表盘
│   ├── ui_project.py                # 项目管理页面
│   ├── ui_scenario_manager.py       # 场景配置页面
│   ├── ui_case_manager.py           # 用例管理页面
│   ├── ui_export.py                 # 导出中心
│   ├── ui_statistics.py             # 统计分析
│   └── ui_dialogs.py                # 对话框组件
├── assets/
│   ├── testcraft.png                # 应用图标源文件 (1024x1024 PNG)
│   └── testcraft.ico                # 多分辨率应用图标 (16/32/48/64/128/256)
├── build.bat                        # Windows 一键打包脚本
├── build.spec                       # PyInstaller 配置文件
├── generate_icon.py                 # 图标生成脚本
├── requirements.txt                 # 依赖列表
└── README.md                        # 项目文档
```

## 🚀 快速开始

### 环境要求

- Python 3.10+
- Windows / macOS / Linux

### 安装依赖

```bash
pip install -r requirements.txt
```

### 运行程序

```bash
python main.py
```

### 打包为 EXE

```bash
# Windows
build.bat

# 或直接使用 PyInstaller
pyinstaller --name "TestCraft" --windowed --add-data "testcase_generator;testcase_generator" main.py
```

打包完成后，可在 `dist/` 目录找到独立的 `TestCraft.exe` 文件。

## 📋 使用指南

### 第一步：创建项目

在「项目管理」页面输入项目名称、选择目标测试框架（pytest / unittest / JUnit / TestNG）。

### 第二步：配置场景

在「场景配置」页面：

1. 点击「新建场景」添加功能模块
2. 为场景设置名称和描述
3. 添加参数（类型、范围、枚举值等）
4. 选择测试方法论（边界值分析 / 等价类划分 / 判定表驱动等）
5. 点击「预览生成的用例」查看效果

### 第三步：一键生成

点击「一键生成用例」按钮，系统将根据各场景的配置自动推导测试用例。

### 第四步：管理用例

在「用例管理」页面：

- 按场景和优先级筛选用例
- 双击编辑用例详情
- 右键菜单快速操作

### 第五步：导出

在「导出中心」页面选择格式：

| 格式 | 说明 |
|------|------|
| Excel | 带优先级颜色标记的专业测试报告 |
| CSV | 通用逗号分隔格式 |
| JSON | 结构化数据，便于程序处理 |
| pytest 代码 | 可直接运行的 Python 测试代码 |
| unittest 代码 | Python unittest 框架代码 |
| JUnit 代码 | Java JUnit 5 框架代码 |
| TestNG 代码 | Java TestNG 框架代码 |

## 🔬 测试方法论引擎详解

### 1. 边界值分析 (Boundary Value Analysis)

针对每个数值型参数，自动生成最小值、略高于最小值、中间值、略低于最大值、最大值以及越界无效值，覆盖所有边界场景。

**适用场景：** 输入框有明确数值范围的功能（如年龄输入 0-150）

### 2. 等价类划分 (Equivalence Partitioning)

将输入域划分为有效等价类和无效等价类，从每个等价类中选取代表性数据进行测试。

**适用场景：** 表单验证、输入校验等功能

### 3. 判定表驱动 (Decision Table Testing)

将多个布尔条件组合成判定表，生成覆盖所有条件组合的测试用例。

**适用场景：** 折扣计算、权限控制等有多重条件的业务逻辑

### 4. 状态转换测试 (State Transition Testing)

识别系统中的状态和转换规则，生成覆盖所有合法/非法状态转换的测试用例。

**适用场景：** 订单状态流转、审批流程等状态机驱动的功能

### 5. 场景法 (Scenario-Based Testing)

基于基本流（正常路径）和备选流（异常路径）生成测试场景。

**适用场景：** 业务流程测试、端到端功能验证

### 6. 正交试验法 (Orthogonal Experimental Design)

利用正交表 L9(3⁴) 等数学工具，以最少的测试用例覆盖最大的参数组合空间。

**适用场景：** 多参数配置、兼容性测试

## 📊 导出示例

### pytest 代码示例

```python
@pytest.mark.边界值分析
def test_TC_01_001_用户名_最小长度():
    """用户名: 最小长度"""
    # 前置条件: 用户登录功能测试
    # 步骤: 输入 用户名 = abc; 输入 密码 = default
    # 预期结果: 系统正确处理 用户名 的最小长度情况
    ...
```

### Excel 输出示例

| 用例ID | 标题 | 前置条件 | 测试步骤 | 预期结果 | 优先级 |
|--------|------|----------|----------|----------|--------|
| TC-01-001 | 用户名: 最小长度 | 用户登录功能测试 | 输入 用户名 = abc... | 系统正确处理... | 🟢 高 |
| TC-01-002 | 用户名: 空字符串(无效) | 用户登录功能测试 | 输入 用户名 = ... | 系统应拒绝... | 🔴 中 |

## 🛠️ 技术栈

- **GUI 框架：** PyQt6 6.11+
- **打包工具：** PyInstaller 6.x
- **Excel 导出：** openpyxl
- **数据处理：** pandas, numpy
- **图表可视化：** matplotlib, seaborn
- **数据模型：** Python dataclasses
- **样式系统：** QSS (Qt Style Sheets)

## 📄 License

MIT License

## 👨‍💻 作者

刘帅强

---

> ⭐ 如果这个项目对你有帮助，欢迎 Star 支持！
