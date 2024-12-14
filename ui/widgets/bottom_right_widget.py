from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QStackedWidget
from ui.widgets.team_management import TeamManagementWidget
from ui.widgets.team_detail_data_widget import TeamDetailDataWidget
from ui.widgets.team_detail_entry_widget import TeamDetailEntryWidget
from utils.logger import logger
from utils.data_loader import TeamDetailDataLoaderThread


def safe_slot(func):
    """装饰器，用于捕获槽函数中的异常并记录日志"""

    def wrapper(*args, **kwargs):
        try:
            func(*args, **kwargs)
        except Exception as e:
            logger.exception(f"槽函数 {func.__name__} 发生异常: {e}")

    return wrapper


class BottomRightWidget(QWidget):
    def __init__(self):
        super().__init__()

        try:
            self.setup_ui()
            logger.info("BottomRightWidget 初始化成功")
        except Exception as e:
            logger.exception(f"BottomRightWidget 初始化失败: {e}")
            raise  # 重新抛出异常，确保程序不会在异常状态下继续运行

    def setup_ui(self):
        """设置 BottomRightWidget 的 UI"""
        self.setObjectName("bottom_right_widget")  # 设置主控件名称

        self.right_panel = QStackedWidget()
        self.right_panel.setObjectName('right_panel')  # 设置右侧面板名称

        self.home_page_label = QLabel("欢迎使用ACE联盟数据管理系统")
        self.home_page_label.setObjectName("home_page_label")  # 设置首页标签名称
        self.home_page_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.team_management_widget = TeamManagementWidget()
        self.team_management_widget.setObjectName('team_management_widget')  # 设置战队管理页面名称

        self.team_detail_data_widget = TeamDetailDataWidget()
        self.team_detail_data_widget.setObjectName('team_detail_data_widget')  # 设置战队数据详情页面名称

        self.team_detail_entry_widget = TeamDetailEntryWidget()
        self.team_detail_entry_widget.setObjectName('team_detail_entry_widget')     # 设置战队登记详情页面名称

        # 添加页面到 QStackedWidget
        self.right_panel.addWidget(self.home_page_label)
        self.right_panel.addWidget(self.team_management_widget)
        self.right_panel.addWidget(self.team_detail_data_widget)
        self.right_panel.addWidget(self.team_detail_entry_widget)

        # 设置布局
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)  # 移除默认边距
        layout.addWidget(self.right_panel)
        self.setLayout(layout)

        # 默认显示首页
        self.right_panel.setCurrentWidget(self.home_page_label)

    @safe_slot
    def switch_to_home_page(self):
        """切换到首页"""
        self.right_panel.setCurrentWidget(self.home_page_label)

    @safe_slot
    def switch_to_team_management(self):
        """切换到战队管理页面"""
        self.right_panel.setCurrentWidget(self.team_management_widget)

    @safe_slot
    def switch_to_team_detail_data(self):
        """切换到战队数据详情页面"""
        self.right_panel.setCurrentWidget(self.team_detail_data_widget)

    @safe_slot
    def switch_to_team_entry_widget(self):
        """切换到战队登记详情页面"""
        self.right_panel.setCurrentWidget(self.team_detail_entry_widget)

    @safe_slot
    def safe_show_team_detail_page(self):
        """切换到战队详细数据面板"""
        self.switch_to_team_detail_data()

    @safe_slot
    def safe_show_home_page(self):
        """切换到欢迎页面"""
        self.switch_to_home_page()

    @safe_slot
    def safe_show_team_table_page(self):
        """切换到战队数据面板"""
        self.switch_to_team_management()

    @safe_slot
    def safe_on_modify_clicked(self):
        """处理修改按钮点击事件"""
        self.on_modify_clicked()

    def on_modify_clicked(self):
        """发射自定义信号或直接调用主面板的槽函数"""
        self.team_detail_data_widget.show_player_registration()
