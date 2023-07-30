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
        self.chart = self.initial_canvas()
        print(self.chart.size())
        self.figures = None

        self.init_widget()

    def init_widget(self):
        self.layout.addWidget(self.separator)
        self.layout.addWidget(self.chart)
        self.setLayout(self.layout)

    def initial_canvas(self):
        """ Initialize empty canvas area """
        frame = QFrame()
        frame.setFrameShape(QFrame.Shape.Box)
        frame.setFrameShadow(QFrame.Shadow.Sunken)
        frame.setFixedHeight(480)

        msg = QLabel("No chart loaded. Create charts by loading results and using the \"Create Plots\" button above.")

        frame_layout = QVBoxLayout()
        frame_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        frame_layout.addWidget(msg)
        frame.setLayout(frame_layout)
        return frame


    def init_separator(self):
        """Initialize separator above canvas area """
        separator = QFrame()
        separator.setFrameShape(QFrame.Shape.HLine)
        separator.setFrameShadow(QFrame.Shadow.Sunken)

        return separator

    def update_graph(self, figure):
        """Destroy existing MplCanvas, create new canvas with chosen figure and add to layout."""
        self.chart.deleteLater()

        # Set DPI explicitly due to matplotlib scaling bug.
        figure.dpi = 100
        self.chart = MplCanvas(fig=figure)

        self.layout.addWidget(self.chart)
        self.layout.update()


class MplCanvas(FigureCanvasQTAgg):
    def __init__(self, fig=Figure()):
        super(MplCanvas, self).__init__(fig)
