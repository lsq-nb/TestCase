"""
场景管理页面
"""

from __future__ import annotations

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QTreeWidget, QTreeWidgetItem,
    QSplitter, QMessageBox, QFileDialog, QHeaderView,
    QDialog,
)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont

from testcase_generator.models import TestProject, TestScenario
from .ui_dialogs import ScenarioConfigDialog


class ScenarioManagerPage(QWidget):
    """场景配置页面"""

    scenario_changed = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.project: TestProject | None = None
        self._init_ui()

    def _init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(12)

        # 标题栏
        title_layout = QHBoxLayout()
        title = QLabel("功能场景配置")
        title.setFont(QFont("Microsoft YaHei UI", 18, QFont.Weight.Bold))
        title_layout.addWidget(title)
        title_layout.addStretch()
        layout.addLayout(title_layout)

        # 工具栏
        toolbar = QHBoxLayout()

        add_btn = QPushButton("➕ 新建场景")
        add_btn.setObjectName("accent")
        add_btn.clicked.connect(self._add_scenario)
        toolbar.addWidget(add_btn)

        edit_btn = QPushButton("✏️ 编辑场景")
        edit_btn.clicked.connect(self._edit_scenario)
        toolbar.addWidget(edit_btn)

        delete_btn = QPushButton("🗑️ 删除场景")
        delete_btn.setObjectName("danger")
        delete_btn.clicked.connect(self._delete_scenario)
        toolbar.addWidget(delete_btn)

        generate_btn = QPushButton("🤖 一键生成用例")
        generate_btn.setObjectName("warning")
        generate_btn.clicked.connect(self._generate_cases)
        toolbar.addWidget(generate_btn)

        toolbar.addStretch()
        layout.addLayout(toolbar)

        # 场景树
        self.tree = QTreeWidget()
        self.tree.setHeaderLabels(["场景名称", "测试方法", "参数数量", "用例数量", "优先级"])
        self.tree.header().setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        self.tree.itemSelectionChanged.connect(self._on_selection_changed)
        layout.addWidget(self.tree)

        # 说明
        tip = QLabel(
            "💡 说明：每个场景代表一个功能模块。添加参数后可以选择不同的测试方法论来自动生成测试用例。"
        )
        tip.setFont(QFont("Microsoft YaHei UI", 10))
        tip.setStyleSheet("color: #7F8C8D; padding: 8px; background-color: #FEF9E7; border-radius: 6px;")
        layout.addWidget(tip)

    def set_project(self, project: TestProject):
        """设置当前项目"""
        self.project = project
        self._refresh_tree()

    def _refresh_tree(self):
        """刷新场景树"""
        self.tree.clear()
        if not self.project:
            return

        for scenario in self.project.scenarios:
            item = QTreeWidgetItem([
                scenario.name,
                scenario.method,
                str(len(scenario.parameters)),
                str(len(scenario.test_cases)),
                scenario.priority,
            ])
            item.setData(0, Qt.ItemDataRole.UserRole, scenario.name)
            self.tree.addTopLevelItem(item)

        self.tree.expandAll()

    def _add_scenario(self):
        """新建场景"""
        if not self.project:
            QMessageBox.warning(self, "提示", "请先创建一个测试项目。")
            return

        dialog = ScenarioConfigDialog()
        if dialog.exec() == QDialog.DialogCode.Accepted:
            self.project.scenarios.append(dialog.scenario)
            self._refresh_tree()
            self.scenario_changed.emit()
            QMessageBox.information(self, "成功", f"场景「{dialog.scenario.name}」已创建！")

    def _edit_scenario(self):
        """编辑场景"""
        selected = self.tree.selectedItems()
        if not selected:
            QMessageBox.warning(self, "提示", "请先选择一个场景。")
            return

        name = selected[0].data(0, Qt.ItemDataRole.UserRole)
        scenario = next((s for s in self.project.scenarios if s.name == name), None)
        if not scenario:
            return

        dialog = ScenarioConfigDialog(scenario)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            self._refresh_tree()
            self.scenario_changed.emit()

    def _delete_scenario(self):
        """删除场景"""
        selected = self.tree.selectedItems()
        if not selected:
            QMessageBox.warning(self, "提示", "请先选择一个场景。")
            return

        name = selected[0].text(0)
        reply = QMessageBox.question(
            self, "确认删除",
            f"确定要删除场景「{name}」及其所有测试用例吗？",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
        )
        if reply == QMessageBox.StandardButton.Yes:
            self.project.scenarios = [
                s for s in self.project.scenarios if s.name != name
            ]
            self._refresh_tree()
            self.scenario_changed.emit()

    def _generate_cases(self):
        """一键生成用例"""
        if not self.project:
            QMessageBox.warning(self, "提示", "请先创建场景。")
            return

        if not self.project.scenarios:
            QMessageBox.warning(self, "提示", "请先添加功能场景。")
            return

        from testcase_generator.engine import generate_for_project
        self.project = generate_for_project(self.project)
        self._refresh_tree()
        self.scenario_changed.emit()

        total = self.project.total_test_cases
        QMessageBox.information(
            self, "生成完成",
            f"已成功为 {self.project.total_scenarios} 个场景生成 {total} 条测试用例！",
        )

    def _on_selection_changed(self):
        """选择变化时的回调"""
        pass
