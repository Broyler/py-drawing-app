from functools import partial
import settings
from typing import Optional


class ToolsManager:
    def __init__(self, m_window):
        self.m_window = m_window
        self.selected: Optional[str] = None
        self.buttons = {}
    
    def init(self):
        for tool in settings.tools:
            btn = getattr(self.m_window, "button_" + tool)
            self.buttons[tool] = btn
            btn.clicked.connect(partial(self.on_tool_select, tool))

            if self.selected is None:
                self.selected = tool
                btn.setChecked(True)

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

