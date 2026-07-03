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
from PyQt6.QtGui import QFont, QPalette, QColor

from testcase_generator.ui_mainwindow import MainWindow
from testcase_generator.theme import LIGHT_THEME


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

    # 设置全局字体
    font = QFont("Microsoft YaHei UI", 12)
    app.setFont(font)

    # 创建主窗口
    window = MainWindow()
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
