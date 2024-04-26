import traceback
from functools import partial
from multiprocessing import Manager
from typing import TYPE_CHECKING

import matplotlib.colors as mcolors
import matplotlib.pyplot as plt
import numpy as np
import pyqtgraph as pg
from qtpy.QtCore import QThreadPool
from qtpy.QtWidgets import (QVBoxLayout, QWidget, )
from scipy.ndimage import map_coordinates

if TYPE_CHECKING:
    import napari

from smlmlab.gui import Ui_Frame as gui
from smlmlab.utils.compute_utils import _utils_compute
from smlmlab.utils.events_utils import _events_utils
from smlmlab.utils.import_utils import _import_utils
from smlmlab.utils.loc_utils import _loc_utils
from smlmlab.utils.picasso_utils import _picasso_detect_utils
from smlmlab.utils.viewer_utils import _viewer_utils


class smlmlabWidget(QWidget, gui, _import_utils, _events_utils, _picasso_detect_utils, _loc_utils, _viewer_utils, _utils_compute, ):

    def __init__(self, viewer: "napari.viewer.Viewer"):
        super().__init__()
        self.viewer = viewer

        self.gui = gui()
        self.gui.setupUi(self)

        # create pyqt graph container
        self.graph_container = self.gui.graph_container
        self.graph_container.setLayout(QVBoxLayout())

        self.graph_canvas = pg.GraphicsLayoutWidget()
        self.graph_container.layout().addWidget(self.graph_canvas)

        self.gui.import_data.clicked.connect(self.import_image_data)

        self.viewer.dims.events.current_step.connect(partial(self.draw_molecules, update_vis=False))

        self.gui.picasso_detect.clicked.connect(partial(self.pixseq_picasso, detect=True, fit=False))
        self.gui.picasso_fit.clicked.connect(partial(self.pixseq_picasso, detect=False, fit=True))
        self.gui.picasso_detectfit.clicked.connect(partial(self.pixseq_picasso, detect=True, fit=True))
        self.gui.picasso_render.clicked.connect(self.picasso_render)

        self.gui.picasso_vis_mode.currentIndexChanged.connect(partial(self.draw_molecules, update_vis=True))
        self.gui.picasso_vis_mode.currentIndexChanged.connect(partial(self.draw_bounding_boxes, update_vis=True))
        self.gui.picasso_vis_size.currentIndexChanged.connect(partial(self.draw_molecules, update_vis=True))
        self.gui.picasso_vis_size.currentIndexChanged.connect(partial(self.draw_bounding_boxes, update_vis=True))
        self.gui.picasso_vis_opacity.currentIndexChanged.connect(partial(self.draw_molecules, update_vis=True))
        self.gui.picasso_vis_opacity.currentIndexChanged.connect(partial(self.draw_bounding_boxes, update_vis=True))
        self.gui.picasso_vis_edge_width.currentIndexChanged.connect(partial(self.draw_molecules, update_vis=True))
        self.gui.picasso_vis_edge_width.currentIndexChanged.connect(partial(self.draw_bounding_boxes, update_vis=True))

        self.gui.plot_mode.currentIndexChanged.connect(self.draw_line_plot)
        self.gui.plot_dataset.currentIndexChanged.connect(self.draw_line_plot)
        self.gui.plot_channel.currentIndexChanged.connect(self.draw_line_plot)

        self.verbose = True

        self.dataset_dict = {}
        self.localisation_dict = {"bounding_boxes": {}, "molecules": {}}
        self.traces_dict = {}
        self.plot_dict = {}
        self.contrast_dict = {}

        self.active_dataset = None
        self.active_channel = None

        self.threadpool = QThreadPool()

        manager = Manager()
        self.stop_event = manager.Event()

        self.worker = None
        self.multiprocessing_active = False

        self.viewer.layers.events.inserted.connect(self.on_add_layer)

    def on_add_layer(self, event):
        if event.value.name == "Shapes":
            layer_list = [layer.name for layer in self.viewer.layers if layer.name != "Shapes"]

            self.shapes_layer = self.viewer.layers["Shapes"]

            self.shapes_layer.events.data.connect(self.shapes_layer_updated)

            self.shapes_layer.current_edge_color = list(mcolors.to_rgb("green"))
            self.shapes_layer.current_face_color = [0, 0, 0, 0]
            self.shapes_layer.current_edge_width = 1

    def shapes_layer_updated(self, event):
        try:
            if event.action in ["added", "changed", "removed"]:
                shapes_layer = self.viewer.layers["Shapes"]
                shape_type = shapes_layer.shape_type[-1]

                if shape_type == "line":
                    shape = shapes_layer.data[-1].copy()
                    shape = shape[:, 1:]
                    self.viewer.layers["Shapes"].data[-1] = shape

                    self.gui.plot_mode.setCurrentIndex(0)

                if shape_type == "rectangle":
                    self.gui.plot_mode.setCurrentIndex(1)

                self.draw_line_plot()

        except:
            print(traceback.format_exc())

    def get_plot_data(self):
        plot_dataset = {}

        try:
            layer_names = [layer.name for layer in self.viewer.layers]

            if "Shapes" in layer_names:
                shapes_layer = self.viewer.layers["Shapes"]
                shapes = shapes_layer.data.copy()
                shape_types = shapes_layer.shape_type.copy()

                plot_mode = self.gui.plot_mode.currentIndex()
                dataset = self.gui.plot_dataset.currentText()

                current_frame = self.viewer.dims.current_step[0]

                for channel in self.dataset_dict[dataset].keys():
                    if channel not in plot_dataset:
                        plot_dataset[channel] = {}

                    for shape_index, (shape, shape_type) in enumerate(zip(shapes, shape_types)):
                        if shape_type == "line" and plot_mode == 0:
                            if shape.shape[-1] == 3:
                                dat = shape[:, 1:]
                            else:
                                dat = shape

                            [[x1, y1], [x2, y2]] = dat

                            x1, y1 = int(x1), int(y1)
                            x2, y2 = int(x2), int(y2)

                            num = int(np.hypot(x2 - x1, y2 - y1))

                            img = self.dataset_dict[dataset][channel]["data"][current_frame]

                            x, y = np.linspace(x1, x2, num), np.linspace(y1, y2, num)
                            coords = np.vstack((x, y))

                            line_profile = map_coordinates(img, coords, order=1, mode="nearest")

                            plot_dataset[channel][shape_index] = line_profile

                        if shape_type == "rectangle" and plot_mode == 1:
                            if shape.shape[-1] == 3:
                                dat = shape[:, 1:]
                            else:
                                dat = shape

                            x1, y1, x2, y2 = (dat[0, 1], dat[0, 0], dat[2, 1], dat[2, 0],)
                            x1, y1 = int(x1), int(y1)
                            x2, y2 = int(x2), int(y2)

                            img = self.dataset_dict[dataset][channel]["data"]

                            box_data = img[:, y1:y2, x1:x2]

                            line_profile = np.mean(box_data, axis=(1, 2))

                            plot_dataset[channel][shape_index] = line_profile

                    if set(["donor", "acceptor"]).issubset(plot_dataset.keys()):
                        plot_dataset = self.calculate_fret(plot_dataset)

        except:
            print(traceback.format_exc())

        return plot_dataset

    def calculate_fret(self, plot_dataset):
        try:
            donor_data = plot_dataset["donor"]
            acceptor_data = plot_dataset["acceptor"]

            for shape_index, (donor, acceptor) in enumerate(zip(donor_data.values(), acceptor_data.values())):
                if "fret" not in plot_dataset.keys():
                    plot_dataset["fret"] = {}

                fret = acceptor / (donor + acceptor)
                plot_dataset["fret"][shape_index] = fret

        except:
            print(traceback.format_exc())

        return plot_dataset

    def draw_line_plot(self):
        try:
            plot_mode = self.gui.plot_mode.currentIndex()
            plot_channel = self.gui.plot_channel.currentText()

            if "efficiency" in plot_channel.lower():
                plot_channel = "fret"

            plot_dataset = self.get_plot_data()

            self.graph_canvas.clear()

            if plot_channel.lower() in plot_dataset.keys():
                plot_data = plot_dataset[plot_channel.lower()]

                if plot_data != {}:
                    if plot_mode == 0:
                        plot_title = "Line profile(s)"
                    if plot_mode == 1:
                        plot_title = "Single Molecule Time Series"

                    ax = self.graph_canvas.addPlot(title=plot_title)

                    for data in plot_data.values():
                        ax.plot(data, pen=(255, 0, 0))

                    plt.show()

        except:
            print(traceback.format_exc())
