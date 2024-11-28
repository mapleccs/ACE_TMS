from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QApplication, QMainWindow, QSplitter, QVBoxLayout, QHBoxLayout, QWidget, QPushButton, \
    QStackedWidget, QLabel, QButtonGroup
from PyQt6.QtCore import Qt, QFile, QTextStream

from ui.widgets.match_management import MatchManagementWidget
from ui.widgets.player_management import PlayerManagementWidget
from ui.widgets.team_management import TeamManagementWidget


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("ACE联盟管理系统")
        self.setGeometry(100, 100, 1000, 600)  # 设置窗口大小

        self.load_stylesheet('ui/resources/QSS/MainWindow.qss')

        # 创建外部水平分割器，将界面分成左右两部分
        main_splitter = QSplitter(Qt.Orientation.Horizontal)

        # 创建左侧垂直分割器，将左侧再分为上、下两部分
        left_splitter = QSplitter(Qt.Orientation.Vertical)

        # 创建右侧垂直分割器，将右侧再分为上、下两部分
        right_splitter = QSplitter(Qt.Orientation.Vertical)

        # 创建左上、左下、右上、右下区域的 QWidget
        self.left_top_widget = QWidget()
        self.left_top_widget.setObjectName("left_top_widget")
        self.left_bottom_widget = QWidget()
        self.left_bottom_widget.setObjectName("left_bottom_widget")
        self.right_top_widget = QWidget()
        self.right_top_widget.setObjectName("right_top_widget")
        self.right_bottom_widget = QWidget()
        self.right_bottom_widget.setObjectName("right_bottom_widget")

        # 在左上区域放置按钮
        self.home_button = QPushButton("ACE联盟管理系统")
        self.home_button.setObjectName("home_button")
        left_top_layout = QHBoxLayout()
        left_top_layout.addWidget(self.home_button)
        self.left_top_widget.setLayout(left_top_layout)

        # 在左下区域放置按钮
        left_bottom_layout = QVBoxLayout()
        self.team_button = QPushButton("战队数据")
        self.team_button.setIcon(QIcon(r"ui\resources\ICON\信号格.png"))
        self.team_button.setObjectName("left_button")

        self.team_details_entry_button = QPushButton("战队资料录入")
        self.team_details_entry_button.setCheckable(True)  # 设置按钮为可选中状态
        self.team_details_entry_button.setChecked(False)   # 初始为未选中状态
        self.team_details_entry_button.setIcon(QIcon(r'ui\resources\ICON\空心圆点.png'))
        self.team_details_entry_button.setObjectName("second_button")

        self.team_details_management_button = QPushButton("战队资料管理")
        self.team_details_management_button.setCheckable(True)  # 设置按钮为可选中状态
        self.team_details_management_button.setChecked(False)   # 初始为未选中状态
        self.team_details_management_button.setIcon(QIcon(r'ui\resources\ICON\空心圆点.png'))
        self.team_details_management_button.setObjectName("second_button")

        self.match_button = QPushButton("对局资料")
        self.match_button.setObjectName("left_button")
        self.match_button.setIcon(QIcon(r"ui\resources\ICON\信号格.png"))

        self.match_details_entry_button = QPushButton("对局资料录入")
        self.match_details_entry_button.setCheckable(True)  # 设置按钮为可选中状态
        self.match_details_entry_button.setChecked(False)   # 初始为未选中状态
        self.match_details_entry_button.setIcon(QIcon(r'ui\resources\ICON\空心圆点.png'))
        self.match_details_entry_button.setObjectName("second_button")

        self.season_info_stats_button = QPushButton("赛季信息统计")
        self.season_info_stats_button.setCheckable(True)  # 设置按钮为可选中状态
        self.season_info_stats_button.setChecked(False)   # 初始为未选中状态
        self.season_info_stats_button.setIcon(QIcon(r'ui\resources\ICON\空心圆点.png'))
        self.season_info_stats_button.setObjectName("second_button")

        self.season_info_button = QPushButton("赛季信息")
        self.season_info_button.setObjectName("left_button")
        self.season_info_button.setIcon(QIcon(r"ui\resources\ICON\信号格.png"))

        self.team_match_stats_button = QPushButton("战队比赛统计")
        self.team_match_stats_button.setCheckable(True)  # 设置按钮为可选中状态
        self.team_match_stats_button.setChecked(False)   # 初始为未选中状态
        self.team_match_stats_button.setIcon(QIcon(r'ui\resources\ICON\空心圆点.png'))
        self.team_match_stats_button.setObjectName("second_button")

        self.player_match_stats_button = QPushButton("选手比赛统计")
        self.player_match_stats_button.setCheckable(True)  # 设置按钮为可选中状态
        self.player_match_stats_button.setChecked(False)   # 初始为未选中状态
        self.player_match_stats_button.setIcon(QIcon(r'ui\resources\ICON\空心圆点.png'))
        self.player_match_stats_button.setObjectName("second_button")

        self.hero_usage_stats_button = QPushButton("英雄使用统计")
        self.hero_usage_stats_button.setCheckable(True)  # 设置按钮为可选中状态
        self.hero_usage_stats_button.setChecked(False)   # 初始为未选中状态
        self.hero_usage_stats_button.setIcon(QIcon(r'ui\resources\ICON\空心圆点.png'))
        self.hero_usage_stats_button.setObjectName("second_button")

        # 创建一个按钮组，并将按钮添加到该组
        self.button_group = QButtonGroup(self)
        self.button_group.addButton(self.team_details_entry_button)
        self.button_group.addButton(self.team_details_management_button)
        self.button_group.addButton(self.match_details_entry_button)
        self.button_group.addButton(self.season_info_stats_button)
        self.button_group.addButton(self.team_match_stats_button)
        self.button_group.addButton(self.player_match_stats_button)
        self.button_group.addButton(self.hero_usage_stats_button)

        left_bottom_layout.addWidget(self.team_button)
        left_bottom_layout.addWidget(self.team_details_entry_button)
        left_bottom_layout.addWidget(self.team_details_management_button)
        left_bottom_layout.addWidget(self.match_button)
        left_bottom_layout.addWidget(self.match_details_entry_button)
        left_bottom_layout.addWidget(self.season_info_stats_button)
        left_bottom_layout.addWidget(self.season_info_button)
        left_bottom_layout.addWidget(self.team_match_stats_button)
        left_bottom_layout.addWidget(self.player_match_stats_button)
        left_bottom_layout.addWidget(self.hero_usage_stats_button)

        self.left_bottom_widget.setLayout(left_bottom_layout)

        # 在右上区域放置 界面 显示不同的内容
        right_top_layout = QHBoxLayout()
        self.right_top_widget.setLayout(right_top_layout)

        # 在右下区域放置 QStackedWidget 以展示不同的内容
        self.right_panel = QStackedWidget()
        self.home_page_label = QLabel("欢迎使用ACE联盟数据管理系统")  # 欢迎界面
        self.home_page_label.setObjectName("home_page_label")

        self.home_page_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.team_management_widget = TeamManagementWidget()
        self.match_management_widget = MatchManagementWidget()
        self.player_management_widget = PlayerManagementWidget()

        self.right_panel.addWidget(self.home_page_label)
        self.right_panel.addWidget(self.team_management_widget)
        self.right_panel.addWidget(self.match_management_widget)
        self.right_panel.addWidget(self.player_management_widget)

        # 将 QStackedWidget 放入右下部分
        self.right_bottom_widget.setLayout(QVBoxLayout())
        self.right_bottom_widget.layout().addWidget(self.right_panel)

        # 默认显示战队数据界面
        self.right_panel.setCurrentWidget(self.home_page_label)

        # 将左上、左下区域添加到左侧垂直分割器中
        left_splitter.addWidget(self.left_top_widget)
        left_splitter.addWidget(self.left_bottom_widget)

        # 将右上、右下区域添加到右侧垂直分割器中
        right_splitter.addWidget(self.right_top_widget)
        right_splitter.addWidget(self.right_bottom_widget)

        # 将左侧和右侧垂直分割器添加到水平分割器中
        main_splitter.addWidget(left_splitter)
        main_splitter.addWidget(right_splitter)

        # 设置主界面为水平分割器
        self.setCentralWidget(main_splitter)

        # 设置左侧和右侧的初始大小比例
        main_splitter.setSizes([200, 800])  # 左侧宽度300px，右侧宽度700px

        # 设置左侧上/下区域的大小比例
        left_splitter.setSizes([50, 550])  # 左侧上部分占比 2，左侧下部分占比 1

        # 设置右侧上/下区域的大小比例
        right_splitter.setSizes([50, 550])  # 右侧上部分占比 2，右侧下部分占比 1

        # 禁止用户调整分割器
        main_splitter.setHandleWidth(0)  # 禁用水平分割器的调整
        left_splitter.setHandleWidth(0)  # 禁用左侧垂直分割器的调整
        right_splitter.setHandleWidth(0)  # 禁用右侧垂直分割器的调整

        # 连接按钮点击事件
        self.home_button.clicked.connect(self.show_home_page)
        self.team_button.clicked.connect(self.show_team_widget)
        self.match_button.clicked.connect(self.show_match_widget)
        self.season_info_button.clicked.connect(self.show_player_widget)

    def show_home_page(self):
        """切换到欢迎页面"""
        self.right_panel.setCurrentWidget(self.home_page_label)

    def show_team_widget(self):
        """切换到战队数据界面"""
        self.right_panel.setCurrentWidget(self.team_management_widget)

    def show_match_widget(self):
        """切换到对局资料界面"""
        self.right_panel.setCurrentWidget(self.match_management_widget)

    def show_player_widget(self):
        """切换到赛季信息界面"""
        self.right_panel.setCurrentWidget(self.player_management_widget)

    def load_stylesheet(self, filename):
        """加载外部 QSS 文件"""
        file = QFile(filename)
        if file.open(QFile.OpenModeFlag.ReadOnly):
            stylesheet = QTextStream(file).readAll()
            self.setStyleSheet(stylesheet)
            file.close()


if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec()
