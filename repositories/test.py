from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from repositories.team_player_repository import TeamPlayerRepository
from repositories.team_repository import TeamRepository
import pprint

USERNAME = 'ACE'
PASSWORD = 'ace%40best%23'
HOST = '47.113.177.195'
DATABASE = 'ACE_db'

# 指定数据库，用于正常连接
DATABASE_URI = f'mysql+pymysql://{USERNAME}:{PASSWORD}@{HOST}/{DATABASE}'

# 创建数据库引擎
engine = create_engine(
    DATABASE_URI,
    echo=True,  # 输出 SQL 日志
    pool_size=10,
    max_overflow=20,
    pool_timeout=30,
    pool_recycle=3600
)

# 创建会话工厂
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 创建 Session
session = SessionLocal()

# 测试连接
try:
    with engine.connect() as conn:
        print("Database connection successful!")
except Exception as e:
    print(f"Database connection failed: {e}")

# 使用 Session
session = SessionLocal()
try:
    # 执行数据库操作
    team_repository = TeamRepository(session)
    pprint.pprint(team_repository.get_all_teams_with_season_detail(team_abbreviation="CB"))
    print("-----------------------------------------------------------------------------------")
    # team_player_repository = TeamPlayerRepository(session)
    # pprint.pprint(team_player_repository.get_team_player_with_season_detail_by_team(31))

    print("Session created successfully!")
finally:
    session.close()
    print("Session closed.")