# Copyright CNRS/Inria/UniCA
# Contributor(s): Eric Debreuve (since 2017)
#
# eric.debreuve@cnrs.fr
#
# This software is governed by the CeCILL  license under French law and
# abiding by the rules of distribution of free software.  You can  use,
# modify and/ or redistribute the software under the terms of the CeCILL
# license as circulated by CEA, CNRS and INRIA at the following URL
# "http://www.cecill.info".
#
# As a counterpart to the access to the source code and  rights to copy,
# modify and redistribute granted by the license, users are provided only
# with a limited warranty  and the software's author,  the holder of the
# economic rights,  and the successive licensors  have only  limited
# liability.
#
# In this respect, the user's attention is drawn to the risks associated
# with loading,  using,  modifying and/or developing or reproducing the
# software by the user in light of its specific status of free software,
# that may mean  that it is complicated to manipulate,  and  that  also
# therefore means  that it is reserved for developers  and  experienced
# professionals having in-depth computer knowledge. Users are therefore
# encouraged to load and test the software's suitability as regards their
# requirements in conditions enabling the security of their systems and/or
# data to be ensured and,  more generally, to use and operate it in the
# same conditions as regards security.
#
# The fact that you are presently reading this means that you have had
# knowledge of the CeCILL license and that you accept its terms.

from os.path import dirname as DetermineFolder
from os.path import expanduser as ExpandTildeBasePath

import numpy
import PyQt6.QtGui as qtui
import PyQt6.QtWidgets as wdgt
from pyvispr.extension.qt6 import ExecuteApp, QtApp
from pyvispr.runtime.backend import SCREEN_BACKEND


_IMG_FORMAT = {
    1: qtui.QImage.Format.Format_Indexed8,
    3: qtui.QImage.Format.Format_RGB888,
    4: qtui.QImage.Format.Format_RGBA8888,
}
_IMG_FORMAT_AS_STR = {1: "Grayscale 8 bits", 3: "RGB 8 bits", 4: "RGBA 8 bits"}


def pyVisprImageViewer(image: numpy.ndarray, /) -> None:
    """"""
    img_shape = image.shape
    if 1 < len(img_shape) < 4:
        width = img_shape[1]
        height = img_shape[0]
        if len(img_shape) == 2:
            depth = 1
        else:
            depth = img_shape[2]
            if depth not in (3, 4):
                wdgt.QMessageBox.critical(
                    None,
                    f"{pyVisprImageViewer.__name__}: Error",
                    f"Input 3rd dimension is {depth}; It must be 3 or 4 instead.",
                )
                return
    else:
        wdgt.QMessageBox.critical(
            None,
            f"{pyVisprImageViewer.__name__}: Error",
            "Input must be a 2D or 3D numpy array",
        )
        return

    app, should_exec = QtApp()
    viewer = viewer_t(
        image,
        width,
        height,
        depth,
        wdgt.QApplication.activeWindow(),
    )
    viewer.show()
    ExecuteApp(app, should_exec)


