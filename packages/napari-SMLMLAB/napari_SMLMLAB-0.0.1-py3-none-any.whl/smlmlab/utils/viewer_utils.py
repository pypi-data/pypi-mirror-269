import traceback


class _viewer_utils:

    def draw_bounding_boxes(self, update_vis=False):

        if hasattr(self, "localisation_dict") and hasattr(
            self, "active_channel"
        ):
            if hasattr(self, "bbox_layer"):
                show_bboxes = self.bbox_layer.visible
            else:
                show_bboxes = True

            if show_bboxes:

                layer_names = [layer.name for layer in self.viewer.layers]

                dataset_name = self.gui.dataset_selector.currentText()
                image_channel = self.active_channel

                if (
                    "localisation_centres"
                    in self.localisation_dict["bounding_boxes"].keys()
                ):
                    if self.verbose:
                        print("Drawing bounding_boxes")

                    loc_dict, n_locs, fitted = self.get_loc_dict(
                        type="bounding_boxes"
                    )

                    localisations = loc_dict["localisations"].copy()
                    localisation_centres = self.get_localisation_centres(
                        localisations, mode="bounding_boxes"
                    )

                    vis_mode = self.gui.picasso_vis_mode.currentText()
                    vis_size = float(self.gui.picasso_vis_size.currentText())
                    vis_opacity = float(
                        self.gui.picasso_vis_opacity.currentText()
                    )
                    vis_edge_width = float(
                        self.gui.picasso_vis_edge_width.currentText()
                    )

                    pixel_size = float(
                        self.dataset_dict[dataset_name][image_channel.lower()][
                            "pixel_size"
                        ]
                    )
                    scale = [pixel_size, pixel_size]

                    if pixel_size != 1:
                        vis_size = vis_size / pixel_size

                    if vis_mode.lower() == "square":
                        symbol = "square"
                    elif vis_mode.lower() == "disk":
                        symbol = "disc"
                    elif vis_mode.lower() == "x":
                        symbol = "cross"

                    if "bounding_boxes" not in layer_names:
                        self.bbox_layer = self.viewer.add_points(
                            localisation_centres,
                            edge_color="white",
                            ndim=2,
                            face_color=[0, 0, 0, 0],
                            opacity=vis_opacity,
                            name="bounding_boxes",
                            symbol=symbol,
                            size=vis_size,
                            visible=True,
                            edge_width=vis_edge_width,
                            scale=scale,
                        )

                        self.bbox_layer.mouse_drag_callbacks.append(
                            self._mouse_event
                        )
                        self.bbox_layer.events.visible.connect(
                            self.draw_bounding_boxes
                        )

                    else:
                        self.viewer.layers["bounding_boxes"].data = (
                            localisation_centres
                        )
                        self.viewer.layers["bounding_boxes"].scale = scale

                    self.bbox_layer.selected_data = list(
                        range(len(self.bbox_layer.data))
                    )
                    self.bbox_layer.opacity = vis_opacity
                    self.bbox_layer.symbol = symbol
                    self.bbox_layer.size = vis_size
                    self.bbox_layer.edge_width = vis_edge_width
                    self.bbox_layer.edge_color = "white"
                    self.bbox_layer.selected_data = []
                    self.bbox_layer.refresh()

                for layer in layer_names:
                    self.viewer.layers[layer].refresh()

    def draw_molecules(self, update_vis=False):
        remove_molecules = True

        if hasattr(self, "localisation_dict") and hasattr(
            self, "active_channel"
        ):
            if hasattr(self, "molecule_layer"):
                show_molecules = self.molecule_layer.visible
            else:
                show_molecules = True

            if show_molecules:
                layer_names = [layer.name for layer in self.viewer.layers]

                active_frame = self.viewer.dims.current_step[0]

                dataset_name = self.gui.dataset_selector.currentText()
                image_channel = self.active_channel

                if image_channel != "" and dataset_name != "":
                    if (
                        image_channel.lower()
                        in self.localisation_dict["molecules"][
                            dataset_name
                        ].keys()
                    ):
                        localisation_dict = self.localisation_dict[
                            "molecules"
                        ][dataset_name][image_channel.lower()].copy()

                        if "render_locs" in localisation_dict.keys():
                            render_locs = localisation_dict["render_locs"]

                            vis_mode = self.gui.picasso_vis_mode.currentText()
                            vis_size = float(
                                self.gui.picasso_vis_size.currentText()
                            )
                            vis_opacity = float(
                                self.gui.picasso_vis_opacity.currentText()
                            )
                            vis_edge_width = float(
                                self.gui.picasso_vis_edge_width.currentText()
                            )

                            pixel_size = float(
                                self.dataset_dict[dataset_name][
                                    image_channel.lower()
                                ]["pixel_size"]
                            )
                            scale = [pixel_size, pixel_size]

                            if pixel_size != 1:
                                vis_size = vis_size / pixel_size

                            if vis_mode.lower() == "square":
                                symbol = "square"
                            elif vis_mode.lower() == "disk":
                                symbol = "disc"
                            elif vis_mode.lower() == "x":
                                symbol = "cross"

                            if active_frame in render_locs.keys():
                                remove_molecules = False

                                if "molecules" not in layer_names:
                                    if self.verbose:
                                        print("Drawing molecules")

                                    self.molecule_layer = (
                                        self.viewer.add_points(
                                            render_locs[active_frame],
                                            ndim=2,
                                            edge_color="red",
                                            face_color=[0, 0, 0, 0],
                                            opacity=vis_opacity,
                                            name="molecules",
                                            symbol=symbol,
                                            size=vis_size,
                                            edge_width=vis_edge_width,
                                            scale=scale,
                                        )
                                    )

                                    self.molecule_layer.mouse_drag_callbacks.append(
                                        self._mouse_event
                                    )
                                    self.molecule_layer.events.visible.connect(
                                        self.draw_molecules
                                    )

                                    update_vis = True

                                else:
                                    if self.verbose:
                                        print("Updating molecule data")

                                    self.molecule_layer.data = render_locs[
                                        active_frame
                                    ]
                                    self.molecule_layer.selected_data = []
                                    self.molecule_layer.scale = scale

                                if update_vis:
                                    if self.verbose:
                                        print(
                                            "Updating molecule visualisation settings"
                                        )

                                    self.molecule_layer.selected_data = list(
                                        range(len(self.molecule_layer.data))
                                    )
                                    self.molecule_layer.opacity = vis_opacity
                                    self.molecule_layer.symbol = symbol
                                    self.molecule_layer.size = vis_size
                                    self.molecule_layer.edge_width = (
                                        vis_edge_width
                                    )
                                    self.molecule_layer.edge_color = "red"
                                    self.molecule_layer.selected_data = []
                                    self.molecule_layer.refresh()

                if remove_molecules:
                    if "molecules" in layer_names:
                        self.viewer.layers["molecules"].data = []

                for layer in layer_names:
                    self.viewer.layers[layer].refresh()

    def get_localisation_centres(self, locs, mode="molecules"):
        loc_centres = []

        try:
            for loc in locs:
                frame = int(loc.frame)
                if mode == "molecules":
                    loc_centres.append([frame, loc.y, loc.x])
                else:
                    loc_centres.append([loc.y, loc.x])

        except:
            print(traceback.format_exc())

        return loc_centres

    def closeEvent(self):
        print("Closing PixSeq")
