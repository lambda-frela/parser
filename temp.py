'''
from PyQt5.QtWidgets import (QWidget, QPushButton, QLineEdit,
                             QApplication, QLabel, QTextEdit,
                             QGridLayout, QListWidget, QComboBox,
                             QMainWindow, QMessageBox)
from PyQt5.QtGui import QPixmap
import sys
class Example(QWidget):

    def __init__(self):
        super().__init__()

        self.initUI()


    def initUI(self):

        self.setGeometry(300, 300, 250, 150)
        self.setWindowTitle('Message box')
        self.show()
        self.msgbox = QMessageBox()
        self.msgbox.setIconPixmap(QPixmap('www.png'))
        self.msgbox.setInformativeText('Проверьте подключение к интернету')
        self.msgbox.addButton('Попробовать снова', QMessageBox.DestructiveRole)
        self.show()
        self.msgbox.show()

if __name__ == '__main__':

    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())
'''
import backend
import sys
import requests
try:
    backend.livelib.get_books_list()
except requests.exceptions.ConnectionError as er:
    print('lol')
