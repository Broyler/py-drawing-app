from PyQt5.QtWidgets import QDialog, QDialogButtonBox, QLabel, QMessageBox, QVBoxLayout


class ConfirmDialog(QDialog):
    def __init__(self, details, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Confirm action")

        QBtn = QDialogButtonBox.Ok | QDialogButtonBox.Cancel
        self.buttonBox = QDialogButtonBox(QBtn)

        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        layout = QVBoxLayout()
        message = QLabel(details)
        layout.addWidget(message)
        layout.addWidget(self.buttonBox)
        self.setLayout(layout)


class ChangesDialog(QMessageBox):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Save changes?")
        self.setText("Do you want to save changes to your drawing?")
        self.setIcon(QMessageBox.Warning)

        self.save_btn = self.addButton("Save", QMessageBox.AcceptRole)
        self.dont_save_btn = self.addButton("Don't Save", QMessageBox.DestructiveRole)
        self.cancel_btn = self.addButton("Cancel", QMessageBox.RejectRole)

        self.setDefaultButton(self.save_btn)

