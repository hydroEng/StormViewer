from PyQt6 import QtCore
from PyQt6.QtGui import QFontMetrics
from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout, QLabel, QTableWidget, QTableWidgetItem,
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
        self.widget = None

        self.init_widget()

    def init_widget(self):

        widget = QWidget()
        widget.setFixedHeight(180)

        layout = QVBoxLayout()
        layout.addWidget(self.dir_label)

        # initialize table
        self.init_table()
        layout.addWidget(self.table)

        widget.setLayout(layout)
        self.widget = widget

    def init_table(self):
        table = QTableWidget()
        table.setColumnCount(4)

        table.setHorizontalHeaderLabels(("Location", "Event", "Critical Storm", "Critical Max Flow"))
        table.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        column_widths = [120, 120, 120, 120]
        table.setFixedWidth(sum(column_widths) + 40)
        table.horizontalHeader().setStretchLastSection(True)

        for i, width in enumerate(column_widths):
            table.setColumnWidth(i, width)

        self.table = table

    def update_label(self):

        self.dir_str = "Directory: " + self.directory
        elided = self.elide_text(self.dir_label.font(), self.dir_str, self.table.width())
        self.dir_label.setText(elided)

        self.widget.update()

    def update_table(self):
        self.table.setRowCount(len(self.data))
        for i, row in enumerate(self.data):
            for j, cell in enumerate(row):
                self.table.setItem(i, j, QTableWidgetItem(str(cell)))

        self.widget.update()

    @staticmethod
    def elide_text(qfont, text: str, width: int):
        metrics = QFontMetrics(qfont)
        elided = metrics.elidedText(text, QtCore.Qt.TextElideMode.ElideMiddle, width)
        return elided