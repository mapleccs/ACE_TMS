from repositories.team_player_repository import TeamPlayerRepository
from repositories.team_repository import TeamRepository
from models.team import Team
from sqlalchemy.orm import Session

"""队伍表service层"""


class TeamService:
    def __init__(self, session: Session):
        self.session = session
        self.team_repository = TeamRepository(session)
        self.team_player_repository = TeamPlayerRepository(session)

    def get_all_teams(self, entity: Team = None):
        """
        功能描述：可以获取队伍的基本信息，
        例如:名称，简称，队长ID等，并根据名称或简称模糊查询
        """
        # 提取查询条件
        team_name = None
        team_abbreviation = None
        if entity is not None:
            team_name = entity.TeamName
            team_abbreviation = entity.TeamAbbreviation

        # 获取队伍数据
        teams = self.team_repository.get_all_teams_with_season_detail(team_name, team_abbreviation)

        print(teams)
        # 新的键名映射
        new_key_names = {
            'teamName': '队伍全称',
            'teamAbbreviation': '队伍名称',
            'captainName': '队长ID',
            'captainQQ': '联系方式',
            'teamNum': '队伍配置',
            'createDate': '建队日期',
            'totalScore': '队伍积分',
            'level': '队伍等级'
        }

        # 处理数据，排除队伍名称并更换键名
        updated_teams = []

        for team in teams:
            updated_team = {}

            # 对每个键值进行转换
            for key, value in team.items():
                if key == 'teamName':  # 排除不需要的字段
                    continue
                elif key == 'createDate':  # 格式化创建日期
                    updated_team[new_key_names[key]] = value.strftime("%Y-%m-%d")  # 转换为 "yyyy-mm-dd" 格式
                elif key == 'teamNum':  # 格式化成员数量
                    updated_team[new_key_names[key]] = f"{value}人"  # 添加 "人"
                else:
                    updated_team[new_key_names[key]] = value  # 其他字段直接映射

            updated_teams.append(updated_team)

        return updated_teams

    def add_team(self, team_name: str):
        team = Team(TeamName=team_name)
        return self.team_repository.add_team(team)

    def update_team(self, team_id: int, new_name: str):
        team = self.team_repository.get_team_by_id(team_id)
        if team:
            team.TeamName = new_name
            return self.team_repository.update_team(team)
        else:
            return None

    def delete_team(self, team_id: int):
        team = self.team_repository.get_team_by_id(team_id)
        if team:
            self.team_repository.delete_team(team)
            return True
        else:
            return False

    def get_team_detail_data(self, teamName: str):
        """
        功能描述：可以获取队伍的基本信息。
        例如:名称，简称，队长ID等，并根据名称或简称模糊查询
        """
        # 队伍基本信息
        team = self.team_repository.get_team_by_name(teamName)
        # 队友信息
        teamPlayerList = self.team_player_repository.get_team_player_with_season_detail_by_team(team.ID)
        # 按队友名称分组
        # teamPlayerMap = groupby(teamPlayerList, key=lambda x: x[2])
        teamPlayerMap = self.group_by(teamPlayerList, "playerName")
        # 将队友数据，放入队伍表中
        team.teamPlayerMap = teamPlayerMap
        return team

    # 公用方法，以后写一个公共方法类，放那里面去
    # 定义一个函数，按照某个键值对数组中的元素进行分组
    def group_by(self, array, key):
        # 初始化一个空字典用于存储分组后的结果
        grouped_dict = {}
        for item in array:
            # 获取分组的键值
            group_key = item[key]
            # 如果字典中不存在这个键，则创建一个空列表
            if group_key not in grouped_dict:
                grouped_dict[group_key] = []
            # 将当前项添加到对应的分组列表中
            grouped_dict[group_key].append(item)
        return grouped_dict
