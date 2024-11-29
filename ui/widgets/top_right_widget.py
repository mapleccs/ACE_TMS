from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import QWidget, QStackedWidget, QHBoxLayout, QLabel, QLineEdit, QVBoxLayout


class TopRightWidget(QWidget):
    # 定义一个信号，用于传递搜索关键词
    search_teams_signal = pyqtSignal(str)

    def __init__(self):
        super().__init__()

        self.right_top_panel = QStackedWidget()

        # 创建战队数据搜索栏界面
        self.team_search_widget = QWidget()
        team_count_layout = QHBoxLayout()
        self.team_count_label = QLabel("战队数据总览")
        self.team_count_label.setObjectName("team_count_label")
        self.team_search_input = QLineEdit()
        self.team_search_input.setObjectName("team_search_input")
        self.team_search_input.setPlaceholderText("检索：队伍名称")

        team_count_layout.addWidget(self.team_count_label)
        team_count_layout.addWidget(self.team_search_input)
        self.team_search_widget.setLayout(team_count_layout)

        # 创建home开始空白页面
        self.home_page_widget = QWidget()
        home_page_layout = QVBoxLayout()
        home_page_layout.addWidget(QLabel())
        self.home_page_widget.setLayout(home_page_layout)

        # 创建其它页面（例如对局数据搜索界面等）
        self.other_widget = QWidget()
        other_layout = QVBoxLayout()
        other_layout.addWidget(QLabel("其他功能"))
        self.other_widget.setLayout(other_layout)

        # 将所有页面添加到 QStackedWidget 中
        self.right_top_panel.addWidget(self.home_page_widget)  # home 页面
        self.right_top_panel.addWidget(self.team_search_widget)  # 战队数据搜索页面
        self.right_top_panel.addWidget(self.other_widget)  # 其他页面

        # 默认显示home空白界面
        self.right_top_panel.setCurrentWidget(self.home_page_widget)

        right_top_layout = QVBoxLayout()
        right_top_layout.addWidget(self.right_top_panel)

        self.setLayout(right_top_layout)

    def emit_search_signal(self):
        """发射信号，将搜索框中的内容传递出去"""
        search_text = self.team_search_input.text()
        self.search_teams_signal.emit(search_text)

    def show_home_page(self):
        """切换到空白界面"""
        self.right_top_panel.setCurrentWidget(self.home_page_widget)

    def show_team_search_page(self):
        """切换到战队数据搜索界面"""
        self.right_top_panel.setCurrentWidget(self.team_search_widget)

