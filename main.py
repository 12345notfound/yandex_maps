import os

import mainwindow
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QShortcut, QMessageBox
import PyQt5.QtGui
import requests


class MainWindow(QMainWindow, mainwindow.Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setup()

    def setup(self):
        self.search_button.clicked.connect(self.search)

    def search(self):
        try:
            latitude = float(self.latitude_input.text())
            longitude = float(self.longitude_input.text())
            scale = float(self.scale_input.text())
            response = requests.get(f'https://static-maps.yandex.ru/1.x/?ll={latitude},{longitude}&spn={scale},{scale}&l=map')
            if not response:
                messagebox = QMessageBox(text=f"Http статус:{response.status_code}({response.reason})\n{response.url}")
                print(response.url)
                messagebox.setWindowTitle('Ошибка выполнения запроса')
                messagebox.setIcon(QMessageBox.Warning)
                messagebox.exec()
            else:
                map_file = 'map.png'
                with open(map_file, "wb") as file:
                    file.write(response.content)
                self.label.setPixmap(PyQt5.QtGui.QPixmap("map.png"))
                self.label.setScaledContents(True)

        except ValueError:
            messagebox = QMessageBox(text='Координаты или масштаб введены в неверном формате')
            messagebox.setWindowTitle('Ошибка')
            messagebox.setIcon(QMessageBox.Warning)
            messagebox.exec()


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.excepthook = except_hook
    sys.exit(app.exec())