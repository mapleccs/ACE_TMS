import json


class DataManager:
    def __init__(self, data_file_path):
        self.data_file_path = data_file_path
        self.team_data = self.load_data()

    def load_data(self):
        try:
            with open(self.data_file_path, 'r', encoding='utf-8') as file:
                return json.load(file)
        except FileNotFoundError:
            print("文件未找到")
            return {}
        except json.JSONDecodeError:
            print("JSON 格式错误")
            return {}
        except Exception as e:
            print(f"发生错误: {e}")
            return {}

    def get_team_detail(self, team_name):
        team = self.team_data.get(team_name)
        if team:
            membership_data = [
                {
                    '位置': member_info['位置'],
                    '昵称': member_name,
                    '游戏ID': member_info['游戏ID'],
                    '积分': member_info['个人积分'],
                    '职务': member_info['队内职务']
                }
                for member_name, member_info in team.get("队员信息", {}).items()
            ]
            team["队员信息"] = membership_data
            return team
        else:
            return {"error": "队伍未找到"}
