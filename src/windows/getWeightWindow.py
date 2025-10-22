from PyQt5.QtWidgets import QDialog
from PyQt5.QtCore import QDate 

from generated.getWeightWindow import Ui_GetWeightWindow

class GetWeightWindow(QDialog, Ui_GetWeightWindow):
    """Окно получения веса"""

    def __init__(self):
        super().__init__()

        self.setupUi(self)
        self.initUI()
        self.setupSignals()
        self.show()

    def initUI(self):
        """Инициализация UI"""

        self.getDate.setDate(QDate.currentDate())
        self.getDate.setMaximumDate(QDate.currentDate())

    def setupSignals(self):
        """Обработка всех сигналов"""   

        self.btnYesNo.accepted.connect(self.close_window)
        self.btnYesNo.rejected.connect(self.close)

    def close_window(self):
        """Закрыть окно при положительном результате"""
        
        if float(self.editWeight.value()) and self.getDate.date():
            self.accept()

    def get_weight(self) -> str:
        """Возвращает вес"""

        return str(self.editWeight.value())
        
    def get_date(self) -> str:
        """Возвращает дату"""

        return self.getDate.date().toString("yyyy-MM-dd")