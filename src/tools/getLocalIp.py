import socket

from exceptions.netConnectError import NetConnectError

def get_local_ip() -> str:
    """Получение локальный ip сети LAN ввиде строки"""

    local_ip = ''

    try:
        server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        server.connect(("8.8.8.8", 80))
        local_ip = server.getsockname()[0]

    except OSError:
        raise NetConnectError("Отстувует подключение к сети")

    finally:    
        server.close()

    return local_ip