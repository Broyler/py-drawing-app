import sys

from PyQt5.QtGui import QImage
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5 import uic

from color_mgr import ColorManager
from canvas import Canvas
from tools_mgr import ToolsManager


class PaintWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("main.ui", self)
        self.setWindowTitle("Python drawing")
        self.setFixedSize(800, 600)

        color_mgr = ColorManager(self)
        color_mgr.init()

        canvas_mgr = Canvas(QImage.Format_ARGB32, self)
        canvas_mgr.fill(0xffffffff)
        canvas_mgr.init()

        tools_mgr = ToolsManager(self)
        tools_mgr.init()

        self.graphics_view.set_canvas(canvas_mgr)
        self.graphics_view.set_color_mgr(color_mgr)
        self.graphics_view.set_tools_mgr(tools_mgr)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = PaintWindow()
    window.show()
    sys.exit(app.exec_())

