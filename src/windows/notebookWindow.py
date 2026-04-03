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

        self.date_weight = self.formatDateWeightDict()
        
        self.setupUi(self)
        self.initUI()
        self.initElements()

        self.show()
        
    def formatDateWeightDict(self) -> dict:
        """Формирование сортированого словаря с датами и весами"""
        
        date_weight = dict()
        
        for data in self.account["dates"].items():
            date_weight[data[0]] = data[1]["weight"]
            
        return dict(sorted(date_weight.items()))
    
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
        self.tableNotebook.setRowCount(len(self.account['dates']))

        for index, element in enumerate(self.date_weight.items()):
            
            item_data = QTableWidgetItem(str(element[0]))
            item_weight = QTableWidgetItem(str(element[1]))
            self.tableNotebook.setItem(index, 0, item_data)
            self.tableNotebook.setItem(index, 1, item_weight)
            
