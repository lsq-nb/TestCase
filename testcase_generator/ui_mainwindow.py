"""
主窗口 - 整合所有功能模块
"""

from __future__ import annotations

import sys
from datetime import datetime

from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QStackedWidget, QLabel, QToolBar,
    QFileDialog, QMessageBox, QSplitter, QStatusBar,
    QPushButton,
)
from PyQt6.QtCore import Qt, QSize, QTimer
from PyQt6.QtGui import QFont, QIcon, QAction

from testcase_generator.models import TestProject
from testcase_generator.theme import LIGHT_THEME, DARK_THEME
from testcase_generator.ui_sidebar import Sidebar
from testcase_generator.ui_dashboard import DashboardPage
from testcase_generator.ui_project import ProjectPage
from testcase_generator.ui_scenario_manager import ScenarioManagerPage
from testcase_generator.ui_case_manager import CaseManagerPage
from testcase_generator.ui_export import ExportPage
from testcase_generator.ui_statistics import StatisticsPage


class MainWindow(QMainWindow):
    """主窗口"""

    def __init__(self):
        super().__init__()
        self.project: TestProject | None = None
        self.dark_mode = False
        self._init_ui()
        self._create_project_if_needed()

    def _init_ui(self):
        """初始化UI"""
        self.setWindowTitle("TestCraft - 智能测试用例生成器 v1.0")
        self.setMinimumSize(1200, 800)
        self.resize(1400, 900)

        # 设置窗口图标（使用emoji作为占位）
        self.setWindowIconFromText("🧪")

        # 创建中央部件
        central = QWidget()
        self.setCentralWidget(central)

        # 主布局：垂直排列顶部栏 + 内容区
        main_layout = QVBoxLayout(central)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # 顶部栏（先创建，以便 apply_theme 能找到 theme_btn）
        self._create_topbar()
        main_layout.addWidget(self.topbar_widget)

        # 内容区：侧边栏 + 页面堆叠
        content_splitter = QSplitter(Qt.Orientation.Horizontal)

        # 侧边栏
        self.sidebar = Sidebar()
        self.sidebar.page_changed.connect(self._navigate)
        content_splitter.addWidget(self.sidebar)

        # 堆叠页面
        self.stack = QStackedWidget()
        self._pages: dict[str, QWidget] = {}

        # 创建各页面
        self.dashboard_page = DashboardPage()
        self.dashboard_page.navigate.connect(self._handle_quick_action)
        self.stack.addWidget(self.dashboard_page)
        self._pages["dashboard"] = self.dashboard_page

        self.project_page = ProjectPage()
        self.project_page.project_created.connect(self._on_project_created)
        self.stack.addWidget(self.project_page)
        self._pages["project"] = self.project_page

        self.scenario_page = ScenarioManagerPage()
        self.scenario_page.scenario_changed.connect(self._on_scenario_changed)
        self.stack.addWidget(self.scenario_page)
        self._pages["scenario"] = self.scenario_page

        self.case_page = CaseManagerPage()
        self.stack.addWidget(self.case_page)
        self._pages["cases"] = self.case_page

        self.export_page = ExportPage()
        self.stack.addWidget(self.export_page)
        self._pages["export"] = self.export_page

        self.stats_page = StatisticsPage()
        self.stack.addWidget(self.stats_page)
        self._pages["statistics"] = self.stats_page

        content_splitter.addWidget(self.stack)
        content_splitter.setStretchFactor(1, 1)
        main_layout.addWidget(content_splitter)

        # 应用主题（此时 theme_btn 已创建）
        self.apply_theme()

        # 状态栏
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_label = QLabel("就绪")
        self.status_bar.addPermanentWidget(self.status_label)
        self.time_label = QLabel()
        self.status_bar.addPermanentWidget(self.time_label)
        self._update_time()

        # 初始页面
        self._navigate("dashboard")

    def setWindowIconFromText(self, text: str):
        """使用emoji设置窗口图标（临时方案）"""
        # PyQt6在Windows上无法直接用emoji做图标，这里设置标题
        pass

    def _create_topbar(self):
        """创建顶部栏"""
        self.topbar_widget = QWidget()
        self.topbar_widget.setObjectName("topbar")
        topbar_layout = QHBoxLayout(self.topbar_widget)
        topbar_layout.setContentsMargins(16, 8, 16, 8)

        self.topbar_title = QLabel("🧪 TestCraft")
        self.topbar_title.setFont(QFont("Microsoft YaHei UI", 16, QFont.Weight.Bold))
        topbar_layout.addWidget(self.topbar_title)

        topbar_layout.addStretch()

        # 主题切换按钮
        self.theme_btn = QPushButton("🌙 深色模式")
        self.theme_btn.setFlat(True)
        self.theme_btn.setFixedHeight(32)
        self.theme_btn.clicked.connect(self._toggle_theme)
        topbar_layout.addWidget(self.theme_btn)

        # 帮助按钮
        help_btn = QPushButton("❓ 帮助")
        help_btn.setFlat(True)
        help_btn.setFixedHeight(32)
        help_btn.clicked.connect(self._show_help)
        topbar_layout.addWidget(help_btn)

    def _navigate(self, page_id: str):
        """导航到指定页面"""
        self.sidebar.select_page(page_id)
        self.stack.setCurrentWidget(self._pages[page_id])
        self._update_status()

    def _handle_quick_action(self, action_id: str):
        """处理快捷操作"""
        if action_id == "new_project":
            self._navigate("project")
        elif action_id == "add_scenario":
            self._navigate("scenario")
        elif action_id == "generate_all":
            self._navigate("scenario")
            # 触发场景页面的生成
            self.scenario_page._generate_cases()
        elif action_id == "export":
            self._navigate("export")

    def _create_project_if_needed(self):
        """如果还没有项目，创建一个示例项目"""
        from datetime import datetime
        self.project = TestProject(
            name="示例项目",
            description="这是一个示例项目，展示了TestCraft的功能。",
            version="1.0",
            target_framework="pytest",
            created_at=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            updated_at=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        )
        self._update_all_pages()

    def _on_project_created(self, project: TestProject):
        """项目创建回调"""
        self.project = project
        self._update_all_pages()
        self.status_label.setText(f"项目: {project.name}")

    def _on_scenario_changed(self):
        """场景变更回调"""
        if self.project:
            self.project.updated_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        # 只在场景变更时更新页面，但不要用旧 project 覆盖 ScenarioManagerPage 的 project
        self._update_all_pages()

    def _update_all_pages(self):
        """更新所有页面的数据和引用"""
        if not self.project:
            return

        # 更新各页面的项目引用
        self.project_page.set_project(self.project)
        self.scenario_page.set_project(self.project)
        self.case_page.set_project(self.project)
        self.export_page.set_project(self.project)
        self.stats_page.set_project(self.project)
        self.dashboard_page.update_stats()

        # 更新侧边栏高亮
        if self.project.total_test_cases > 0:
            self.sidebar.highlight_new(self.project.total_test_cases)

    def _update_status(self):
        """更新状态栏"""
        if self.project:
            self.status_label.setText(
                f"项目: {self.project.name} | "
                f"模块: {self.project.total_scenarios} | "
                f"用例: {self.project.total_test_cases}"
            )

    def _toggle_theme(self):
        """切换主题"""
        self.dark_mode = not self.dark_mode
        self.apply_theme()

    def apply_theme(self):
        """应用主题"""
        theme = DARK_THEME if self.dark_mode else LIGHT_THEME
        self.setStyleSheet(theme)

        if self.dark_mode:
            self.theme_btn.setText("☀️ 浅色模式")
        else:
            self.theme_btn.setText("🌙 深色模式")

    def _show_help(self):
        """显示帮助"""
        help_text = (
            "🧪 TestCraft - 智能测试用例生成器 v1.0\n\n"
            "使用指南：\n\n"
            "1️⃣ 项目管理：创建或加载测试项目\n"
            "2️⃣ 场景配置：添加功能模块，设置参数和测试方法\n"
            "3️⃣ 用例管理：查看和管理生成的测试用例\n"
            "4️⃣ 导出中心：导出为Excel/CSV/JSON或测试代码\n"
            "5️⃣ 统计分析：查看用例统计和分布\n\n"
            "支持的测试方法：\n"
            "• 边界值分析\n"
            "• 等价类划分\n"
            "• 判定表驱动\n"
            "• 状态转换测试\n"
            "• 场景法\n"
            "• 正交试验法\n\n"
            "支持的导出框架：\n"
            "• pytest / unittest (Python)\n"
            "• JUnit / TestNG (Java)\n"
        )
        QMessageBox.information(self, "帮助", help_text)

    def _update_time(self):
        """更新时间显示"""
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.time_label.setText(now)
        QTimer.singleShot(1000, self._update_time)
