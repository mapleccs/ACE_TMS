import json
import copy
from utils.logger import logger


class DataManager:
    def __init__(self, data_file_path):
        self.data_file_path = data_file_path
        self.team_data = self.load_data()

    def load_data(self):
        """加载JSON数据文件"""
        try:
            with open(self.data_file_path, 'r', encoding='utf-8') as file:
                data = json.load(file)
            logger.info(f"成功加载数据文件: {self.data_file_path}")
            return data
        except FileNotFoundError:
            logger.error("文件未找到")
            return {}
        except json.JSONDecodeError:
            logger.error("JSON 格式错误")
            return {}
        except Exception as e:
            logger.exception(f"发生错误: {e}")
            return {}

    def get_team_detail(self, team_name):
        """获取指定战队的详细数据"""
        try:
            team = self.team_data.get(team_name)
            if team:
                # 创建团队数据的深拷贝，避免修改原始数据
                team_copy = copy.deepcopy(team)

                team_members = team_copy.get("队员信息", {})
                if not isinstance(team_members, dict):
                    logger.error(f"'队员信息' 的格式不正确: {type(team_members)}")
                    return {"error": "'队员信息' 格式错误"}

                # 将队员信息从字典转换为列表
                membership_data = [
                    {
                        '位置': member_info.get('位置', ''),
                        '昵称': member_name,
                        '游戏ID': member_info.get('游戏ID', ''),
                        '积分': member_info.get('个人积分', ''),
                        '职务': member_info.get('队内职务', '')
                    }
                    for member_name, member_info in team_members.items()
                ]

                # 更新复制的团队数据
                team_copy["队员信息"] = membership_data
                return team_copy
            else:
                logger.error(f"队伍未找到: {team_name}")
                return {"error": "队伍未找到"}
        except Exception as e:
            logger.exception(f"获取战队详细数据失败: {e}")
            return {"error": "获取战队详细数据失败"}
