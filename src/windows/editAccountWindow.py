from windows.addAccountWindow import AddAccountWindow

class EditAccountWindow(AddAccountWindow):
    """Окно изменения имени аккаунта"""

    def __init__(self):
        super().__init__()

        self.updateBtnCreateToEdit()

    def updateBtnCreateToEdit(self):
        """Обновляет кнопку создания аккаунта на кнопку редактирования"""

        self.btnAddAccount.setText("Изменить")

