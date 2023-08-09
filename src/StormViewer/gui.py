from PyQt6 import QtCore
from PyQt6.QtWidgets import QApplication, QWidget, QGridLayout, QFileDialog
from PyQt6.QtCore import QObject, QThreadPool, QRunnable, Qt
from PyQt6.QtGui import QIcon
import os
import sys
from StormViewer import te
from shutil import copyfile
from StormViewer.table import TableView
from StormViewer.graph import GraphView
from StormViewer.controls import BottomControls, InputControls, resource_path
import csv


class App(QWidget):
    def __init__(self):
        super().__init__()

        self.input_directory = None
        self.output_directory = None
        self.title = "StormViewer"

        self.threadpool = QThreadPool()
        self.main_layout = QGridLayout()
        self.processor = Processor()
        self.top_controls = InputControls()

        self.bottom_controls = BottomControls()
        self.table_view = TableView()
        self.graph_view = GraphView()

        self.iconPath = resource_path("assets/rain-svgrepo-com.svg")

        self.initUI()

        # Button click connections

        self.top_controls.input_btn.clicked.connect(self.read_input_path)
        self.top_controls.create_plots_btn.clicked.connect(self.create_plots)
        self.table_view.table.cellClicked.connect(self.update_graph_view)
        self.bottom_controls.save_btn.clicked.connect(self.save_plots)

        # Window controls

        self.setWindowFlags(
            self.windowFlags() & ~Qt.WindowType.WindowMaximizeButtonHint
        )
        self.setFixedSize(self.size())

    def initUI(self):

        self.setWindowTitle("StormViewer")
        self.setWindowIcon(QIcon(self.iconPath))
        self.setUpMainWindow()
        self.show()

    def setUpMainWindow(self):
        """Layouts for main window"""
        self.main_layout.addWidget(self.table_view, 0, 1)
        self.main_layout.addWidget(self.bottom_controls, 2, 0, 1, 2)
        self.main_layout.addWidget(self.top_controls, 0, 0)
        self.main_layout.addWidget(self.graph_view, 1, 0, 1, 2)

        self.setLayout(self.main_layout)

    # CONTROLLER FUNCTIONS

    def read_input_path(self):

        try:
            self.input_directory = str(
                QFileDialog.getExistingDirectory(self, "Select Input Folder")
            )

            if self.input_directory:
                self.graph_view.chart.update_frame_text(
                    "Calculating storm attributes...", color="blue"
                )
                self.top_controls.input_btn.setEnabled(False)

                self.processor = Processor(self.input_directory)
                self.threadpool.start(self.processor.run)

                self.processor.signals.finished.connect(self.update_table_view)
                self.processor.signals.error.connect(self.data_failure)

        except:
            # Update canvas text to reflect failure.
            pass

    def create_plots(self):

        self.threadpool.start(self.processor.plot)
        self.processor.signals.finished.connect(self.update_graph_view)
        self.bottom_controls.save_btn.setEnabled(True)

    def update_table_view(self):
        self.top_controls.input_btn.setEnabled(True)
        self.top_controls.create_plots_btn.setEnabled(True)
        self.graph_view.chart.update_frame_text(
            'Results loaded: Click "Create Plots" to see plots.', color="green"
        )
        table_data = []
        storms = self.processor.po_lines

        for storm in storms:
            crit_storm = f"{storm.crit_duration}m, {storm.crit_tp}"
            storm_data = [storm.loc, storm.event, crit_storm, storm.crit_flow]
            assert len(storm_data) == 4

            table_data.append(storm_data)

        self.table_view.data = table_data
        self.table_view.update_table()

        self.table_view.directory = self.input_directory
        self.table_view.update_label()

    def data_failure(self):
        self.top_controls.input_btn.setEnabled(True)
        self.graph_view.chart.update_frame_text(
            "Could not load results from chosen directory. Your data may be invalid or named incorrectly.\nPlease see help for instructions.",
            color="red",
        )

        self.table_view.clear_table_view()
        self.top_controls.create_plots_btn.setEnabled(False)
        self.bottom_controls.save_btn.setEnabled(False)

    def plot_success(self):
        self.graph_view.chart.update_frame_text(
            f"Plots and results saved to {self.output_directory}", "green"
        )

    def plot_failure(self):
        self.graph_view.chart.update_frame_text(
            f"Could not save results. Do you have access to the output directory?",
            "red",
        )

    def update_graph_view(self):

        if self.processor.figs is not None:
            self.graph_view.chart.show_figure(
                self.processor.figs[self.table_view.selected_row]
            )

    def save_plots(self):
        # Clear output directory
        self.output_directory = None

        if self.processor.figs is not None:
            self.processor.signals.save_finished.connect(self.plot_success)
            self.processor.signals.save_error.connect(self.plot_failure)

            self.output_directory = QFileDialog.getExistingDirectory(
                caption="Select Output Directory"
            )
            if self.output_directory:
                table_data = self.table_view.get_table_output()
                filename = "StormViewer_results.csv"
                self.processor.save_plots(self.output_directory, table_data, filename)


### Backend Script Connections ###
class Processor(QRunnable):
    def __init__(self, input_directory=None):
        super(Processor).__init__()
        self.input_directory = input_directory
        self.signals = WorkerSignals()
        self.po_lines = None
        self.figs = None

    def run(self):
        try:
            self.po_lines = te.read_input_directory(self.input_directory)

            if self.po_lines:
                self.signals.finished.emit()
        except:
            self.signals.error.emit()

    def plot(self):

        if not self.po_lines:
            raise ValueError(
                "Cannot plot as no POLine objects have been generated yet."
            )

        self.figs = []

        for po_line in self.po_lines:
            po_line.plot()
            self.figs.append(po_line.fig)

        self.signals.finished.emit()

    def save_plots(self, output_dir, tabular_data, filename: str):
        if self.po_lines:

            try:
                for po_line in self.po_lines:
                    file_name = _str_to_valid_filename(po_line.name) + ".png"
                    copyfile(
                        po_line.temp_file.name, os.path.join(output_dir, file_name)
                    )
                _list_to_csv(tabular_data, filename, output_dir)
                self.signals.save_finished.emit()
            except:
                print(f"Could not plot {po_line.name}")
                self.signals.save_error.emit()


class WorkerSignals(QObject):
    """
    This class holds signals for QRunnable Object. Supports:

    finished
        Send signal that QRunnable has finished execution.
    error
        Send error signal if QRunnable has encountered an error.

    """

    finished = QtCore.pyqtSignal()
    error = QtCore.pyqtSignal()

    save_finished = QtCore.pyqtSignal()
    save_error = QtCore.pyqtSignal()


# Utils


def _str_to_valid_filename(name: str) -> str:
    """
    Removes troublesome chars from filename. Tries not over-prescribe - keeps underscore and dash chars as this is
    common in TUFLOW results files.

    Args:
        name: Proposed filename for cleaning.

    Returns:
        a string with more valid filename.
    """

    invalid_chars = r"%:/,\[]<>*?"
    valid_name = ""

    for c in name:
        if c in invalid_chars:
            c = "-"
        valid_name += c

    return valid_name


def _list_to_csv(data: list[list[str]], filename: str, output_directory: str):
    # Write a 2d list of strings to a csv file in the output directory.
    assert filename.endswith(".csv")
    output_fp = os.path.join(output_directory, filename)
    with open(output_fp, "w", newline="") as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerows(data)


if __name__ == "__main__":
    app = QApplication(sys.argv)

    ex = App()
    ex.show()
    sys.exit(app.exec())
