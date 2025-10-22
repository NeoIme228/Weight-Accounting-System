from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt 

from tools.makeGraph import make_graph

# Чтобы бы подходящий для графика размер
MAX_WIDTH = 0
MAX_HEIGHT = 0

class GraphWindow(QWidget):
    """Класс окна с графиком статистики"""

    def __init__(self, name_account: str, listDates: list, listWeight: list):
        super().__init__()

        self.name_account = name_account
        self.listDates = listDates
        self.listWeight = listWeight

        self.initUI()

    def initUI(self):
        """Инициализация UI"""

        self.setWindowTitle(" ")
        self.setMaximumSize(MAX_WIDTH, MAX_HEIGHT)

        self.move(100, 100)
        
        graphPixmap = QPixmap.fromImage(make_graph(self.name_account, self.listDates, self.listWeight))

        graph = QLabel()
        graph.setScaledContents(True)
        graph.setPixmap(graphPixmap)

        self.setupLayout([graph,])

        self.show()

    def setupLayout(self, widgets: list):
        """Устанавливает все нужные элементы в Layout"""

        layout = QVBoxLayout()
        
        for widget in widgets:
            layout.addWidget(widget, stretch=1)

        self.setLayout(layout)