class viewer_t(wdgt.QMainWindow):
    DEFAULT_SAVE_EXTENSION = "png"  # lowercase

    def __init__(
        self,
        image: numpy.ndarray,
        width: int,
        height: int,
        depth: int,
        wdw: wdgt.QWidget,
    ):
        """"""
        super().__init__(wdw)
        self.setWindowTitle("pyVispr Image Viewer")

        self.quit_action = None
        self.save_action = None
        self.copy_action = None
        self.zoom_in_action = None
        self.zoom_out_action = None
        self.original_size_action = None
        self.fit_to_window_action = None

        self.last_save_location = ExpandTildeBasePath("~")

        screen_size = self.screen().availableGeometry()
        wdw_width = min(width, int(0.75 * screen_size.width()))
        wdw_height = min(height, int(0.75 * screen_size.height()))
        self.resize(wdw_width, wdw_height)

        min_value, max_value, mean_value, median_value = _ImageStatistics(image, depth)
        self._CreateMenus(
            width,
            height,
            depth,
            min_value,
            max_value,
            mean_value,
            median_value,
        )

        self.image_container = wdgt.QLabel()
        self.image_container.setBackgroundRole(qtui.QPalette.ColorRole.Base)
        self.image_container.setSizePolicy(
            wdgt.QSizePolicy.Policy.Ignored, wdgt.QSizePolicy.Policy.Ignored
        )
        self.image_container.setScaledContents(True)

        self.scroll_area = wdgt.QScrollArea()
        self.scroll_area.setBackgroundRole(qtui.QPalette.ColorRole.Dark)
        self.scroll_area.setWidget(self.image_container)

        self.scale_bars = _ScaleBars(min_value, max_value, depth)

        layout = wdgt.QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.scroll_area)
        for scale_bar in self.scale_bars:
            layout.addWidget(scale_bar)

        central_widget = wdgt.QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        image = _NewNImage_0_255(image, min_value, max_value, depth)
        self.q_img, self.np_img = _NewQImage(image, width, height, depth)
        self.image_container.setPixmap(qtui.QPixmap.fromImage(self.q_img))
        self.image_scale = 1.0
        self.fit_to_window_action.setEnabled(True)
        if not self.fit_to_window_action.isChecked():
            self.image_container.adjustSize()

    def _CreateMenus(
        self,
        width,
        height,
        depth,
        min_value,
        max_value,
        mean_value,
        median_value,
    ) -> None:
        """"""
        self._CreateActions()

        numpy.set_printoptions(precision=1, floatmode="fixed")

        menu_bar = self.menuBar()

        menu = wdgt.QMenu("&Viewer", self)
        menu.addAction(self.quit_action)
        menu_bar.addMenu(menu)

        menu = wdgt.QMenu("&Image", self)
        menu.addAction(self.save_action)
        menu.addAction(self.copy_action)
        menu_bar.addMenu(menu)

        menu = wdgt.QMenu("Image &Size", self)
        menu.addAction(self.zoom_in_action)
        menu.addAction(self.zoom_out_action)
        menu.addAction(self.original_size_action)
        menu.addSeparator()
        menu.addAction(self.fit_to_window_action)
        menu_bar.addMenu(menu)

        menu = wdgt.QMenu("Image I&nfo", self)
        action = menu.addAction(f"WxH: {width}x{height}")
        action.setEnabled(False)
        menu.addAction(_IMG_FORMAT_AS_STR[depth])
        action.setEnabled(False)
        menu.addAction(f"min: {min_value}")
        action.setEnabled(False)
        menu.addAction(f"max: {max_value}")
        action.setEnabled(False)
        menu.addAction(f"mean: {mean_value}")
        action.setEnabled(False)
        menu.addAction(f"median: {median_value}")
        action.setEnabled(False)
        menu_bar.addMenu(menu)

        self._UpdateActions()

    def _CreateActions(self) -> None:
        """"""
        attributes = (
            "quit",
            "save",
            "copy",
            "zoom_in",
            "zoom_out",
            "original_size",
            "fit_to_window",
        )
        entries = (
            "&Quit",
            "&Save",
            "&Copy",
            "Zoom &In (25%)",
            "Zoom &Out (25%)",
            "Original Si&ze",
            "&Fit to Window",
        )
        shortcuts = (
            qtui.QKeySequence.StandardKey.Quit,
            qtui.QKeySequence.StandardKey.Save,
            qtui.QKeySequence.StandardKey.Copy,
            "Ctrl++",
            "Ctrl+-",
            "Ctrl+=",
            "Ctrl+/",
        )
        Functions = (
            self.close,
            self.SaveImage,
            self.CopyImage,
            self.ZoomImageIn,
            self.ZoomImageOut,
            self.RevertImageToOriginalSize,
            self.FitImageToWindow,
        )
        for attribute, entry, shortcut, Function in zip(
            attributes,
            entries,
            shortcuts,
            Functions,
        ):
            action = qtui.QAction(entry, self)
            action.setShortcut(shortcut)
            SCREEN_BACKEND.CreateMessageCanal(action, "triggered", Function)
            setattr(self, f"{attribute}_action", action)

        self.fit_to_window_action.setCheckable(True)

    def _UpdateActions(self) -> None:
        """"""
        self.zoom_in_action.setEnabled(not self.fit_to_window_action.isChecked())
        self.zoom_out_action.setEnabled(not self.fit_to_window_action.isChecked())
        self.original_size_action.setEnabled(not self.fit_to_window_action.isChecked())

    def ZoomImageIn(self) -> None:
        """"""
        self._ScaleImage(1.25)

    def ZoomImageOut(self) -> None:
        """"""
        self._ScaleImage(0.8)

    def _ScaleImage(self, factor: float, /) -> None:
        """"""
        self.image_scale *= factor
        self.image_container.resize(
            self.image_scale * self.image_container.pixmap().size()
        )

        _AdjustScrollBarPosition(self.scroll_area.horizontalScrollBar(), factor)
        _AdjustScrollBarPosition(self.scroll_area.verticalScrollBar(), factor)

        self.zoom_in_action.setEnabled(self.image_scale < 3.0)
        self.zoom_out_action.setEnabled(self.image_scale > 0.333)

    def RevertImageToOriginalSize(self) -> None:
        """"""
        self.image_container.adjustSize()
        self.image_scale = 1.0

    def FitImageToWindow(self) -> None:
        """"""
        img_should_fit_to_wdw = self.fit_to_window_action.isChecked()
        self.scroll_area.setWidgetResizable(img_should_fit_to_wdw)
        if not img_should_fit_to_wdw:
            self.RevertImageToOriginalSize()

        self._UpdateActions()

    def CopyImage(self) -> None:
        """"""
        wdgt.QApplication.clipboard().setImage(self.q_img)

    def SaveImage(self) -> None:
        """"""
        supported_formats = list(
            map(
                lambda elm: bytearray(elm).decode().lower(),
                qtui.QImageWriter.supportedImageFormats(),
            )
        )
        supported_formats.sort()

        default_save_extension = viewer_t.DEFAULT_SAVE_EXTENSION
        if default_save_extension not in supported_formats:
            default_save_extension = supported_formats[0]
        default_save_format = _MakeImageFilterFromExtension(default_save_extension)

        supported_formats = ";;".join(
            map(_MakeImageFilterFromExtension, supported_formats)
        )

        filename = wdgt.QFileDialog.getSaveFileName(
            self,
            "Save Image",
            self.last_save_location,
            supported_formats,
            default_save_format,
        )
        if (filename is None) or (len(filename[0]) == 0):
            return
        filename = filename[0]

        self.last_save_location = DetermineFolder(filename)

        img_writer = qtui.QImageWriter(filename)

        if not img_writer.write(self.q_img):
            wdgt.QMessageBox.critical(
                self,
                f"{pyVisprImageViewer.__name__}: Error",
                f"Failure in saving image to '{filename}': {img_writer.errorString()}",
            )


