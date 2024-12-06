from PyQt6.QtWidgets import QWidget, QVBoxLayout
from ui.widgets.components.match_records_table import MatchRecordsTableView, MatchRecordsTableModel


class MatchRecordsWidget(QWidget):
    def __init__(self, match_records_data, parent=None):
        super().__init__(parent)
        self.initUI(match_records_data)

    def initUI(self, match_records_data):
        layout = QVBoxLayout(self)
        layout.setObjectName("match_records_layout")

        self.match_records_table = MatchRecordsTableView(self)
        self.match_records_model = MatchRecordsTableModel(match_records_data)
        self.match_records_table.setModel(self.match_records_model)
        layout.addWidget(self.match_records_table)

    def update_data(self, match_records_data):
        self.match_records_model.set_data(match_records_data)
