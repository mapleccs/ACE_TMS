from repositories.player_repository import PlayerRepository
from repositories.team_player_repository import TeamPlayerRepository
from models.player import Player
from models.team_player import TeamPlayer
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from datetime import datetime


class PlayerService:
    def __init__(self, session: Session):
        self.session = session
        self.player_repository = PlayerRepository(session)
        self.team_player_repository = TeamPlayerRepository(session)

    def get_all_players(self):
        return self.player_repository.get_all_players()

    def get_player_by_id(self, player_id: int):
        return self.player_repository.get_player_by_id(player_id)

    def add_player(self, player_name: str):
        # 检查玩家是否已存在
        existing_player = self.player_repository.get_player_by_name(player_name)
        if existing_player:
            raise ValueError("玩家名称已存在")
        new_player = Player(PlayerName=player_name)
        self.player_repository.add_player(new_player)
        return new_player

    def update_player(self, player_id: int, new_name: str):
        player = self.player_repository.get_player_by_id(player_id)
        if not player:
            raise ValueError("未找到指定的玩家")
        # 检查新名称是否已存在
        existing_player = self.player_repository.get_player_by_name(new_name)
        if existing_player and existing_player.PlayerID != player_id:
            raise ValueError("玩家名称已存在")
        player.PlayerName = new_name
        self.player_repository.update_player(player)
        return player

    def delete_player(self, player_id: int):
        player = self.player_repository.get_player_by_id(player_id)
        if not player:
            raise ValueError("未找到指定的玩家")
        self.player_repository.delete_player(player)