def _ImageStatistics(image: numpy.ndarray, depth: int, /) -> tuple[
    int | float | numpy.ndarray,
    int | float | numpy.ndarray,
    int | float | numpy.ndarray,
    int | float | numpy.ndarray,
]:
    """"""
    if depth == 1:
        min_value = numpy.amin(image).item()
        max_value = numpy.amax(image).item()
        mean_value = numpy.around(numpy.mean(image), decimals=2).item()
        median_value = numpy.around(numpy.median(image), decimals=2).item()
    else:
        min_value = numpy.amin(numpy.amin(image, axis=0), axis=0)
        max_value = numpy.amax(numpy.amax(image, axis=0), axis=0)
        mean_value = numpy.around(
            numpy.mean(numpy.mean(image, axis=0), axis=0), decimals=2
        )
        median_value = numpy.around(
            [numpy.median(image[:, :, _elm]) for _elm in range(depth)],
            decimals=2,
        )

    return min_value, max_value, mean_value, median_value


def _NewNImage_0_255(
    image: numpy.ndarray,
    min_value: int | float | numpy.ndarray,
    max_value: int | float | numpy.ndarray,
    depth: int,
    /,
) -> numpy.ndarray:
    """"""
    if depth < 4:
        only_colors = image
    else:
        only_colors = image[..., :3]

    # Min and max ignoring alpha channel.
    if isinstance(min_value, numpy.ndarray):
        global_min = numpy.amin(min_value[: min(depth, 3)])
        global_max = numpy.amax(max_value[: min(depth, 3)])
    else:
        global_min, global_max = min_value, max_value
    if (global_max > global_min) and ((global_min, global_max) != (0, 255)):
        factor = 255.0 / (global_max - global_min)
        with_min_zero = only_colors.astype(numpy.float64, copy=False) - global_min
        only_colors = numpy.round(factor * with_min_zero)

    if depth < 4:
        np_img = only_colors
    else:
        np_img = numpy.dstack((only_colors, image[..., 3]))

    return np_img.astype(numpy.uint8, copy=False)


