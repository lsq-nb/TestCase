"""
侧边栏组件
"""

from __future__ import annotations

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QPushButton, QLabel,
    QScrollArea, QFrame,
)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont, QIcon


class SidebarButton(QPushButton):
    """侧边栏按钮"""

    def __init__(self, icon: str, text: str, parent=None):
        super().__init__(parent)
        self.setText(text)
        self.setCheckable(True)
        self.setIconSize(self.sizeHint() * 0)
        self.setMinimumHeight(40)
        self.setProperty("icon", icon)


class Sidebar(QWidget):
    """左侧导航栏"""

    page_changed = pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("sidebar")
        self.setMinimumWidth(220)
        self.setMaximumWidth(280)
        self._init_ui()

    def _init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # Logo区域
        logo_frame = QFrame()
        logo_frame.setStyleSheet("background-color: transparent;")
        logo_layout = QVBoxLayout(logo_frame)
        logo_layout.setContentsMargins(16, 20, 16, 12)

        logo_label = QLabel("🧪 TestCraft")
        logo_label.setFont(QFont("Microsoft YaHei UI", 16, QFont.Weight.Bold))
        logo_label.setStyleSheet("color: #FFFFFF; background-color: transparent;")
        logo_layout.addWidget(logo_label)

        version_label = QLabel("智能测试用例生成器 v1.0")
        version_label.setFont(QFont("Microsoft YaHei UI", 9))
        version_label.setStyleSheet("color: #6B8299; background-color: transparent;")
        logo_layout.addWidget(version_label)
        logo_layout.addStretch()

        layout.addWidget(logo_frame)

        # 分隔线
        separator = QFrame()
        separator.setFrameShape(QFrame.Shape.HLine)
        separator.setFrameShadow(QFrame.Shadow.Sunken)
        separator.setStyleSheet("color: #2C3E56;")
        layout.addWidget(separator)

        # 导航按钮组
        self._pages = [
            ("🏠", "工作台", "dashboard"),
            ("📁", "项目管理", "project"),
            ("⚙️", "场景配置", "scenario"),
            ("📋", "用例管理", "cases"),
            ("📤", "导出中心", "export"),
            ("📊", "统计分析", "statistics"),
        ]

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.Shape.NoFrame)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        scroll_content = QWidget()
        scroll_layout = QVBoxLayout(scroll_content)
        scroll_layout.setContentsMargins(0, 8, 0, 8)
        scroll_layout.setSpacing(2)

        self._buttons = []
        for icon, text, page_id in self._pages:
            btn = SidebarButton(icon, text)
            btn.page_id = page_id
            btn.clicked.connect(lambda checked, p=page_id: self.page_changed.emit(p))
            scroll_layout.addWidget(btn)
            self._buttons.append(btn)

        scroll_layout.addStretch()
        scroll.setWidget(scroll_content)
        layout.addWidget(scroll)

        # 底部链接
        footer = QLabel("TestCraft © 2026")
        footer.setAlignment(Qt.AlignmentFlag.AlignCenter)
        footer.setFont(QFont("Microsoft YaHei UI", 8))
        footer.setStyleSheet("color: #4A5568; background-color: transparent; padding: 12px;")
        layout.addWidget(footer)

        # 默认选中工作台
        self._buttons[0].setChecked(True)

    def select_page(self, page_id: str):
        """选择指定页面"""
        for btn in self._buttons:
            btn.setChecked(btn.page_id == page_id)

    def highlight_new(self, count: int):
        """高亮显示新增内容"""
        if count > 0 and len(self._buttons) > 3:
            self._buttons[3].setText(f"📋 用例管理 ({count})")
