"""
TestCraft - 智能测试用例生成器
入口文件

作者: TestCraft Team
版本: 1.0.0
"""

import sys
import os

# 添加当前目录到路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QFontDatabase, QPalette, QColor, QIcon

from testcase_generator.ui_mainwindow import MainWindow
from testcase_generator.theme import LIGHT_THEME


def get_resource_path(relative_path):
    """获取资源文件的绝对路径（兼容 PyInstaller 打包）"""
    base_path = sys._MEIPASS if hasattr(sys, "_MEIPASS") else os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base_path, relative_path)


def main():
    """主函数"""
    # 启用高DPI缩放
    QApplication.setHighDpiScaleFactorRoundingPolicy(
        Qt.HighDpiScaleFactorRoundingPolicy.PassThrough
    )

    app = QApplication(sys.argv)
    app.setApplicationName("TestCraft")
    app.setApplicationVersion("1.0.0")
    app.setOrganizationName("TestCraft")

    # 设置全局字体（兜底：如果 Microsoft YaHei UI 不可用则使用默认字体）
    font = QFont()
    families = QFontDatabase.families()
    if "Microsoft YaHei UI" in families:
        font.setFamily("Microsoft YaHei UI")
    font.setPointSize(12)
    app.setFont(font)

    # 设置应用图标
    icon_path = get_resource_path("assets/testcraft.ico")
    if os.path.exists(icon_path):
        app.setWindowIcon(QIcon(icon_path))

    # 创建主窗口
    window = MainWindow()
    window.setWindowIcon(QIcon(icon_path) if os.path.exists(icon_path) else QIcon())
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
