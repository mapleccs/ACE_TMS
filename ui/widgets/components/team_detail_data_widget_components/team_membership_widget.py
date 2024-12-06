from PyQt6.QtWidgets import QWidget, QGridLayout, QLabel
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt
from ui.widgets.components.team_membership_table import TeamMembershipTableView, TeamMembershipTableModel


class TeamMembershipWidget(QWidget):
    def __init__(self, team_data, parent=None):
        super().__init__(parent)
        self.initUI(team_data)

    def initUI(self, team_data):
        grid_layout = QGridLayout(self)
        grid_layout.setObjectName("team_membership_layout")

        # 队伍图标
        self.team_icon = QLabel(self)
        pixmap = QPixmap(r"ui\GUI设计.png")  # 替换为你的图片路径
        self.team_icon.setPixmap(pixmap.scaled(100, 100, Qt.AspectRatioMode.KeepAspectRatio))
        grid_layout.addWidget(self.team_icon, 0, 0, 2, 1)

        # 队伍名称
        self.team_name_label = QLabel("{0}".format(team_data.get("队伍全称")), self)
        self.team_name_label.setObjectName("long_label")
        grid_layout.addWidget(self.team_name_label, 0, 1, 1, 2)

        # 队伍简称
        self.team_label = QLabel("队伍简称：{0}".format(team_data.get("队伍简称")), self)
        self.team_label.setObjectName("short_label")
        grid_layout.addWidget(self.team_label, 0, 3)

        # 成员数量和建队时间
        self.long_text_label = QLabel(
            "成员数量：{0} \t 建立时间：{1}".format(
                team_data.get("成员数量"), team_data.get("建队日期")
            ),
            self
        )
        self.long_text_label.setObjectName("long_text_label")
        grid_layout.addWidget(self.long_text_label, 1, 1, 1, 3)

        # 对局数量
        self.match_count_label = QLabel("对局数量{0}".format(team_data.get("对局数量")), self)
        self.match_count_label.setObjectName("short_label")
        grid_layout.addWidget(self.match_count_label, 2, 0)

        # 对局胜率
        self.win_rate_label = QLabel("对局胜率：{0}".format(team_data.get("胜率")), self)
        self.win_rate_label.setObjectName("short_label")
        grid_layout.addWidget(self.win_rate_label, 2, 1)

        # 队伍积分
        self.team_score_label = QLabel("队伍积分：{0}分".format(team_data.get("积分")), self)
        self.team_score_label.setObjectName("short_label")
        grid_layout.addWidget(self.team_score_label, 2, 2)

        # 队伍评级 Label
        self.team_rating_label = QLabel("队伍评级：{0}级".format(team_data.get("等级")), self)
        self.team_rating_label.setObjectName("short_label")
        grid_layout.addWidget(self.team_rating_label, 2, 3)

        # 联系方式1 Label
        self.contact1_label = QLabel("联系方式1：{0}".format(team_data.get("联系方式1")), self)
        self.contact1_label.setObjectName("long_label")
        grid_layout.addWidget(self.contact1_label, 3, 0, 1, 2)  # 跨2列

        # 联系方式2 Label
        self.contact2_label = QLabel("联系方式2：{0}".format(team_data.get("联系方式2")), self)
        self.contact2_label.setObjectName("long_label")
        grid_layout.addWidget(self.contact2_label, 3, 2, 1, 2)  # 跨2列

        # 队伍成员表格
        self.team_membership_table = TeamMembershipTableView(self)
        self.membership_model = TeamMembershipTableModel(team_data.get("队员信息", []))
        self.team_membership_table.setModel(self.membership_model)
        grid_layout.addWidget(self.team_membership_table, 4, 0, 1, 4)

    def update_data(self, team_data):
        self.team_name_label.setText("{0}".format(team_data.get("队伍全称")))
        self.team_label.setText(f"队伍简称: {team_data.get('队伍简称')}")
        self.long_text_label.setText(
            f"成员数量: {team_data.get('成员数量')} 建队时间: {team_data.get('建队日期')}"
        )
        self.match_count_label.setText("对局数量：{0}".format(team_data.get("对局数量")))
        self.win_rate_label.setText("对局胜率：{0}".format(team_data.get("胜率")))
        self.team_score_label.setText("队伍积分：{0}分".format(team_data.get("积分")))
        self.team_rating_label.setText("队伍评级：{0}级".format(team_data.get("等级")))
        self.contact1_label.setText("联系方式1：{0}".format(team_data.get("联系方式1")))
        self.contact2_label.setText("联系方式2：{0}".format(team_data.get("联系方式2")))
        # 更新其他标签...
        self.membership_model.set_data(team_data.get("队员信息", []))
