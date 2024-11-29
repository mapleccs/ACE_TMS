from PyQt6.QtWidgets import QWidget, QStackedWidget, QHBoxLayout, QLabel, QLineEdit, QVBoxLayout


class TopRightWidget(QWidget):
    def __init__(self):
        super().__init__()

        self.right_top_panel = QStackedWidget()

        # 创建战队数据搜索栏界面
        self.team_search_widget = QWidget()
        team_search_layout = QHBoxLayout()
        self.team_search_label = QLabel("搜索战队数据")
        self.team_search_label.setObjectName("team_search_label")
        self.team_search_input = QLineEdit()
        self.team_search_input.setObjectName("team_search_input")
        self.team_search_input.setPlaceholderText("请输入搜索内容...")

        team_search_layout.addWidget(self.team_search_label)
        team_search_layout.addWidget(self.team_search_input)
        self.team_search_widget.setLayout(team_search_layout)

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

    def show_home_page(self):
        """切换到空白界面"""
        self.right_top_panel.setCurrentWidget(self.home_page_widget)

    def show_team_search_page(self):
        """切换到战队数据搜索界面"""
        self.right_top_panel.setCurrentWidget(self.team_search_widget)
