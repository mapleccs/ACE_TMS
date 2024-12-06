from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import QWidget, QStackedWidget, QHBoxLayout, QLabel, QLineEdit, QVBoxLayout, QComboBox, QPushButton
from utils.logger import logger


def safe_slot(func):
    """装饰器，用于捕获槽函数中的异常并记录日志"""

    def wrapper(*args, **kwargs):
        try:
            func(*args, **kwargs)
        except Exception as e:
            logger.exception(f"槽函数 {func.__name__} 发生异常: {e}")

    return wrapper


class TopRightWidget(QWidget):
    """
    右上侧导航栏小部件。

    提供主界面空白页、战队数据搜索栏、战队详情导航栏和其他页面的切换功能。
    发射多个信号：search_teams_signal、sort_teams_signal、team_selection_signal，
    用于上层逻辑对战队数据进行搜索、排序和选择。
    """

    search_teams_signal = pyqtSignal(str)  # 传递搜索关键词
    sort_teams_signal = pyqtSignal(str)  # 传递排序字段变化
    team_selection_signal = pyqtSignal(str)  # 传递队伍选择字段

    def __init__(self):
        super().__init__()
        logger.info("初始化 TopRightWidget")
        self._updating_combo = False  # 标志位，用于防止重复触发队伍选择信号
        self.init_ui()
        self.connect_signals()

    def init_ui(self):
        """初始化UI和子页面组件。"""
        self.right_top_panel = QStackedWidget()

        # 创建home空白页面
        self.home_page_widget = QWidget()
        home_page_layout = QVBoxLayout()
        home_page_layout.addWidget(QLabel())
        self.home_page_widget.setLayout(home_page_layout)

        # 战队数据搜索导航栏
        self.team_search_widget = self.create_team_search_widget()

        # 战队详情导航栏
        self.team_detail_widget = self.create_team_detail_widget()

        # 其他页面（示例）
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

        layout = QVBoxLayout()
        layout.addWidget(self.right_top_panel)
        self.setLayout(layout)

    def create_team_search_widget(self):
        """创建战队数据搜索导航栏页面。"""
        widget = QWidget()
        layout = QHBoxLayout()
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

        layout.addWidget(self.team_count_label)
        layout.addWidget(self.sort_combo)
        layout.addWidget(self.team_search_input)
        widget.setLayout(layout)
        return widget

    def create_team_detail_widget(self):
        """创建战队详情导航栏页面。"""
        widget = QWidget()
        layout = QHBoxLayout()
        layout.setObjectName("team_detail_layout")

        self.team_detail_label = QLabel("战队详情")
        self.team_detail_label.setObjectName("team_detail_label")

        self.team_detail_combo = QComboBox()
        for team_name in ["CB", "SSW", "QT", "DF"]:
            self.team_detail_combo.addItem(team_name)
        self.team_detail_combo.setObjectName("sort_combo")

        self.team_detail_modify_button = QPushButton("修改信息")
        self.team_detail_modify_button.setObjectName("team_button")

        self.team_detail_cancel_button = QPushButton("取消修改")
        self.team_detail_cancel_button.setObjectName("team_button")

        self.team_detail_save_button = QPushButton("保存修改")
        self.team_detail_save_button.setObjectName("team_button")

        # 初始隐藏取消和保存按钮
        self.team_detail_cancel_button.hide()
        self.team_detail_save_button.hide()

        layout.addWidget(self.team_detail_label)
        layout.addWidget(self.team_detail_combo)
        layout.addWidget(self.team_detail_modify_button)
        layout.addWidget(self.team_detail_cancel_button)
        layout.addWidget(self.team_detail_save_button)

        # 调整布局比例
        layout.setStretch(0, 1)
        layout.setStretch(1, 3)
        layout.setStretch(2, 1)
        layout.setStretch(3, 1)
        layout.setStretch(4, 1)

        widget.setLayout(layout)
        return widget

    def connect_signals(self):
        """连接信号与槽函数。"""
        self.team_search_input.textChanged.connect(self.emit_search_signal)
        self.sort_combo.currentIndexChanged.connect(self.emit_sort_signal)
        self.team_detail_combo.currentIndexChanged.connect(self.emit_team_selection_signal)

        self.team_detail_modify_button.clicked.connect(self.enter_edit_mode)
        self.team_detail_cancel_button.clicked.connect(self.exit_edit_mode)
        self.team_detail_save_button.clicked.connect(self.save_changes)

    @safe_slot
    def emit_search_signal(self, *args, **kwargs):
        """发射搜索队伍信号。"""
        search_text = self.team_search_input.text()
        self.search_teams_signal.emit(search_text)

    @safe_slot
    def emit_sort_signal(self, *args, **kwargs):
        """发射排序方式信号。"""
        sort_criteria = self.sort_combo.currentText()
        self.sort_teams_signal.emit(sort_criteria)

    @safe_slot
    def emit_team_selection_signal(self, *args, **kwargs):
        """发射队伍选择信号。"""
        if self._updating_combo:
            return
        team_selection = self.team_detail_combo.currentText()
        self.team_selection_signal.emit(team_selection)

    def show_home_page(self):
        """切换到首页空白界面。"""
        self.right_top_panel.setCurrentWidget(self.home_page_widget)

    def show_team_search_page(self):
        """切换到战队数据搜索导航栏。"""
        self.right_top_panel.setCurrentWidget(self.team_search_widget)

    def show_team_detail_page(self):
        """切换到战队详情导航栏。"""
        self.right_top_panel.setCurrentWidget(self.team_detail_widget)

    @safe_slot
    def enter_edit_mode(self, *args, **kwargs):
        """进入编辑模式，显示取消和保存按钮，并隐藏修改按钮。"""
        self.team_detail_modify_button.hide()
        self.team_detail_cancel_button.show()
        self.team_detail_save_button.show()
        # 启用编辑
        self.team_detail_combo.setEnabled(True)

    @safe_slot
    def exit_edit_mode(self, *args, **kwargs):
        """退出编辑模式，恢复初始状态。"""
        self.team_detail_modify_button.show()
        self.team_detail_cancel_button.hide()
        self.team_detail_save_button.hide()
        # self.team_detail_combo.setEnabled(False)
        # 如果需要，重置状态
        # self.team_detail_combo.setCurrentIndex(0)

    @safe_slot
    def save_changes(self, *args, **kwargs):
        """保存修改并退出编辑模式。"""
        selected_team = self.team_detail_combo.currentText()
        # 在此添加保存逻辑，如更新数据库或模型
        self.exit_edit_mode()

    def set_team_detail_combo_text(self, TeamName: str):
        """外部调用，用于更新队伍选择下拉框的文本。"""
        if self.team_detail_combo.currentText() != TeamName:
            self._updating_combo = True
            self.team_detail_combo.setCurrentText(TeamName)
            self._updating_combo = False
