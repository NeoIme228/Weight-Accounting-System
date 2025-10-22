from PyQt5.QtWidgets import QWidget, QListWidget, QListWidgetItem
from PyQt5.QtCore import QSize, pyqtSignal

from windows.widgets.accountItem import AccountItem
from infrastructure.json_base.jsonTools import JsonTools

WEDTH_WINDOW = 400
HEIGHT_WINDOW = 600

class AccountsListWindow(QWidget):
    """Окно списка учёток"""

    signalUpdate = pyqtSignal()

    def __init__(self, 
                 jTools: JsonTools):
        super().__init__()

        self.jtools = jTools

        self.initUI()

    def initUI(self):
        """Инициализация UI"""

        self.setWindowTitle("Список учёток")
        self.setFixedSize(WEDTH_WINDOW, HEIGHT_WINDOW)

        self.accountsList = QListWidget(self)
        self.accountsList.setGeometry(0, 0, WEDTH_WINDOW, HEIGHT_WINDOW)

        self.setupList()

        self.show()

    def update_list(self):
        """ Обновление списка """

        self.accountsList.clear()

        self.setupList()

        self.signalUpdate.emit()

    def setupList(self):
        """ Устанивливает список """

        for account_id in self.jtools.get_accounts().keys():
            accountItem = AccountItem(account_id, self.jtools)

            accountItem.signalClose.connect(self.close_window)
            accountItem.signalUpdate.connect(self.update_list)

            item = QListWidgetItem()
            item.setSizeHint(QSize(400, 100))

            self.accountsList.addItem(item)
            self.accountsList.setItemWidget(item, accountItem)

    def close_window(self):
        """Закрытие окна"""
        
        self.signalUpdate.emit()
        self.close()
        