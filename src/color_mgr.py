from typing import Optional, List
from functools import partial

from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QColorDialog
import settings


class ColorManager:
    def __init__(self, m_window):
        self.m_window = m_window
        self.selected: Optional[str] = None
        self.buttons = {}
        self.selected_custom = None
        self.color_settings = settings.colors

    @property
    def selected_btn(self):
        return self.buttons.get(self.selected)

    @property
    def selected_color(self) -> Optional[str]:
        if self.selected is not None:
            return self.color_settings.get(self.selected)
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

    def custom_color_select(self):
        color = QColorDialog.getColor(QColor(self.selected_custom or "#ffffff"), self.m_window, "Select Color")

        if color.isValid():
            self.m_window.btn_customcolor.setStyleSheet(f"background-color: {color.name()};")
            self.color_settings["customcolor"] = color.name()
            self.selected_custom = color.name()
            self.on_color_select("customcolor")
            return True
        return False

    def init(self):
        self.m_window.button_other_color.clicked.connect(self.custom_color_select)

        for color in self.color_settings.keys():
            btn = getattr(self.m_window, "btn_" + color)
            self.buttons[color] = btn
            btn.clicked.connect(partial(self.on_color_select, color))

            if self.selected is None:
                self.selected = color
                btn.setChecked(True)

            else:
                btn.setChecked(False)

    def on_color_select(self, color: str) -> None:
        if color == "customcolor" and self.selected_custom is None:
            if not self.custom_color_select():
                return

        new = self.buttons.get(color)
        if new is None:
            return

        if self.selected_btn is not None:
            self.selected_btn.setChecked(False)

        self.selected = color
        if self.selected_btn:
            self.selected_btn.setChecked(True)

