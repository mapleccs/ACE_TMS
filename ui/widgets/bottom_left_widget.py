import os
from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QButtonGroup
from PyQt6.QtGui import QIcon
from utils.logger import logger


def safe_slot(func):
    """装饰器，用于捕获槽函数中的异常并记录日志"""

    def wrapper(*args, **kwargs):
        try:
            func(*args, **kwargs)
        except Exception as e:
            logger.exception(f"槽函数 {func.__name__} 发生异常: {e}")

    return wrapper


class BottomLeftWidget(QWidget):
    """
    左下侧的控制面板小部件。

    提供战队数据、对局数据、赛季信息等按钮。
    发射相应的自定义信号以供主窗口或其他部件使用。
    """
    # 自定义信号
    team_button_clicked = pyqtSignal()
    team_details_entry_button_clicked = pyqtSignal()
    team_details_management_button_clicked = pyqtSignal()

    def __init__(self):
        super().__init__()
        logger.info("初始化 BottomLeftWidget")
        self.init_ui()

    def init_ui(self):
        """初始化UI组件和布局。"""
        layout = QVBoxLayout()

        # 创建主按钮
        self.team_button = self.create_button("战队数据", icon_path=":/ICON/信号格.png", object_name="left_button")

        # 可选按钮（勾选状态）
        self.team_details_entry_button = self.create_checkable_button("战队资料录入", icon_path=":/ICON/空心圆点.png")
        self.team_details_management_button = self.create_checkable_button("战队资料管理",
                                                                           icon_path=":/ICON/空心圆点.png")

        self.match_button = self.create_button("对局资料", icon_path=":/ICON/信号格.png", object_name="left_button")

        self.match_details_entry_button = self.create_checkable_button("对局资料录入", icon_path=":/ICON/空心圆点.png")
        self.season_info_stats_button = self.create_checkable_button("赛季信息统计", icon_path=":/ICON/空心圆点.png")

        self.season_info_button = self.create_button("赛季信息", icon_path=":/ICON/信号格.png",
                                                     object_name="left_button")

        self.team_match_stats_button = self.create_checkable_button("战队比赛统计", icon_path=":/ICON/空心圆点.png")
        self.player_match_stats_button = self.create_checkable_button("选手比赛统计", icon_path=":/ICON/空心圆点.png")
        self.hero_usage_stats_button = self.create_checkable_button("英雄使用统计", icon_path=":/ICON/空心圆点.png")

        # 创建按钮组以保证同一时间仅选中一个可选按钮（如果有此逻辑需求）
        self.button_group = QButtonGroup(self)
        for btn in [
            self.team_details_entry_button,
            self.team_details_management_button,
            self.match_details_entry_button,
            self.season_info_stats_button,
            self.team_match_stats_button,
            self.player_match_stats_button,
            self.hero_usage_stats_button
        ]:
            self.button_group.addButton(btn)

        # 添加到布局
        layout.addWidget(self.team_button)
        layout.addWidget(self.team_details_entry_button)
        layout.addWidget(self.team_details_management_button)
        layout.addWidget(self.match_button)
        layout.addWidget(self.match_details_entry_button)
        layout.addWidget(self.season_info_stats_button)
        layout.addWidget(self.season_info_button)
        layout.addWidget(self.team_match_stats_button)
        layout.addWidget(self.player_match_stats_button)
        layout.addWidget(self.hero_usage_stats_button)

        self.setLayout(layout)

        # 连接按钮点击事件到自定义信号
        self.team_button.clicked.connect(self.emit_team_button_clicked)
        self.team_details_management_button.clicked.connect(self.emit_team_details_management_button_clicked)
        self.team_details_entry_button.clicked.connect(self.emit_team_details_entry_button_clicked)

    def create_button(self, text, icon_path=None, object_name=None):
        """创建普通按钮的辅助方法。"""
        btn = QPushButton(text)
        if icon_path:
            btn.setIcon(QIcon(icon_path))
        if object_name:
            btn.setObjectName(object_name)
        return btn

    def create_checkable_button(self, text, icon_path=None):
        """创建可选中按钮的辅助方法。"""
        btn = QPushButton(text)
        btn.setCheckable(True)
        btn.setChecked(False)
        if icon_path:
            btn.setIcon(QIcon(icon_path))
        btn.setObjectName("second_button")
        return btn

    @safe_slot
    def emit_team_button_clicked(self, *args, **kwargs):
        """发射团队按钮点击信号。"""
        self.team_button_clicked.emit()

    @safe_slot
    def emit_team_details_entry_button_clicked(self, *args, **kwargs):
        """发射团队资料录入按钮点击信号。"""
        self.team_details_entry_button_clicked.emit()

    @safe_slot
    def emit_team_details_management_button_clicked(self, *args, **kwargs):
        """发射团队资料管理按钮点击信号。"""
        self.team_details_management_button_clicked.emit()
