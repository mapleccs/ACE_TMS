import os
from PyQt6.QtWidgets import QMainWindow, QSplitter
from PyQt6.QtCore import Qt
from ui.widgets.top_left_widget import TopLeftWidget
from ui.widgets.top_right_widget import TopRightWidget
from ui.widgets.bottom_left_widget import BottomLeftWidget
from ui.widgets.bottom_right_widget import BottomRightWidget
from utils.LoadQSS import apply_stylesheets
from utils.logger import logger


def safe_slot(func):
    """装饰器，用于捕获槽函数中的异常并记录日志"""
    def wrapper(*args, **kwargs):
        try:
            func(*args, **kwargs)
        except Exception as e:
            logger.exception(f"槽函数 {func.__name__} 发生异常: {e}")
    return wrapper


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        try:
            logger.info("应用程序启动")
            self.setup_ui()
            self.connect_signals()
            logger.info("主窗口初始化成功")
        except Exception as e:
            logger.exception(f"主窗口初始化失败: {e}")
            raise  # 重新抛出异常，确保程序不会在异常状态下继续运行

    def setup_ui(self):
        """设置主窗口的UI"""
        self.setWindowTitle("ACE联盟管理系统")
        self.setGeometry(100, 100, 1600, 900)  # 设置窗口大小

        # 应用样式表
        self.apply_styles()

        # 创建外部水平分割器，将界面分成左右两部分
        main_splitter = QSplitter(Qt.Orientation.Horizontal)

        # 创建左侧垂直分割器，将左侧再分为上、下两部分
        left_splitter = QSplitter(Qt.Orientation.Vertical)

        # 创建右侧垂直分割器，将右侧再分为上、下两部分
        right_splitter = QSplitter(Qt.Orientation.Vertical)

        # 创建各个部分的控件
        self.left_top_widget = TopLeftWidget()
        self.right_top_widget = TopRightWidget()
        self.left_bottom_widget = BottomLeftWidget()
        self.right_bottom_widget = BottomRightWidget()

        # 将各个部分添加到垂直分割器中
        left_splitter.addWidget(self.left_top_widget)
        left_splitter.addWidget(self.left_bottom_widget)
        right_splitter.addWidget(self.right_top_widget)
        right_splitter.addWidget(self.right_bottom_widget)

        # 将左侧和右侧垂直分割器添加到水平分割器中
        main_splitter.addWidget(left_splitter)
        main_splitter.addWidget(right_splitter)

        # 设置主界面为水平分割器
        self.setCentralWidget(main_splitter)

        # 设置分割器的初始大小比例
        main_splitter.setSizes([300, 1300])  # 根据需要调整比例
        left_splitter.setSizes([100, 200])  # 上下部分比例
        right_splitter.setSizes([100, 1000])  # 上下部分比例

        # 禁止用户调整分割器（可选，根据需要决定）
        main_splitter.setHandleWidth(0)
        left_splitter.setHandleWidth(0)
        right_splitter.setHandleWidth(0)

    def apply_styles(self):
        """应用样式表"""
        try:
            apply_stylesheets(self)
            logger.info("样式表应用成功")
        except Exception as e:
            logger.exception(f"应用样式表失败: {e}")

    def connect_signals(self):
        """连接信号与槽"""
        # 使用装饰器包装槽函数，确保异常被捕获并记录
        self.left_top_widget.home_button_clicked.connect(self.safe_show_home_page)
        self.left_top_widget.home_button_clicked.connect(self.right_top_widget.show_home_page)

        self.left_bottom_widget.team_button_clicked.connect(self.safe_show_team_table_page)
        self.left_bottom_widget.team_button_clicked.connect(self.right_top_widget.show_team_search_page)

        self.left_bottom_widget.team_details_management_button_clicked.connect(self.safe_show_team_detail_page)
        self.left_bottom_widget.team_details_management_button_clicked.connect(
            self.right_top_widget.show_team_detail_page)

        self.right_top_widget.search_teams_signal.connect(
            self.right_bottom_widget.team_management_widget.update_table_data)
        self.right_top_widget.sort_teams_signal.connect(self.right_bottom_widget.team_management_widget.sort_teams)
        self.right_top_widget.team_selection_signal.connect(
            self.right_bottom_widget.team_detail_data_widget.update_team_details)
        self.right_top_widget.team_detail_modify_button.clicked.connect(self.safe_on_modify_clicked)

        # 连接表格中的队伍选中信号
        self.right_bottom_widget.team_management_widget.team_table.team_selected.connect(
            self.safe_show_team_detail_page)
        self.right_bottom_widget.team_management_widget.team_table.team_selected.connect(
            self.right_top_widget.show_team_detail_page)
        self.right_bottom_widget.team_management_widget.team_table.team_selected.connect(
            self.right_bottom_widget.team_detail_data_widget.update_team_details)
        self.right_bottom_widget.team_management_widget.team_table.team_selected.connect(
            self.right_top_widget.set_team_detail_combo_text)

    @safe_slot
    def safe_show_home_page(self):
        """切换到欢迎页面"""
        self.right_bottom_widget.right_panel.setCurrentWidget(self.right_bottom_widget.home_page_label)

    @safe_slot
    def safe_show_team_table_page(self):
        """切换到战队数据面板"""
        self.right_bottom_widget.right_panel.setCurrentWidget(self.right_bottom_widget.team_management_widget)

    @safe_slot
    def safe_show_team_detail_page(self, *args, **kwargs):
        """切换到战队详细数据面板"""
        self.right_bottom_widget.right_panel.setCurrentWidget(self.right_bottom_widget.team_detail_data_widget)

    @safe_slot
    def safe_on_modify_clicked(self, *args, **kwargs):
        """处理修改按钮点击事件"""
        self.on_modify_clicked()

    @safe_slot
    def on_modify_clicked(self):
        """发射自定义信号或直接调用主面板的槽函数"""
        self.right_bottom_widget.team_detail_data_widget.show_player_registration()
