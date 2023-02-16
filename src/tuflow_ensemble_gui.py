from PyQt6.QtWidgets import QApplication, QWidget, QFileDialog, QPushButton, QLabel, QVBoxLayout
import sys
import tuflow_ensemble


class App(QWidget):

    def __init__(self):
        super().__init__()

        self.title = 'TUFLOW Ensemble Tool'

        self.left = 10
        self.top = 10
        self.width = 320
        self.height = 200

        self.initUI()

    def initUI(self):

        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        # Input Directory Field
        self.input_dir = QLabel(self)
        self.input_dir.setText("Select Input Folder with PO.csv Files:")

        self.input_dir_btn = QPushButton('Select', self)
        self.input_dir_btn.clicked.connect(self.get_input_dir)

        # Output Directory Field
        self.output_dir = QLabel(self)
        self.output_dir.setText("Select Output Directory")
        self.output_dir_btn = QPushButton('Select', self)
        self.output_dir_btn.clicked.connect(self.get_output_dir)

        # Run Button
        self.run_btn = QPushButton('Run', self)
        self.run_btn.clicked.connect(self.run_main)

        # Vertical layout
        layout = QVBoxLayout()
        layout.addWidget(self.input_dir)
        layout.addWidget(self.input_dir_btn)
        layout.addWidget(self.output_dir)
        layout.addWidget(self.output_dir_btn)
        layout.addWidget(self.run_btn)

        self.setLayout(layout)

    def get_input_dir(self):
        input_dir = str(QFileDialog.getExistingDirectory(self, "Select Input Folder"))
        self.input_dir.setText("Input Directory: " + input_dir)

    def get_output_dir(self):
        output_dir = str(QFileDialog.getExistingDirectory(self, "Select Output Folder"))
        self.output_dir.setText("Output Directory: " + output_dir)

    def run_main(self):

        # Get input and output directory paths
        input_dir_path = self.input_dir.text().split(": ")[1]
        output_dir_path = self.output_dir.text().split(": ")[1]

        tuflow_ensemble.main(input_dir_path, output_dir_path)



if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    ex.show()
    sys.exit(app.exec())
