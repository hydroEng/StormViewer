import PyQt6
from PyQt6.QtCore import Qt
import matplotlib

matplotlib.use("Qt5Agg")
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QFrame, QLabel


class GraphView(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout()
        self.separator = self.init_separator()
        self.chart = Canvas()
        self.figures = None

        self.init_widget()

    def init_widget(self):
        self.layout.addWidget(self.separator)
        self.layout.addWidget(self.chart)
        self.setLayout(self.layout)

    def init_separator(self):
        """Initialize separator above canvas area """
        separator = QFrame()
        separator.setFrameShape(QFrame.Shape.HLine)
        separator.setFrameShadow(QFrame.Shadow.Sunken)

        return separator


class Canvas(QFrame):
    def __init__(self):
        super().__init__()
        self.label = QLabel("")

        self.layout = QVBoxLayout()
        self.layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.init_frame()
        self.update_frame_text("No results loaded. Create charts by loading results first.")

        self.chart = None

        self.setLayout(self.layout)

    def init_frame(self):

        self.setFrameShape(QFrame.Shape.Box)
        self.setFrameShadow(QFrame.Shadow.Sunken)

    def update_frame_text(self, msg: str, color: str = 'black'):

        self.clear_layout()
        self.label = QLabel(msg)
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label.setStyleSheet(f'QLabel {{color: {color}}}')
        self.layout.addWidget(self.label)

        self.update()

    def show_figure(self, figure):

        """Destroy existing MplCanvas, create new canvas with chosen figure and add to layout."""

        self.clear_layout()
        # Set DPI explicitly due to matplotlib scaling bug.
        figure.dpi = 100
        self.chart = MplCanvas(fig=figure)
        self.layout.addWidget(self.chart)
        self.update()

    def clear_layout(self):
        # Deletes all widgets in frame layout.
        while self.layout.count():
            item = self.layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()


class MplCanvas(FigureCanvasQTAgg):
    def __init__(self, fig=Figure()):
        super(MplCanvas, self).__init__(fig)
