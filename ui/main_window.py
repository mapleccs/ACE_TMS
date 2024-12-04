from PyQt6.QtWidgets import QMainWindow, QSplitter
from PyQt6.QtCore import Qt
from ui.widgets.top_left_widget import TopLeftWidget
from ui.widgets.top_right_widget import TopRightWidget
from ui.widgets.bottom_left_widget import BottomLeftWidget
from ui.widgets.bottom_right_widget import BottomRightWidget
from utils.LoadQSS import apply_stylesheets


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("ACE联盟管理系统")
        self.setGeometry(100, 100, 1600, 900)  # 设置窗口大小

        # 调用加载 QSS 样式的函数，自动加载 QSS 文件
        self.apply_styles()

        # 创建外部水平分割器，将界面分成左右两部分
        main_splitter = QSplitter(Qt.Orientation.Horizontal)

        # 创建左侧垂直分割器，将左侧再分为上、下两部分
        left_splitter = QSplitter(Qt.Orientation.Vertical)

        # 创建右侧垂直分割器，将右侧再分为上、下两部分
        right_splitter = QSplitter(Qt.Orientation.Vertical)

        # 创建各个部分的控件
        self.left_top_widget = TopLeftWidget()
        self.right_top_widget = TopRightWidget()
        self.left_bottom_widget = BottomLeftWidget()
        self.right_bottom_widget = BottomRightWidget()

        # 将各个部分添加到垂直分割器中
        left_splitter.addWidget(self.left_top_widget)
        left_splitter.addWidget(self.left_bottom_widget)
        right_splitter.addWidget(self.right_top_widget)
        right_splitter.addWidget(self.right_bottom_widget)

        # 将左侧和右侧垂直分割器添加到水平分割器中
        main_splitter.addWidget(left_splitter)
        main_splitter.addWidget(right_splitter)

        # 设置主界面为水平分割器
        self.setCentralWidget(main_splitter)

        # 设置左侧和右侧的初始大小比例
        main_splitter.setSizes([10, 600])  # 左侧宽度300px，右侧宽度700px

        # 设置左侧上/下区域的大小比例
        left_splitter.setSizes([50, 550])  # 左侧上部分占比 2，左侧下部分占比 1

        # 设置右侧上/下区域的大小比例
        right_splitter.setSizes([50, 550])  # 右侧上部分占比 2，右侧下部分占比 1

        # 禁止用户调整分割器
        main_splitter.setHandleWidth(0)  # 禁用水平分割器的调整
        left_splitter.setHandleWidth(0)  # 禁用左侧垂直分割器的调整
        right_splitter.setHandleWidth(0)  # 禁用右侧垂直分割器的调整

        # -----------------------------> 信号连接 <---------------------------------------
        # 点击"ACE联盟管理系统"按钮，显示主界面
        self.left_top_widget.home_button_clicked.connect(self.show_home_page)
        # 点击"ACE联盟管理系统"按钮，对"导航栏"进行显示，这里为空白导航栏
        self.left_top_widget.home_button_clicked.connect(self.right_top_widget.show_home_page)
        # 点击"战队管理"按钮，显示"战队表格"
        self.left_bottom_widget.team_button_clicked.connect(self.show_team_table_page)
        # "战队管理" -> "导航栏" -> 点击"战队搜索栏"，对表格进行查询搜索
        self.right_top_widget.search_teams_signal.connect(self.right_bottom_widget.team_management_widget.update_table_data)
        # "战队管理" -> "导航栏" -> 点击"排序下拉框"，对表格进行排序
        self.right_top_widget.sort_teams_signal.connect(self.right_bottom_widget.team_management_widget.sort_teams)
        # 点击"战队管理"按钮，显示"战队数据总览"导航栏
        self.left_bottom_widget.team_button_clicked.connect(self.right_top_widget.show_team_search_page)
        # 点击"战队管理资料"按钮，显示"战队数据"
        self.left_bottom_widget.team_details_management_button.clicked.connect(self.show_team_detail_page)
        # 点击"战队管理资料"按钮，显示"战队详情"导航栏
        self.left_bottom_widget.team_details_management_button.clicked.connect(self.right_top_widget.show_team_detail_page)
        # 点击"team_table"中的队伍配置，显示"战队详情页面"
        self.right_bottom_widget.team_management_widget.team_table.team_selected.connect(self.show_team_detail_page)
        # 点击"team_table"中的队伍配置，显示"战队详情"导航栏
        self.right_bottom_widget.team_management_widget.team_table.team_selected.connect(self.right_top_widget.show_team_detail_page)
        # "战队详情" -> "导航栏" -> 点击"队伍选择"下拉框，跳转到对应的队伍界面
        self.right_top_widget.team_selection_signal.connect(self.right_bottom_widget.team_detail_data_widget.update_team_details)
        # 点击"team_table"中的队伍配置，跳转到对应的"战队详情页面"
        self.right_bottom_widget.team_management_widget.team_table.team_selected.connect(self.right_bottom_widget.team_detail_data_widget.update_team_details)
        # 点击"team_table"中的队伍配置，改变"战队详情" -> "导航栏" -> 点击"队伍选择"下拉框的队伍名称
        self.right_bottom_widget.team_management_widget.team_table.team_selected.connect(self.right_top_widget.set_team_detail_combo_text)

    def show_home_page(self):
        """切换到欢迎页面"""
        self.right_bottom_widget.right_panel.setCurrentWidget(self.right_bottom_widget.home_page_label)

    def show_team_table_page(self):
        """切换到战队数据面板"""
        self.right_bottom_widget.right_panel.setCurrentWidget(self.right_bottom_widget.team_management_widget)

    def show_team_detail_page(self):
        """切换到战队详细数据面板"""
        self.right_bottom_widget.right_panel.setCurrentWidget(self.right_bottom_widget.team_detail_data_widget)

    def apply_styles(self):
        """应用样式表"""
        # 调用 LoadQSS.py 中的 apply_stylesheets 函数
        apply_stylesheets(self)
