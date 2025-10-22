import socket
import time

PORT = 12345

class Server:
    """Класс сервера"""

    def __init__(self):
        
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server.bind(('0.0.0.0', PORT))
        self.server.listen(1)

    def get_android_ip(self, my_data: str) -> str:
        """Получение ip с телефона"""

        connection, client_adress = self.server.accept()
        
        try:
            data = connection.recv(1024).decode().strip()
            time.sleep(0.1)
            connection.sendall(my_data.replace("'", '"').encode())

            if data:
                return data

        finally:
            connection.close()
            self.server.close()
