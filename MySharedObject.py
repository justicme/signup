from PyQt5.QtCore import  QObject
from PyQt5.QtCore import pyqtProperty
from PyQt5.QtWidgets import QWidget,QMessageBox

class MySharedObject(QWidget):
    def __init__(self,strval = '106.2936\n29.600466320785827'):
        super(MySharedObject,self).__init__()
        self.strval = strval
        # self.lng = ""
        # self.lat = ""
    def _getStrValue(self):
        return self.strval
    def _setStrValue(self,str):
        self.strval = str
        print('获得页面参数：%s'% str)
        # QMessageBox.information(self,"Infomation", '获得的页面参数%s' % str)
    def getCoordinates(self,lon,lat):
        print("在执行了")
        print(lon)
        print(lat)

    #需要定义的对外发布的方法
    strValue= pyqtProperty(str,_getStrValue,_setStrValue)