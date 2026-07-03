"""
项目管理页面
"""

from __future__ import annotations

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QGroupBox, QFormLayout, QLineEdit,
    QTextEdit, QComboBox, QMessageBox, QFileDialog,
)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont

from testcase_generator.models import TestProject


class ProjectPage(QWidget):
    """项目管理页面"""

    project_created = pyqtSignal(TestProject)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.project: TestProject | None = None
        self._init_ui()

    def _init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(16)

        # 标题
        title = QLabel("项目管理")
        title.setFont(QFont("Microsoft YaHei UI", 18, QFont.Weight.Bold))
        layout.addWidget(title)

        # 新建项目表单
        create_group = QGroupBox("新建测试项目")
        create_layout = QFormLayout()

        self.name_edit = QLineEdit()
        self.name_edit.setPlaceholderText("例如：用户管理系统测试")
        create_layout.addRow("项目名称:", self.name_edit)

        self.desc_edit = QTextEdit()
        self.desc_edit.setMaximumHeight(60)
        self.desc_edit.setPlaceholderText("项目描述...")
        create_layout.addRow("项目描述:", self.desc_edit)

        self.version_edit = QLineEdit("1.0")
        create_layout.addRow("版本号:", self.version_edit)

        self.framework_combo = QComboBox()
        self.framework_combo.addItems(["pytest", "unittest", "JUnit", "TestNG"])
        create_layout.addRow("目标框架:", self.framework_combo)

        create_group.setLayout(create_layout)
        layout.addWidget(create_group)

        # 按钮
        btn_layout = QHBoxLayout()
        create_btn = QPushButton("🚀 创建项目")
        create_btn.setObjectName("accent")
        create_btn.clicked.connect(self._create_project)
        btn_layout.addWidget(create_btn)

        load_btn = QPushButton("📂 加载项目")
        load_btn.clicked.connect(self._load_project)
        btn_layout.addWidget(load_btn)

        save_btn = QPushButton("💾 保存项目")
        save_btn.clicked.connect(self._save_project)
        btn_layout.addWidget(save_btn)

        btn_layout.addStretch()
        layout.addLayout(btn_layout)

        # 项目信息
        info_group = QGroupBox("当前项目信息")
        info_layout = QFormLayout()

        self.info_name = QLabel("无")
        self.info_desc = QLabel("无")
        self.info_version = QLabel("无")
        self.info_framework = QLabel("无")
        self.info_scenarios = QLabel("0")
        self.info_cases = QLabel("0")
        self.info_updated = QLabel("无")

        info_layout.addRow("项目名称:", self.info_name)
        info_layout.addRow("项目描述:", self.info_desc)
        info_layout.addRow("版本号:", self.info_version)
        info_layout.addRow("目标框架:", self.info_framework)
        info_layout.addRow("功能模块:", self.info_scenarios)
        info_layout.addRow("测试用例:", self.info_cases)
        info_layout.addRow("更新时间:", self.info_updated)

        info_group.setLayout(info_layout)
        layout.addWidget(info_group)

        layout.addStretch()

    def set_project(self, project: TestProject):
        """设置当前项目"""
        self.project = project
        self._update_info()

    def _update_info(self):
        """更新项目信息显示"""
        if not self.project:
            self.info_name.setText("无")
            self.info_desc.setText("无")
            return

        self.info_name.setText(self.project.name)
        self.info_desc.setText(self.project.description or "无")
        self.info_version.setText(self.project.version)
        self.info_framework.setText(self.project.target_framework)
        self.info_scenarios.setText(str(self.project.total_scenarios))
        self.info_cases.setText(str(self.project.total_test_cases))
        self.info_updated.setText(self.project.updated_at or "无")

    def _create_project(self):
        """创建新项目"""
        name = self.name_edit.text().strip()
        if not name:
            QMessageBox.warning(self, "提示", "请输入项目名称。")
            return

        from datetime import datetime
        project = TestProject(
            name=name,
            description=self.desc_edit.toPlainText().strip(),
            version=self.version_edit.text() or "1.0",
            target_framework=self.framework_combo.currentText(),
            created_at=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            updated_at=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        )

        self.project = project
        self._update_info()
        self.project_created.emit(project)
        QMessageBox.information(self, "成功", f"项目「{name}」已创建！")

    def _load_project(self):
        """加载项目"""
        filepath, _ = QFileDialog.getOpenFileName(
            self, "加载项目", "",
            "TestCraft Projects (*.tcproj);;JSON Files (*.json);;All Files (*)",
        )
        if not filepath:
            return

        try:
            import json
            with open(filepath, "r", encoding="utf-8") as f:
                data = json.load(f)

            from datetime import datetime
            project = TestProject.from_dict(data)
            project.updated_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            self.project = project
            self._update_info()
            self.project_created.emit(project)
            QMessageBox.information(self, "成功", f"已加载项目「{project.name}」")
        except Exception as e:
            QMessageBox.critical(self, "错误", f"加载项目失败:\n{str(e)}")

    def _save_project(self):
        """保存项目"""
        if not self.project:
            QMessageBox.warning(self, "提示", "请先创建一个项目。")
            return

        from datetime import datetime
        self.project.updated_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        filepath, _ = QFileDialog.getSaveFileName(
            self, "保存项目",
            f"{self.project.name}.tcproj",
            "TestCraft Projects (*.tcproj);;JSON Files (*.json)",
        )
        if not filepath:
            return

        try:
            import json
            with open(filepath, "w", encoding="utf-8") as f:
                json.dump(self.project.to_dict(), f, ensure_ascii=False, indent=2)
            self._update_info()
            QMessageBox.information(self, "成功", f"项目已保存到:\n{filepath}")
        except Exception as e:
            QMessageBox.critical(self, "错误", f"保存项目失败:\n{str(e)}")
