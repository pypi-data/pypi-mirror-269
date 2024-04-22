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

import collections.abc as cllt
import pprint as pprt
import typing as h

import numpy
import PyQt6.QtCore as core
import PyQt6.QtGui as qtui
import PyQt6.QtWidgets as wdgt
from PyQt6.QtCore import QRunnable as task_base_t
from PyQt6.QtCore import QThreadPool as thread_manager_t
from pyvispr.extension.qt6 import ExecuteApp, QtApp
from pyvispr.runtime.backend import SCREEN_BACKEND


def pyVisprValueViewer(value: h.Any, /) -> None:
    """"""
    app, should_exec = QtApp()
    value_viewer = value_viewer_t(value, wdgt.QApplication.activeWindow())
    value_viewer.show()
    ExecuteApp(app, should_exec)
    # TODO: Solve the following error:
    #     QBasicTimer::stop: Failed. Possibly trying to stop from a different thread
    #     The code below makes it disappear, but the table is not correctly populated then.
    # if value_viewer.thread_manager is not None:
    #     value_viewer.thread_manager.waitForDone()
    # Test also somewhere (not here though; it does not work):
    # value_viewer.thread_manager.moveToThread(wdgt.QApplication.instance().thread())


class task_t(task_base_t):
    def __init__(
        self,
        viewer: wdgt.QTableView,
        model: qtui.QStandardItemModel,
        value: cllt.Iterable[cllt.Iterable],
        /,
    ) -> None:
        """"""
        task_base_t.__init__(self)
        self.viewer = viewer
        self.model = model
        self.value = value

    @core.pyqtSlot()
    def run(self) -> None:
        """"""
        min_value, max_value = numpy.amin(self.value), numpy.amax(self.value)
        if max_value > min_value:
            color = qtui.QColor()
            if (min_value, max_value) != (0, 255):
                factor = 255.0 / (max_value - min_value)
            else:
                factor = None
        else:
            color = factor = None

        for row in self.value:
            cells = map(str, row)
            cells = tuple(map(qtui.QStandardItem, cells))
            if color is None:
                for cell in cells:
                    cell.setTextAlignment(core.Qt.AlignmentFlag.AlignRight)
            else:
                for cell, value in zip(cells, row):
                    if factor is None:
                        gray = value
                    else:
                        gray = int(round(factor * (value - min_value)))
                    color.setRgb(255 - gray, 255, 255 - gray, 255)
                    cell.setData(
                        core.QVariant(qtui.QBrush(color)),
                        core.Qt.ItemDataRole.BackgroundRole,
                    )
                    cell.setTextAlignment(core.Qt.AlignmentFlag.AlignRight)
            self.model.appendRow(cells)

        self.viewer.resizeRowsToContents()
        self.viewer.resizeColumnsToContents()

        self.viewer.setEnabled(True)

        self.value = None


class value_viewer_t(wdgt.QMainWindow):
    def __init__(self, value: h.Any, wdw: wdgt.QWidget, /) -> None:
        """"""
        super().__init__(wdw)

        try:
            as_array = numpy.array(value)
        except:
            as_array = None
        if (
            (as_array is not None)
            and (as_array.ndim < 3)
            and (as_array.size > 1)
            and (
                numpy.issubdtype(as_array.dtype, numpy.integer)
                or numpy.issubdtype(as_array.dtype, numpy.floating)
            )
        ):
            self.value = as_array

            self.viewer = wdgt.QTableView()
            self.viewer.setEnabled(False)

            self.model = qtui.QStandardItemModel(self.viewer)
            self.model.setColumnCount(max(_elm.__len__() for _elm in self.value))

            self.viewer.setModel(self.model)

            self.filling_task = task_t(self.viewer, self.model, self.value)
            thread_manager_t.globalInstance().start(self.filling_task)
        else:
            as_str = pprt.pformat(value, width=120, compact=True, sort_dicts=False)
            self.viewer = wdgt.QTextEdit(as_str)

        done = wdgt.QPushButton("Done")

        layout = wdgt.QVBoxLayout()
        layout.addWidget(self.viewer)
        layout.addWidget(done)

        central = wdgt.QWidget()
        central.setLayout(layout)
        self.setCentralWidget(central)

        self.setWindowTitle("pyVispr Value Viewer")

        SCREEN_BACKEND.CreateMessageCanal(done, "clicked", self.close)
