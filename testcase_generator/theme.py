"""
全局样式表 - 提供深色/浅色主题
"""

from __future__ import annotations

LIGHT_THEME = """
/* ========== 全局 ========== */
QWidget {
    background-color: #F5F7FA;
    color: #2C3E50;
    font-family: "Microsoft YaHei UI", "Segoe UI", sans-serif;
    font-size: 13px;
}

/* ========== 主窗口 ========== */
QMainWindow {
    background-color: #F5F7FA;
}

/* ========== 侧边栏 ========== */
#sidebar {
    background-color: #1E2A3A;
    border: none;
}

#sidebar QPushButton {
    background-color: transparent;
    color: #A0B4C8;
    border: none;
    border-radius: 8px;
    padding: 10px 16px;
    text-align: left;
    font-size: 14px;
    margin: 2px 8px;
}

#sidebar QPushButton:hover {
    background-color: #2C3E56;
    color: #FFFFFF;
}

#sidebar QPushButton:checked {
    background-color: #3498DB;
    color: #FFFFFF;
    font-weight: bold;
}

#sidebar QLabel {
    color: #6B8299;
    font-size: 11px;
    text-transform: uppercase;
    letter-spacing: 1px;
    margin: 12px 16px 4px;
}

/* ========== 顶部栏 ========== */
#topbar {
    background-color: #FFFFFF;
    border-bottom: 1px solid #E8ECF1;
    padding: 8px 16px;
}

#topbar QLabel {
    color: #2C3E50;
    font-size: 18px;
    font-weight: bold;
}

/* ========== 按钮 ========== */
QPushButton {
    background-color: #3498DB;
    color: #FFFFFF;
    border: none;
    border-radius: 6px;
    padding: 8px 20px;
    font-weight: bold;
    font-size: 13px;
}

QPushButton:hover {
    background-color: #2980B9;
}

QPushButton:pressed {
    background-color: #21618C;
}

QPushButton:disabled {
    background-color: #BDC3C7;
    color: #7F8C8D;
}

QPushButton#accent {
    background-color: #2ECC71;
}

QPushButton#accent:hover {
    background-color: #27AE60;
}

QPushButton#danger {
    background-color: #E74C3C;
}

QPushButton#danger:hover {
    background-color: #C0392B;
}

QPushButton#warning {
    background-color: #F39C12;
}

QPushButton#warning:hover {
    background-color: #E67E22;
}

/* ========== 标签页 ========== */
QTabWidget::pane {
    border: 1px solid #E8ECF1;
    border-radius: 8px;
    background-color: #FFFFFF;
}

QTabBar::tab {
    background-color: #ECF0F1;
    color: #7F8C8D;
    padding: 10px 24px;
    border-top-left-radius: 6px;
    border-top-right-radius: 6px;
    margin-right: 2px;
    font-weight: bold;
}

QTabBar::tab:selected {
    background-color: #FFFFFF;
    color: #3498DB;
}

QTabBar::tab:hover:!selected {
    background-color: #D5DBDB;
}

/* ========== 表格 ========== */
QTableWidget {
    background-color: #FFFFFF;
    border: 1px solid #E8ECF1;
    border-radius: 8px;
    gridline-color: #ECF0F1;
    selection-background-color: #EBF5FB;
    alternate-background-color: #F8FAFB;
}

QTableWidget::item {
    padding: 6px 8px;
}

QTableWidget::item:selected {
    background-color: #EBF5FB;
    color: #2C3E50;
}

QHeaderView::section {
    background-color: #F8F9FA;
    color: #7F8C8D;
    padding: 8px;
    border: none;
    border-bottom: 1px solid #E8ECF1;
    font-weight: bold;
    font-size: 12px;
}

QHeaderView::section:first {
    border-top-left-radius: 8px;
}

QHeaderView::section:last {
    border-top-right-radius: 8px;
}

/* ========== 滚动条 ========== */
QScrollBar:vertical {
    background-color: #F5F7FA;
    width: 8px;
    border-radius: 4px;
}

QScrollBar::handle:vertical {
    background-color: #CBD5E0;
    border-radius: 4px;
    min-height: 30px;
}

QScrollBar::handle:vertical:hover {
    background-color: #A0B4C8;
}

QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
    height: 0;
}

QScrollBar:horizontal {
    background-color: #F5F7FA;
    height: 8px;
    border-radius: 4px;
}

QScrollBar::handle:horizontal {
    background-color: #CBD5E0;
    border-radius: 4px;
    min-width: 30px;
}

QScrollBar::handle:horizontal:hover {
    background-color: #A0B4C8;
}

/* ========== 输入框 ========== */
QLineEdit, QTextEdit, QPlainTextEdit {
    background-color: #FFFFFF;
    border: 1px solid #DCE1E8;
    border-radius: 6px;
    padding: 6px 12px;
    color: #2C3E50;
    selection-background-color: #3498DB;
}

QLineEdit:focus, QTextEdit:focus, QPlainTextEdit:focus {
    border-color: #3498DB;
}

QLineEdit:disabled, QTextEdit:disabled, QPlainTextEdit:disabled {
    background-color: #ECF0F1;
    color: #A0AAB5;
}

/* ========== 下拉框 ========== */
QComboBox {
    background-color: #FFFFFF;
    border: 1px solid #DCE1E8;
    border-radius: 6px;
    padding: 6px 12px;
    color: #2C3E50;
}

QComboBox:hover {
    border-color: #3498DB;
}

QComboBox::drop-down {
    border: none;
    padding-right: 8px;
}

QComboBox QAbstractItemView {
    background-color: #FFFFFF;
    border: 1px solid #DCE1E8;
    selection-background-color: #3498DB;
    color: #2C3E50;
    outline: none;
    padding: 4px;
}

/* ========== 复选框 ========== */
QCheckBox {
    color: #2C3E50;
    spacing: 8px;
}

QCheckBox::indicator {
    width: 18px;
    height: 18px;
    border: 2px solid #BDC3C7;
    border-radius: 4px;
    background-color: #FFFFFF;
}

QCheckBox::indicator:checked {
    background-color: #3498DB;
    border-color: #3498DB;
}

/* ========== 分组框 ========== */
QGroupBox {
    background-color: #FFFFFF;
    border: 1px solid #E8ECF1;
    border-radius: 8px;
    margin-top: 12px;
    padding-top: 16px;
    font-weight: bold;
    color: #2C3E50;
}

QGroupBox::title {
    subcontrol-origin: margin;
    left: 12px;
    padding: 0 6px;
}

/* ========== 标签 ========== */
QLabel {
    background-color: transparent;
    color: #2C3E50;
}

/* ========== 工具栏 ========== */
QToolBar {
    background-color: #FFFFFF;
    border: none;
    border-bottom: 1px solid #E8ECF1;
    padding: 4px;
    spacing: 4px;
}

QToolBar QPushButton {
    background-color: transparent;
    border: none;
    border-radius: 4px;
    padding: 6px 12px;
    color: #2C3E50;
}

QToolBar QPushButton:hover {
    background-color: #EBF5FB;
}

/* ========== 消息提示框 ========== */
QMessageBox {
    background-color: #FFFFFF;
}

QMessageBox QLabel {
    color: #2C3E50;
}

QMessageBox QPushButton {
    min-width: 80px;
}

/* ========== 进度条 ========== */
QProgressBar {
    border: 1px solid #DCE1E8;
    border-radius: 6px;
    text-align: center;
    background-color: #ECF0F1;
    height: 20px;
}

QProgressBar::chunk {
    background-color: #3498DB;
    border-radius: 5px;
}

/* ========== 树形控件 ========== */
QTreeWidget {
    background-color: #FFFFFF;
    border: 1px solid #E8ECF1;
    border-radius: 8px;
    gridline-color: #ECF0F1;
}

QTreeWidget::item {
    padding: 4px 8px;
    border-radius: 4px;
}

QTreeWidget::item:selected {
    background-color: #EBF5FB;
}

/* ========== 分割器 ========== */
QSplitter::handle {
    background-color: #E8ECF1;
}

/* ========== 状态栏 ========== */
QStatusBar {
    background-color: #FFFFFF;
    border-top: 1px solid #E8ECF1;
    color: #7F8C8D;
    font-size: 12px;
}

/* ========== 对话框 ========== */
QDialog {
    background-color: #F5F7FA;
}

/* ========== 下拉面板 ========== */
QMenu {
    background-color: #FFFFFF;
    border: 1px solid #E8ECF1;
    border-radius: 8px;
    padding: 4px;
}

QMenu::item {
    padding: 8px 24px 8px 12px;
    border-radius: 4px;
}

QMenu::item:selected {
    background-color: #EBF5FB;
    color: #3498DB;
}

QMenu::separator {
    height: 1px;
    background-color: #E8ECF1;
    margin: 4px 12px;
}

/* ========== 工具提示 ========== */
QToolTip {
    background-color: #2C3E50;
    color: #FFFFFF;
    border: none;
    border-radius: 4px;
    padding: 4px 8px;
}

/* ========== 卡片式面板 ========== */
.QFrame#card {
    background-color: #FFFFFF;
    border: 1px solid #E8ECF1;
    border-radius: 12px;
}

/* ========== 统计数字 ========== */
.stat-value {
    font-size: 28px;
    font-weight: bold;
    color: #3498DB;
}

.stat-label {
    font-size: 12px;
    color: #7F8C8D;
}
"""

