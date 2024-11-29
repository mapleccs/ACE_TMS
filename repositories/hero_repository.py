from models.hero import Hero
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

class HeroRepository:
    def __init__(self, session: Session):
        self.session = session

    def add_hero(self, hero: Hero):
        """添加新英雄"""
        try:
            self.session.add(hero)
            self.session.commit()
            return hero
        except SQLAlchemyError as e:
            self.session.rollback()
            raise e

    def get_hero_by_id(self, hero_id: int):
        """根据ID获取英雄"""
        return self.session.query(Hero).filter(hero_id == Hero.ID).first()

    def get_hero_by_name(self, hero_name: str):
        """根据名称获取英雄"""
        return self.session.query(Hero).filter(hero_name ==Hero.HeroName).first()

    def get_all_heroes(self):
        """获取所有英雄"""
        return self.session.query(Hero).all()

    def update_hero(self, hero: Hero):
        """更新英雄信息"""
        try:
            self.session.commit()
            return hero
        except SQLAlchemyError as e:
            self.session.rollback()
            raise e

    def delete_hero(self, hero: Hero):
        """删除英雄"""
        try:
            self.session.delete(hero)
            self.session.commit()
        except SQLAlchemyError as e:
            self.session.rollback()
            raise e
