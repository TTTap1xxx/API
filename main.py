import os
import sys
import requests
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QWidget, QLabel
from PyQt5.QtCore import Qt


class API(QWidget):
    def __init__(self):
        super().__init__()
        self.size = 0.0054931640625
        self.ll = [37.530887, 55.70311]
        self.resolution = [600, 450]
        self.map_file = self.getImage()
        self.offset_width = int(self.screen().size().width() / 2 - self.resolution[0] / 2 + 0.5)
        self.offset_height = int(self.screen().size().height() / 2 - self.resolution[1] / 2 + 0.5)
        self.setGeometry(self.offset_width, self.offset_height, *[600, 450])
        self.setWindowTitle('Отображение карты')
        self.pixmap = QPixmap()
        self.pixmap.loadFromData(self.map_file)
        self.image = QLabel(self)
        self.image.move(0, 0)
        self.image.resize(600, 450)
        self.image.setPixmap(self.pixmap)

    def getImage(self):
        """
        Возвращает png карты в байтах по запросу к yandex API с установленными переменными size и ll
        """
        map_request = f"http://static-maps.yandex.ru/1.x/?ll={self.ll[0]},{self.ll[1]}&spn={self.size},0.002&l=map"
        response = requests.get(map_request)

        if not response:
            print(f'Http статус: {response.status_code} ({response.reason})')
        else:
            print(f'Map Downloaded: size = {self.size}, ll = {self.ll}')

        return response.content

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_PageDown and self.size > 0.0054931640625:
            self.size /= 2
        elif event.key() == Qt.Key_PageUp and self.size < 180:
            self.size *= 2

        elif event.key() == Qt.Key_Up:
            self.ll[1] += 1 * self.size / 4
            if self.ll[1] > 85:
                self.ll[1] = 85
        elif event.key() == Qt.Key_Left:
            self.ll[0] -= 1 * self.size / 2
            if self.ll[0] < -180:
                self.ll[0] = -179.99
        elif event.key() == Qt.Key_Down:
            self.ll[1] -= 1 * self.size / 4
            if self.ll[1] < -85:
                self.ll[1] = -85
        elif event.key() == Qt.Key_Right:
            self.ll[0] += 1 * self.size / 2
            if self.ll[0] >= 180:
                self.ll[0] = 179.99

        self.map_file = self.getImage()
        self.pixmap.loadFromData(self.map_file)
        self.image.setPixmap(self.pixmap)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = API()
    ex.show()
    sys.exit(app.exec())
