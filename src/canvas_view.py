from PyQt5.QtWidgets import QGraphicsView
import cv2
from settings import Tool
import numpy as np
from collections import deque

from confirm_dialog import ConfirmDialog


class CanvasView(QGraphicsView):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._canvas = None
        self._dragging = False
        self._thickness = 1
        self._line_start = None

    def set_canvas(self, canvas):
        self._canvas = canvas

    def set_color_mgr(self, color_mgr):
        self._color_mgr = color_mgr

    def set_tools_mgr(self, tools_mgr):
        self._tools_mgr = tools_mgr

    def set_files_mgr(self, files_mgr):
        self._files_mgr = files_mgr

    def set_main_window(self, m_window):
        self._m_window = m_window
        self._m_window.btn_clear.clicked.connect(self.clear_screen)
        self._m_window.thicknessBox.currentTextChanged.connect(self.thickness_changed)

    def thickness_changed(self, t: str):
        pixels = t.rstrip('px')
        if not pixels.isdigit():
            return
        self._thickness = int(pixels)

    def change_with_thickness(self, x: int, y: int, color):
        if self._canvas is None:
            return
        arr = self._canvas.to_arr()
        l = self._thickness // 2
        r = self._thickness - l
        yl = max(0, y - l)
        yr = min(arr.shape[0], y + r)
        xl = max(0, x - l)
        xr = min(arr.shape[1], x + r)

        arr[yl:yr, xl:xr, :] = color

    def pencil_tool(self, x, y):
        if self._canvas is None:
            return

        self.change_with_thickness(x, y, self._color_mgr.selected_bgra)
        self._canvas.refresh()

    def eraser_tool(self, x, y):
        if self._canvas is None:
            return
        self.change_with_thickness(x, y, [255, 255, 255, 255])
        self._canvas.refresh()

    def fill_tool(self, lx, ly):
        if self._canvas is None:
            return
        # BFS flood fill
        arr = self._canvas.to_arr()
        orig_color = tuple(arr[ly,lx])
        target_color = tuple(self._color_mgr.selected_bgra)
        visited = np.zeros(arr.shape[:2], dtype=bool)
        queue = deque([(ly, lx)])
        while queue:
            y, x = queue.popleft()
            if visited[y, x]:
                continue

            visited[y, x] = True
            arr[y, x] = target_color

            for dy, dx in ((y-1, x), (y+1, x), (y, x-1), (y, x+1)):
                if 0 <= dy < arr.shape[0] and 0 <= dx < arr.shape[1]:
                    if not visited[dy, dx] and tuple(arr[dy, dx]) == orig_color:
                        queue.append((dy, dx))

        self._canvas.refresh()

    def line_tool(self, x, y):
        if self._canvas is None:
            return

        if self._line_start is None:
            self._line_start = (x, y)

        self._canvas._arr_temp = np.zeros_like(self._canvas._arr)
        cv2.line(self._canvas._arr_temp, self._line_start, (x, y), self._color_mgr.selected_bgra, self._thickness)
        self._canvas.refresh()

    def clear_screen(self):
        if not self._canvas:
            return

        dlg = ConfirmDialog("Are you sure you want to clear the canvas?", self)
        if not dlg.exec():
            return

        arr = self._canvas.to_arr()
        arr[:, :, :] = [255, 255, 255, 255]
        self._canvas.refresh()

    def mousePressEvent(self, event):
        if not self._canvas or event is None:
            return

        self._dragging = True
        self.handle_paint(event)

    def mouseMoveEvent(self, event):
        if not self._dragging or not self._canvas or not self._color_mgr:
            return
        self.handle_paint(event)

    def mouseReleaseEvent(self, event):
        self._dragging = False
        self.handle_release(event)

    def handle_release(self, event):
        if not self._canvas or event is None:
            return

        scene_pos = self.mapToScene(event.pos())
        x = int(scene_pos.x() / self._canvas._scale_factor)
        y = int(scene_pos.y() / self._canvas._scale_factor)

        match self._tools_mgr.selected:
            case Tool.LINE.value:
                if self._line_start is not None:
                    cv2.line(self._canvas._arr, self._line_start, (x, y), self._color_mgr.selected_bgra, self._thickness)
                    self._canvas._arr_temp = None
                    self._line_start = None

    def handle_paint(self, event):
        if not self._canvas or event is None:
            return

        scene_pos = self.mapToScene(event.pos())
        x = int(scene_pos.x() / self._canvas._scale_factor)
        y = int(scene_pos.y() / self._canvas._scale_factor)

        if not (0 <= x < self._canvas.width() and 0 <= y < self._canvas.height()):
            return

        # Tool selection check
        match self._tools_mgr.selected:
            case Tool.PENCIL.value:
                self.pencil_tool(x, y)

            case Tool.ERASER.value:
                self.eraser_tool(x, y)

            case Tool.FILL.value:
                self.fill_tool(x, y)

            case Tool.LINE.value:
                self.line_tool(x, y)

            case _:
                return

        self._files_mgr.updated()

