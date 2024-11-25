from repositories.player_match_stats_repository import PlayerMatchStatsRepository
from models.player_match_stats import PlayerMatchStats
from sqlalchemy.orm import Session

## 英雄表service层
class PlayerMatchStatsService:
    def __init__(self, session: Session):
        self.session = session
        self.player_match_stats_repository = PlayerMatchStatsRepository(session)

    def get_all_player_match_statss(self, entity: PlayerMatchStats):
        return self.player_match_stats_repository.get_all_player_match_statss()

    def add_player_match_stats(self, entity: PlayerMatchStats):
        ## player_match_stats = PlayerMatchStats(PlayerMatchStatsName=player_match_stats_name)
        return self.player_match_stats_repository.add_player_match_stats(entity)

    def update_player_match_stats(self, entity: PlayerMatchStats):
        player_match_stats = self.player_match_stats_repository.get_player_match_stats_by_id(entity.ID)
        if player_match_stats:
            ## player_match_stats.PlayerMatchStatsName = new_name
            return self.player_match_stats_repository.update_player_match_stats(entity)
        else:
            return None

    def delete_player_match_stats(self, player_match_stats_id: int):
        player_match_stats = self.player_match_stats_repository.get_player_match_stats_by_id(player_match_stats_id)
        if player_match_stats:
            self.player_match_stats_repository.delete_player_match_stats(player_match_stats)
            return True
        else:
            return False
