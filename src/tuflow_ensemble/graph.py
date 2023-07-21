import PyQt6
import matplotlib

matplotlib.use("Qt5Agg")
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure
from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout, QFrame
)


class GraphView(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout()
        self.separator = None
        self.chart = MplCanvas()
        self.canvas = QVBoxLayout()
        self.canvas.addWidget(self.chart)

        self.figures = None

        self.init_widget()

    def init_widget(self):
        self.init_separator()
        self.layout.addWidget(self.separator)
        self.layout.addLayout(self.canvas)
        self.setLayout(self.layout)

    def init_separator(self):
        """ Initialize separator above graph area """
        self.separator = QFrame()
        self.separator.setFrameShape(QFrame.Shape.HLine)
        self.separator.setFrameShadow(QFrame.Shadow.Sunken)

    def update_graph(self, figure):
        if self.figures:
            self.chart = MplCanvas(fig=figure)
            self.canvas = QVBoxLayout()
            self.canvas.addWidget(self.chart)
            self.layout.update()


class MplCanvas(FigureCanvasQTAgg):
    def __init__(self, fig=Figure(), width=5, height=4, dpi=200):
        self.axes = fig.add_subplot(111)
        super(MplCanvas, self).__init__(fig)
