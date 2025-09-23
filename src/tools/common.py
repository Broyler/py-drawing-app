import numpy as np
from abc import ABC, abstractmethod


class ToolOperation(ABC):
    requires_drag: bool = True

    def __init__(self, context):
        self._ctx = context
        self._diff = None

    @abstractmethod
    def draw(self, x, y):
        raise NotImplementedError()

    def _apply_diff(self, undo: bool = False):
        if self._diff is None or len(self._diff) == 0:
            return
        
        x_coords = self._diff[:, 0].astype(int)
        y_coords = self._diff[:, 1].astype(int)
        
        if undo:
            colors_to_apply = self._diff[:, 2:6]
        else:
            colors_to_apply = self._diff[:, 6:10]
        
        self._ctx._canvas._arr[y_coords, x_coords] = colors_to_apply
        self._ctx._canvas.refresh()

    def exec(self, x, y):
        self.tmp = np.zeros_like(self._ctx.arr)
        self.draw(x, y)
        before = self._ctx.arr
        after = self._ctx.arr.copy()
        mask = self.tmp[:, :, 3] > 0
        after[mask] = self.tmp[mask]
        if before.ndim == 3:
            changed = np.any(before !=  after, axis=2)
        else:
            changed = before != after

        if not np.any(changed):
            ch = before.shape[2] if before.nvim == 3 else 1
            self._diff = np.empty((0, 2 + ch * 2), dtype=before.dtype)
            return

        yc, xc = np.where(changed)
        old_col = before[yc, xc]
        new_col = after[yc, xc]
        self._diff = np.column_stack([xc, yc, old_col, new_col])
        self._apply_diff()

    def undo(self):
        self._apply_diff(undo=True)

    def redo(self):
        self._apply_diff()
        

def preview_tool(func):
    def wrapper(self, *args, **kwargs):
        ctx = None
        if hasattr(self, "_ctx"):
            ctx = self._ctx
        else:
            ctx = self

        if ctx._canvas is None:
            return

        if ctx._line_start is None:
            ctx._line_start = (args[0], args[1])

        ctx._canvas._arr_temp = np.zeros_like(ctx._canvas._arr)
        func(self, *args, **kwargs)
        ctx._canvas.refresh()
    return wrapper


def continuous_tool(func):
    def wrapper(self, *args, **kwargs):
        ctx = None
        if hasattr(self, "_ctx"):
            ctx = self._ctx
        else:
            ctx = self

        if ctx._canvas is None:
            return
        
        if ctx._line_start is None:
            ctx._line_start = (args[0], args[1])

        func(self, *args, **kwargs)

        ctx._line_start = (args[0], args[1])
        ctx._canvas.refresh()
    return wrapper

