from PyQt6.QtWidgets import QMainWindow, QTabWidget
from ui.widgets.team_management import TeamManagementWidget
from ui.widgets.player_management import PlayerManagementWidget
from ui.widgets.match_management import MatchManagementWidget


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__(parent=None)
        self.setWindowTitle("英雄联盟比赛管理系统")
        self.resize(1024, 768)
        self.init_ui()

    def init_ui(self):
        self.init_menu_bar()
        self.init_tool_bar()
        self.init_status_bar()
        self.init_central_widget()

    def init_menu_bar(self):
        menu_bar = self.menuBar()

        # 文件菜单
        file_menu = menu_bar.addMenu("文件")
        # 添加菜单项，如打开、保存、退出等

        # 编辑菜单
        edit_menu = menu_bar.addMenu("编辑")
        # 添加菜单项，如撤销、重做等

        # 视图菜单
        view_menu = menu_bar.addMenu("视图")
        # 添加菜单项，如切换主题等

        # 帮助菜单
        help_menu = menu_bar.addMenu("帮助")
        # 添加菜单项，如关于、帮助文档等

    def init_tool_bar(self):
        tool_bar = self.addToolBar("工具栏")
        # 添加工具按钮，如添加队伍、添加玩家、添加比赛等

    def init_status_bar(self):
        status_bar = self.statusBar()
        status_bar.showMessage("就绪")

    def init_central_widget(self):
        # 使用 QTabWidget 管理各个功能模块
        self.tabs = QTabWidget()
        self.team_management = TeamManagementWidget()
        self.player_management = PlayerManagementWidget()
        self.match_management = MatchManagementWidget()
        # 其他模块...

        self.tabs.addTab(self.team_management, "队伍管理")
        self.tabs.addTab(self.player_management, "玩家管理")
        self.tabs.addTab(self.match_management, "比赛管理")
        # 添加其他模块的标签页

        self.setCentralWidget(self.tabs)
