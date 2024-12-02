import sys
from PyQt6.QtWidgets import QApplication
from ui.main_window import MainWindow
from utils.db_utils import init_db


def main():
    # 创建 QApplication 实例
    app = QApplication(sys.argv)

    # 初始化数据库
    init_db()

    # 创建主窗口
    window = MainWindow()
    window.show()

    # 进入事件循环
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
