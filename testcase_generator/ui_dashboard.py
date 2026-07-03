"""
仪表盘页面
"""

from __future__ import annotations

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QFrame, QGridLayout, QPushButton, QSpacerItem,
    QSizePolicy,
)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont

from testcase_generator.models import TestProject


class StatCard(QFrame):
    """统计卡片"""

    def __init__(self, icon: str, title: str, value: str | int, color: str = "#3498DB", parent=None):
        super().__init__(parent)
        self.setObjectName("card")
        self.setMinimumHeight(120)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 16, 20, 16)
        layout.setSpacing(8)

        # 图标和标题行
        top_layout = QHBoxLayout()
        icon_label = QLabel(icon)
        icon_label.setFont(QFont("Microsoft YaHei UI", 28))
        top_layout.addWidget(icon_label)
        top_layout.addStretch()

        color_dot = QLabel()
        color_dot.setFixedWidth(6)
        color_dot.setFixedHeight(40)
        color_dot.setStyleSheet(f"background-color: {color}; border-radius: 3px;")
        top_layout.addWidget(color_dot)
        layout.addLayout(top_layout)

        # 数值
        value_label = QLabel(str(value))
        value_label.setFont(QFont("Microsoft YaHei UI", 28, QFont.Weight.Bold))
        value_label.setStyleSheet(f"color: {color};")
        value_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(value_label)

        # 标题
        title_label = QLabel(title)
        title_label.setFont(QFont("Microsoft YaHei UI", 11))
        title_label.setStyleSheet("color: #7F8C8D;")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title_label)


class QuickActionCard(QFrame):
    """快捷操作卡片"""

    clicked = pyqtSignal()
    action_triggered = pyqtSignal(str)

    def __init__(self, icon: str, title: str, action_id: str, parent=None):
        super().__init__(parent)
        self.setObjectName("card")
        self.action_id = action_id
        self.setMinimumHeight(80)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(16, 12, 16, 12)
        layout.setSpacing(12)

        icon_label = QLabel(icon)
        icon_label.setFont(QFont("Microsoft YaHei UI", 24))
        layout.addWidget(icon_label)

        text_layout = QVBoxLayout()
        title_label = QLabel(title)
        title_label.setFont(QFont("Microsoft YaHei UI", 13, QFont.Weight.Bold))
        text_layout.addWidget(title_label)
        text_layout.addStretch()
        layout.addLayout(text_layout)

        arrow = QLabel("→")
        arrow.setFont(QFont("Microsoft YaHei UI", 16))
        arrow.setStyleSheet("color: #BDC3C7;")
        layout.addWidget(arrow)

        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.clicked.connect(lambda: self.action_triggered.emit(action_id))

    def mousePressEvent(self, event):
        self.action_triggered.emit(self.action_id)
        super().mousePressEvent(event)


class DashboardPage(QWidget):
    """工作台页面"""

    navigate = pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.project: TestProject | None = None
        self._init_ui()

    def _init_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(20)

        # 欢迎区域
        welcome = QLabel("欢迎使用 TestCraft ✨")
        welcome.setFont(QFont("Microsoft YaHei UI", 22, QFont.Weight.Bold))
        welcome.setAlignment(Qt.AlignmentFlag.AlignCenter)
        welcome.setStyleSheet("color: #2C3E50; padding: 10px;")
        layout.addWidget(welcome)

        subtitle = QLabel("智能测试用例生成器 — 让测试更高效、更专业")
        subtitle.setFont(QFont("Microsoft YaHei UI", 12))
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        subtitle.setStyleSheet("color: #7F8C8D; padding: 5px;")
        layout.addWidget(subtitle)

        # 统计卡片
        stats_grid = QGridLayout()
        stats_grid.setSpacing(16)

        self.cards = [
            StatCard("📁", "功能模块", 0, "#3498DB"),
            StatCard("🧪", "测试用例", 0, "#2ECC71"),
            StatCard("🔥", "高优先级", 0, "#E74C3C"),
            StatCard("✅", "已覆盖", 0, "#F39C12"),
        ]

        for i, card in enumerate(self.cards):
            col = i % 4
            row = 0
            stats_grid.addWidget(card, row, col)

        layout.addLayout(stats_grid)

        # 快捷操作
        actions_title = QLabel("快捷操作")
        actions_title.setFont(QFont("Microsoft YaHei UI", 16, QFont.Weight.Bold))
        actions_title.setStyleSheet("color: #2C3E50; padding: 8px 0 4px;")
        layout.addWidget(actions_title)

        actions_grid = QGridLayout()
        actions_grid.setSpacing(12)

        actions = [
            ("📝", "新建测试项目", "new_project"),
            ("➕", "添加功能场景", "add_scenario"),
            ("🤖", "一键生成用例", "generate_all"),
            ("📤", "导出测试报告", "export"),
        ]

        self.action_cards = []
        for i, (icon, title, action_id) in enumerate(actions):
            card = QuickActionCard(icon, title, action_id)
            card.action_triggered.connect(self._on_action)
            col = i % 2
            row = i // 2
            actions_grid.addWidget(card, row, col)
            self.action_cards.append(card)

        layout.addLayout(actions_grid)

        # 底部提示
        tip = QLabel(
            "💡 提示：先在「项目管理」中创建场景，然后在「场景配置」中添加参数，"
            "最后点击「一键生成用例」即可自动根据测试方法论生成测试用例。"
        )
        tip.setFont(QFont("Microsoft YaHei UI", 11))
        tip.setStyleSheet("color: #7F8C8D; background-color: #EBF5FB; border-radius: 8px; padding: 12px;")
        tip.setWordWrap(True)
        layout.addWidget(tip)

        layout.addStretch()

    def update_stats(self):
        """更新统计数字"""
        if not self.project:
            return

        total_cases = self.project.total_test_cases
        total_scenarios = self.project.total_scenarios
        high_priority = sum(
            1 for s in self.project.scenarios for tc in s.test_cases if tc.priority == "高"
        )
        covered = sum(
            1 for s in self.project.scenarios for tc in s.test_cases if tc.id
        )

        self.cards[0].findChild(QLabel, "").setText(str(total_scenarios) if False else "")
        self.cards[0].layout().itemAt(2).widget().setText(str(total_cases))
        self.cards[1].layout().itemAt(2).widget().setText(str(high_priority))
        self.cards[2].layout().itemAt(2).widget().setText(str(covered))
        self.cards[3].layout().itemAt(2).widget().setText(f"{total_scenarios}个")

    def _on_action(self, action_id: str):
        self.navigate.emit(action_id)
