from typing import Optional
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import QGraphicsPixmapItem, QGraphicsScene
import numpy as np
from settings import canvas_channels, scale_factor, canvas_pad


class Canvas(QImage):
    def __init__(self, fmt, m_window):
        view_w = m_window.graphics_view.width() - canvas_pad
        view_h = m_window.graphics_view.height() - canvas_pad

        base_size = min(view_w, view_h)
        snapped_size = base_size - (base_size % scale_factor)
        canvas_size = snapped_size // scale_factor

        super().__init__(canvas_size, canvas_size, fmt)

        self._width = canvas_size
        self._height = canvas_size
        self._channels = canvas_channels
        self.arr: Optional[np.ndarray] = None
        self._graphics_view = m_window.graphics_view
        self._scale_factor = scale_factor
        self._scene = None
        self._pixmap_item = None

    def to_arr(self) -> Optional[np.ndarray]:
        ptr = self.bits()
        if not ptr:
            return

        ptr.setsize(self.byteCount())
        buf = memoryview(ptr)

        bytes_per_pixel = self._channels
        bytes_per_line = self.bytesPerLine()
        padded_width_px = bytes_per_line // bytes_per_pixel

        raw = np.ndarray(
            shape=(self._height, padded_width_px, bytes_per_pixel),
            dtype=np.uint8,
            buffer=buf,
        )
        self.arr = raw[:, : self._width, :]
        return self.arr

    def init(self):
        self.to_arr()
        if self.arr is None:
            return

        if self._scene is None:
            self._scene = QGraphicsScene()

        if self._pixmap_item is None:
            self._pixmap_item = QGraphicsPixmapItem(QPixmap.fromImage(self))
            self._scene.addItem(self._pixmap_item)

        self._pixmap_item.setScale(self._scale_factor)
        self._graphics_view.setScene(self._scene)

    def refresh(self):
        if self._pixmap_item is None:
            return
        self._pixmap_item.setPixmap(QPixmap.fromImage(self))

