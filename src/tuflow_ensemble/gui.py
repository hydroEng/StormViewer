from PyQt6 import QtCore
from PyQt6.QtGui import QPalette, QColor, QFont, QPixmap, QIcon, QFontMetrics
from PyQt6.QtWidgets import (
    QFrame,
    QTableWidget,
    QMessageBox,
    QApplication,
    QWidget,
    QGridLayout,
    QFileDialog,
    QPushButton,
    QLabel,
    QVBoxLayout,
    QHBoxLayout,
    QDialog,
    QHeaderView,
    QTableWidgetItem,
)
from PyQt6.QtCore import QObject, QThreadPool, QRunnable, pyqtSignal, pyqtSlot
import os
import sys


# from tuflow_ensemble import te

def resource_path(relative_path):
    """Get absolute path to resource, works for dev and for PyInstaller.
    From https://stackoverflow.com/questions/31836104/pyinstaller-and-onefile-how-to-include-an-image-in-the-exe-file"""
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


class App(QWidget):
    def __init__(self):
        super().__init__()

        self.title = "StormViewer"
        # self.iconPath = resource_path("assets/rain-svgrepo-com.svg")

        # self.setWindowIcon(QIcon(self.iconPath))

        # self.left = 10
        # self.top = 10
        # self.width = 320
        # self.height = 200

        self.threadpool = QThreadPool()

        self.initUI()

    def initUI(self):
        # self.setGeometry(self.left, self.top, self.width, self.height)
        self.setWindowTitle("StormViewer")

        self.setUpMainWindow()
        self.show()

    def apply_debug_style(self, widget):
        widget.setStyleSheet("border: 1px solid red;")

    def setUpMainWindow(self):
        """ Layouts for main window"""
        layout = QGridLayout()

        input_1 = self.input_controls()
        input_2 = self.input_view()

        layout.addWidget(input_1, 0, 0)
        layout.addWidget(input_2, 0, 1)
        layout.addWidget(QPushButton("Graph Area"), 1, 0, 1, 2)

        self.setLayout(layout)

    def input_controls(self):

        widget = QWidget()
        widget.setFixedWidth(150)
        widget.setFixedHeight(180)

        layout = QVBoxLayout()

        icon = self.app_icon_label()

        browse_input = QPushButton("Select Results\n Folder")
        read_storms = QPushButton("Analyse Storms")
        read_storms.setFixedHeight(30)

        layout.addWidget(icon)
        layout.addWidget(browse_input)
        layout.addWidget(read_storms)

        layout.addStretch()
        widget.setLayout(layout)

        return widget

    def app_icon_label(self):

        """ Rain Cloud Icon"""
        # Icon and file inputs cell

        iconPath = resource_path("assets/rain-svgrepo-com.svg")

        # Add App Icon

        app_icon_label = QLabel(self)
        app_icon = QPixmap(iconPath).scaledToWidth(80)

        # Format app icon

        app_icon_label.setPixmap(app_icon)
        app_icon_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        return app_icon_label

    def elide_text(self, qfont, text: str, width: int):
        metrics = QFontMetrics(qfont)
        elided = metrics.elidedText(text, QtCore.Qt.TextElideMode.ElideMiddle, width)
        return elided

    def input_view(self):
        widget = QWidget()
        widget.setFixedHeight(180)

        layout = QVBoxLayout()

        table = self.storm_table()

        dir_str = "Directory: " + "C:/Users/Public/TUFLOW_Runs/Results/gis/Cootamundra_To_Parkes_Results/BoogaBoogaBoogaBoogaBoogaBoogaBoogaBoogaBoogaBooga"
        directory = QLabel()
        elided_str = self.elide_text(directory.font(), dir_str, table.width())

        directory.setText(elided_str)

        layout.addWidget(directory)
        layout.addWidget(table)

        widget.setLayout(layout)

        return widget

    def storm_table(self):
        """ Add table of detected storms"""

        storms = [["Cootamundra to Parkes Catchment", "1AEP", "360m", "1, 2, 3, 4, 5, 6, 7, 8, 9, 10"]]

        table = QTableWidget()
        table.setColumnCount(4)
        table.setRowCount(10)

        table.setHorizontalHeaderLabels(("ID", "Event", "Duration", "TPs"))

        column_widths = [220, 60, 60, 150]
        table.setFixedWidth(sum(column_widths) + 40)
        table.horizontalHeader().setStretchLastSection(True)

        for i, width in enumerate(column_widths):
            table.setColumnWidth(i, width)

        for storm in storms:
            for i, item in enumerate(storm):
                table.setItem(0, i, QTableWidgetItem(item))

        return table


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = App()
    ex.show()
    sys.exit(app.exec())
