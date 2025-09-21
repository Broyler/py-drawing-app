import os
from PyQt5.QtCore import QUrl
from PyQt5.QtWidgets import QFileDialog
import cv2

import settings
from confirm_dialog import ChangesDialog


class FilesManager:
    def __init__(self, m_window, canvas_mgr):
        self._m_window = m_window
        self._canvas_mgr = canvas_mgr
        self.saved = True
        self.file_path = None

    def init(self):
        self.update_title()
        self._m_window.actionSave.triggered.connect(lambda _: self._save())
        self._m_window.actionSave_as.triggered.connect(lambda _: self.save_as())
        self._m_window.actionNew.triggered.connect(lambda _: self.new_file())
        self._m_window.actionOpen.triggered.connect(lambda _: self.open_file())

    def updated(self):
        if self.saved:
            self.saved = False
            self.update_title()

    @property
    def file_name(self):
        if not self.file_path:
            return 'new file'
        return os.path.normpath(self.file_path).split(os.path.sep)[-1]

    def update_title(self):
        self._m_window.setWindowTitle(f"{self.file_name}{'' if self.saved else '*'} - Python drawing")

    def save_img(self):
        arr = self._canvas_mgr.to_arr()
        new_w = int(settings.scale_factor * arr.shape[1])
        new_h = int(settings.scale_factor * arr.shape[0])
        im = cv2.resize(
            arr,
            (new_w, new_h),
            interpolation=cv2.INTER_NEAREST
        )
        cv2.imwrite(str(self.file_path), im)
        self.saved = True
        self.update_title()

    def ready_destructive(self):
        if not self.saved:
            dlg = ChangesDialog()
            dlg.exec_()
            clicked = dlg.clickedButton()

            if clicked == dlg.save_btn:
                if not self._save():
                    return False
                
            elif clicked == dlg.cancel_btn:
                return False
        return True

    def open_file(self):
        if not self.ready_destructive():
            return

        pref_path = self.file_path or '.'
        file_url, _ = QFileDialog.getOpenFileUrl(
            self._m_window,
            "Select File",
            QUrl.fromLocalFile(pref_path),
            "Images (*.png *.jpg *.jpeg);;All Files (*)"
        )
        
        if file_url.isValid():
            self.file_path = file_url.toLocalFile()
            loaded_im = cv2.imread(self.file_path, cv2.IMREAD_UNCHANGED)
            if loaded_im is None:
                return

            if loaded_im.ndim == 2:
                loaded_im = cv2.cvtColor(loaded_im, cv2.COLOR_GRAY2BGRA)

            elif loaded_im.shape[2] == 3:
                loaded_im = cv2.cvtColor(loaded_im, cv2.COLOR_BGR2BGRA)

            arr = self._canvas_mgr.to_arr()
            size = (arr.shape[1], arr.shape[0])
            scaled_im = cv2.resize(loaded_im, size, interpolation=cv2.INTER_AREA)
            arr[:, :, :] = scaled_im[:, :, :]

        self.saved = True
        self.update_title()
        self._canvas_mgr.refresh()

    def handle_close(self, event):
        if not self.ready_destructive():
            event.ignore()
            return
        event.accept()

    def new_file(self):
        if not self.ready_destructive():
            return

        arr = self._canvas_mgr.to_arr()
        arr[:, :, :] = [255, 255, 255, 255]
        self._canvas_mgr.refresh()
        self.clear_file()

    def clear_file(self):
        self.saved = True
        self.file_path = None
        self.update_title()

    def save_as(self):
        pref_path = self.file_path or '.'
        file_url, flt = QFileDialog.getSaveFileUrl(
            self._m_window, "Save drawing",
            QUrl.fromLocalFile(pref_path),
            "PNG Image (*.png);;JPEG Image (*.jpg);;All Files (*)"
        )
        if file_url.isValid():
            self.file_path = file_url.toLocalFile()
            fpl = self.file_path.lower()
            if flt.startswith("PNG") and not fpl.endswith(".png"):
                self.file_path += '.png'

            if flt.startswith("JPEG") and not (fpl.endswith(".jpg") or fpl.endswith(".jpeg")):
                self.file_path += '.jpg'

            self.save_img()
            return True
        return False

    def _save(self):
        if self.file_path:
            self.save_img()
            return True

        return self.save_as()

