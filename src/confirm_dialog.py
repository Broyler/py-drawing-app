from PyQt5.QtWidgets import QDialog, QDialogButtonBox, QLabel, QVBoxLayout


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

