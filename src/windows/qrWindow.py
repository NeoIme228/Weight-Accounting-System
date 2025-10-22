from PyQt5.QtWidgets import QWidget, QLabel
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt 

from tools.getLocalIp import get_local_ip
from tools.makeQR import make_QR

WIDTH_QR = HEIGHT_QR = 400

class QrWindow(QWidget):
    """Класс окна с qr-кодом"""
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        """Инициализация UI"""

        self.setWindowTitle(" ")

        self.setFixedSize(WIDTH_QR, HEIGHT_QR)
        self.move(100, 100)

        qrPixmap = QPixmap.fromImage(make_QR(get_local_ip()))

        if qrPixmap.width() > WIDTH_QR and qrPixmap.height() > HEIGHT_QR:
            qrPixmap.scaled(WIDTH_QR, HEIGHT_QR, aspectRatioMode=Qt.KeepAspectRatio)

        qr = QLabel(self)
        qr.setPixmap(qrPixmap)

        self.show()
