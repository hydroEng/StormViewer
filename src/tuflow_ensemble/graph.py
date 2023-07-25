import PyQt6
import matplotlib

matplotlib.use("Qt5Agg")
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QFrame


class GraphView(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout()
        self.separator = None
        self.chart = MplCanvas()

        self.figures = None

        self.init_widget()

    def init_widget(self):
        self.init_separator()
        self.layout.addWidget(self.separator)
        self.layout.addWidget(self.chart)
        self.setLayout(self.layout)

    def init_separator(self):
        """Initialize separator above graph area"""
        self.separator = QFrame()
        self.separator.setFrameShape(QFrame.Shape.HLine)
        self.separator.setFrameShadow(QFrame.Shadow.Sunken)

    def update_graph(self, figure):

        self.chart.deleteLater()
        figure.dpi = 100
        self.chart = MplCanvas(fig=figure)

        self.layout.addWidget(self.chart)
        self.layout.update()


class MplCanvas(FigureCanvasQTAgg):
    def __init__(self, fig=Figure()):
        super(MplCanvas, self).__init__(fig)
