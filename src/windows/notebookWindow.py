from PyQt5.QtWidgets import QWidget, QTableWidgetItem, QHeaderView

from generated.notebookWindow import Ui_NotebookWindow

class NotebookWindow(QWidget, Ui_NotebookWindow):
    """Окно журнала"""

    def __init__(self, account: dict["name": str, "dates": dict["weight": int, "weather": str]]):
        super().__init__()

        self.account = account

        self.setupUi(self)
        self.initUI()
        self.initElements()

        self.show()
        
    def initUI(self):
        """Инициализация UI"""
        
        header = self.tableNotebook.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.Stretch)

        
    def initElements(self):
        """Инициализация элементов журнала"""

        self.setWindowTitle(f"Статистика: {self.account['name']}")
        self.tableNotebook.setRowCount(len(self.account) + 1)

        for index_date, data in enumerate(self.account["dates"].items()):
            for index_item, element in enumerate([data[0], data[1]["weight"], data[1]["weather"]]):
                
                item = QTableWidgetItem(str(element))
                self.tableNotebook.setItem(index_date, index_item, item)
            