from datetime import datetime
import sys
from threading import Thread

from PyQt5.QtWidgets import QMainWindow, QDialog, QMessageBox, QFileDialog
from PyQt5.QtCore import Qt, QTimer 

from exceptions.jsonFormatError import JsonFormatError
from exceptions.missingDatesError import MissingDatesError
from exceptions.netConnectError import NetConnectError

from infrastructure.json_base.jsonTools import JsonTools
from infrastructure.server import Server

from tools.exportToExcel import export_to_excel

from generated.mainWindow import Ui_MainWindow

from windows.qrWindow import QrWindow
from windows.getWeightWindow import GetWeightWindow
from windows.addAccountWindow import AddAccountWindow
from windows.accountsListWindow import AccountsListWindow
from windows.graphWindow import GraphWindow
from windows.notebookWindow import NotebookWindow

class MainWindow(QMainWindow, Ui_MainWindow):
    """Главное окно"""

    def __init__(self):
        super().__init__()

        self.initTimer()
        self.initData() 

        self.setupUi(self)
        self.setupSignals()

        self.updateLabels()

        self.show()

    def initData(self):
        """ Загрузка основных данных и классов"""

        try:

            self.jtools = JsonTools()
            self.server_thread = None
            self.is_server_running = False

        except JsonFormatError:
            QMessageBox.critical(self, "Ошибка", "Файл json некорректного формата!")
            
            response = QMessageBox.question(self, "Что дальше?", 
                """Хотите попытаться сново открыть json?
Если вы не можете исправить json, то удалите его, мы создадим новый!""",
                QMessageBox.Yes | QMessageBox.No)
            
            if response == QMessageBox.Yes:
                 self.initData()
            else:
                sys.exit()    

    def updateLabels(self):
        """Обновление всех Labels"""

        self.labelList.setText(self.jtools.get_account_name(self.jtools.get_current_account_id()))
        self.date.setText(str(datetime.now().date()))
        self.weight.setText(str(self.jtools.get_weight_date(self.jtools.get_current_account_id(), 
                                                            str(datetime.now().date()))))

    def initTimer(self):
        """Инициализация таймера"""

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_data)
        self.timer.start(1000)

    def setupSignals(self):
        """Обработка всех сигналов"""

        self.weight.mouseReleaseEvent = lambda event: self.onLabelClicked(event, 
                                                                            self.view_window_add_weight)
        self.btnNewAccounting.clicked.connect(self.add_account_window)
        self.btnList.clicked.connect(self.accounts_list_window)
        self.btnGraph.clicked.connect(self.graph_window)
        self.btnExport.clicked.connect(self.export_file_window)
        self.btnNotebook.clicked.connect(self.notebook_window)
        self.btnSync.clicked.connect(self.sync_process)
        
    def view_qr_code(self):
        """Вывести qr"""
        try:
            self.qrWindow = QrWindow() # self - обязательно
        except NetConnectError:
            QMessageBox.critical(self, "Ошибка", "Отсутствует подключение к локальной сети!")

    def view_window_add_weight(self):
        """ Вызов окна добавления веса """

        self.getWeightWindow = GetWeightWindow()

        result = self.getWeightWindow.exec_()

        if result == QDialog.Accepted:
            new_weight = self.getWeightWindow.get_weight()
            date = self.getWeightWindow.get_date()

            if self.jtools.set_info_date(self.jtools.get_current_account_id(), date, new_weight):
                    if date == str(datetime.now().date()):
                        self.weight.setText(new_weight)
                    self.jtools.jbase._save()
            else:
                QMessageBox.warning(self, " ", "У вас нету учётов.\nСоздайте с помощью '+'")

    def add_account_window(self):
        """Добавить учётку"""

        self.addAccountWindow = AddAccountWindow()

        result = self.addAccountWindow.exec_()

        if result == QDialog.Accepted:
            name_account = self.addAccountWindow.get_name_account()

            self.jtools.create_account(name_account)
            self.jtools.jbase._save()

            self.updateLabels()

    def accounts_list_window(self):
        """ Список учётов """

        if len(self.jtools.get_accounts()):
            self.accountsListWindow = AccountsListWindow(self.jtools)

            self.accountsListWindow.signalUpdate.connect(self.updateLabels)
        else:
            QMessageBox.information(
                self, 
                "Список учёток", 
                "Список учёток пуст"
            )

    def graph_window(self):
        """Окно с графиком по дням"""

        try:
            self.graphWindow = GraphWindow(self.jtools.get_account_name(self.jtools.get_current_account_id()),
                                  self.jtools.get_dates_account_id(self.jtools.get_current_account_id()),
                                  self.jtools.get_weight_account_id(self.jtools.get_current_account_id()))
        except MissingDatesError:
            QMessageBox.warning(self, " ", "У вас нету данных!")
        
    def export_file_window(self):
        """Окно для экспорта файла"""

        if accounts := self.jtools.get_accounts():
            file_path, select_type_file = QFileDialog.getSaveFileName(
                self, 
                'Экспортировать данные файл',
                '', 
                'Excel файл (*.xlsx)')
            
            if select_type_file == "Excel файл (*.xlsx)":
                file_path += ".xlsx"
                export_to_excel(file_path, accounts)
        else:
            QMessageBox.warning(self, " ", "У вас нету данных!")

    def notebook_window(self):
        """Окно с журналом"""
        
        try:
            self.notebookWindow = NotebookWindow(self.jtools.get_account(self.jtools.get_current_account_id()))
        except TypeError:
            QMessageBox.warning(self, " ", "У вас нету данных!")

    def sync_process(self):
        """Процесс синхронизации"""

        if not self.is_server_running:
            self.view_qr_code()
            
            self.server_thread = Thread(target=self.start_server, daemon=True)
            self.is_server_running = True
            self.server_thread.start()
        else:
            self.view_qr_code()

    def start_server(self):
        """Запуск сервера"""

        self.server = Server()
        data = self.server.get_android_ip(str({
            "accounts": self.jtools.get_accounts(),
                }
            )
        )

        self.jtools.sync_data(data)

        self.is_server_running = False
        self.qrWindow.close()
        self.updateLabels()

    def update_data(self):
        """ Обновление даты """

        if self.date.text() != str(datetime.now().date()):
            self.updateLabels()

    def onLabelClicked(self, event, func):
        """Обработчик клика по QLabel"""

        if event.button() == Qt.LeftButton:
            func()

