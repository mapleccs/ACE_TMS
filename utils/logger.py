import logging
import os
from datetime import datetime

logger = logging.getLogger("ACE联盟管理系统")
logger.setLevel(logging.DEBUG)  # 设置最低日志级别

formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

# 控制台处理器
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)

# 文件处理器
log_directory = "logs"
if not os.path.exists(log_directory):
    os.makedirs(log_directory)

log_filename = datetime.now().strftime("app_%Y%m%d_%H%M%S.log")
file_handler = logging.FileHandler(os.path.join(log_directory, log_filename))
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

# 如果需要，添加更多处理器（例如，SMTPHandler发送错误邮件）
