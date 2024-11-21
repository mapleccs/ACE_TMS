from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base
import config
from sqlalchemy_utils import database_exists, create_database

# 直接导入所有模型
from models.team import Team
from models.player import Player
from models.team_player import TeamPlayer
from models.hero import Hero
from models.match import Match
from models.match_bans import MatchBan
from models.match_picks import MatchPick
from models.player_match_stats import PlayerMatchStat


def main():
    engine = create_engine(config.DATABASE_URI, echo=True)

    # 检查数据库是否存在，如果不存在则创建
    if not database_exists(engine.url):
        create_database(engine.url)
        print("Database created.")
    else:
        print("Database already exists.")

    # 创建所有表
    Base.metadata.create_all(engine)
    print("All tables created.")

    # 创建会话
    Session = sessionmaker(bind=engine)
    session = Session()


if __name__ == '__main__':
    main()
