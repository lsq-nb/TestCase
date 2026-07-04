"""
场景配置对话框
"""

from __future__ import annotations

from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
    QTextEdit, QComboBox, QPushButton, QGroupBox,
    QFormLayout, QSpinBox, QMessageBox, QTableWidget,
    QTableWidgetItem, QHeaderView, QScrollArea, QWidget,
)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont

from testcase_generator.models import ParameterRule, TestScenario


class ParameterEditor(QWidget):
    """参数编辑器"""

    param_added = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.parameters: list[ParameterRule] = []
        self._init_ui()

    def _init_ui(self):
        layout = QVBoxLayout(self)

        # 参数表格
        self.table = QTableWidget()
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels(["参数名", "类型", "必填", "最小值", "最大值", "操作"])
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.Fixed)
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.Fixed)
        header.setSectionResizeMode(3, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(4, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(5, QHeaderView.ResizeMode.Fixed)
        self.table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.Fixed)
        self.table.setColumnWidth(1, 100)
        self.table.setColumnWidth(2, 60)
        self.table.setColumnWidth(5, 60)
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.table.verticalHeader().setVisible(False)
        self.table.setStyleSheet("""
            QTableWidget { border: none; border-radius: 6px; }
            QTableWidget::item { padding: 4px; }
        """)
        layout.addWidget(self.table)

        # 按钮行
        btn_layout = QHBoxLayout()
        add_btn = QPushButton("+ 添加参数")
        add_btn.setObjectName("accent")
        add_btn.clicked.connect(self._add_param)
        btn_layout.addWidget(add_btn)

        remove_btn = QPushButton("- 删除选中")
        remove_btn.setObjectName("danger")
        remove_btn.clicked.connect(self._remove_param)
        btn_layout.addWidget(remove_btn)

        btn_layout.addStretch()
        layout.addLayout(btn_layout)

    def _add_param(self):
        rule = ParameterRule(
            name=f"参数{len(self.parameters) + 1}",
            param_type="字符串",
            required=True,
        )
        self.parameters.append(rule)
        self._refresh_table()
        self.param_added.emit()

    def _remove_param(self):
        rows = sorted(set(row.row() for row in self.table.selectedItems()), reverse=True)
        for row in rows:
            if 0 <= row < len(self.parameters):
                self.parameters.pop(row)
        self._refresh_table()
        self.param_added.emit()

    def _refresh_table(self):
        self.table.setRowCount(len(self.parameters))
        for i, p in enumerate(self.parameters):
            self.table.setItem(i, 0, QTableWidgetItem(p.name))
            self.table.setItem(i, 1, QTableWidgetItem(p.param_type))
            self.table.setItem(i, 2, QTableWidgetItem("是" if p.required else "否"))
            self.table.setItem(i, 3, QTableWidgetItem(str(p.min_value or "")))
            self.table.setItem(i, 4, QTableWidgetItem(str(p.max_value or "")))

            del_btn = QPushButton("✏️")
            del_btn.setFixedSize(36, 28)
            del_btn.clicked.connect(lambda checked, idx=i: self._edit_param(idx))
            self.table.setCellWidget(i, 5, del_btn)

    def _edit_param(self, index: int):
        if 0 <= index < len(self.parameters):
            rule = self.parameters[index]
            dialog = ParamDetailDialog(rule, self)
            if dialog.exec() == QDialog.DialogCode.Accepted:
                self._refresh_table()
                self.param_added.emit()

    def get_parameters(self) -> list[ParameterRule]:
        """从表格中同步最新数据"""
        for i in range(min(self.table.rowCount(), len(self.parameters))):
            if i < len(self.parameters):
                name_item = self.table.item(i, 0)
                min_item = self.table.item(i, 3)
                max_item = self.table.item(i, 4)
                req_item = self.table.item(i, 2)
                if name_item:
                    self.parameters[i].name = name_item.text()
                if min_item:
                    self.parameters[i].min_value = min_item.text() or None
                if max_item:
                    self.parameters[i].max_value = max_item.text() or None
                if req_item:
                    self.parameters[i].required = req_item.text() == "是"
        return self.parameters


class ParamDetailDialog(QDialog):
    """参数详情编辑对话框"""

    def __init__(self, rule: ParameterRule, parent=None):
        super().__init__(parent)
        self.rule = rule
        self.setWindowTitle("编辑参数")
        self.setModal(True)
        self.setMinimumWidth(400)
        self._init_ui()

    def _init_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(12)

        form = QFormLayout()
        form.setLabelAlignment(Qt.AlignmentFlag.AlignLeft)

        self.name_edit = QLineEdit(self.rule.name)
        self.type_combo = QComboBox()
        self.type_combo.addItems(["字符串", "整数", "浮点数", "布尔值", "邮箱", "手机号", "日期", "枚举"])
        self.type_combo.setCurrentText(self.rule.param_type)
        self.required_check = QPushButton("必填" if self.rule.required else "非必填")
        self.required_check.setCheckable(True)
        self.required_check.setChecked(self.rule.required)
        self.required_check.clicked.connect(lambda: self.required_check.setText(
            "必填" if self.required_check.isChecked() else "非必填"))
        self.min_edit = QLineEdit(str(self.rule.min_value or ""))
        self.max_edit = QLineEdit(str(self.rule.max_value or ""))
        self.enum_edit = QLineEdit(self.rule.enum_values)
        self.enum_edit.setPlaceholderText("用逗号分隔多个值")
        self.default_edit = QLineEdit(self.rule.default_value)

        form.addRow("参数名称:", self.name_edit)
        form.addRow("数据类型:", self.type_combo)
        form.addRow("是否必填:", self.required_check)
        form.addRow("最小值:", self.min_edit)
        form.addRow("最大值:", self.max_edit)
        form.addRow("枚举值:", self.enum_edit)
        form.addRow("默认值:", self.default_edit)

        layout.addLayout(form)

        btn_layout = QHBoxLayout()
        cancel_btn = QPushButton("取消")
        ok_btn = QPushButton("确定")
        ok_btn.setObjectName("accent")
        btn_layout.addWidget(cancel_btn)
        btn_layout.addStretch()
        btn_layout.addWidget(ok_btn)
        layout.addLayout(btn_layout)

        cancel_btn.clicked.connect(self.reject)
        ok_btn.clicked.connect(self._accept)

    def _accept(self):
        self.rule.name = self.name_edit.text() or "未命名参数"
        self.rule.param_type = self.type_combo.currentText()
        self.rule.required = self.required_check.isChecked()
        self.rule.min_value = self.min_edit.text() or None
        self.rule.max_value = self.max_edit.text() or None
        self.rule.enum_values = self.enum_edit.text()
        self.rule.default_value = self.default_edit.text()
        self.accept()


class ScenarioConfigDialog(QDialog):
    """场景配置对话框"""

    scenario_saved = pyqtSignal(TestScenario)

    def __init__(self, scenario: TestScenario = None, parent=None):
        super().__init__(parent)
        self.scenario = scenario or TestScenario()
        self.setWindowTitle("场景配置" if not scenario else "编辑场景")
        self.setModal(True)
        self.setMinimumSize(700, 600)
        self._init_ui()

    def _init_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(12)

        # 基本信息
        info_group = QGroupBox("基本信息")
        info_layout = QFormLayout()

        self.name_edit = QLineEdit(self.scenario.name)
        self.name_edit.setPlaceholderText("例如：用户登录功能")
        self.desc_edit = QTextEdit()
        self.desc_edit.setPlainText(self.scenario.description)
        self.desc_edit.setMaximumHeight(60)
        self.method_combo = QComboBox()
        self.method_combo.addItems([
            "边界值分析", "等价类划分", "判定表驱动",
            "状态转换测试", "场景法", "正交试验法",
        ])
        self.method_combo.setCurrentText(self.scenario.method)
        self.priority_combo = QComboBox()
        self.priority_combo.addItems(["高", "中", "低"])
        self.priority_combo.setCurrentText(self.scenario.priority)

        info_layout.addRow("场景名称:", self.name_edit)
        info_layout.addRow("场景描述:", self.desc_edit)
        info_layout.addRow("测试方法:", self.method_combo)
        info_layout.addRow("优先级:", self.priority_combo)
        info_group.setLayout(info_layout)
        layout.addWidget(info_group)

        # 参数编辑器
        param_scroll = QScrollArea()
        param_scroll.setWidgetResizable(True)
        param_scroll.setMaximumHeight(250)
        self.param_editor = ParameterEditor()
        self.param_editor.parameters = self.scenario.parameters.copy()
        self.param_editor._refresh_table()
        param_scroll.setWidget(self.param_editor)
        layout.addWidget(param_scroll)

        # 底部按钮
        btn_layout = QHBoxLayout()
        gen_preview = QPushButton("预览生成的用例")
        gen_preview.setObjectName("warning")
        gen_preview.clicked.connect(self._preview_cases)
        btn_layout.addWidget(gen_preview)

        cancel_btn = QPushButton("取消")
        ok_btn = QPushButton("保存场景")
        ok_btn.setObjectName("accent")
        btn_layout.addWidget(cancel_btn)
        btn_layout.addStretch()
        btn_layout.addWidget(ok_btn)
        layout.addLayout(btn_layout)

        cancel_btn.clicked.connect(self.reject)
        ok_btn.clicked.connect(self._save)

    def _preview_cases(self):
        """预览生成的用例"""
        self._sync_data()
        from testcase_generator.engine import generate_test_cases
        cases = generate_test_cases(self.scenario)
        if not cases:
            QMessageBox.information(self, "提示", "没有生成测试用例，请检查参数配置。")
            return

        msg = f"共生成 {len(cases)} 条测试用例：\n\n"
        for tc in cases[:10]:
            msg += f"[{tc.id}] {tc.title}\n"
        if len(cases) > 10:
            msg += f"\n... 还有 {len(cases) - 10} 条"
        QMessageBox.information(self, "用例预览", msg)

    def _sync_data(self):
        """从UI同步数据到场景对象"""
        self.scenario.name = self.name_edit.text() or "未命名场景"
        self.scenario.description = self.desc_edit.toPlainText()
        self.scenario.method = self.method_combo.currentText()
        self.scenario.priority = self.priority_combo.currentText()
        self.scenario.parameters = self.param_editor.get_parameters()

    def _save(self):
        self._sync_data()
        self.scenario_saved.emit(self.scenario)
        self.accept()
