from functools import partial
import settings
from settings import Tool
from typing import Optional
import numpy as np

from tools.pencil import Pencil
from tools.circle import Circle
from tools.rect import Rect
from tools.line import Line
from tools.floodfill import FloodFill
from tools.common import ToolOperation

tools = {
    Tool.LINE.value: Line,
    Tool.RECT.value: Rect,
    Tool.CIRCLE.value: Circle,
    Tool.PENCIL.value: Pencil
}


class ToolsManager:
    def __init__(self, m_window):
        self.m_window = m_window
        self.selected: Optional[str] = None
        self.buttons = {}
        self.operation = None

    def set_context(self, ctx):
        self._ctx = ctx
    
    def select(self):
        if not self.selected:
            return

        tool = tools.get(self.selected)

        if tool is not None and issubclass(tool, ToolOperation):
            self.operation = tool(
                    self._ctx,
                    self._ctx._canvas._arr_temp,
                    self._ctx._canvas._arr,
            )

        else:
            self.operation = None

    def preview_tool(self, x, y):
        if self.operation is None:
            return
        self.operation.preview(x, y)

    def apply_tool(self, x, y):
        if self.operation is None:
            return

        op = self.operation
        op.exec(x, y)
        self._ctx.update_undo_stack(op)

    def init(self):
        for tool in settings.tools:
            btn = getattr(self.m_window, "button_" + tool)
            self.buttons[tool] = btn
            btn.clicked.connect(partial(self.on_tool_select, tool))

            if self.selected is None:
                self.selected = tool
                btn.setChecked(True)
                self.select()

            else:
                btn.setChecked(False)

    @property
    def selected_btn(self):
        return self.buttons.get(self.selected)

    def on_tool_select(self, tool: str) -> None:
        new_tool = self.buttons.get(tool)
        if new_tool is None:
            return

        if self.selected_btn is not None:
            self.selected_btn.setChecked(False)

        self.selected = tool
        if self.selected_btn:
            self.selected_btn.setChecked(True)

