from draw.line import draw_line
from tools.common import ToolOperation


class Line(ToolOperation):
    def draw(self, x, y, arr):
        draw_line(arr, self._ctx._line_start, (x, y),
                  self._ctx.color, self._ctx._thickness)

