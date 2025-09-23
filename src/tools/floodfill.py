from draw.floodfill import fill_tool
from tools.common import ToolOperation


class FloodFill(ToolOperation):
    requires_drag = False

    def draw(self, x, y):
        fill_tool(self._ctx._canvas._arr, self.tmp, x, y, self._ctx.color)

