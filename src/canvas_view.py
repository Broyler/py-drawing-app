from PyQt5.QtWidgets import QGraphicsView
from settings import Tool, undo_buffer
import numpy as np

from confirm_dialog import ConfirmDialog
from tools.pencil import Pencil
from tools.circle import Circle
from tools.rect import Rect
from tools.line import Line
from tools.floodfill import FloodFill

from tools.common import ToolOperation


class CanvasView(QGraphicsView):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._canvas = None
        self._dragging = False
        self._thickness = 1
        self._line_start = None
        self._undo_stack = []
        self._undo_ptr = 0

    def set_props(self, canvas, color_mgr, tools_mgr, files_mgr, m_window):
        self._canvas = canvas
        self._color_mgr = color_mgr
        self._tools_mgr = tools_mgr
        self._files_mgr = files_mgr
        self._m_window = m_window
        self._bind()

    def _bind(self):
        self._m_window.btn_clear.clicked.connect(self.clear_screen)
        self._m_window.thicknessBox.currentTextChanged.connect(self.thickness_changed)
        self._m_window.actionUndo.triggered.connect(lambda _: self.undo())
        self._m_window.actionRedo.triggered.connect(lambda _: self.redo())

    def undo(self):
        if len(self._undo_stack) == 0 or self._undo_ptr == 0:
            return

        self._undo_ptr -= 1
        action = self._undo_stack[self._undo_ptr]
        action.undo()
        self._files_mgr.updated()

    def redo(self):
        if len(self._undo_stack) <= self._undo_ptr:
            return

        action = self._undo_stack[self._undo_ptr]
        self._undo_ptr += 1
        action.redo()
        self._files_mgr.updated()

    # def exec_oper(self, oper, x, y):
    #     op = oper(self, self._canvas._arr_temp, self._canvas._arr)
    #     op.exec(x, y)
    #     if len(self._undo_stack) > self._undo_ptr:
    #         self._undo_stack = self._undo_stack[:self._undo_ptr]
    #
    #     self._undo_stack.append(op)
    #     self._undo_ptr += 1
    #
    #     if len(self._undo_stack) > undo_buffer:
    #         self._undo_stack = self._undo_stack[-undo_buffer:]
    #         self._undo_ptr = len(self._undo_stack)
    #
    #     self._files_mgr.updated()

    def update_undo_stack(self, op):
        if len(self._undo_stack) > self._undo_ptr:
            self._undo_stack = self._undo_stack[:self._undo_ptr]

        self._undo_stack.append(op)
        self._undo_ptr += 1

        if len(self._undo_stack) > undo_buffer:
            self._undo_stack = self._undo_stack[-undo_buffer:]
            self._undo_ptr = len(self._undo_stack)

        self._files_mgr.updated()

    def thickness_changed(self, t: str):
        pixels = t.rstrip('px')
        if not pixels.isdigit():
            return
        self._thickness = int(pixels)


    # @continuous_tool
    # def pencil_tool(self, x, y):
    #     draw_line(self._canvas._arr, self._line_start, (x, y),
    #           self._color_mgr.selected_bgra, self._thickness)

    # @continuous_tool
    def eraser_tool(self, x, y):
        pass
        # draw_line(self._canvas._arr, self._line_start, (x, y),
        #           [255, 255, 255, 255], self._thickness)

    @property
    def color(self):
        return self._color_mgr.selected_bgra

    @property
    def arr(self):
        return self._canvas._arr

    # @preview_tool
    # def line_tool(self, x, y):
    #     draw_line(self._canvas._arr_temp, self._line_start, (x, y),
    #           self._color_mgr.selected_bgra, self._thickness)
    #
    # @preview_tool
    # def rect_tool(self, x, y):
    #     draw_rectangle(self._canvas._arr_temp, self._line_start, (x, y),
    #                self._color_mgr.selected_bgra, self._thickness)

    # @preview_tool
    # def circle_tool(self, x, y):
    #     dx = abs(x - self._line_start[0])
    #     dy = abs(y - self._line_start[1])
    #     rad = round(np.sqrt(dx*dx + dy*dy))
    #     draw_circle(self._canvas._arr_temp, self._line_start, rad,
    #                 self._color_mgr.selected_bgra, self._thickness)

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
        self._tools_mgr.operation = None

    def handle_release(self, event):
        if not self._canvas or event is None:
            return
        scene_pos = self.mapToScene(event.pos())
        x = int(scene_pos.x() / self._canvas._scale_factor)
        y = int(scene_pos.y() / self._canvas._scale_factor)

        # tools = {
        #     Tool.LINE.value: Line,
        #     Tool.RECT.value: Rect,
        #     Tool.CIRCLE.value: Circle,
        #     Tool.FILL.value: FloodFill,
        # }

        # tool = tools.get(self._tools_mgr.selected)
        # if tool is not None and issubclass(tool, ToolOperation):
        #     if not (tool.requires_drag and not self._line_start):
        #         self.exec_oper(tool, x, y)

        self._tools_mgr.apply_tool(x, y)
        self._line_start = None
        self._canvas._arr_temp[:, :, :] = 0
        self._files_mgr.updated()

    def handle_paint(self, event):
        if not self._canvas or event is None:
            return

        scene_pos = self.mapToScene(event.pos())
        x = int(scene_pos.x() / self._canvas._scale_factor)
        y = int(scene_pos.y() / self._canvas._scale_factor)

        if self._line_start is None:
            self._line_start = (x, y)

        if not (0 <= x < self._canvas.width() and 0 <= y < self._canvas.height()):
            return

        self._tools_mgr.preview_tool(x, y)
        self._files_mgr.updated()

