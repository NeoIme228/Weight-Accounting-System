import socket
import time

PORT = 12345
BUFFER_SIZE = 4096

class Server:
    """Класс сервера"""

    def __init__(self):
        
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server.bind(('0.0.0.0', PORT))
        self.server.listen(1)

    def receive_all(self, conn: socket.socket) -> str:
        """Читает все данные из сокета до его закрытия"""
        chunks = list()

        while True:
            chunk = conn.recv(BUFFER_SIZE)
            if not chunk:
                break
            chunks.append(chunk)
        return b''.join(chunks).decode('utf-8')


    def get_android_ip(self, my_data: str) -> str:
        """Получение данных с телефона"""

        connection, client_adress = self.server.accept()
        
        try:

            data = self.receive_all(connection)

            connection.sendall(my_data.replace("'", '"').encode('utf-8'))
            print(data)
            if data:
                print(data)
                return data
            return ""

        finally:
            connection.close()
            self.server.close()
