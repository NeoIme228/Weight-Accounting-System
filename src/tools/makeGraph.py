from matplotlib import pyplot as plt
import io

from PyQt5.QtGui import QImage

def make_graph(name_account: str, listDates: list, listWeight: list) -> QImage:
    """ Создаёт график и переделывает его в QImage"""

    listWeight = list(map(float, listWeight))

    plt.plot(listDates, listWeight, marker='o', markersize=5)
    plt.title(f'График учёта "{name_account}"')
    plt.xlabel("Дата")
    plt.ylabel("Вес")

    with io.BytesIO() as buffer:

        plt.savefig(buffer, format='png')
        buffer.seek(0)

        data = buffer.read()

    plt.close('all')
    return QImage.fromData(data)

