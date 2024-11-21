from models.player import Player
from sqlalchemy.orm import Session


class PlayerRepository:
    def __init__(self, session: Session):
        self.session = session

    def add_player(self, player: Player):
        """添加新玩家"""
        self.session.add(player)
        self.session.commit()
        return player

    def get_player_by_id(self, player_id: int):
        """根据ID获取玩家"""
        return self.session.query(Player).filter(Player.PlayerID == player_id).first()

    def get_player_by_name(self, player_name: str):
        """根据名称获取玩家"""
        return self.session.query(Player).filter(Player.PlayerName == player_name).first()

    def get_all_players(self):
        """获取所有玩家"""
        return self.session.query(Player).all()

    def update_player(self, player: Player):
        """更新玩家信息"""
        self.session.commit()
        return player

    def delete_player(self, player: Player):
        """删除玩家"""
        self.session.delete(player)
        self.session.commit()
