from PyQt6 import QtCore
from PyQt6.QtGui import QPalette, QColor, QFont, QPixmap, QIcon
from PyQt6.QtWidgets import QMessageBox, QApplication, QWidget, QFileDialog, QPushButton, QLabel, QVBoxLayout, QHBoxLayout
from PyQt6.QtCore import QObject, QThreadPool, QRunnable, pyqtSignal, pyqtSlot

import sys
import tuflow_ensemble

class WorkerSignals(QObject):

    """
    This class holds signals for QRunnable Object. Supports:

    finished
        Send signal that QRunnable has finished execution.

    """
    finished = QtCore.pyqtSignal()

class TuflowEnsemble(QRunnable):

    """ Worker Thread for main function"""
    def __init__(self, input_dir_path, output_dir_path):
        super(TuflowEnsemble, self).__init__()
        self.input_dir_path = input_dir_path
        self.output_dir_path = output_dir_path
        self.signals = WorkerSignals()

    @pyqtSlot()
    def run(self):

        print(self.input_dir_path)
        tuflow_ensemble.main(self.input_dir_path, self.output_dir_path)

        # Sent finished signal to GUI App
        self.signals.finished.emit()

class App(QWidget):

    def __init__(self):
        super().__init__()

        self.title = 'TUFLOW Ensemble Tool'
        self.setWindowIcon(QIcon(r"assets/rain-svgrepo-com.svg"))
        windowIcon = QIcon(r"assets/rain-svgrepo-com.svg")

        self.left = 10
        self.top = 10
        self.width = 320
        self.height = 200

        self.threadpool = QThreadPool()

        self.initUI()

    def initUI(self):

        self.setWindowTitle(self.title)
        self.setFixedWidth(self.width)

        # Title of app in UI Window

        self.title_label = QLabel(self)
        self.title_label.setText("TUFLOW Ensemble Tool")

        # Set title label formatting

        label_font = QFont()
        label_font.setBold(True)
        label_font.setPointSize(15)

        self.title_label.setFont(label_font)
        self.title_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignHCenter)

        # Horizontal Layout for Help / About buttons

        self.help_about_links = QLabel(self)
        self.help_about_links.setText("<a href=\"https://github.com/hydroEng/tuflow_ensemble/blob/master/USER_MANUAL.md\">Help</a> | "
                                      "<a href=\"https://github.com/hydroEng/tuflow_ensemble/\">About</a>")

        about_font = QFont()
        about_font.setPointSize(8)

        self.help_about_links.setFont(about_font)
        self.help_about_links.setAlignment(QtCore.Qt.AlignmentFlag.AlignHCenter)

        self.help_about_links.setOpenExternalLinks(True)

        # Add App Icon

        self.app_icon_label = QLabel(self)
        self.app_icon = QPixmap(r"assets/rain-svgrepo-com.svg").scaledToWidth(80)

        # Format app icon

        self.app_icon_label.setPixmap(self.app_icon)
        self.app_icon_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        # Input Directory Field
        self.input_dir = QLabel(self)
        self.input_dir.setText("Select Input Folder with *PO.csv Files:")
        self.input_dir.setAlignment(QtCore.Qt.AlignmentFlag.AlignBottom)

        self.input_dir_btn = QPushButton('Select', self)
        self.input_dir_btn.clicked.connect(self.get_input_dir)

        # Output Directory Field
        self.output_dir = QLabel(self)
        self.output_dir.setText("Select Output Directory:")
        self.output_dir.setAlignment(QtCore.Qt.AlignmentFlag.AlignBottom)

        self.output_dir_btn = QPushButton('Select', self)
        self.output_dir_btn.clicked.connect(self.get_output_dir)

        # Run Button

        self.run_btn = QPushButton(self)
        self.run_btn.setText('Run')

        self.run_btn.clicked.connect(self.run_main)

        # Vertical layout
        layout = QVBoxLayout()
        layout.addWidget(self.title_label)
        layout.addWidget(self.help_about_links)
        layout.addWidget(self.app_icon_label)
        layout.addWidget(self.input_dir)
        layout.addWidget(self.input_dir_btn)
        layout.addWidget(self.output_dir)
        layout.addWidget(self.output_dir_btn)
        layout.addWidget(self.run_btn)

        self.setLayout(layout)

    def get_input_dir(self):
        input_dir = str(QFileDialog.getExistingDirectory(self, "Select Input Folder"))
        self.input_dir.setText("Input Directory: " + input_dir)
        self.input_dir.setWordWrap(True)
        self.adjustSize()

    def get_output_dir(self):

        output_dir = str(QFileDialog.getExistingDirectory(self, "Select Output Folder"))
        self.output_dir.setText("Output Directory: " + output_dir)
        self.output_dir.setWordWrap(True)

        self.adjustSize()

    def update_button(self):
        if self.run_btn.text() == 'Run':
            self.run_btn.setDisabled(True)
            self.run_btn.setText('Running...')
            self.run_btn.update()
        else:
            self.run_btn.setEnabled(True)
            self.run_btn.setText('Run')
            self.run_btn.update()

    def run_main(self):

        input_dir_path = self.input_dir.text().split(": ")[1]
        output_dir_path = self.output_dir.text().split(": ")[1]

        self.update_button()

        self.worker = TuflowEnsemble(input_dir_path,output_dir_path)

        self.threadpool.start(self.worker.run)
        self.worker.signals.finished.connect(self.update_button)

    def about(self):
        about_dialog = QMessageBox(self)
        about_dialog.setWindowTitle("About")
        about_dialog.setText("Version: 1.0\nReport Bugs: https://github.com/suryaya/tuflow_ensemble")
        about_dialog.exec()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    ex.show()
    sys.exit(app.exec())