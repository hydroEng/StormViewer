import PyQt6

from PyQt6.QtWidgets import (
    QPushButton,
    QWidget,
    QMessageBox,
    QFileDialog,
    QHBoxLayout
)
from models import POLine

class BottomControls(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QHBoxLayout()
        self.output_directory = None
        self.save_btn = self.save_button()
        self.layout.addWidget(self.save_btn)
        self.setLayout(self.layout)

    def init_controls(self):
        pass

    def save_button(self):
        button = QPushButton("Save Results")

        button.clicked.connect(self.save_results)
        return button

    def save_results(self):
        self.output_directory = str(QFileDialog.getExistingDirectory(self, "Select Output Folder"))

        if self.output_directory:
            "foo"
