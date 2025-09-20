import os
from PyQt5.QtCore import QUrl
from PyQt5.QtWidgets import QFileDialog
import cv2

import settings


class FilesManager:
    def __init__(self, m_window, canvas_mgr):
        self._m_window = m_window
        self._canvas_mgr = canvas_mgr
        self.saved = True
        self.file_path = None

    def init(self):
        self.update_title()
        self._m_window.actionSave.triggered.connect(lambda _: self._save())

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

    def _save(self):
        if self.file_path:
            return self.save_img()

        file_url, _ = QFileDialog.getSaveFileUrl(
            None, "Save drawing",
            QUrl.fromLocalFile('.'),
            None
        )
        if file_url.isValid():
            self.file_path = file_url.toLocalFile()
            self.save_img()

