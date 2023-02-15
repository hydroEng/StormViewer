import sys
from PyQt5.QtWidgets import QApplication, QLabel

if __name__ == '__main__':
    app = QApplication(sys.argv)

    label = QLabel("TUFLOW Ensemble Tool")
    label.show()

    sys.exit(app.exec())
