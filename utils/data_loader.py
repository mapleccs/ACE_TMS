from PyQt6.QtCore import QThread, pyqtSignal
from services.team_service import TeamService
from utils.db_utils import get_database_session
from utils.logger import logger


class BaseDataLoaderThread(QThread):
    """
    基类，用于封装数据加载线程的通用逻辑。
    """
    data_loaded = pyqtSignal(object)  # 发射加载完成的数据
    load_failed = pyqtSignal(str)  # 发射加载失败的错误信息

    def __init__(self, parent=None):
        super().__init__(parent)

    def run(self):
        """
        子类需要重写此方法，实现具体的数据加载逻辑。
        """
        raise NotImplementedError("Subclasses must implement this method.")


class TeamDataLoaderThread(BaseDataLoaderThread):
    """
    线程类，用于加载所有团队数据。
    """

    def run(self):
        try:
            session = get_database_session()
            if session is None:
                raise ConnectionError("无法获取数据库会话")

            team_service = TeamService(session)
            logger.info("AAAAA")
            teams = team_service.get_all_teams()
            logger.info("BBBBB")

            if not isinstance(teams, list):
                raise ValueError("获取的团队数据格式不正确")

            self.data_loaded.emit(teams)
            logger.info(f"成功加载了 {len(teams)} 支队伍的数据")
        except Exception as e:
            logger.exception(f"加载团队数据失败: {e}")
            self.load_failed.emit(str(e))


class TeamDetailDataLoaderThread(BaseDataLoaderThread):
    """
    线程类，用于加载指定团队的详细数据。
    """

    def __init__(self, data_manager, team_name, parent=None):
        super().__init__(parent)
        self.data_manager = data_manager
        self.team_name = team_name

    def run(self):
        try:
            team_data = self.data_manager.get_team_detail(self.team_name)
            if "error" in team_data:
                raise ValueError(team_data["error"])

            self.data_loaded.emit(team_data)
            logger.info(f"成功加载战队 '{self.team_name}' 的详细数据")
        except Exception as e:
            logger.exception(f"加载战队 '{self.team_name}' 的详细数据失败: {e}")
            self.load_failed.emit(str(e))
