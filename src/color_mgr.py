from typing import Optional, List
from functools import partial
import settings


class ColorManager:
    def __init__(self, m_window):
        self.m_window = m_window
        self.selected: Optional[str] = None
        self.buttons = {}

    @property
    def selected_btn(self):
        return self.buttons.get(self.selected)

    @property
    def selected_color(self) -> Optional[str]:
        if self.selected is not None:
            return settings.colors.get(self.selected)
        return None

    @property
    def selected_ints(self) -> List[int]:
        if not self.selected_color:
            return [255, 255, 255]
        col = self.selected_color.lstrip('#')
        return [int(col[i:i+2], 16) for i in (0, 2, 4)]

    @property 
    def selected_bgra(self) -> List[int]:
        r, g, b = self.selected_ints
        return [b, g, r, 255]

    def init(self):
        for color in settings.colors.keys():
            btn = getattr(self.m_window, "btn_" + color)
            self.buttons[color] = btn
            btn.clicked.connect(partial(self.on_color_select, color))

            if self.selected is None:
                self.selected = color
                btn.setChecked(True)

            else:
                btn.setChecked(False)

    def on_color_select(self, color: str) -> None:
        new = self.buttons.get(color)
        if new is None:
            return

        if self.selected_btn is not None:
            self.selected_btn.setChecked(False)

        self.selected = color
        if self.selected_btn:
            self.selected_btn.setChecked(True)

