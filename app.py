import sys
from PyQt6.QtWidgets import QApplication
from ui.main_window import MainWindow
from utils.db_utils import init_db
from utils.logger import logger  # 导入日志记录器


def main():
    # 记录应用程序启动
    logger.info("应用程序启动")

    # 创建 QApplication 实例
    app = QApplication(sys.argv)

    # 初始化数据库
    init_db()

    # 创建主窗口
    window = MainWindow()
    window.show()

    # 捕获异常并记录
    try:
        # 进入事件循环
        sys.exit(app.exec())
    except Exception as e:
        logger.exception("应用程序异常退出")


if __name__ == '__main__':
    main()
