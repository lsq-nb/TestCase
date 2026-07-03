"""
用例管理页面
"""

from __future__ import annotations

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QTableWidget, QTableWidgetItem, QHeaderView,
    QPushButton, QMessageBox, QFileDialog, QMenu,
    QGroupBox, QFormLayout, QLineEdit,
    QTextEdit, QComboBox, QSplitter,
)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont, QAction

from testcase_generator.models import TestProject, TestCase


class CaseManagerPage(QWidget):
    """用例管理页面"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.project: TestProject | None = None
        self._current_scenario: TestScenario | None = None
        self._init_ui()

    def _init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(12)

        # 标题栏
        title_layout = QHBoxLayout()
        title = QLabel("测试用例管理")
        title.setFont(QFont("Microsoft YaHei UI", 18, QFont.Weight.Bold))
        title_layout.addWidget(title)
        title_layout.addStretch()
        layout.addLayout(title_layout)

        # 场景筛选
        filter_layout = QHBoxLayout()
        filter_layout.addWidget(QLabel("场景:"))
        self.scenario_filter = QComboBox()
        self.scenario_filter.addItem("全部场景")
        self.scenario_filter.currentTextChanged.connect(self._apply_filter)
        filter_layout.addWidget(self.scenario_filter)

        filter_layout.addWidget(QLabel("优先级:"))
        self.priority_filter = QComboBox()
        self.priority_filter.addItems(["全部", "高", "中", "低"])
        self.priority_filter.currentTextChanged.connect(self._apply_filter)
        filter_layout.addWidget(self.priority_filter)

        filter_layout.addStretch()
        layout.addLayout(filter_layout)

        # 用例表格
        self.table = QTableWidget()
        self.table.setColumnCount(8)
        self.table.setHorizontalHeaderLabels([
            "用例ID", "标题", "前置条件", "测试步骤",
            "预期结果", "优先级", "测试类型", "标签",
        ])
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.Fixed)
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.Fixed)
        header.setSectionResizeMode(3, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(4, QHeaderView.ResizeMode.Fixed)
        header.setSectionResizeMode(5, QHeaderView.ResizeMode.Fixed)
        header.setSectionResizeMode(6, QHeaderView.ResizeMode.Fixed)
        header.setSectionResizeMode(7, QHeaderView.ResizeMode.Fixed)
        header.resizeSection(0, 100)
        header.resizeSection(2, 120)
        header.resizeSection(4, 150)
        header.resizeSection(5, 70)
        header.resizeSection(6, 100)
        header.resizeSection(7, 80)
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.table.setEditTriggers(QTableWidget.EditTrigger.DoubleClicked)
        self.table.setAlternatingRowColors(True)
        self.table.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.table.customContextMenuRequested.connect(self._show_context_menu)
        self.table.itemDoubleClicked.connect(self._edit_case)
        layout.addWidget(self.table)

        # 工具栏
        toolbar = QHBoxLayout()
        refresh_btn = QPushButton("🔄 刷新")
        refresh_btn.clicked.connect(self._refresh)
        toolbar.addWidget(refresh_btn)

        delete_btn = QPushButton("🗑️ 删除选中")
        delete_btn.setObjectName("danger")
        delete_btn.clicked.connect(self._delete_selected)
        toolbar.addWidget(delete_btn)

        toolbar.addStretch()

        # 统计
        self.case_count = QLabel("共 0 条用例")
        self.case_count.setFont(QFont("Microsoft YaHei UI", 10))
        self.case_count.setStyleSheet("color: #7F8C8D;")
        toolbar.addWidget(self.case_count)

        layout.addLayout(toolbar)

        # 详情面板
        detail_group = QGroupBox("用例详情（双击编辑）")
        detail_layout = QFormLayout()
        self.detail_id = QLineEdit()
        self.detail_id.setReadOnly(True)
        self.detail_title = QLineEdit()
        self.detail_precondition = QLineEdit()
        self.detail_steps = QTextEdit()
        self.detail_steps.setMaximumHeight(80)
        self.detail_expected = QTextEdit()
        self.detail_expected.setMaximumHeight(80)
        self.detail_priority = QComboBox()
        self.detail_priority.addItems(["高", "中", "低"])
        self.detail_type = QLineEdit()
        self.detail_tags = QLineEdit()

        detail_layout.addRow("ID:", self.detail_id)
        detail_layout.addRow("标题:", self.detail_title)
        detail_layout.addRow("前置条件:", self.detail_precondition)
        detail_layout.addRow("测试步骤:", self.detail_steps)
        detail_layout.addRow("预期结果:", self.detail_expected)
        detail_layout.addRow("优先级:", self.detail_priority)
        detail_layout.addRow("测试类型:", self.detail_type)
        detail_layout.addRow("标签:", self.detail_tags)

        detail_group.setLayout(detail_layout)
        layout.addWidget(detail_group)

    def set_project(self, project: TestProject):
        """设置当前项目"""
        self.project = project
        self._refresh()

    def _refresh(self):
        """刷新表格"""
        if not self.project:
            return

        # 更新场景筛选
        self.scenario_filter.blockSignals(True)
        self.scenario_filter.clear()
        self.scenario_filter.addItem("全部场景")
        for s in self.project.scenarios:
            self.scenario_filter.addItem(s.name)
        self.scenario_filter.blockSignals(False)

        self._apply_filter()

    def _apply_filter(self):
        """应用筛选"""
        scenario_name = self.scenario_filter.currentText()
        priority = self.priority_filter.currentText()

        self.table.setRowCount(0)
        cases = []

        for scenario in self.project.scenarios:
            if scenario_name != "全部场景" and scenario.name != scenario_name:
                continue
            for tc in scenario.test_cases:
                if priority != "全部" and tc.priority != priority:
                    continue
                cases.append(tc)

        for tc in cases:
            row = self.table.rowCount()
            self.table.insertRow(row)
            self.table.setItem(row, 0, QTableWidgetItem(tc.id))
            self.table.setItem(row, 1, QTableWidgetItem(tc.title))
            self.table.setItem(row, 2, QTableWidgetItem(tc.precondition))
            self.table.setItem(row, 3, QTableWidgetItem(tc.steps))
            self.table.setItem(row, 4, QTableWidgetItem(tc.expected_result))
            self.table.setItem(row, 5, QTableWidgetItem(tc.priority))
            self.table.setItem(row, 6, QTableWidgetItem(tc.test_type))
            self.table.setItem(row, 7, QTableWidgetItem(tc.tags))

        self.case_count.setText(f"共 {len(cases)} 条用例")

    def _show_context_menu(self, pos):
        """右键菜单"""
        selected = self.table.selectedItems()
        if not selected:
            return

        menu = QMenu(self)
        edit_action = QAction("✏️ 编辑用例", self)
        edit_action.triggered.connect(self._edit_case)
        menu.addAction(edit_action)

        delete_action = QAction("🗑️ 删除用例", self)
        delete_action.triggered.connect(self._delete_selected)
        menu.addAction(delete_action)

        menu.exec(self.table.viewport().mapToGlobal(pos))

    def _edit_case(self, item: QTableWidgetItem):
        """编辑用例"""
        row = item.row()
        id_item = self.table.item(row, 0)
        if not id_item:
            return

        case_id = id_item.text()
        # 找到对应的用例
        tc = None
        for scenario in self.project.scenarios:
            for case in scenario.test_cases:
                if case.id == case_id:
                    tc = case
                    break
            if tc:
                break

        if not tc:
            return

        # 填充详情面板
        self.detail_id.setText(tc.id)
        self.detail_title.setText(tc.title)
        self.detail_precondition.setText(tc.precondition)
        self.detail_steps.setPlainText(tc.steps)
        self.detail_expected.setPlainText(tc.expected_result)
        self.detail_priority.setCurrentText(tc.priority)
        self.detail_type.setText(tc.test_type)
        self.detail_tags.setText(tc.tags)

    def _save_edits(self):
        """保存编辑"""
        case_id = self.detail_id.text()
        for scenario in self.project.scenarios:
            for tc in scenario.test_cases:
                if tc.id == case_id:
                    tc.title = self.detail_title.text()
                    tc.precondition = self.detail_precondition.text()
                    tc.steps = self.detail_steps.toPlainText()
                    tc.expected_result = self.detail_expected.toPlainText()
                    tc.priority = self.detail_priority.currentText()
                    tc.tags = self.detail_tags.text()
                    return

    def _delete_selected(self):
        """删除选中用例"""
        selected = self.table.selectedItems()
        if not selected:
            return

        rows = sorted(set(item.row() for item in selected))
        reply = QMessageBox.question(
            self, "确认删除",
            f"确定要删除 {len(rows)} 条测试用例吗？",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
        )
        if reply == QMessageBox.StandardButton.Yes:
            # 反向删除避免索引变化
            for row in reversed(rows):
                case_id = self.table.item(row, 0).text()
                for scenario in self.project.scenarios:
                    scenario.test_cases = [
                        tc for tc in scenario.test_cases if tc.id != case_id
                    ]
            self._apply_filter()
