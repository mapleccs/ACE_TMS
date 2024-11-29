from models.player_match_stats import PlayerMatchStats
from sqlalchemy.orm import Session


class PlayerMatchStatsRepository:
    def __init__(self, session: Session):
        self.session = session

    def add_player_match_stats(self, stats: PlayerMatchStats):
        """添加玩家比赛统计数据"""
        self.session.add(stats)
        self.session.commit()
        return stats

    def get_stats_by_match_and_player(self, match_id: int, player_id: int):
        """获取指定比赛中指定玩家的统计数据"""
        return self.session.query(PlayerMatchStats).filter(
            match_id == PlayerMatchStats.MatchID,
            player_id == PlayerMatchStats.PlayerID
        ).first()

    def get_stats_by_match(self, match_id: int):
        """获取指定比赛的所有玩家统计数据"""
        return self.session.query(PlayerMatchStats).filter(
            match_id == PlayerMatchStats.MatchID
        ).all()

    def update_player_match_stats(self, stats: PlayerMatchStats):
        """更新玩家比赛统计数据"""
        self.session.commit()
        return stats

    def delete_stats_by_match(self, match_id: int):
        """删除指定比赛的所有玩家统计数据"""
        stats_list = self.get_stats_by_match(match_id)
        for stats in stats_list:
            self.session.delete(stats)
        self.session.commit()
