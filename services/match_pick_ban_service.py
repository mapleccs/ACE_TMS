from repositories.match_pick_ban_repository import MatchPickBanRepository
from models.match_pick_ban import MatchPickBan
from sqlalchemy.orm import Session


"""英雄表service层"""
class MatchPickBanService:
    def __init__(self, session: Session):
        self.session = session
        self.match_pick_ban_repository = MatchPickBanRepository(session)

    def get_all_match_pick_bans(self, entity: MatchPickBan):
        return self.match_pick_ban_repository.get_all_match_pick_bans()

    def add_match_pick_ban(self, entity: MatchPickBan):
        ## match_pick_ban = MatchPickBan(MatchPickBanName=match_pick_ban_name)
        return self.match_pick_ban_repository.add_match_pick_ban(entity)

    def update_match_pick_ban(self, entity: MatchPickBan):
        match_pick_ban = self.match_pick_ban_repository.get_match_pick_ban_by_id(entity.ID)
        if match_pick_ban:
            ## match_pick_ban.MatchPickBanName = new_name
            return self.match_pick_ban_repository.update_match_pick_ban(entity)
        else:
            return None

    def delete_match_pick_ban(self, match_pick_ban_id: int):
        match_pick_ban = self.match_pick_ban_repository.get_match_pick_ban_by_id(match_pick_ban_id)
        if match_pick_ban:
            self.match_pick_ban_repository.delete_match_pick_ban(match_pick_ban)
            return True
        else:
            return False
