# Импрот основных модулей
import sys

from PyQt5.QtWidgets import QApplication

from windows.mainWindow import MainWindow

# Точка входа приложения
if __name__ == "__main__":
    
    app = QApplication(sys.argv) # Экземпляр приложения
    window = MainWindow() # Экземпляр гланого окна
    sys.exit(app.exec_()) # Запуск приложения
