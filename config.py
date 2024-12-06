from urllib.parse import quote_plus

USERNAME = 'ACE'
PASSWORD = 'ace@best#'
HOST = '47.113.177.195'
DATABASE = 'ACE_db'

# 对密码进行 URL 编码
encoded_password = quote_plus(PASSWORD)

# 构建连接字符串
DATABASE_URI = f'mysql+pymysql://{USERNAME}:{encoded_password}@{HOST}/{DATABASE}'

# 如果需要不指定数据库的 URI
DATABASE_URI_NO_DB = f'mysql+pymysql://{USERNAME}:{encoded_password}@{HOST}/'
