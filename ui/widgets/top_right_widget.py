from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import QWidget, QStackedWidget, QHBoxLayout, QLabel, QLineEdit, QVBoxLayout, QComboBox, QPushButton


class TopRightWidget(QWidget):

    search_teams_signal = pyqtSignal(str)       # 定义一个信号，用于传递搜索关键词
    sort_teams_signal = pyqtSignal(str)         # 添加一个信号，用于排序字段的变化
    team_selection_signal = pyqtSignal(str)     # 添加一个信号，用于传递队伍选择字段

    def __init__(self):
        super().__init__()
        self._updating_combo = False  # 添加标志位
        self.right_top_panel = QStackedWidget()

        # 创建home开始空白页面
        self.home_page_widget = QWidget()
        home_page_layout = QVBoxLayout()
        home_page_layout.addWidget(QLabel())
        self.home_page_widget.setLayout(home_page_layout)

        # -----------------------------> 创建战队数据搜索栏导航栏 <----------------------------------
        self.team_search_widget = QWidget()
        team_count_layout = QHBoxLayout()
        self.team_count_label = QLabel("战队数据总览")
        self.team_count_label.setObjectName("team_label")
        self.team_search_input = QLineEdit()
        self.team_search_input.setObjectName("team_search_input")
        self.team_search_input.setPlaceholderText("检索：队伍名称")
        self.sort_combo = QComboBox()
        self.sort_combo.addItem("排序方式：积分")
        self.sort_combo.addItem("排序方式：日期")
        self.sort_combo.addItem("排序方式：队名")
        self.sort_combo.addItem("排序方式：人数")
        self.sort_combo.setObjectName("sort_combo")
        team_count_layout.addWidget(self.team_count_label)
        team_count_layout.addWidget(self.sort_combo)
        team_count_layout.addWidget(self.team_search_input)
        self.team_search_widget.setLayout(team_count_layout)

        # -----------------------------> 创建战队管理导航栏 <----------------------------------
        self.team_detail_widget = QWidget()
        self.team_detail_label = QLabel("战队详情")
        self.team_detail_label.setObjectName("team_detail_label")
        self.team_detail_combo = QComboBox()
        self.team_detail_combo.addItem("CB")
        self.team_detail_combo.addItem("SSW")
        self.team_detail_combo.addItem("QT")
        self.team_detail_combo.addItem("DF")
        self.team_detail_combo.setObjectName("sort_combo")
        self.team_detail_modify_button = QPushButton("修改信息")
        self.team_detail_modify_button.setObjectName("team_button")

        # 创建“取消修改”和“保存修改”按钮，但初始时隐藏
        self.team_detail_cancel_button = QPushButton("取消修改")
        self.team_detail_cancel_button.setObjectName("team_button")
        self.team_detail_save_button = QPushButton("保存修改")
        self.team_detail_save_button.setObjectName("team_button")

        team_detail_layout = QHBoxLayout()
        team_detail_layout.setObjectName("team_detail_layout")
        team_detail_layout.addWidget(self.team_detail_label)
        team_detail_layout.addWidget(self.team_detail_combo)
        team_detail_layout.addWidget(self.team_detail_modify_button)
        team_detail_layout.addWidget(self.team_detail_cancel_button)
        team_detail_layout.addWidget(self.team_detail_save_button)

        # 设置按钮的初始可见性
        self.team_detail_cancel_button.hide()
        self.team_detail_save_button.hide()

        # 设置各控件在布局中的占比
        team_detail_layout.setStretch(0, 1)  # 控件 0（team_detail_label）占1份空间
        team_detail_layout.setStretch(1, 3)  # 控件 1（team_detail_combo）占3份空间
        team_detail_layout.setStretch(2, 1)  # 控件 2（team_detail_modify_button）占1份空间
        team_detail_layout.setStretch(3, 1)  # 控件 3（team_detail_cancel_button）占1份空间
        team_detail_layout.setStretch(4, 1)  # 控件 4（team_detail_save_button）占1份空间

        self.team_detail_widget.setLayout(team_detail_layout)

        # 创建其它页面（例如对局数据搜索界面等）
        self.other_widget = QWidget()
        other_layout = QVBoxLayout()
        other_layout.addWidget(QLabel("其他功能"))
        self.other_widget.setLayout(other_layout)

        # 将所有页面添加到 QStackedWidget 中
        self.right_top_panel.addWidget(self.home_page_widget)  # home 页面
        self.right_top_panel.addWidget(self.team_search_widget)  # 战队数据搜索导航栏
        self.right_top_panel.addWidget(self.team_detail_widget)  # 战队详情导航栏
        self.right_top_panel.addWidget(self.other_widget)  # 其他页面

        # 默认显示home空白界面
        self.right_top_panel.setCurrentWidget(self.home_page_widget)

        right_top_layout = QVBoxLayout()
        right_top_layout.addWidget(self.right_top_panel)

        self.setLayout(right_top_layout)

        # 连接信号
        self.team_search_input.textChanged.connect(self.emit_search_signal)
        self.sort_combo.currentIndexChanged.connect(self.emit_sort_signal)
        self.team_detail_combo.currentIndexChanged.connect(self.emit_team_selection_signal)

        # 连接按钮点击信号
        self.team_detail_modify_button.clicked.connect(self.enter_edit_mode)
        self.team_detail_cancel_button.clicked.connect(self.exit_edit_mode)
        self.team_detail_save_button.clicked.connect(self.save_changes)

    def emit_search_signal(self):
        """发射信号，将搜索框中的内容传递出去"""
        search_text = self.team_search_input.text()
        self.search_teams_signal.emit(search_text)

    def emit_sort_signal(self):
        """发射信号，将选择的排序字段传递出去"""
        sort_criteria = self.sort_combo.currentText()
        self.sort_teams_signal.emit(sort_criteria)

    def emit_team_selection_signal(self):
        if self._updating_combo:
            return
        team_selection = self.team_detail_combo.currentText()
        self.team_selection_signal.emit(team_selection)

    def show_home_page(self):
        """切换到空白界面"""
        self.right_top_panel.setCurrentWidget(self.home_page_widget)

    def show_team_search_page(self):
        """切换到战队数据搜索导航栏"""
        self.right_top_panel.setCurrentWidget(self.team_search_widget)

    def show_team_detail_page(self):
        """切换到战队详情导航栏"""
        self.right_top_panel.setCurrentWidget(self.team_detail_widget)

    def enter_edit_mode(self):
        """进入编辑模式，显示取消和保存按钮，隐藏修改按钮"""
        self.team_detail_modify_button.hide()
        self.team_detail_cancel_button.show()
        self.team_detail_save_button.show()

        # 你可以在这里启用编辑功能，例如允许修改 ComboBox 或其他控件
        self.team_detail_combo.setEnabled(True)

    def exit_edit_mode(self):
        """退出编辑模式，隐藏取消和保存按钮，显示修改按钮"""
        self.team_detail_modify_button.show()
        self.team_detail_cancel_button.hide()
        self.team_detail_save_button.hide()

        # 取消编辑，恢复原始状态
        # self.team_detail_combo.setEnabled(False)

        # 如果需要，可以重置 ComboBox 的选择或其他控件的状态
        # 例如，重新加载数据或清除输入
        # self.team_detail_combo.setCurrentIndex(0)

    def save_changes(self):
        """保存修改，执行相应的操作，然后退出编辑模式"""
        # 在这里添加保存修改的逻辑
        # 例如，获取 ComboBox 的当前值并更新数据源
        selected_team = self.team_detail_combo.currentText()
        # 你可以在这里添加更多逻辑，比如更新数据库或模型

        # 退出编辑模式
        self.exit_edit_mode()

    def set_team_detail_combo_text(self, TeamName: str):
        if self.team_detail_combo.currentText() != TeamName:
            self._updating_combo = True
            self.team_detail_combo.setCurrentText(TeamName)
            self._updating_combo = False
