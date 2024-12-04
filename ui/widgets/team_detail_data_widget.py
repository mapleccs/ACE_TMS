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

        # 使用数据库获取数据, 以CB为例
        team_data = self.team_detail_data("CB")

        # 队伍图标 (假设使用一个示例图片)
        self.team_icon = QLabel(team_membership_widget)
        self.team_icon.setObjectName("team_icon")
        pixmap = QPixmap(r"ui\GUI设计.png")  # 替换为你的图片路径
        self.team_icon.setPixmap(pixmap.scaled(100, 100, Qt.AspectRatioMode.KeepAspectRatio))
        grid_layout.addWidget(self.team_icon, 0, 0, 2, 1)  # 队伍图标跨2行1列

        # 队伍名称 Label
        self.team_name_label = QLabel("{0}".format(team_data.get("队伍全称")), team_membership_widget)
        self.team_name_label.setObjectName("long_label")
        grid_layout.addWidget(self.team_name_label, 0, 1, 1, 2)

        # CB Label
        self.team_label = QLabel("队伍简称：{0}".format(team_data.get("队伍简称")), team_membership_widget)
        self.team_label.setObjectName("short_label")
        grid_layout.addWidget(self.team_label, 0, 3)

        # 长文本 Label
        self.long_text_label = QLabel("成员数量：{0} \t 建立时间：{1}".format(team_data.get("成员数量"), team_data.get("建队日期")),
                                 team_membership_widget)
        self.long_text_label.setObjectName("long_text_label")
        grid_layout.addWidget(self.long_text_label, 1, 1, 1, 3)  # 跨3列放置长文本

        # 对局数量 Label
        self.match_count_label = QLabel("对局数量：{0}".format(team_data.get("对局数量")), team_membership_widget)
        self.match_count_label.setObjectName("short_label")
        grid_layout.addWidget(self.match_count_label, 2, 0)

        # 对局胜率 Label
        self.win_rate_label = QLabel("对局胜率：{0}".format(team_data.get("胜率")), team_membership_widget)
        self.win_rate_label.setObjectName("short_label")
        grid_layout.addWidget(self.win_rate_label, 2, 1)

        # 队伍积分 Label
        self.team_score_label = QLabel("队伍积分：{0}分".format(team_data.get("积分")), team_membership_widget)
        self.team_score_label.setObjectName("short_label")
        grid_layout.addWidget(self.team_score_label, 2, 2)

        # 队伍评级 Label
        self.team_rating_label = QLabel("队伍评级：{0}级".format(team_data.get("等级")), team_membership_widget)
        self.team_rating_label.setObjectName("short_label")
        grid_layout.addWidget(self.team_rating_label, 2, 3)

        # 联系方式1 Label
        self.contact1_label = QLabel("联系方式1：{0}".format(team_data.get("联系方式1")), team_membership_widget)
        self.contact1_label.setObjectName("long_label")
        grid_layout.addWidget(self.contact1_label, 3, 0, 1, 2)  # 跨2列

        # 联系方式2 Label
        self.contact2_label = QLabel("联系方式2：{0}".format(team_data.get("联系方式2")), team_membership_widget)
        self.contact2_label.setObjectName("long_label")
        grid_layout.addWidget(self.contact2_label, 3, 2, 1, 2)  # 跨2列

        # 使用独立的表格视图
        self.team_membership_table = TeamMembershipTableView(team_membership_widget)
        membership_data = team_data.get("队员信息")
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
        main_splitter.setSizes([500, 500])  # 将左侧的宽度设置为80px，右侧的宽度为700px

        # 设置右侧上/下区域的大小比例
        right_splitter.setSizes([50, 550])  # 右侧上部分占比 50px，右侧下部分占比 550px

        # 固定大小，防止用户调整
        main_splitter.setFixedWidth(900)  # 强制设置宽度为固定值（80 + 700）
        right_splitter.setFixedHeight(600)  # 强制设置高度为固定值（50 + 550）

        # 设置主布局，main_splitter已经是布局了，不需要再调用setLayout
        layout = QVBoxLayout(self)
        layout.setObjectName("team_detail_data_layout")
        layout.addWidget(main_splitter)
        self.setLayout(layout)  # 只需要调用一次

    def team_detail_data(self, TeamName: str):
        # 这是你的队伍数据，通常应该从数据库或其他数据源获取
        team_data = {
            "CB": {
                "队标url": "https://zhihuiss2024.oss-cn-nanjing.aliyuncs.com/img/202408012254082.png",
                "队伍全称": "CryBaby",
                "队伍简称": "CB",
                "成员数量": "13人",
                "建队日期": "2024-12-10",
                "对局数量": "10场",
                "胜率": "62%",
                "积分": "10",
                "等级": "C",
                "联系方式1": "10086",
                "联系方式2": "10086",
                "队员信息": {
                    "LS": {"位置": "上单", "游戏ID": "kxs#10086", "个人积分": "5", "队内职务": "队长"},
                    "子仁": {"位置": "打野", "游戏ID": "sa#10086", "个人积分": "5", "队内职务": "副队长"}
                }
            },
            "SSW": {
                "队标url": "https://zhihuiss2024.oss-cn-nanjing.aliyuncs.com/img/202408012254082.png",
                "队伍全称": "SuperStar Warriors",
                "队伍简称": "SSW",
                "成员数量": "11人",
                "建队日期": "2024-11-05",
                "对局数量": "8场",
                "胜率": "75%",
                "积分": "15",
                "等级": "C",
                "联系方式1": "10010",
                "联系方式2": "10010",
                "队员信息": {
                    "小明": {"位置": "中单", "游戏ID": "xiaoMing#12334", "个人积分": "8", "队内职务": "队长"},
                    "大龙": {"位置": "辅助", "游戏ID": "daLong#45623", "个人积分": "7", "队内职务": "副队长"}
                }
            },
            "QT": {
                "队标url": "https://zhihuiss2024.oss-cn-nanjing.aliyuncs.com/img/202408012254082.png",
                "队伍全称": "QuickTeam",
                "队伍简称": "QT",
                "成员数量": "12人",
                "建队日期": "2024-10-20",
                "对局数量": "15场",
                "胜率": "80%",
                "积分": "18",
                "等级": "C",
                "联系方式1": "123456789",
                "联系方式2": "987654321",
                "队员信息": {
                    "雷霆": {"位置": "上单", "游戏ID": "leiTing#78923", "个人积分": "10", "队内职务": "队长"},
                    "风暴": {"位置": "打野", "游戏ID": "fengBao#98723", "个人积分": "9", "队内职务": "副队长"}
                }
            },
            "DF": {
                "队标url": "https://zhihuiss2024.oss-cn-nanjing.aliyuncs.com/img/202408012254082.png",
                "队伍全称": "DreamForce",
                "队伍简称": "DF",
                "成员数量": "14人",
                "建队日期": "2024-09-10",
                "对局数量": "20场",
                "胜率": "85%",
                "积分": "20",
                "等级": "C",
                "联系方式1": "1122334455",
                "联系方式2": "5566778899",
                "队员信息": {
                    "风云": {"位置": "上单", "游戏ID": "fengYun#11223", "个人积分": "12", "队内职务": "队长"},
                    "星辰": {"位置": "辅助", "游戏ID": "xingChen#22323", "个人积分": "11", "队内职务": "副队长"}
                }
            }
        }

        # 查找队伍信息
        if TeamName in team_data:
            team = team_data[TeamName]

            # 将队员信息整理成列表格式
            membership_data = []
            for member_name, member_info in team["队员信息"].items():
                # 按照需求的格式构造字典
                member_data = {
                    '位置': member_info['位置'],
                    '昵称': member_name,  # 使用队员的名字作为“昵称”
                    '游戏ID': member_info['游戏ID'],
                    '积分': member_info['个人积分'],
                    '职务': member_info['队内职务']
                }
                membership_data.append(member_data)

            # 添加整理后的队员信息到返回结果中
            team["队员信息"] = membership_data

            return team
        else:
            return {"error": "队伍未找到"}

    def update_team_details(self, TeamName):
        team_data = self.team_detail_data(TeamName)
        self.team_name_label.setText("{0}".format(team_data.get("队伍全称")))
        self.team_label.setText(f"队伍简称: {team_data.get('队伍简称')}")
        self.long_text_label.setText(f"成员数量: {team_data.get('成员数量')} 建队时间: {team_data.get('建队日期')}")
        self.match_count_label.setText(f"对局数量: {team_data.get('对局数量')}")
        self.win_rate_label.setText(f"对局胜率: {team_data.get('胜率')}")
        self.team_score_label.setText(f"队伍积分: {team_data.get('积分')}")
        self.team_rating_label.setText(f"队伍评级: {team_data.get('等级')}")
        self.contact1_label.setText(f"联系方式1: {team_data.get('联系方式1')}")
        self.contact2_label.setText(f"联系方式2: {team_data.get('联系方式2')}")
        # 更新队员信息表格
        membership_data = team_data.get("队员信息")
        self.membership_model.set_data(membership_data)
