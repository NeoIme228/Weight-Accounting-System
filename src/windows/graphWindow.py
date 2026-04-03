from pyqtgraph import PlotWidget
import pyqtgraph as pg 

class GraphWindow(PlotWidget):
    """Класс окна с графиком статистики"""

    def __init__(self, name_account: str, listDates: list, listWeight: list):
        super().__init__()
        
        self.name_account = name_account
        self.listDates = listDates
        self.listWeight = listWeight
        
        self.data_weight = self.formatDataWeightDict()
        
        self.initGraph()
    
    def formatDataWeightDict(self) -> dict:
        """Формирование словаря с датами и весами"""
        
        data_weight = dict()
        
        for index in range(len(self.listDates)):
            data_weight[self.listDates[index]] = self.listWeight[index]
            
        return dict(sorted(data_weight.items()))
        
    def initGraph(self):
        """Инициализация графика"""
        
        self.setWindowTitle(f"График: {self.name_account}")
        self.setBackground("white")
        
        # Необходимо для подстановки дат в абсциссу
        dates_indexes = list(range(len(self.listDates)))
          
        self.plot(dates_indexes, 
                  list(self.data_weight.values()), 
                  symbol='o',
                  symbolBrush="#dede3cff",
                  pen=pg.mkPen(color='#ffff7fff', width=4), 
                  antialias=True
            )
        
        x_axis = self.getAxis('bottom')
        x_axis.setTicks(
            [
                list(
                    zip(
                        dates_indexes, 
                        list(self.data_weight.keys())
                    )
                )
            ]
        )
        
        self.show()

