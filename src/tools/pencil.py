from tools.common import ToolOperation
from draw.line import draw_line


class Pencil(ToolOperation):
    def draw(self, x, y, arr):
        draw_line(arr, self._ctx._line_start, (x, y),
              self._ctx.color, self._ctx._thickness)

