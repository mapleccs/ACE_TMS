USERNAME = 'root'
PASSWORD = '123456'
HOST = 'localhost'
DATABASE = 'ace_tms'

# 不指定数据库，用于创建数据库
DATABASE_URI_NO_DB = f'mysql+pymysql://{USERNAME}:{PASSWORD}@{HOST}/'

# 指定数据库，用于正常连接
DATABASE_URI = f'mysql+pymysql://{USERNAME}:{PASSWORD}@{HOST}/{DATABASE}'
