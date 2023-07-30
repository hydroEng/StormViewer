from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QPushButton, QWidget, QStyle, QFileDialog, QHBoxLayout


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
