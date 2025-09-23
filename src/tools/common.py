import numpy as np
from abc import ABC, abstractmethod


class ToolOperation(ABC):
    requires_drag: bool = True
    temp_flush: bool = True
    continuous: bool = False

    def __init__(self, context, canvas):
        self._ctx = context
        self._diff = None
        self._canvas = canvas

    @abstractmethod
    def draw(self, x, y, arr):
        raise NotImplementedError()

    def preview(self, x, y):
        if not self.requires_drag:
            return
        if self._canvas._arr_temp is None or self.temp_flush:
            self._canvas._arr_temp = np.zeros_like(self._canvas._arr)
        self.draw(x, y, self._canvas._arr_temp)
        if self.continuous:
            self._ctx._line_start = (x, y)
        self._canvas.refresh()

    def _apply_diff(self, undo: bool = False):
        if self._diff is None or len(self._diff) == 0:
            return
        
        x_coords = self._diff[:, 0].astype(int)
        y_coords = self._diff[:, 1].astype(int)
        height, width = self._canvas._arr.shape[:2]

        valid_mask = (x_coords < width) & (y_coords < height) & (x_coords >= 0) & (y_coords >= 0)

        valid_x = x_coords[valid_mask]
        valid_y = y_coords[valid_mask]

        if undo:
            valid_colors = self._diff[valid_mask, 2:6]
        else:
            valid_colors = self._diff[valid_mask, 6:10]

        if len(valid_x) > 0:
            self._canvas._arr[valid_y, valid_x] = valid_colors
            self._canvas.refresh()       

    def exec(self, x, y):
        self.tmp = np.zeros_like(self._canvas._arr)
        if not self.requires_drag:
            self.draw(x, y, self.tmp)
        else:
            self.tmp = self._canvas._arr_temp

        before = self._canvas._arr
        after = before.copy()
        mask = self.tmp[:, :, 3] > 0
        after[mask] = self.tmp[mask]
        if before.ndim == 3:
            changed = np.any(before != after, axis=2)
        else:
            changed = before != after

        if not np.any(changed):
            ch = before.shape[2] if before.ndim == 3 else 1
            self._diff = np.empty((0, 2 + ch * 2), dtype=before.dtype)
            return

        yc, xc = np.where(changed)
        old_col = before[yc, xc]
        new_col = after[yc, xc]
        self._diff = np.column_stack([xc, yc, old_col, new_col])
        self._apply_diff()
        self._canvas._arr_temp = np.zeros_like(self._canvas._arr)

    def undo(self):
        self._apply_diff(undo=True)

    def redo(self):
        self._apply_diff()
        
