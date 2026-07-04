"""
导出中心页面
"""

from __future__ import annotations

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QGroupBox, QFormLayout, QComboBox,
    QFileDialog, QMessageBox, QTextEdit, QSplitter, QApplication,
)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont

from testcase_generator.models import TestProject, Framework
from testcase_generator.exporter import export_project
from testcase_generator.codegen import generate_code


class ExportPage(QWidget):
    """导出中心页面"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.project: TestProject | None = None
        self._init_ui()

    def _init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(16)

        # 标题
        title = QLabel("导出中心")
        title.setFont(QFont("Microsoft YaHei UI", 18, QFont.Weight.Bold))
        layout.addWidget(title)

        # 导出选项
        option_group = QGroupBox("导出选项")
        option_layout = QFormLayout()

        self.format_combo = QComboBox()
        self.format_combo.addItems([
            "Excel (.xlsx)", "CSV (.csv)", "JSON (.json)",
            "pytest 代码 (.py)", "unittest 代码 (.py)",
            "JUnit 代码 (.java)", "TestNG 代码 (.java)",
        ])
        option_layout.addRow("导出格式:", self.format_combo)

        self.framework_combo = QComboBox()
        self.framework_combo.addItems([f.value for f in Framework])
        option_layout.addRow("目标框架:", self.framework_combo)

        option_group.setLayout(option_layout)
        layout.addWidget(option_group)

        # 导出按钮
        btn_layout = QHBoxLayout()
        export_btn = QPushButton("📤 开始导出")
        export_btn.setObjectName("accent")
        export_btn.clicked.connect(self._export)
        btn_layout.addWidget(export_btn)

        preview_btn = QPushButton("👁️ 预览代码")
        preview_btn.setObjectName("warning")
        preview_btn.clicked.connect(self._preview)
        btn_layout.addWidget(preview_btn)

        btn_layout.addStretch()
        layout.addLayout(btn_layout)

        # 预览区域
        preview_group = QGroupBox("代码预览")
        preview_layout = QVBoxLayout()

        self.preview_text = QTextEdit()
        self.preview_text.setReadOnly(True)
        font = QFont("Consolas", 11)
        if font.pointSize() <= 0:
            font = QFont()
            font.setPointSize(11)
        self.preview_text.setFont(font)
        self.preview_text.setPlaceholderText("点击「预览代码」按钮查看生成的测试代码...")
        preview_layout.addWidget(self.preview_text)

        copy_btn = QPushButton("📋 复制代码")
        copy_btn.clicked.connect(self._copy_code)
        preview_layout.addWidget(copy_btn)

        preview_group.setLayout(preview_layout)
        layout.addWidget(preview_group)

        layout.addStretch()

    def set_project(self, project: TestProject):
        """设置当前项目"""
        self.project = project

    def _get_format_info(self) -> tuple[str, str]:
        """获取导出格式和扩展名"""
        fmt = self.format_combo.currentText()
        mapping = {
            "Excel (.xlsx)": ("xlsx", "测试用例报告.xlsx"),
            "CSV (.csv)": ("csv", "测试用例.csv"),
            "JSON (.json)": ("json", "测试用例.json"),
            "pytest 代码 (.py)": ("py", "test_cases.py"),
            "unittest 代码 (.py)": ("py", "test_cases_unittest.py"),
            "JUnit 代码 (.java)": ("java", "TestCases.java"),
            "TestNG 代码 (.java)": ("java", "TestCasesTestNG.java"),
        }
        return mapping.get(fmt, ("json", "testcase.json"))

    def _get_framework(self) -> str:
        """获取目标框架"""
        text = self.framework_combo.currentText()
        if "pytest" in text:
            return "pytest"
        elif "unittest" in text:
            return "unittest"
        elif "JUnit" in text:
            return "JUnit"
        elif "TestNG" in text:
            return "TestNG"
        return "pytest"

    def _export(self):
        """执行导出"""
        if not self.project:
            QMessageBox.warning(self, "提示", "请先创建一个测试项目。")
            return

        if self.project.total_test_cases == 0:
            QMessageBox.warning(
                self, "提示",
                "当前没有可导出的测试用例。请先生成测试用例。",
            )
            return

        fmt, filename = self._get_format_info()
        filepath, _ = QFileDialog.getSaveFileName(
            self, "保存文件", filename,
            f"{fmt.upper()} Files (*.{fmt});;All Files (*)",
        )
        if not filepath:
            return

        try:
            result_fmt = export_project(self.project, filepath)
            QMessageBox.information(
                self, "导出成功",
                f"文件已导出到:\n{filepath}\n\n格式: {result_fmt}",
            )
        except Exception as e:
            QMessageBox.critical(self, "导出失败", f"导出过程中出错:\n{str(e)}")

    def _preview(self):
        """预览代码"""
        if not self.project:
            QMessageBox.warning(self, "提示", "请先创建一个测试项目。")
            return

        framework = self._get_framework()
        code = generate_code(self.project, framework)
        self.preview_text.setPlainText(code)

    def _copy_code(self):
        """复制代码到剪贴板"""
        clipboard = QApplication.clipboard()
        clipboard.setText(self.preview_text.toPlainText())
        QMessageBox.information(self, "成功", "代码已复制到剪贴板！")