def _NewQImage(
    image: numpy.ndarray,
    width: int,
    height: int,
    depth: int,
    /,
) -> tuple[qtui.QImage, numpy.ndarray]:
    """"""
    np_img = image
    try:
        q_img = qtui.QImage(
            np_img.data, width, height, depth * width, _IMG_FORMAT[depth]
        )
    except TypeError:
        # /!\ Without .copy(), qtui.QImage sometimes complains with:
        #     QImage(): too many arguments
        #     ...
        np_img = np_img.copy()
        q_img = qtui.QImage(
            np_img.data, width, height, depth * width, _IMG_FORMAT[depth]
        )

    return q_img, np_img


def _AdjustScrollBarPosition(scroll_bar: wdgt.QScrollBar, factor: float, /) -> None:
    """"""
    scroll_bar.setValue(
        int(factor * scroll_bar.value() + ((factor - 1) * scroll_bar.pageStep() / 2))
    )


def _MakeImageFilterFromExtension(extension: str, /) -> str:
    """"""
    return f"{extension.upper()} Images (*.{extension})"


def _ScaleBars(
    min_value: int | float | numpy.ndarray,
    max_value: int | float | numpy.ndarray,
    depth: int,
    /,
) -> tuple[wdgt.QLabel, ...]:
    """"""
    output = []

    for p_idx in range(depth):
        scale_bar = wdgt.QLabel()
        scale_bar.setBackgroundRole(qtui.QPalette.ColorRole.Base)
        scale_bar.setSizePolicy(
            wdgt.QSizePolicy.Policy.Fixed, wdgt.QSizePolicy.Policy.Ignored
        )
        scale_bar.setScaledContents(True)

        if isinstance(min_value, numpy.ndarray):
            current_min = min_value[p_idx]
            current_max = max_value[p_idx]
        else:
            current_min = min_value
            current_max = max_value

        non_empty_plane = numpy.repeat(
            numpy.flipud(numpy.linspace(current_min, current_max, num=256))[:, None],
            20,
            axis=1,
        )
        if (p_idx < 3) and (depth > 1):
            n_planes = 3
            img_format = qtui.QImage.Format.Format_RGB888
            all_planes = numpy.zeros(
                non_empty_plane.shape + (n_planes,), dtype=numpy.uint8
            )
            all_planes[..., p_idx] = non_empty_plane[...]
        else:
            n_planes = 1
            img_format = qtui.QImage.Format.Format_Indexed8
            all_planes = numpy.uint8(non_empty_plane)

        q_scale_bar = qtui.QImage(
            all_planes.data,
            non_empty_plane.shape[1],
            non_empty_plane.shape[0],
            n_planes * non_empty_plane.shape[1],
            img_format,
        )
        scale_bar.setPixmap(qtui.QPixmap.fromImage(q_scale_bar))

        output.append(scale_bar)

    return tuple(output)
