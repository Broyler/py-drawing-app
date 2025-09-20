from PyQt5.QtWidgets import QGraphicsView
from settings import Tool
import numpy as np
from collections import deque


class CanvasView(QGraphicsView):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._canvas = None
        self._dragging = False

    def set_canvas(self, canvas):
        self._canvas = canvas

    def set_color_mgr(self, color_mgr):
        self._color_mgr = color_mgr

    def set_tools_mgr(self, tools_mgr):
        self._tools_mgr = tools_mgr

    def pencil_tool(self, x, y):
        if self._canvas is None:
            return
        arr = self._canvas.to_arr()
        arr[y, x] = self._color_mgr.selected_bgra
        self._canvas.refresh()

    def eraser_tool(self, x, y):
        if self._canvas is None:
            return
        arr = self._canvas.to_arr()
        arr[y, x] = [255, 255, 255, 255]
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

