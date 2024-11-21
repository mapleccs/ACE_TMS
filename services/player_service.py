from repositories.player_repository import PlayerRepository
from models.player import Player


class PlayerService:
    def __init__(self, player_repository: PlayerRepository):
        self.player_repository = player_repository

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
