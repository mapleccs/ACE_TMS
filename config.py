from urllib.parse import quote_plus

USERNAME = '虚拟的'
PASSWORD = '虚拟的'
HOST = '127.0.0.1'
DATABASE = '虚拟的'

# 对密码进行 URL 编码
encoded_password = quote_plus(PASSWORD)

# 构建连接字符串
DATABASE_URI = f'mysql+pymysql://{USERNAME}:{encoded_password}@{HOST}/{DATABASE}'

# 如果需要不指定数据库的 URI
DATABASE_URI_NO_DB = f'mysql+pymysql://{USERNAME}:{encoded_password}@{HOST}/'
