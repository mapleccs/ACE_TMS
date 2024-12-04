from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QSplitter, QPushButton, QGridLayout
from ui.widgets.components.match_records_table import MatchRecordsTableView, MatchRecordsTableModel
from ui.widgets.components.team_membership_table import TeamMembershipTableView, TeamMembershipTableModel


class TeamDetailDataWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUI()

    def initUI(self):
        # 创建外部水平分割器，将界面分成左右两部分
        main_splitter = QSplitter(Qt.Orientation.Horizontal)
        main_splitter.setObjectName('team_detail_data_splitter')

        # 创建右侧垂直分割器，将右侧再分为上、下两部分
        right_splitter = QSplitter(Qt.Orientation.Vertical)
        right_splitter.setObjectName('team_detail_data_splitter')

        # 创建三个示例子部件
        team_membership_widget = QWidget()
        team_membership_widget.setObjectName("team_membership_widget")
        team_honor_widget = QWidget()
        team_honor_widget.setObjectName("team_honor_widget")
        match_records_widget = QWidget()
        match_records_widget.setObjectName("match_records_widget")

        # ----------------------> 战队成员配置panel <------------------------
        grid_layout = QGridLayout(team_membership_widget)
        grid_layout.setObjectName("team_detail_data_layout")

        # 队伍图标 (假设使用一个示例图片)
        team_icon = QLabel(team_membership_widget)
        team_icon.setObjectName("team_icon")
        pixmap = QPixmap(r"ui\GUI设计.png")  # 替换为你的图片路径
        team_icon.setPixmap(pixmap.scaled(100, 100, Qt.AspectRatioMode.KeepAspectRatio))
        grid_layout.addWidget(team_icon, 0, 0, 2, 1)  # 队伍图标跨2行1列

        # 队伍名称 Label
        team_name_label = QLabel("队伍名称：CryBaby", team_membership_widget)
        team_name_label.setObjectName("long_label")
        grid_layout.addWidget(team_name_label, 0, 1, 1, 2)

        # CB Label
        team_label = QLabel("队伍简称：CB", team_membership_widget)
        team_label.setObjectName("short_label")
        grid_layout.addWidget(team_label, 0, 3)

        # 长文本 Label
        long_text_label = QLabel("成员数量：14人 \t 建立时间：2024-10-12",
                                 team_membership_widget)
        long_text_label.setObjectName("long_text_label")
        grid_layout.addWidget(long_text_label, 1, 1, 1, 3)  # 跨3列放置长文本

        # 对局数量 Label
        match_count_label = QLabel("对局数量：10局", team_membership_widget)
        match_count_label.setObjectName("short_label")
        grid_layout.addWidget(match_count_label, 2, 0)

        # 对局胜率 Label
        win_rate_label = QLabel("对局胜率：60%", team_membership_widget)
        win_rate_label.setObjectName("short_label")
        grid_layout.addWidget(win_rate_label, 2, 1)

        # 队伍积分 Label
        team_score_label = QLabel("队伍积分：13分", team_membership_widget)
        team_score_label.setObjectName("short_label")
        grid_layout.addWidget(team_score_label, 2, 2)

        # 队伍评级 Label
        team_rating_label = QLabel("队伍评级：C级", team_membership_widget)
        team_rating_label.setObjectName("short_label")
        grid_layout.addWidget(team_rating_label, 2, 3)

        # 联系方式1 Label
        contact1_label = QLabel("联系方式1：1008610010", team_membership_widget)
        contact1_label.setObjectName("long_label")
        grid_layout.addWidget(contact1_label, 3, 0, 1, 2)  # 跨2列

        # 联系方式2 Label
        contact2_label = QLabel("联系方式2：12345678910", team_membership_widget)
        contact2_label.setObjectName("long_label")
        grid_layout.addWidget(contact2_label, 3, 2, 1, 2)  # 跨2列

        # 使用独立的表格视图
        self.team_membership_table = TeamMembershipTableView(team_membership_widget)
        membership_data = [
            {'位置': '上单', '昵称': 'Player A', '游戏ID': 'KK#10000', '积分': '12', '职务': '队长'},
            {'位置': '上单', '昵称': 'Player B', '游戏ID': 'KK#10000', '积分': '12', '职务': '队员'},
            # 添加更多数据
        ]
        self.membership_model = TeamMembershipTableModel(membership_data)
        self.team_membership_table.setModel(self.membership_model)
        grid_layout.addWidget(self.team_membership_table, 4, 0, 1, 4)  # 表格跨4列

        # ----------------------> 战队荣誉panel <---------------------------
        top_layout = QVBoxLayout(team_honor_widget)
        top_layout.setObjectName("team_detail_data_layout")
        top_layout.addWidget(QPushButton("Top Button"))

        # ----------------------> 比赛记录panel <---------------------------
        self.match_records_table = MatchRecordsTableView(match_records_widget)
        match_records_data = [
            {'胜负': 'WIN', '时间': '2024-12-02', '比分': '1:2', '赛事类型': '第一季度常规赛',
             '回放': 'https://www.bilibili.com/', '数据': None},
            {'胜负': 'LOSE', '时间': '2024-12-03', '比分': '1:2', '赛事类型': '第一季度常规赛', '回放': None,
             '数据': None},
            # 添加更多数据
        ]
        self.match_records_model = MatchRecordsTableModel(match_records_data)
        self.match_records_table.setModel(self.match_records_model)
        match_records_layout = QVBoxLayout(match_records_widget)
        match_records_layout.setObjectName("team_detail_data_layout")
        match_records_layout.addWidget(self.match_records_table)

        # 将右侧的两个部件添加到右侧分割器
        right_splitter.addWidget(team_honor_widget)
        right_splitter.addWidget(match_records_widget)

        # 将左侧部件和右侧分割器添加到主分割器
        main_splitter.addWidget(team_membership_widget)
        main_splitter.addWidget(right_splitter)

        # 设置左侧和右侧的初始大小比例，左侧宽度尽量小
        main_splitter.setSizes([80, 700])  # 将左侧的宽度设置为80px，右侧的宽度为700px

        # 设置右侧上/下区域的大小比例
        right_splitter.setSizes([50, 550])  # 右侧上部分占比 50px，右侧下部分占比 550px

        # 设置主布局，main_splitter已经是布局了，不需要再调用setLayout
        layout = QVBoxLayout(self)
        layout.setObjectName("team_detail_data_layout")
        layout.addWidget(main_splitter)
        self.setLayout(layout)  # 只需要调用一次
