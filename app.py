import sys
from PyQt6.QtWidgets import QApplication
from ui.main_window import MainWindow
from utils.db_utils import init_db


def main():
    # 初始化数据库
    init_db()

    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
