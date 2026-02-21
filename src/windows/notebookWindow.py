from PyQt5.QtWidgets import (QApplication, QWidget, QTableWidgetItem, 
                             QHeaderView, QAction)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QKeySequence

from generated.notebookWindow import Ui_NotebookWindow

class NotebookWindow(QWidget, Ui_NotebookWindow):
    """Окно журнала"""

    def __init__(self, account: dict["name": str, "dates": dict["weight": int]]):
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
        
        self.tableNotebook.setFocusPolicy(Qt.NoFocus)
        
        self.tableNotebook.setContextMenuPolicy(Qt.ActionsContextMenu)
        
        copy_action = QAction("Копировать", self)
        copy_action.setShortcut(QKeySequence.Copy)
        copy_action.triggered.connect(self.copy_selection_to_clipboard)
        
        self.tableNotebook.addAction(copy_action)
        
    def copy_selection_to_clipboard(self):
        """Копирование выделенных ячеек в буфер"""
        
        selection = self.tableNotebook.selectedRanges()
                
        if not selection:
            return

        rows = []
        for r in selection:
            for row in range(r.topRow(), r.bottomRow() + 1):
                row_data = []
                for column in range(r.leftColumn(), r.rightColumn() + 1):                
                    item = self.tableNotebook.item(row, column)
                    text = item.text() if item else ""
                    row_data.append(text)
                rows.append("\t".join(row_data))

        clipboard_text = "\n".join(rows)
        clipboard = QApplication.clipboard()
        clipboard.setText(clipboard_text)
        
    def initElements(self):
        """Инициализация элементов журнала"""

        self.setWindowTitle(f"Статистика: {self.account['name']}")
        self.tableNotebook.setRowCount(len(self.account) + 1)

        for index_date, data in enumerate(self.account["dates"].items()):
            for index_item, element in enumerate([data[0], data[1]["weight"], data[1]["weather"]]):
                
                item = QTableWidgetItem(str(element))
                self.tableNotebook.setItem(index_date, index_item, item)
            