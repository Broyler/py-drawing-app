from draw.floodfill import fill_tool
from tools.common import ToolOperation


class FloodFill(ToolOperation):
    requires_drag = False

    def draw(self, x, y, arr):
        fill_tool(arr, self.tmp, x, y, self._ctx.color)

