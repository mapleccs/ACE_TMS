import logging
import os
from datetime import datetime

# 确保 logs 文件夹存在
LOG_DIR = os.path.join(os.path.dirname(__file__), '..', 'logs')
os.makedirs(LOG_DIR, exist_ok=True)

# 创建日志文件名，格式为 app_YYYY-MM-DD_HH-MM-SS.log
log_filename = datetime.now().strftime("app_%Y-%m-%d_%H-%M-%S.log")
log_filepath = os.path.join(LOG_DIR, log_filename)

# 创建 logger
logger = logging.getLogger("ACE_TMS")
logger.setLevel(logging.DEBUG)

# 创建控制台处理器
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)

# 创建文件处理器
fh = logging.FileHandler(log_filepath, encoding='utf-8')
fh.setLevel(logging.DEBUG)

# 创建日志格式
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
fh.setFormatter(formatter)

# 避免重复添加处理器
if not logger.handlers:
    # 添加处理器到 logger
    logger.addHandler(ch)
    logger.addHandler(fh)
