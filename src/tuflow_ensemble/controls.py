from PyQt6 import QtCore
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QPushButton, QWidget, QStyle, QFileDialog, QHBoxLayout, QVBoxLayout, QLabel


class BottomControls(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QHBoxLayout()
        self.output_directory = None
        self.save_btn = self.save_button()
        self.help_btn = self.help_button()
        self.layout.addWidget(self.help_btn, alignment=Qt.AlignmentFlag.AlignLeft)
        self.layout.addWidget(self.save_btn)
        self.setFixedHeight(40)
        self.setLayout(self.layout)

    def init_controls(self):
        pass

    def save_button(self):
        button = QPushButton("Save Plots")
        button.setFixedHeight(30)
        button.setFixedWidth(100)
        return button

    def help_button(self):
        """
        Help button: Connects to help dialog
        """
        button = QPushButton("Help")
        button.setFixedHeight(30)
        btn_pixmap = QStyle.StandardPixmap.SP_MessageBoxQuestion
        icon = self.style().standardIcon(btn_pixmap)
        button.setIcon(icon)
        return button

class InputControls(QWidget):
    """
    Class for input controls.
    """
    def __init__(self):

        self.setFixedWidth(150)
        self.setFixedHeight(180)

        self.layout = QVBoxLayout()

        self.icon = self.app_icon_label()
        self.input_btn = QPushButton("Select Results\n Folder")

        self.create_plots_btn = QPushButton("Create Plots")
        self.create_plots_btn.setEnabled(False)
        self.create_plots_btn.setFixedHeight(30)

        self.layout.addWidget()
        # self.layout

    def app_icon_label(self):
        """Rain Cloud Icon"""
        # Icon and file inputs cell

        iconPath = resource_path("assets/rain-svgrepo-com.svg")

        # Add App Icon

        app_icon_label = QLabel(self)
        app_icon = QPixmap(iconPath).scaledToWidth(80)

        # Format app icon

        app_icon_label.setPixmap(app_icon)
        app_icon_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        return app_icon_label

def resource_path(relative_path):
    """Get absolute path to resource, works for dev and for PyInstaller.
    From https://stackoverflow.com/questions/31836104/pyinstaller-and-onefile-how-to-include-an-image-in-the-exe-file"""
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)