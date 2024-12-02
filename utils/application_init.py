from PyQt6.QtWidgets import QApplication, QWidget
import sys


def ensure_qapplication_initialized():
    """检查是否已创建 QApplication 实例，防止 QWidget 在 QApplication 之前创建"""
    if QApplication.instance() is None:
        print("Error: QApplication must be created before any QWidget!")
        sys.exit(1)  # 终止程序，防止创建 QWidget 对象
