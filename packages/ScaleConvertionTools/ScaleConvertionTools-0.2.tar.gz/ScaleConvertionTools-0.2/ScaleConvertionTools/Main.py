# -*- coding: utf-8 -*-
# @Time    : 2024/3/5 14:02
# @Author  : qxcnwu
# @FileName: Main.py
# @Software: PyCharm
import sys

sys.path.append("../")

from PyQt5.QtWidgets import QMainWindow
from qtpy import QtWidgets

# 导入pyUIC转化出来的.py文件,Ui_Form就是转化出的.py文件的类名
from CommonObject.InputObject import InputObject
from Form import MainWindow
from Form.WindowEvent import EventInit


class Ui(QMainWindow, MainWindow.Ui_MainWindow):
    def __init__(self, parent=None):
        super(Ui, self).__init__(parent)
        self.setupUi(self)
        self.inObj = InputObject()
        self.EventInit = EventInit(self, self.inObj)


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = Ui()
    window.show()
    sys.exit(app.exec_())
