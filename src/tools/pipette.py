from tools.common import ToolOperation


class Pipette(ToolOperation):
    no_effect = True
    requires_drag = False

    def draw(self, x, y, arr):
        bgra = self._ctx._canvas._arr[y,x]
        self._ctx._color_mgr.select_bgra(bgra)

