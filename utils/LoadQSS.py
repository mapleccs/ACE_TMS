from PyQt6.QtCore import QFile, QTextStream

# 定义一个常量，包含 QSS 文件的路径
QSS_FILES = [
    'ui/resources/QSS/TeamTable.qss',
    'ui/resources/QSS/MainWindow.qss',
    'ui/resources/QSS/MainNavigator.qss',
    'ui/resources/QSS/TeamDetailDataWidget.qss',
]


def load_stylesheet(filename):
    """加载单个 QSS 文件并返回样式表内容"""
    file = QFile(filename)
    if file.open(QFile.OpenModeFlag.ReadOnly):
        stylesheet = QTextStream(file).readAll()
        file.close()
        return stylesheet
    else:
        print(f"无法打开文件: {filename}")
        return ""


def apply_stylesheets(window):
    """加载并合并多个 QSS 文件，并应用到窗口"""
    combined_stylesheet = ""
    for filename in QSS_FILES:  # 使用 QSS_FILES 中的文件路径
        combined_stylesheet += load_stylesheet(filename)

    window.setStyleSheet(combined_stylesheet)
