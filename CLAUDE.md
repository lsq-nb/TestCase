# TestCraft - 智能测试用例生成器
# 项目开发说明

## 项目概述
桌面端测试用例自动生成工具，基于 PyQt6 构建现代化 UI。

## 核心模块

### models.py
数据模型层，定义了 TestProject、TestScenario、TestCase、ParameterRule 等核心数据结构。
使用 Python dataclasses 实现，支持序列化/反序列化。

### engine.py
测试方法论引擎层，实现了6种经典测试方法：
- BoundaryValueEngine: 边界值分析
- EquivalenceClassEngine: 等价类划分  
- DecisionTableEngine: 判定表驱动
- StateTransitionEngine: 状态转换测试
- ScenarioEngine: 场景法
- OrthogonalEngine: 正交试验法

### codegen.py
代码生成器，将测试用例转换为可执行的测试代码：
- pytest 风格
- unittest 风格
- JUnit 5 风格
- TestNG 风格

### exporter.py
导出器，支持多种文件格式：
- Excel (openpyxl) - 带样式和颜色标记
- CSV (UTF-8 with BOM)
- JSON

### theme.py
全局样式表，定义浅色和深色两套 QSS 主题。

### UI 模块
- ui_mainwindow.py: 主窗口，集成所有页面
- ui_sidebar.py: 左侧导航栏
- ui_dashboard.py: 工作台仪表盘
- ui_project.py: 项目管理
- ui_scenario_manager.py: 场景配置与管理
- ui_case_manager.py: 用例查看与管理
- ui_export.py: 导出中心
- ui_statistics.py: 统计分析
- ui_dialogs.py: 场景配置对话框和参数编辑器

## 开发命令
```bash
# 运行
python main.py

# 打包
pyinstaller --name "TestCraft" --windowed --add-data "testcase_generator;testcase_generator" main.py

# 或
build.bat
```

## 扩展建议
1. 添加更多测试引擎（如随机测试、探索性测试）
2. 支持自定义模板导出
3. 添加测试用例去重和合并功能
4. 支持团队协作（云端存储）
5. 添加测试覆盖率分析功能
