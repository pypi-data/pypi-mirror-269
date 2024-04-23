import sys

import cv2
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from behavysis_core.data_models.bouts import Bouts
from behavysis_viewer.pydantic_models.experiment_configs import ExperimentConfigs
from behavysis_viewer.utils.cv2_qt_mixin import Cv2QtMixin
from pyqtgraph import BarGraphItem, InfiniteLine, PlotWidget, mkPen
from pyqtgraph.exporters import ImageExporter
from PySide6.QtWidgets import QApplication


class GraphView(PlotWidget):

    bars: list[BarGraphItem]
    time_marker_line: InfiniteLine

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.bars = []
        self.time_marker_line = InfiniteLine(pos=0, angle=90)

    def set_plot_attr(self, **kwargs):
        if "xmin" in kwargs and "xmax" in kwargs:
            self.setXRange(
                kwargs["xmin"],
                kwargs["xmax"],
                # padding=kwargs.get("xpadding", 0),  # type: ignore
            )
        if "ymin" in kwargs and "ymax" in kwargs:
            self.setYRange(
                kwargs["ymin"],
                kwargs["ymax"],
                # padding=kwargs.get("ypadding", 0),  # type: ignore
            )

    def plot_bouts_init(self, bouts: Bouts, configs: ExperimentConfigs):
        # Getting necessary configs
        fps = configs.auto.formatted_vid.fps
        # Getting data
        start_ls = np.array([i.start for i in bouts.bouts]) / fps
        stop_ls = np.array([i.stop for i in bouts.bouts]) / fps
        behavs_ls = np.array([i.behaviour for i in bouts.bouts])
        # Plotting data
        self.plot_init(start_ls, stop_ls, behavs_ls)

    def plot_init(self, start_ls, stop_ls, behavs_ls, **kwargs):
        behavs_ls_i, behavs = pd.factorize(behavs_ls)
        self.clear()
        self.bars = []
        # Plotting data
        # TODO: fix this up. Un-pythonic for loop
        # TODO: change colour of bar depending on bout "actual" value
        for i in range(len(start_ls)):
            bar = BarGraphItem(
                x0=start_ls[i],
                x1=stop_ls[i],
                y=behavs_ls_i[i],
                height=0.5,
                pen=mkPen(color="r"),
            )
            self.bars.append(bar)
            self.addItem(bar)
        # self.plot(x, y)
        # Setting current time marker line
        self.time_marker_line.setPos(0)
        self.addItem(self.time_marker_line)
        # Plot aesthetics
        self.set_plot_attr(**kwargs)

    def plot_update(self, i, **kwargs):
        # Plotting data
        self.time_marker_line.setPos(i)
        # Plot aesthetics
        self.set_plot_attr(**kwargs)

    def plot_2_cv(self):
        # Making pyqtgraph image exporter to bytes
        exporter = ImageExporter(self.plotItem)
        # exporter.parameters()["width"] = self.width()
        # Exporting to QImage (bytes)
        img_qt = exporter.export(toBytes=True)
        # QImage to cv2 image (using mixin)
        img_cv = Cv2QtMixin.qt_2_cv(img_qt)
        # cv2 BGR to RGB
        img_cv = cv2.cvtColor(img_cv, cv2.COLOR_BGR2RGB)
        # Resize to widget size
        w, h = self.width(), self.height()
        img_cv = cv2.resize(img_cv, (w, h), interpolation=cv2.INTER_AREA)
        # Return cv2 image
        return img_cv


from behavysis_core.mixins.behaviour_mixin import BehaviourMixin

if __name__ == "__main__":
    app = QApplication(sys.argv)

    graph_viewer = GraphView()
    graph_viewer.setWindowTitle("CvView Test")
    graph_viewer.resize(800, 600)
    graph_viewer.move(100, 100)

    fp = "/Users/timothylee/Desktop/Work/dev/behavysis_viewer/tests/resources/2_Round1.1_20220530_AGG-MOA_test3-M3_a2.feather"

    behavs_df = pd.read_feather(fp)
    # frames_df to bouts_dict
    bouts_dict = BehaviourMixin.frames_2_bouts(behavs_df)
    # Updating graph_viewer
    start_ls = np.array([])
    stop_ls = np.array([])
    behavs_ls = np.array([])
    for behav, bouts_behav_ls in bouts_dict["behaviours"].items():
        start_ls = np.append(start_ls, [i["start"] for i in bouts_behav_ls])
        stop_ls = np.append(stop_ls, [i["stop"] for i in bouts_behav_ls])
        behavs_ls = np.append(behavs_ls, np.repeat(behav, len(bouts_behav_ls)))
    start_ls = start_ls / 15
    stop_ls = stop_ls / 15
    graph_viewer.plot_init(start_ls, stop_ls, behavs_ls)

    i = 15
    v = 5
    graph_viewer.plot_update(i, xmin=i - v, xmax=i + v)

    img_cv = graph_viewer.plot_2_cv()
    print(img_cv.shape)
    print(graph_viewer.height(), graph_viewer.width())
    print()

    graph_viewer.setFixedSize(200, 1000)

    img_cv = graph_viewer.plot_2_cv()
    print(img_cv.shape)
    print(graph_viewer.height(), graph_viewer.width())
    print()

    # cv2.imwrite("graph_viewer.png", img_cv)

    graph_viewer.show()
    sys.exit(app.exec())
