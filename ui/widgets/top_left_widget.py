from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import QWidget, QHBoxLayout, QPushButton
from utils.logger import logger


def safe_slot(func):
    """装饰器，用于捕获槽函数中的异常并记录日志"""

    def wrapper(*args, **kwargs):
        try:
            func(*args, **kwargs)
        except Exception as e:
            logger.exception(f"槽函数 {func.__name__} 发生异常: {e}")

    return wrapper


class TopLeftWidget(QWidget):
    """
    左上侧的小部件，包含“ACE联盟管理系统”按钮。
    当用户点击该按钮时发射 `home_button_clicked` 信号。
    """
    home_button_clicked = pyqtSignal()

    def __init__(self):
        super().__init__()
        logger.info("初始化 TopLeftWidget")
        self.init_ui()

    def init_ui(self):
        """初始化UI组件和布局。"""
        self.home_button = QPushButton("ACE联盟管理系统")
        self.home_button.setObjectName("home_button")

        layout = QHBoxLayout()
        layout.addWidget(self.home_button)
        self.setLayout(layout)

        # 连接按钮点击事件到自定义信号
        self.home_button.clicked.connect(self.emit_home_button_clicked)

    @safe_slot
    def emit_home_button_clicked(self, *args, **kwargs):
        """发射home按钮点击信号。"""
        self.home_button_clicked.emit()
