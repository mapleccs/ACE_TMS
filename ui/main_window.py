from PyQt6.QtWidgets import QApplication, QMainWindow, QSplitter, QVBoxLayout, QWidget, QPushButton, QStackedWidget, \
    QLabel
from PyQt6.QtCore import Qt
from ui.widgets.components.team_table import TeamTable
from ui.widgets.team_management import TeamManagementWidget
from ui.widgets.match_management import MatchManagementWidget
from ui.widgets.player_management import PlayerManagementWidget


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("英雄联盟比赛管理系统")
        self.setGeometry(100, 100, 1000, 600)  # 设置窗口大小

        # 创建 QSplitter，用于分隔左侧和右侧的内容
        splitter = QSplitter(Qt.Orientation.Horizontal)

        # 左侧：按钮区
        self.left_panel = QWidget()
        self.left_layout = QVBoxLayout()
        self.left_panel.setLayout(self.left_layout)

        # 创建按钮
        self.team_button = QPushButton("战队数据")
        self.match_button = QPushButton("对局资料")
        self.player_button = QPushButton("赛季信息")

        # 按钮点击事件
        self.team_button.clicked.connect(self.show_team_management)  # 切换到战队管理界面
        self.match_button.clicked.connect(self.show_match_management)  # 切换到对局管理界面
        self.player_button.clicked.connect(self.show_player_management)  # 切换到赛季信息管理界面

        # 将按钮添加到左侧
        self.left_layout.addWidget(self.team_button)
        self.left_layout.addWidget(self.match_button)
        self.left_layout.addWidget(self.player_button)

        # 右侧：内容展示区
        self.right_panel = QStackedWidget()

        # 初始化各个子界面
        self.home_page_widget = QLabel("欢迎使用ACE联盟数据管理系统")  # 欢迎界面
        self.home_page_widget.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.team_management_widget = TeamManagementWidget()  # 战队数据管理界面
        self.match_management_widget = MatchManagementWidget()  # 对局管理界面
        self.player_management_widget = PlayerManagementWidget()  # 赛季信息管理界面

        # 将子界面添加到 stacked widget
        self.right_panel.addWidget(self.home_page_widget)  # 欢迎界面
        self.right_panel.addWidget(self.team_management_widget)  # 战队管理界面
        self.right_panel.addWidget(self.match_management_widget)  # 对局管理界面
        self.right_panel.addWidget(self.player_management_widget)  # 赛季管理界面

        # 将左侧和右侧添加到 QSplitter
        splitter.addWidget(self.left_panel)
        splitter.addWidget(self.right_panel)

        # 设置 QSplitter 为主界面
        self.setCentralWidget(splitter)

    def show_home_page(self):
        """切换到欢迎页面"""
        self.right_panel.setCurrentWidget(self.home_page_widget)

    def show_team_management(self):
        """切换到战队管理页面"""
        self.right_panel.setCurrentWidget(self.team_management_widget)

    def show_match_management(self):
        """切换到对局管理页面"""
        self.right_panel.setCurrentWidget(self.match_management_widget)

    def show_player_management(self):
        """切换到赛季信息管理页面"""
        self.right_panel.setCurrentWidget(self.player_management_widget)


if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec()
