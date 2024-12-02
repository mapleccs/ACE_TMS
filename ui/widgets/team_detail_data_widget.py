from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QSplitter, QPushButton, QLineEdit, QGridLayout, QTableWidget, \
    QTableWidgetItem


class TeamDetailDataWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUI()

    def initUI(self):
        # 创建外部水平分割器，将界面分成左右两部分
        main_splitter = QSplitter(Qt.Orientation.Horizontal)

        # 创建右侧垂直分割器，将右侧再分为上、下两部分
        right_splitter = QSplitter(Qt.Orientation.Vertical)

        # 创建三个示例子部件
        team_membership_widget = QWidget()
        team_honor_widget = QWidget()
        match_records_widget = QWidget()

        # ----------------------> 战队成员配置panel <------------------------
        grid_layout = QGridLayout(team_membership_widget)

        # 队伍图标 (假设使用一个示例图片)
        team_icon = QLabel(team_membership_widget)
        team_icon.setObjectName("team_icon")
        pixmap = QPixmap(r"ui\GUI设计.png")  # 这里可以放置实际的图片路径
        team_icon.setPixmap(pixmap.scaled(100, 100, Qt.AspectRatioMode.KeepAspectRatio))
        grid_layout.addWidget(team_icon, 0, 0, 2, 1)  # 队伍图标跨2行1列

        # 队伍名称 Label
        team_name_label = QLabel("队伍名称", team_membership_widget)
        team_name_label.setObjectName("team_name_label")
        grid_layout.addWidget(team_name_label, 0, 1)

        # CB Label
        cb_label = QLabel("CB", team_membership_widget)
        cb_label.setObjectName("cb_label")
        grid_layout.addWidget(cb_label, 0, 3)

        # 长文本 Label
        long_text_label = QLabel("这是长文本内容，用来描述队伍的相关信息，可以详细介绍队伍的背景、成绩等。",
                                 team_membership_widget)
        long_text_label.setObjectName("long_text_label")
        grid_layout.addWidget(long_text_label, 1, 1, 1, 3)  # 跨3列放置长文本

        # 对局数量 Label
        match_count_label = QLabel("对局数量", team_membership_widget)
        match_count_label.setObjectName("match_count_label")
        grid_layout.addWidget(match_count_label, 2, 0)

        # 对局胜率 Label
        win_rate_label = QLabel("对局胜率", team_membership_widget)
        win_rate_label.setObjectName("win_rate_label")
        grid_layout.addWidget(win_rate_label, 2, 1)

        # 队伍积分 Label
        team_score_label = QLabel("队伍积分", team_membership_widget)
        team_score_label.setObjectName("team_score_label")
        grid_layout.addWidget(team_score_label, 2, 2)

        # 队伍评级 Label
        team_rating_label = QLabel("队伍评级", team_membership_widget)
        team_rating_label.setObjectName("team_rating_label")
        grid_layout.addWidget(team_rating_label, 2, 3)

        # 联系方式1 Label
        contact1_label = QLabel("联系方式1", team_membership_widget)
        contact1_label.setObjectName("contact1_label")
        grid_layout.addWidget(contact1_label, 3, 0, 1, 2)  # 跨2列

        # 联系方式2 Label
        contact2_label = QLabel("联系方式2", team_membership_widget)
        contact2_label.setObjectName("contact2_label")
        grid_layout.addWidget(contact2_label, 3, 2, 1, 2)  # 跨2列

        # 创建一个示例表格放在第5行
        table_widget = QTableWidget(team_membership_widget)
        table_widget.setObjectName("team_table")
        table_widget.setRowCount(5)  # 设置5行
        table_widget.setColumnCount(4)  # 设置4列

        # 填充表格中的一些示例数据
        table_widget.setItem(0, 0, QTableWidgetItem("数据1"))
        table_widget.setItem(0, 1, QTableWidgetItem("数据2"))
        table_widget.setItem(1, 0, QTableWidgetItem("数据3"))
        table_widget.setItem(1, 1, QTableWidgetItem("数据4"))

        # 添加表格到布局
        grid_layout.addWidget(table_widget, 4, 0, 1, 4)  # 表格跨4列

        # ----------------------> 战队荣誉panel <---------------------------
        top_layout = QVBoxLayout(team_honor_widget)
        top_layout.addWidget(QPushButton("Top Button"))

        # ----------------------> 比赛记录panel <---------------------------

        # 创建一个新的 widget 来容纳表格
        match_records_content_widget = QWidget(match_records_widget)
        match_records_content_widget.setObjectName("match_records_content_widget")

        # 创建一个布局来将表格放入这个 widget
        match_records_layout = QVBoxLayout(match_records_content_widget)

        # 创建一个表格
        match_table_widget = QTableWidget(match_records_content_widget)
        match_table_widget.setObjectName("match_table_widget")
        match_table_widget.setRowCount(5)  # 设置5行
        match_table_widget.setColumnCount(3)  # 设置3列

        # 设置表格的标题
        match_table_widget.setHorizontalHeaderLabels(["比赛时间", "对战队伍", "结果"])

        # 填充一些示例数据
        match_table_widget.setItem(0, 0, QTableWidgetItem("2024-12-01"))
        match_table_widget.setItem(0, 1, QTableWidgetItem("队伍A"))
        match_table_widget.setItem(0, 2, QTableWidgetItem("胜"))

        match_table_widget.setItem(1, 0, QTableWidgetItem("2024-12-02"))
        match_table_widget.setItem(1, 1, QTableWidgetItem("队伍B"))
        match_table_widget.setItem(1, 2, QTableWidgetItem("负"))

        # 将表格添加到布局
        match_records_layout.addWidget(match_table_widget)

        # 将这个新的 widget 添加到比赛记录 panel
        bottom_layout = QVBoxLayout(match_records_widget)
        bottom_layout.addWidget(match_records_content_widget)

        # 将右侧的两个部件添加到右侧分割器
        right_splitter.addWidget(team_honor_widget)
        right_splitter.addWidget(match_records_widget)

        # 将左侧部件和右侧分割器添加到主分割器
        main_splitter.addWidget(team_membership_widget)
        main_splitter.addWidget(right_splitter)

        # 设置左侧和右侧的初始大小比例，左侧宽度尽量小
        main_splitter.setSizes([80, 700])  # 将左侧的宽度设置为50px，右侧的宽度为700px

        # 设置右侧上/下区域的大小比例
        right_splitter.setSizes([50, 550])  # 右侧上部分占比 2，右侧下部分占比 1

        # 设置主布局，main_splitter已经是布局了，不需要再调用setLayout
        layout = QVBoxLayout(self)
        layout.addWidget(main_splitter)
        self.setLayout(layout)  # 只需要调用一次
