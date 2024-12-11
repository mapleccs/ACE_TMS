from functools import wraps
from sqlalchemy.exc import SQLAlchemyError
from utils.logger import logger


def transactional(func):
    """
    装饰器：管理数据库事务。
    成功时提交事务，失败时回滚事务。
    """

    @wraps(func)
    def wrapper(*args, **kwargs):
        self = args[0]  # 假设第一个参数是 self
        try:
            result = func(*args, **kwargs)
            self.session.commit()
            return result
        except SQLAlchemyError as e:
            self.session.rollback()
            logger.exception(f"事务执行失败: {e}")
            raise

    return wrapper
