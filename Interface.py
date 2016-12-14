import os
import sys
import requests
import backend
from PyQt5.QtWidgets import (QWidget, QPushButton, QLineEdit,
                             QApplication, QLabel, QTextEdit,
                             QGridLayout, QListWidget, QComboBox,
                             QMainWindow, QMessageBox, QDesktopWidget)
from PyQt5.QtGui import QIcon
# Wtf??! мой Qt не робит без переменной окружения,
# установленной непосредственно в словарь пайтона, это странно
# пробуйте закомментить эти строки на своих платформах
path = r'C:\Users\Тимур\AppData\Local\Programs\Python\Python35-32\Lib\site-packages\PyQt5\Qt\plugins\platforms'
os.environ['QT_QPA_PLATFORM_PLUGIN_PATH'] = path


class Window(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):

        self.lineinp = QLineEdit(self)
        self.lineinp.setPlaceholderText("Enter the site's URL here")

        self.boxinp = QComboBox(self)
        self.boxinp.addItems(['LiveLib', 'ReadRate',
                              'Libs', 'Readly'])

        self.prsbtn = QPushButton('Parse!', self)
        self.prsbtn.clicked.connect(self.prsbuttonClicked)

        self.wtfbtn = QPushButton('WTF', self)
        self.wtfbtn.clicked.connect(self.wtfbuttonClicked)

        self.datalist = QListWidget(self)

        self.msgbox = QMessageBox()
        self.msgbtn = QPushButton('Попробовать снова')
        self.msgbox.addButton(self.msgbtn, QMessageBox.DestructiveRole)
        self.msgbox.setWindowTitle('Ой, что-то не так')
        self.msgbox.setWindowIcon(QIcon('sad.png'))
        self.center(self.msgbox)

        grid = QGridLayout()
        grid.addWidget(self.lineinp, 1, 0, 1, 2)
        grid.addWidget(self.boxinp, 2, 0, 1, 2)
        grid.addWidget(self.prsbtn, 3, 0)
        grid.addWidget(self.wtfbtn, 3, 1)
        grid.addWidget(self.datalist, 4, 0, 4, 2)

        self.setLayout(grid)

        self.boxinp.hide()

        self.resize( 600, 600)
        self.center(self)
        self.setWindowTitle('My big fully-functional parser')
        self.setWindowIcon(QIcon('www.png'))
        self.show()

    def center(self, obj):
        qr = obj.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def wtfbuttonClicked(self):
        if self.boxinp.isVisible():
            self.boxinp.hide()
            self.lineinp.show()
        else:
            self.boxinp.show()
            self.lineinp.hide()

    def prsbuttonClicked(self):
        if self.lineinp.isVisible():
            self.setTopByLine()
        else:
            self.setTopByBox()

    def msgbuttonClicked(self):                     #вот эту штуку нужно убрать, слот-метод же есть
        self.prsbtn.setText('Исправил, проверяйте')

    def connection_try(self):
        try:
            data = backend.sites[self.sitename].get_books_list()
        except requests.exceptions.ConnectionError:
            self.msgbox.setText('Ошибка сети')
            self.msgbox.setInformativeText('Проверьте подключение к интернету')
            self.msgbox.show()
        else:
            self.datalist.addItems(data)

    def setTopByBox(self):
        self.datalist.clear()
        self.sitename = self.boxinp.currentText()
        self.connection_try()

    def setTopByLine(self):
        self.datalist.clear()
        sitename = self.datalist.clear()
        if sitename in backend.urls:
            self.connection_try()
        else:
            self.msgbox.setText('Что такое?')
            self.msgbox.setInformativeText('Введите нормальный URL')
            self.msgbtn.clicked.connect(self.msgbuttonClicked)
            self.msgbox.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Window()
    sys.exit(app.exec_())
