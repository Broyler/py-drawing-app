from draw.rect import draw_rectangle
from tools.common import ToolOperation


class Rect(ToolOperation):
    def draw(self, x, y):
        draw_rectangle(self.tmp, self._ctx._line_start, (x, y),
                       self._ctx.color, self._ctx._thickness)

