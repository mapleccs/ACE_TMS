from repositories.match_repository import MatchRepository
from models.match import Match
from sqlalchemy.orm import Session

"""英雄表service层"""
class MatchService:
    def __init__(self, session: Session):
        self.session = session
        self.match_repository = MatchRepository(session)

    def get_all_matchs(self, entity: Match):
        return self.match_repository.get_all_matchs()

    def add_match(self, entity: Match):
        ## match = Match(MatchName=match_name)
        return self.match_repository.add_match(entity)

    def update_match(self, match_id: int, entity: Match):
        match = self.match_repository.get_match_by_id(entity.MatchID)
        if match:
            ## match.MatchName = new_name
            return self.match_repository.update_match(entity)
        else:
            return None

    def delete_match(self, match_id: int):
        match = self.match_repository.get_match_by_id(match_id)
        if match:
            self.match_repository.delete_match(match)
            return True
        else:
            return False
