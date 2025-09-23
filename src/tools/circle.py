from draw.circle import draw_circle
from tools.common import ToolOperation
from numpy import sqrt


class Circle(ToolOperation):
    def draw(self, x, y):
        dx = abs(x - self._ctx._line_start[0])
        dy = abs(y - self._ctx._line_start[1])
        rad = round(sqrt(dx*dx + dy*dy))
        draw_circle(self.tmp, self._ctx._line_start, rad,
                    self._ctx.color, self._ctx._thickness)

