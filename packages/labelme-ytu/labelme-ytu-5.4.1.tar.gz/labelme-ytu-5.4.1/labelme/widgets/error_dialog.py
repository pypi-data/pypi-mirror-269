from qtpy import QtWidgets

class ErrorDialog(QtWidgets.QMessageBox):
    def __init__(self, msg = "", parent = None):
        super(ErrorDialog, self).__init__(parent)
        self.setText(msg)

    def show(self):
        self.exec()