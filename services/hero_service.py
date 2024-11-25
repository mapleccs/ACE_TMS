from repositories.hero_repository import HeroRepository
from models.hero import Hero
from sqlalchemy.orm import Session

## 英雄表service层
class HeroService:
    def __init__(self, session: Session):
        self.session = session
        self.hero_repository = HeroRepository(session)

    def get_all_heros(self, entity: Hero):
        return self.hero_repository.get_all_heros()

    def add_hero(self, entity: Hero):
        ## hero = Hero(HeroName=hero_name)
        return self.hero_repository.add_hero(entity)

    def update_hero(self, entity: Hero):
        hero = self.hero_repository.get_hero_by_id(entity.HeroID)
        if hero:
            ## hero.HeroName = new_name
            return self.hero_repository.update_hero(entity)
        else:
            return None

    def delete_hero(self, hero_id: int):
        hero = self.hero_repository.get_hero_by_id(hero_id)
        if hero:
            self.hero_repository.delete_hero(hero)
            return True
        else:
            return False
