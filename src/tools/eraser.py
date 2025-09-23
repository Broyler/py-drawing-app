from tools.common import ToolOperation
from draw.line import draw_line


class Eraser(ToolOperation):
    continuous = True
    temp_flush = False

    def draw(self, x, y, arr):
        draw_line(arr, self._ctx._line_start, (x, y),
              [255, 255, 255, 255], self._ctx._thickness)

