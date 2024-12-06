import re
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QMessageBox
from ui.widgets.components.team_table import TeamTableView, TeamTableModel
from services.team_service import TeamService
from utils.db_utils import get_database_session
from utils.logger import logger
from PyQt6.QtCore import pyqtSignal
from utils.data_loader import TeamDataLoaderThread


def safe_slot(func):
    """装饰器，用于捕获槽函数中的异常并记录日志"""
    def wrapper(*args, **kwargs):
        try:
            func(*args, **kwargs)
        except Exception as e:
            logger.exception(f"槽函数 {func.__name__} 发生异常: {e}")
            QMessageBox.critical(None, "错误", f"发生错误: {e}")
    return wrapper


class TeamManagementWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.teams = []  # 初始化为空列表
        self.init_ui()

    def init_ui(self):
        """初始化UI组件"""
        try:
            layout = QVBoxLayout()

            # 初始化TeamTable视图，显示队伍信息
            self.team_table = TeamTableView()
            layout.addWidget(self.team_table)

            # 设置模型
            self.model = TeamTableModel()
            self.team_table.setModel(self.model)

            # 设置布局
            self.setLayout(layout)

            # 初始化数据加载线程
            self.data_loader_thread = TeamDataLoaderThread()
            self.data_loader_thread.data_loaded.connect(self.on_data_loaded)
            self.data_loader_thread.load_failed.connect(self.on_load_failed)
            self.data_loader_thread.start()

            logger.info("TeamManagementWidget UI 初始化成功")
        except Exception as e:
            logger.exception(f"TeamManagementWidget UI 初始化失败: {e}")
            QMessageBox.critical(self, "错误", f"初始化界面时发生错误: {e}")

    def on_data_loaded(self, teams):
        """数据加载完成的处理"""
        try:
            self.teams = teams
            self.model.set_data(self.teams)
            self.team_table.reset()  # 刷新表格视图
            logger.info(f"加载了 {len(self.teams)} 支队伍的数据")
        except Exception as e:
            logger.exception(f"处理加载完成的数据失败: {e}")
            QMessageBox.critical(self, "错误", f"处理加载完成的数据失败: {e}")

    def on_load_failed(self, error_message):
        """数据加载失败的处理"""
        logger.error(f"数据加载失败: {error_message}")
        QMessageBox.critical(self, "错误", f"数据加载失败: {error_message}")

    @safe_slot
    def update_table_data(self, search_text):
        """根据搜索文本更新表格数据"""
        try:
            if not search_text:
                # 如果搜索文本为空，显示所有数据
                filtered_data = self.teams
                logger.debug("搜索文本为空，显示所有队伍")
            else:
                # 根据搜索文本过滤数据
                filtered_data = self.filter_teams(search_text)
                logger.debug(f"根据搜索文本 '{search_text}' 过滤出 {len(filtered_data)} 支队伍")

            self.model.set_data(filtered_data)
            self.team_table.reset()  # 刷新表格视图
        except Exception as e:
            logger.exception(f"更新表格数据失败: {e}")
            QMessageBox.critical(self, "错误", f"更新表格数据失败: {e}")

    def filter_teams(self, search_text):
        """根据搜索文本过滤队伍数据"""
        try:
            search_text_lower = search_text.lower()
            filtered_data = [team for team in self.teams if search_text_lower in team.get('队伍名称', '').lower()]
            return filtered_data
        except Exception as e:
            logger.exception(f"过滤队伍数据失败: {e}")
            return []

    @safe_slot
    def sort_teams(self, sort_criteria):
        """根据选择的排序标准对队伍进行排序"""
        try:
            logger.debug(f"开始根据 '{sort_criteria}' 进行排序")
            if sort_criteria == "排序方式：队名":
                self.teams.sort(key=lambda x: x.get('队伍名称', ''))
            elif sort_criteria == "排序方式：人数":
                self.teams.sort(key=self.extract_team_size, reverse=True)
            elif sort_criteria == "排序方式：日期":
                self.teams.sort(key=lambda x: x.get('建队日期', ''))
            elif sort_criteria == "排序方式：积分":
                self.teams.sort(key=lambda x: x.get('队伍积分', 0), reverse=True)
            else:
                logger.warning(f"未知的排序标准: {sort_criteria}")
                return  # 不执行任何操作

            self.model.set_data(self.teams)
            self.team_table.reset()
            logger.info(f"已根据 '{sort_criteria}' 排序队伍")
        except Exception as e:
            logger.exception(f"排序队伍失败: {e}")
            QMessageBox.critical(self, "错误", f"排序队伍失败: {e}")

    def extract_team_size(self, team):
        """从'队伍配置'字段中提取数字部分并返回"""
        try:
            match = re.search(r'(\d+)', team.get('队伍配置', ''))
            if match:
                return int(match.group(1))
            return 0
        except Exception as e:
            logger.exception(f"提取队伍人数失败: {e}")
            return 0
