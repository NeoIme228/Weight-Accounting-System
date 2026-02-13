from pyqtgraph import PlotWidget
import pyqtgraph as pg 

class GraphWindow(PlotWidget):
    """Класс окна с графиком статистики"""

    def __init__(self, name_account: str, listDates: list, listWeight: list):
        super().__init__()
        
        self.name_account = name_account
        self.listDates = listDates
        self.listWeight = listWeight
        
        self.initGraph()

    def initGraph(self):
        """Инициализация графика"""
        
        self.setWindowTitle(f"График: {self.name_account}")
        self.setBackground("white")
        
        # Необходимо для подстановки дат в абсциссу
        dates_indexes = list(range(len(self.listDates)))  

        self.plot(dates_indexes, 
                  self.listWeight, 
                  symbol='o',
                  pen=pg.mkPen('b', width=2), 
                  antialias=True
            )
        
        x_axis = self.getAxis('bottom')
        x_axis.setTicks([list(zip(dates_indexes, self.listDates))])
        
        self.show()