DARK_THEME = """
QWidget {
    background-color: #1A1D23;
    color: #E0E6ED;
    font-family: "Microsoft YaHei UI", "Segoe UI", sans-serif;
    font-size: 13px;
}

QMainWindow {
    background-color: #1A1D23;
}

#sidebar {
    background-color: #12141A;
    border: none;
}

#sidebar QPushButton {
    background-color: transparent;
    color: #6B8299;
    border: none;
    border-radius: 8px;
    padding: 10px 16px;
    text-align: left;
    font-size: 14px;
    margin: 2px 8px;
}

#sidebar QPushButton:hover {
    background-color: #1E2230;
    color: #FFFFFF;
}

#sidebar QPushButton:checked {
    background-color: #2980B9;
    color: #FFFFFF;
    font-weight: bold;
}

#sidebar QLabel {
    color: #4A5568;
    font-size: 11px;
    text-transform: uppercase;
    letter-spacing: 1px;
    margin: 12px 16px 4px;
}

#topbar {
    background-color: #1E2230;
    border-bottom: 1px solid #2D3748;
    padding: 8px 16px;
}

#topbar QLabel {
    color: #E0E6ED;
    font-size: 18px;
    font-weight: bold;
}

QPushButton {
    background-color: #2980B9;
    color: #FFFFFF;
    border: none;
    border-radius: 6px;
    padding: 8px 20px;
    font-weight: bold;
    font-size: 13px;
}

QPushButton:hover {
    background-color: #3498DB;
}

QPushButton:pressed {
    background-color: #21618C;
}

QPushButton:disabled {
    background-color: #4A5568;
    color: #718096;
}

QPushButton#accent {
    background-color: #27AE60;
}

QPushButton#accent:hover {
    background-color: #2ECC71;
}

QPushButton#danger {
    background-color: #C0392B;
}

QPushButton#danger:hover {
    background-color: #E74C3C;
}

QPushButton#warning {
    background-color: #E67E22;
}

QPushButton#warning:hover {
    background-color: #F39C12;
}

QTabWidget::pane {
    border: 1px solid #2D3748;
    border-radius: 8px;
    background-color: #1E2230;
}

QTabBar::tab {
    background-color: #2D3748;
    color: #718096;
    padding: 10px 24px;
    border-top-left-radius: 6px;
    border-top-right-radius: 6px;
    margin-right: 2px;
    font-weight: bold;
}

QTabBar::tab:selected {
    background-color: #1E2230;
    color: #3498DB;
}

QTabBar::tab:hover:!selected {
    background-color: #363F52;
}

QTableWidget {
    background-color: #1E2230;
    border: 1px solid #2D3748;
    border-radius: 8px;
    gridline-color: #2D3748;
    selection-background-color: #1A365D;
    alternate-background-color: #222836;
}

QTableWidget::item {
    padding: 6px 8px;
}

QTableWidget::item:selected {
    background-color: #1A365D;
    color: #E0E6ED;
}

QHeaderView::section {
    background-color: #222836;
    color: #718096;
    padding: 8px;
    border: none;
    border-bottom: 1px solid #2D3748;
    font-weight: bold;
    font-size: 12px;
}

QHeaderView::section:first {
    border-top-left-radius: 8px;
}

QHeaderView::section:last {
    border-top-right-radius: 8px;
}

QScrollBar:vertical {
    background-color: #1A1D23;
    width: 8px;
    border-radius: 4px;
}

QScrollBar::handle:vertical {
    background-color: #4A5568;
    border-radius: 4px;
    min-height: 30px;
}

QScrollBar::handle:vertical:hover {
    background-color: #6B8299;
}

QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
    height: 0;
}

QScrollBar:horizontal {
    background-color: #1A1D23;
    height: 8px;
    border-radius: 4px;
}

QScrollBar::handle:horizontal {
    background-color: #4A5568;
    border-radius: 4px;
    min-width: 30px;
}

QScrollBar::handle:horizontal:hover {
    background-color: #6B8299;
}

QLineEdit, QTextEdit, QPlainTextEdit {
    background-color: #222836;
    border: 1px solid #2D3748;
    border-radius: 6px;
    padding: 6px 12px;
    color: #E0E6ED;
    selection-background-color: #2980B9;
}

QLineEdit:focus, QTextEdit:focus, QPlainTextEdit:focus {
    border-color: #3498DB;
}

QComboBox {
    background-color: #222836;
    border: 1px solid #2D3748;
    border-radius: 6px;
    padding: 6px 12px;
    color: #E0E6ED;
}

QComboBox:hover {
    border-color: #3498DB;
}

QComboBox::drop-down {
    border: none;
    padding-right: 8px;
}

QComboBox QAbstractItemView {
    background-color: #222836;
    border: 1px solid #2D3748;
    selection-background-color: #2980B9;
    color: #E0E6ED;
    outline: none;
}

QCheckBox {
    color: #E0E6ED;
    spacing: 8px;
}

QCheckBox::indicator {
    width: 18px;
    height: 18px;
    border: 2px solid #4A5568;
    border-radius: 4px;
    background-color: #222836;
}

QCheckBox::indicator:checked {
    background-color: #2980B9;
    border-color: #2980B9;
}

QGroupBox {
    background-color: #1E2230;
    border: 1px solid #2D3748;
    border-radius: 8px;
    margin-top: 12px;
    padding-top: 16px;
    font-weight: bold;
    color: #E0E6ED;
}

QGroupBox::title {
    subcontrol-origin: margin;
    left: 12px;
    padding: 0 6px;
}

QLabel {
    background-color: transparent;
    color: #E0E6ED;
}

QToolBar {
    background-color: #1E2230;
    border: none;
    border-bottom: 1px solid #2D3748;
    padding: 4px;
    spacing: 4px;
}

QToolBar QPushButton {
    background-color: transparent;
    border: none;
    border-radius: 4px;
    padding: 6px 12px;
    color: #E0E6ED;
}

QToolBar QPushButton:hover {
    background-color: #222836;
}

QProgressBar {
    border: 1px solid #2D3748;
    border-radius: 6px;
    text-align: center;
    background-color: #222836;
    height: 20px;
}

QProgressBar::chunk {
    background-color: #3498DB;
    border-radius: 5px;
}

QTreeWidget {
    background-color: #1E2230;
    border: 1px solid #2D3748;
    border-radius: 8px;
    gridline-color: #2D3748;
}

QTreeWidget::item {
    padding: 4px 8px;
    border-radius: 4px;
}

QTreeWidget::item:selected {
    background-color: #1A365D;
}

QSplitter::handle {
    background-color: #2D3748;
}

QStatusBar {
    background-color: #1E2230;
    border-top: 1px solid #2D3748;
    color: #718096;
    font-size: 12px;
}

QDialog {
    background-color: #1A1D23;
}

QMenu {
    background-color: #1E2230;
    border: 1px solid #2D3748;
    border-radius: 8px;
    padding: 4px;
}

QMenu::item {
    padding: 8px 24px 8px 12px;
    border-radius: 4px;
}

QMenu::item:selected {
    background-color: #222836;
    color: #3498DB;
}

QMenu::separator {
    height: 1px;
    background-color: #2D3748;
    margin: 4px 12px;
}

QToolTip {
    background-color: #2C3E50;
    color: #FFFFFF;
    border: none;
    border-radius: 4px;
    padding: 4px 8px;
}
"""
