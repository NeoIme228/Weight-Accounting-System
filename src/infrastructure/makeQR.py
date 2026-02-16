import socket
import io
import segno

from PyQt5.QtGui import QImage

def make_QR(ip: str) -> QImage:
    """Создаёт QR и переделывает его в QImage"""

    qr = segno.make(ip, version=4)
        
    with io.BytesIO() as buffer:
        
        qr.save(buffer, kind='png', scale=10)
        buffer.seek(0)

        data = buffer.read()

    return QImage.fromData(data)


