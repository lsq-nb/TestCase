"""
统计分析页面
"""

from __future__ import annotations

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QFrame, QGridLayout, QTableWidget, QTableWidgetItem,
    QHeaderView, QGroupBox, QFormLayout,
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QBrush, QColor


class StatisticsPage(QWidget):
    """统计分析页面"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.project: TestProject | None = None
        self._init_ui()

    def _init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(16)

        title = QLabel("统计分析")
        title.setFont(QFont("Microsoft YaHei UI", 18, QFont.Weight.Bold))
        layout.addWidget(title)

        # 总体统计
        overview_group = QGroupBox("总体概览")
        overview_layout = QGridLayout()
        overview_layout.setSpacing(12)

        self.overview_stats = []
        labels = [
            ("功能模块数", "📁", "#3498DB"),
            ("总用例数", "🧪", "#2ECC71"),
            ("高优先级", "🔥", "#E74C3C"),
            ("中优先级", "⚡", "#F39C12"),
            ("低优先级", "🌿", "#1ABC9C"),
            ("用例覆盖率", "📊", "#9B59B6"),
        ]

        for i, (label, icon, color) in enumerate(labels):
            card = self._create_stat_card(icon, label, "0", color)
            col = i % 3
            row = i // 3
            overview_layout.addWidget(card, row, col)
            self.overview_stats.append(card)

        overview_group.setLayout(overview_layout)
        layout.addWidget(overview_group)

        # 优先级分布表
        priority_group = QGroupBox("优先级分布")
        priority_layout = QVBoxLayout()

        self.priority_table = QTableWidget()
        self.priority_table.setColumnCount(3)
        self.priority_table.setHorizontalHeaderLabels(["优先级", "用例数", "占比"])
        self.priority_table.horizontalHeader().setSectionResizeMode(
            QHeaderView.ResizeMode.Stretch
        )
        self.priority_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.priority_table.verticalHeader().setVisible(False)
        priority_layout.addWidget(self.priority_table)
        priority_group.setLayout(priority_layout)
        layout.addWidget(priority_group)

        # 测试类型分布表
        type_group = QGroupBox("测试类型分布")
        type_layout = QVBoxLayout()

        self.type_table = QTableWidget()
        self.type_table.setColumnCount(3)
        self.type_table.setHorizontalHeaderLabels(["测试类型", "用例数", "占比"])
        self.type_table.horizontalHeader().setSectionResizeMode(
            QHeaderView.ResizeMode.Stretch
        )
        self.type_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.type_table.verticalHeader().setVisible(False)
        type_layout.addWidget(self.type_table)
        type_group.setLayout(type_layout)
        layout.addWidget(type_group)

        # 场景详细表
        detail_group = QGroupBox("场景详细统计")
        detail_layout = QVBoxLayout()

        self.detail_table = QTableWidget()
        self.detail_table.setColumnCount(5)
        self.detail_table.setHorizontalHeaderLabels([
            "场景名称", "测试方法", "参数数", "用例数", "优先级",
        ])
        header = self.detail_table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.Fixed)
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.Fixed)
        header.setSectionResizeMode(3, QHeaderView.ResizeMode.Fixed)
        header.setSectionResizeMode(4, QHeaderView.ResizeMode.Fixed)
        header.resizeSection(1, 120)
        header.resizeSection(2, 70)
        header.resizeSection(3, 70)
        header.resizeSection(4, 70)
        self.detail_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.detail_table.verticalHeader().setVisible(False)
        detail_layout.addWidget(self.detail_table)
        detail_group.setLayout(detail_layout)
        layout.addWidget(detail_group)

        layout.addStretch()

    def _create_stat_card(self, icon: str, title: str, value: str, color: str) -> QFrame:
        """创建统计卡片"""
        card = QFrame()
        card.setObjectName("card")
        card.setMinimumHeight(90)

        layout = QVBoxLayout(card)
        layout.setContentsMargins(16, 12, 16, 12)
        layout.setSpacing(4)

        icon_label = QLabel(icon)
        icon_label.setFont(QFont("Microsoft YaHei UI", 22))
        icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(icon_label)

        value_label = QLabel(value)
        value_label.setFont(QFont("Microsoft YaHei UI", 22, QFont.Weight.Bold))
        value_label.setStyleSheet(f"color: {color};")
        value_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(value_label)

        title_label = QLabel(title)
        title_label.setFont(QFont("Microsoft YaHei UI", 10))
        title_label.setStyleSheet("color: #7F8C8D;")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title_label)

        return card

    def set_project(self, project: TestProject):
        """设置当前项目"""
        self.project = project
        self._update_statistics()

    def _update_statistics(self):
        """更新统计数据"""
        if not self.project:
            return

        total_cases = self.project.total_test_cases
        total_scenarios = self.project.total_scenarios

        high_count = sum(
            1 for s in self.project.scenarios for tc in s.test_cases if tc.priority == "高"
        )
        medium_count = sum(
            1 for s in self.project.scenarios for tc in s.test_cases if tc.priority == "中"
        )
        low_count = sum(
            1 for s in self.project.scenarios for tc in s.test_cases if tc.priority == "低"
        )

        coverage = f"{(total_cases / max(total_scenarios, 1)):.1f}条/模块"

        # 更新概览卡片
        stat_values = [
            str(total_scenarios),
            str(total_cases),
            str(high_count),
            str(medium_count),
            str(low_count),
            coverage,
        ]
        for card, value in zip(self.overview_stats, stat_values):
            card.findChildren(QLabel)[1].setText(value)

        # 更新优先级分布表
        priorities = [("高", high_count), ("中", medium_count), ("低", low_count)]
        self.priority_table.setRowCount(len(priorities))
        priority_colors = {"高": "#E74C3C", "中": "#F39C12", "低": "#1ABC9C"}
        for i, (pri, count) in enumerate(priorities):
            self.priority_table.setItem(i, 0, QTableWidgetItem(pri))
            self.priority_table.setItem(i, 1, QTableWidgetItem(str(count)))
            pct = f"{count / max(total_cases, 1) * 100:.1f}%" if total_cases else "0%"
            self.priority_table.setItem(i, 2, QTableWidgetItem(pct))
            # 颜色标记
            item = self.priority_table.item(i, 0)
            if item:
                item.setForeground(QBrush(QColor(priority_colors[pri])))

        # 更新测试类型分布表
        type_counts: dict[str, int] = {}
        for s in self.project.scenarios:
            for tc in s.test_cases:
                type_counts[tc.test_type] = type_counts.get(tc.test_type, 0) + 1

        self.type_table.setRowCount(len(type_counts))
        for i, (test_type, count) in enumerate(sorted(type_counts.items())):
            self.type_table.setItem(i, 0, QTableWidgetItem(test_type))
            self.type_table.setItem(i, 1, QTableWidgetItem(str(count)))
            pct = f"{count / max(total_cases, 1) * 100:.1f}%" if total_cases else "0%"
            self.type_table.setItem(i, 2, QTableWidgetItem(pct))

        # 更新场景详细表
        self.detail_table.setRowCount(len(self.project.scenarios))
        for i, scenario in enumerate(self.project.scenarios):
            self.detail_table.setItem(i, 0, QTableWidgetItem(scenario.name))
            self.detail_table.setItem(i, 1, QTableWidgetItem(scenario.method))
            self.detail_table.setItem(i, 2, QTableWidgetItem(str(len(scenario.parameters))))
            self.detail_table.setItem(i, 3, QTableWidgetItem(str(len(scenario.test_cases))))
            self.detail_table.setItem(i, 4, QTableWidgetItem(scenario.priority))
