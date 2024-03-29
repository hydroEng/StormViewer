from PyQt6 import QtCore
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap, QFont, QIcon
from PyQt6.QtWidgets import (
    QPushButton,
    QWidget,
    QStyle,
    QDialog,
    QHBoxLayout,
    QVBoxLayout,
    QLabel,
)
import os
import sys


class BottomControls(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QHBoxLayout()
        self.output_directory = None
        self.save_btn = self.save_button()
        self.save_btn.setEnabled(False)
        self.help_btn = self.help_button()
        self.layout.addWidget(self.help_btn, alignment=Qt.AlignmentFlag.AlignLeft)
        self.layout.addWidget(self.save_btn)
        self.setFixedHeight(40)
        self.setLayout(self.layout)

    def init_controls(self):
        pass

    def save_button(self):
        button = QPushButton("Save Results...")
        button.setFixedHeight(30)
        button.setFixedWidth(100)
        btn_pixmap = QStyle.StandardPixmap.SP_DialogSaveButton
        icon = self.style().standardIcon(btn_pixmap)
        button.setIcon(icon)
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
        button.clicked.connect(self.open_help)
        return button

    def open_help(self):
        HelpBox()


class InputControls(QWidget):
    """
    Class for input controls.
    """

    def __init__(self):
        super().__init__()
        self.setFixedWidth(150)
        self.setFixedHeight(180)

        self.layout = QVBoxLayout()

        self.icon = self.app_icon_label()
        self.input_btn = QPushButton("Select Results\n Folder")

        self.create_plots_btn = QPushButton("Create Plots")
        self.create_plots_btn.setEnabled(False)
        self.create_plots_btn.setFixedHeight(30)

        self.layout.addWidget(self.icon)
        self.layout.addWidget(self.input_btn)
        self.layout.addWidget(self.create_plots_btn)
        self.layout.addStretch()

        self.setLayout(self.layout)

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


def debug(widget):
    widget.setStyleSheet("border: 2px solid red;")


class HelpBox(QDialog):
    """Provides help dialog box."""

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Help")
        self.init_help_ui()

    def init_help_ui(self):
        self.setWindowFlags(
            self.windowFlags() & ~Qt.WindowType.WindowMaximizeButtonHint
        )

        help_icon_path = resource_path("assets/help-question-svgrepo-com.svg")

        #### Help icon

        self.setWindowIcon(QIcon(help_icon_path))
        help_icon_label = QLabel()
        help_icon = QPixmap(help_icon_path).scaledToWidth(72)
        help_icon_label.setPixmap(help_icon)
        help_icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        #### Help text area

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Add header text
        header_msg = "StormViewer v.1.3"
        header = QLabel()
        header.setText(header_msg)

        header_font = QFont()
        header_font.setBold(True)
        header_font.setPointSize(12)
        header.setFont(header_font)

        help_label = QLabel(
            'For detailed help instructions, please visit the <a href="https://github.com/hydroEng/tuflow_ensemble/blob/master/USER_MANUAL.md"> official user manual</a>.'
        )
        help_label.setWordWrap(True)


        help_label.setOpenExternalLinks(True)

        #### lose button
        close_button = QPushButton("Close", self)
        close_button.clicked.connect(self.close)

        #### Build layout
        layout.addWidget(help_icon_label)
        layout.addWidget(header)
        layout.addWidget(help_label)
        layout.addWidget(close_button)

        self.setLayout(layout)
        self.exec()


def resource_path(relative_path):
    """Get absolute path to resource, works for dev and for PyInstaller.
    From https://stackoverflow.com/questions/31836104/pyinstaller-and-onefile-how-to-include-an-image-in-the-exe-file"""
    if hasattr(sys, "_MEIPASS"):
        return os.path.join(sys._MEIPASS, relative_path)
    else:
        return relative_path
