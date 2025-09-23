import sys, os

from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5 import uic
from color_mgr import ColorManager
from canvas import Canvas
from tools_mgr import ToolsManager
from files_mgr import FilesManager
import canvas_view


class PaintWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        if getattr(sys, "frozen", False):
            base_path = sys._MEIPASS
        else:
            base_path = os.path.dirname(os.path.abspath(__file__)).rstrip('src/')

        ui_path = os.path.join(base_path, "main.ui")
        uic.loadUi(ui_path, self)
        self.setWindowTitle("Python drawing")

        color_mgr = ColorManager(self)
        color_mgr.init()

        canvas_mgr = Canvas(self)
        canvas_mgr.fill(0xffffffff)

        tools_mgr = ToolsManager(self)

        self.files_mgr = FilesManager(self, canvas_mgr)

        self.graphics_view.set_props(
                canvas_mgr,
                color_mgr,
                tools_mgr,
                self.files_mgr,
                self
        )
        tools_mgr.set_context(self.graphics_view)
        tools_mgr.init()
        self.files_mgr.set_context(self.graphics_view)
        self.files_mgr.init()

    def closeEvent(self, a0) -> None:
        self.files_mgr.handle_close(a0)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = PaintWindow()
    window.show()
    sys.exit(app.exec_())

