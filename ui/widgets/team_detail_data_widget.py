from PyQt6.QtWidgets import QWidget, QVBoxLayout, QSplitter, QStackedWidget
from PyQt6.QtCore import Qt

from ui.widgets.components.team_detail_data_widget_components.data_manager import DataManager
from ui.widgets.components.team_detail_data_widget_components.team_membership_widget import TeamMembershipWidget
from ui.widgets.components.team_detail_data_widget_components.team_honor_widget import TeamHonorWidget
from ui.widgets.components.team_detail_data_widget_components.match_records_widget import MatchRecordsWidget
from ui.widgets.components.team_detail_data_widget_components.team_player_registration_widget import TeamPlayerRegistrationWidget  # 导入新面板


class TeamDetailDataWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.data_manager = DataManager(r"E:\Project\ACE_TMS\ui\team_data.json")
        self.initUI()

    def initUI(self):
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

        # 固定大小，防止调整
        self.main_splitter.setFixedWidth(900)
        self.right_splitter.setFixedHeight(600)

        # 主布局
        layout = QVBoxLayout(self)
        layout.setObjectName("team_detail_data_layout")
        layout.addWidget(self.main_splitter)
        self.setLayout(layout)

        # 连接队员登记面板的 back_clicked 信号到 restore_match_records 槽
        self.team_player_registration_widget.back_clicked.connect(self.restore_match_records)

    def update_team_details(self, team_name):
        team_data = self.data_manager.get_team_detail(team_name)
        if "error" in team_data:
            # 处理错误（例如，显示消息）
            print(team_data["error"])
            return

        # 更新战队成员
        self.team_membership_widget.update_data(team_data)

        # 更新比赛记录（这里假设从 team_data 获取比赛记录）
        match_records_data = team_data.get("比赛记录", [
            {'胜负': 'WIN', '时间': '2024-12-02', '比分': '1:2', '赛事类型': '第一季度常规赛',
             '回放': 'https://www.bilibili.com/', '数据': None},
            {'胜负': 'LOSE', '时间': '2024-12-03', '比分': '1:2', '赛事类型': '第一季度常规赛', '回放': None,
             '数据': None},
            # 添加更多数据
        ])
        self.match_records_widget.update_data(match_records_data)
        # 同样，可以更新荣誉面板的数据

    def show_player_registration(self):
        # 显示队员登记面板
        self.content_stack.setCurrentIndex(1)  # 显示队员登记面板

    def restore_match_records(self):
        # 显示比赛记录面板
        self.content_stack.setCurrentIndex(0)  # 显示比赛记录面板