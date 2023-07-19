from PyQt6 import QtCore
from PyQt6.QtGui import QPalette, QColor, QFont, QPixmap, QIcon, QFontMetrics
from PyQt6.QtWidgets import (
    QFrame,
    QTableWidget,
    QStyle,
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
    QStyleFactory,
    QTableWidgetItem,
)
from PyQt6.QtCore import QObject, QThreadPool, QRunnable, pyqtSignal, pyqtSlot
import os
import sys
import te
from src.tuflow_ensemble.models import POLine


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

        self.input_directory = None
        self.title = "StormViewer"
        # self.iconPath = resource_path("assets/rain-svgrepo-com.svg")

        # self.setWindowIcon(QIcon(self.iconPath))

        self.threadpool = QThreadPool()
        self.main_layout = QGridLayout()

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

        input_1 = self.input_controls()
        input_2 = self.input_view()
        input_3 = self.graph_view()

        self.main_layout.addWidget(input_1, 0, 0)
        self.main_layout.addWidget(input_2, 0, 1)
        self.main_layout.addWidget(input_3, 1, 0, 1, 2)

        self.setLayout(self.main_layout)

    def input_controls(self):

        widget = QWidget()
        widget.setFixedWidth(150)
        widget.setFixedHeight(180)

        layout = QVBoxLayout()

        icon = self.app_icon_label()

        browse_input = QPushButton("Select Results\n Folder")
        browse_input.clicked.connect(self.read_input_path)

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

    def input_view(self, data=None):

        if data is None:
            data = [[]]

        widget = QWidget()
        widget.setFixedHeight(180)

        layout = QVBoxLayout()

        table = self.storm_table(data)

        filedir_str = self.input_directory if self.input_directory else ''
        dir_str = "Directory: " + filedir_str

        dir_label = QLabel()
        elided_str = self.elide_text(dir_label.font(), dir_str, table.width())

        dir_label.setText(elided_str)

        layout.addWidget(dir_label)
        layout.addWidget(table)

        widget.setLayout(layout)

        return widget

    def storm_table(self, data):
        """ Add table of detected storms"""

        table = QTableWidget()
        table.setColumnCount(4)

        if len(data[0]) != 0:
            # Set num of rows if data is not empty.
            table.setRowCount(len(data))

        table.setHorizontalHeaderLabels(("Location", "Event", "Critical Storm", "Critical Max Flow"))
        table.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        column_widths = [120, 120, 120, 120]
        table.setFixedWidth(sum(column_widths) + 40)
        table.horizontalHeader().setStretchLastSection(True)

        for i, width in enumerate(column_widths):
            table.setColumnWidth(i, width)

        for row_num, row in enumerate(data):
            for i, item in enumerate(row):
                table.setItem(row_num, i, QTableWidgetItem(str(item)))

        return table

    def graph_view(self):
        widget = QWidget()

        layout = QVBoxLayout()
        separator = self.separator()
        layout.addWidget(separator)
        layout.addStretch()

        widget.setLayout(layout)
        return widget

    def separator(self):

        separator = QFrame()
        separator.setFrameShape(QFrame.Shape.HLine)
        separator.setFrameShadow(QFrame.Shadow.Sunken)

        return separator

    # CONTROLLER FUNCTIONS

    def read_input_path(self):

        self.input_directory = str(QFileDialog.getExistingDirectory(self, "Select Input Folder"))
        self.worker = ReadInputDirectory(self.input_directory)
        self.threadpool.start(self.worker.run)

        self.worker.signals.finished.connect(self.update_table)

    def update_table(self):
        table_data = []
        storms = self.worker.po_lines

        for storm in storms:
            crit_storm = f"{storm.crit_duration}m, {storm.crit_tp}"
            storm_data = [storm.id, storm.event, crit_storm, storm.crit_flow]
            assert len(storm_data) == 4

            table_data.append(storm_data)

        input_view = self.input_view(table_data)

        self.main_layout.addWidget(input_view, 0, 1)
        self.setLayout(self.main_layout)


### Backend Script Connections ###
class ReadInputDirectory(QRunnable):
    def __init__(self, input_directory):
        super(ReadInputDirectory).__init__()
        self.input_directory = input_directory
        self.signals = WorkerSignals()
        self.po_lines = None

    def run(self):
        self.po_lines = te.read_input_directory(self.input_directory)

        if self.po_lines:
            self.signals.finished.emit()
        else:
            self.signals.error.emit()


class WorkerSignals(QObject):
    """
    This class holds signals for QRunnable Object. Supports:

    finished
        Send signal that QRunnable has finished execution.
    error
        Send error signal if QRunnable has encountered an error.

    """

    finished = QtCore.pyqtSignal()
    error = QtCore.pyqtSignal()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle(QStyleFactory.create("Fusion"))

    ex = App()
    ex.show()
    sys.exit(app.exec())
