from PyQt6 import QtCore
from PyQt6.QtGui import QFontMetrics
from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QTableWidget,
    QTableWidgetItem,
    QTableView,
)


class TableView(QWidget):
    def __init__(self):
        super().__init__()

        self.data = [[]]
        self.layout = QVBoxLayout()
        self.directory = ""
        self.dir_str = "Directory: " + self.directory
        self.dir_label = QLabel(self.dir_str)
        self.table = None
        self.selected_row = 0

        self.init_widget()

    def init_widget(self):
        """Initialize UI for table view widget."""
        self.setFixedHeight(180)

        self.layout.addWidget(self.dir_label)

        # initialize table

        self.init_table()
        self.layout.addWidget(self.table)

        self.setLayout(self.layout)

    def init_table(self):

        """Initialize critical storm table."""
        table = QTableWidget()
        table.setColumnCount(4)

        table.setHorizontalHeaderLabels(
            ("Location", "Event", "Critical Storm", "Critical Max Flow")
        )
        table.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        column_widths = [120, 120, 120, 120]
        table.setFixedWidth(sum(column_widths) + 40)
        table.horizontalHeader().setStretchLastSection(True)

        for i, width in enumerate(column_widths):
            table.setColumnWidth(i, width)

        table.setSelectionBehavior(QTableView.SelectionBehavior.SelectRows)
        table.cellClicked.connect(self.update_selected_row)
        self.table = table

    def update_selected_row(self, row, col):
        self.selected_row = row

    def update_label(self):
        """Update directory label with middle elision. Call after setting self.directory."""
        self.dir_str = "Directory: " + self.directory
        elided = self.elide_text(
            self.dir_label.font(), self.dir_str, self.table.width()
        )
        self.dir_label.setText(elided)

        self.update()

    def update_table(self):
        """Update table with class storm data. Call after setting self.data."""
        self.table.setRowCount(len(self.data))

        for i, row in enumerate(self.data):
            for j, cell in enumerate(row):
                self.table.setItem(i, j, QTableWidgetItem(str(cell)))

        self.update()

    @staticmethod
    def elide_text(QFont, text: str, width: int):
        """Helper function for eliding label text"""
        metrics = QFontMetrics(QFont)
        elided = metrics.elidedText(text, QtCore.Qt.TextElideMode.ElideMiddle, width)
        return elided
