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
        self.graph = None
        self.figures = None

    def init_separator(self):
        """ Initialize separator above graph area """
        self.separator = QFrame()
        self.separator.setFrameShape(QFrame.Shape.HLine)
        self.separator.setFrameShadow(QFrame.Shadow.Sunken)

    def init_graph(self):
        pass

    def update_graph(self, i):
        pass



class MplCanvas(FigureCanvasQTAgg):
    def __init__(self, fig=Figure(), width=5, height=4, dpi=200):
        self.axes = fig.add_subplot(111)
        super(MplCanvas, self).__init__(fig)
