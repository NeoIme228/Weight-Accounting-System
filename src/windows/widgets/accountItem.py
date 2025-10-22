from PyQt5.QtWidgets import QWidget, QDialog, QMessageBox
from PyQt5.QtCore import Qt, pyqtSignal

from infrastructure.json_base.jsonTools import JsonTools

from generated.nameCardWidget import Ui_NameCardWidget

from windows.editAccountWindow import EditAccountWindow

class AccountItem(QWidget, Ui_NameCardWidget):
    """Виджет для управления учётом"""

    signalClose = pyqtSignal()
    signalUpdate = pyqtSignal()

    def __init__(self, 
                 account_id: str,
                 jtools: JsonTools,
                 parent: QWidget = None,):
        
        super().__init__(parent)

        self.jtools = jtools
        self.account_id = account_id
        self.account_name = self.jtools.get_account_name(self.account_id)

        self.setupUi(self)
        self.setupSignals()
        self.initUI()

    def initUI(self):
        """Инициализация UI"""

        self.accountName.setText(self.account_name)

    def setupSignals(self):
        """Обработка всех сигналов"""

        self.accountName.mouseReleaseEvent = lambda event: self.choose_account(event)
        self.btnEdit.clicked.connect(self.edit_account)
        self.btnDel.clicked.connect(self.del_account)

    def choose_account(self, event):
        """Выбор учёта"""

        if event.button() == Qt.LeftButton:
            self.jtools.set_current_account_id(self.account_id)
            self.jtools.jbase._save()
            self.signalClose.emit()

    def edit_account(self):
        """Изменить имя учёта"""

        self.editAccountWindow = EditAccountWindow()

        result = self.editAccountWindow.exec_()

        if result == QDialog.Accepted:
            new_name = self.editAccountWindow.get_name_account()

            self.jtools.edit_account_name(self.account_id, new_name)
            self.jtools.jbase._save()
            self.signalUpdate.emit()

    def del_account(self):
        """Удаление учёта"""

        reply = QMessageBox.question(self, 
                                    "Подтверждение", 
                                    "Вы уверены?", 
                                    QMessageBox.Yes | QMessageBox.No)

        if reply == QMessageBox.Yes:
            if self.jtools.del_account(self.account_id):
                self.jtools.jbase._save()
                if self.jtools.get_accounts():
                    self.signalUpdate.emit()
                else:
                    self.signalClose.emit()
                
