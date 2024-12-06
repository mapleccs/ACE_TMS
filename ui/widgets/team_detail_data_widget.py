import os
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QSplitter, QStackedWidget, QMessageBox
from PyQt6.QtCore import Qt
from utils.data_manager import DataManager
from ui.widgets.components.team_detail_data_widget_components.team_membership_widget import TeamMembershipWidget
from ui.widgets.components.team_detail_data_widget_components.team_honor_widget import TeamHonorWidget
from ui.widgets.components.team_detail_data_widget_components.match_records_widget import MatchRecordsWidget
from ui.widgets.components.team_detail_data_widget_components.team_player_registration_widget import \
    TeamPlayerRegistrationWidget
from utils.logger import logger
from utils.data_loader import TeamDetailDataLoaderThread


def safe_slot(func):
    """装饰器，用于捕获槽函数中的异常并记录日志"""

    def wrapper(*args, **kwargs):
        try:
            func(*args, **kwargs)
        except Exception as e:
            logger.exception(f"槽函数 {func.__name__} 发生异常: {e}")
            QMessageBox.critical(None, "错误", f"发生错误: {e}")

    return wrapper


class TeamDetailDataWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        data_file_path = os.path.join(os.path.dirname(__file__), '..', 'team_data.json')
        self.data_manager = DataManager(data_file_path)
        self.initUI()

    def initUI(self):
        """初始化UI组件"""
        try:
            self.main_splitter = QSplitter(Qt.Orientation.Horizontal)
            self.main_splitter.setObjectName('team_detail_data_splitter')

            # 战队成员面板
            self.team_membership_widget = TeamMembershipWidget({}, self)
            self.main_splitter.addWidget(self.team_membership_widget)

            # 右侧分割器（荣誉和内容区域）
            self.right_splitter = QSplitter(Qt.Orientation.Vertical)
            self.right_splitter.setObjectName('right_splitter')

            self.team_honor_widget = TeamHonorWidget(self)
            self.right_splitter.addWidget(self.team_honor_widget)

            # 使用 QStackedWidget 来管理比赛记录和队员登记面板
            self.content_stack = QStackedWidget(self)
            self.match_records_widget = MatchRecordsWidget([], self)
            self.team_player_registration_widget = TeamPlayerRegistrationWidget(self)

            self.content_stack.addWidget(self.match_records_widget)  # 索引 0
            self.content_stack.addWidget(self.team_player_registration_widget)  # 索引 1

            self.right_splitter.addWidget(self.content_stack)

            self.main_splitter.addWidget(self.right_splitter)

            # 设置初始大小比例
            self.main_splitter.setSizes([500, 500])
            self.right_splitter.setSizes([50, 550])

            # 主布局
            layout = QVBoxLayout(self)
            layout.setContentsMargins(0, 0, 0, 0)  # 移除默认边距
            layout.addWidget(self.main_splitter)
            self.setLayout(layout)

            # 连接队员登记面板的 back_clicked 信号到 restore_match_records 槽
            self.team_player_registration_widget.back_clicked.connect(self.restore_match_records)

            logger.info("TeamDetailDataWidget UI 初始化成功")
        except Exception as e:
            logger.exception(f"TeamDetailDataWidget UI 初始化失败: {e}")
            QMessageBox.critical(self, "错误", f"初始化界面时发生错误: {e}")

    def load_team_details(self, team_name):
        """加载指定战队的详细数据"""
        try:
            self.team_name = team_name
            self.data_loader_thread = TeamDetailDataLoaderThread(self.data_manager, team_name)
            self.data_loader_thread.data_loaded.connect(self.on_data_loaded)
            self.data_loader_thread.load_failed.connect(self.on_load_failed)
            self.data_loader_thread.start()
            logger.info(f"开始加载战队 '{team_name}' 的详细数据")
        except Exception as e:
            logger.exception(f"启动数据加载线程失败: {e}")
            QMessageBox.critical(self, "错误", f"启动数据加载线程失败: {e}")

    def on_data_loaded(self, team_data):
        """处理加载完成的数据"""
        try:
            # 更新战队成员
            self.team_membership_widget.update_data(team_data)

            # 更新比赛记录
            match_records_data = team_data.get("比赛记录", [
                {'胜负': 'WIN', '时间': '2024-12-02', '比分': '1:2', '赛事类型': '第一季度常规赛',
                 '回放': 'https://www.bilibili.com/', '数据': None},
                {'胜负': 'LOSE', '时间': '2024-12-03', '比分': '1:2', '赛事类型': '第一季度常规赛', '回放': None,
                 '数据': None},
                # 添加更多数据
            ])
            self.match_records_widget.update_data(match_records_data)

            # 更新荣誉面板的数据（假设需要）
            # self.team_honor_widget.update_data(team_data.get("荣誉", []))

            logger.info(f"战队 '{self.team_name}' 的详细数据已更新")
        except Exception as e:
            logger.exception(f"处理加载完成的数据失败: {e}")
            QMessageBox.critical(self, "错误", f"处理加载完成的数据失败: {e}")

    def on_load_failed(self, error_message):
        """数据加载失败的处理"""
        logger.error(f"数据加载失败: {error_message}")
        QMessageBox.critical(self, "错误", f"数据加载失败: {error_message}")

    @safe_slot
    def update_team_details(self, team_name):
        """外部调用，用于更新战队详细数据"""
        self.load_team_details(team_name)

    @safe_slot
    def show_player_registration(self):
        """显示队员登记面板"""
        self.content_stack.setCurrentIndex(1)  # 显示队员登记面板

    @safe_slot
    def restore_match_records(self):
        """显示比赛记录面板"""
        self.content_stack.setCurrentIndex(0)  # 显示比赛记录面板
