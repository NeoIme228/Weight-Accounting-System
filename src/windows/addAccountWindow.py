from PyQt5.QtWidgets import QDialog

from generated.addAccountWindow import Ui_AddAccountWindow

class AddAccountWindow(QDialog, Ui_AddAccountWindow):
    """Окно добавления аккаунта"""

    def __init__(self):
        super().__init__()

        self.setupUi(self)
        self.setupSignals()
        self.show()

    def setupSignals(self):
        """Обработка всех сигналов"""   

        self.btnCancel.clicked.connect(self.close)
        self.btnAddAccount.clicked.connect(self.close_window)
        self.editNameAccount.returnPressed.connect(self.close_window)

    def close_window(self):
        """Закрыть окно при положительном результате"""

        if not (self.editNameAccount.text()).isdigit(): 
            if self.editNameAccount.text() != "":
                self.accept()
            else: 
                self.labelError.setText("Имя не может быть пустое")
        else:
            self.labelError.setText("Имя не может быть числом")
            
    def get_name_account(self) -> str:
        """Возвращает имя аккаунта"""

        return self.editNameAccount.text()

