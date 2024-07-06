from PyQt5.QtCore import pyqtSignal, QObject
from PyQt5.QtWidgets import QMessageBox
import parametros as p
import utils

class StartUpBackend(QObject):

    signal_start_game = pyqtSignal()

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

    def validate_name(self, name: str):
        if (p.MIN_CARACTERES <= len(name) <= p.MAX_CARACTERES) and name.isalnum():
            self.signal_start_game.emit()
        else:
            msg = QMessageBox()
            msg.setWindowTitle('Error')
            msg.setText('Nombre invalido')
            msg.setIcon(QMessageBox.Critical)
            msg.setInformativeText(f"El nombre debe tener entre {p.MIN_CARACTERES} y {p.MAX_CARACTERES} caracteres alfanumericos.")
            msg.setStandardButtons(QMessageBox.Abort)
            msg.setDefaultButton(QMessageBox.Abort)
            msg.setDetailedText(utils.error_msg(name=name))
            msg.exec()
    