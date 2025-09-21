from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import QGraphicsPixmapItem, QGraphicsScene
import numpy as np
from settings import canvas_channels, scale_factor, canvas_pad

import numpy as np
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import QGraphicsScene, QGraphicsPixmapItem, QGraphicsView


class Canvas(QImage):
    def __init__(self, m_window):
        self._graphics_view = m_window.graphics_view
        self._channels = canvas_channels
        self._scale_factor = scale_factor

        self._scene = QGraphicsScene()
        self._pixmap_item = QGraphicsPixmapItem()
        self._scene.addItem(self._pixmap_item)
        self._graphics_view.setScene(self._scene)

        width, height = self._calculate_canvas_size()
        super().__init__(width, height, QImage.Format_ARGB32)
        self._width = width
        self._height = height

        self._arr = self._create_array()
        self._arr_temp = None
        self._pixmap_item.setPixmap(QPixmap.fromImage(self))
        self._pixmap_item.setScale(self._scale_factor)

        self._graphics_view.resizeEvent = self._on_view_resize

    def _calculate_canvas_size(self):
        view_w = max(1, self._graphics_view.width() - canvas_pad)
        view_h = max(1, self._graphics_view.height() - canvas_pad)
        return view_w // self._scale_factor, view_h // self._scale_factor

    def _create_array(self):
        ptr = self.bits()
        if ptr is None:
            return
        ptr.setsize(self.byteCount())
        arr = np.ndarray(
            shape=(self.height(), self.width(), self._channels),
            dtype=np.uint8,
            buffer=ptr
        )
        arr[:, :, :] = 255
        return arr

    @property
    def arr(self):
        return self._arr

    def to_arr(self):
        return self._arr

    def _on_view_resize(self, event):
        new_w, new_h = self._calculate_canvas_size()
        if new_w == self._width and new_h == self._height:
            return

        if self._arr is None:
            return

        old_arr = self._arr.copy()
        old_w, old_h = self._width, self._height

        self._width, self._height = new_w, new_h
        super().__init__(new_w, new_h, QImage.Format_ARGB32)
        self._arr = self._create_array()

        if self._arr is None:
            return

        h = min(old_h, new_h)
        w = min(old_w, new_w)
        self._arr[:h, :w, :] = old_arr[:h, :w, :]

        self.refresh()

    def refresh(self):
        if self._arr is None:
            return

        if self._arr_temp is None:
            self._pixmap_item.setPixmap(QPixmap.fromImage(self))
            return

        arr_disp = self._arr.copy()
        mask = self._arr_temp[:, :, 3] > 0
        arr_disp[mask] = self._arr_temp[mask]
        self._pixmap_item.setPixmap(QPixmap.fromImage(QImage(
            arr_disp.data,
            arr_disp.shape[1],
            arr_disp.shape[0],
            arr_disp.strides[0],
            QImage.Format_ARGB32
        )))

