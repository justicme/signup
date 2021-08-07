import sys

from PyQt5.QtWidgets import QDialog, QApplication
from qtpy import QtWidgets, QtCore


class Ui_Dialog(object)  :
    def setupUi(self , Dialog):
        Dialog . setObjectName ("Dialog")
        Dialog . resize(440,353)
        self . gridLayout = QtWidgets . QGridLayout (Dialog)
        self . gridLayout . setObjectName("gridLayout")
        self . verticalLayout = QtWidgets . QVBoxLayout()
        self . verticalLayout . setObjectName("verticalLayout")
        self . tableWidget = QtWidgets.QTableWidget(Dialog)
        self . tableWidget . setMinimumSize(QtCore.QSize(0,0))
        self . tableWidget . setObjectName( "tableWidget" )
        self . tableWidget . setColumnCount(5)
        self . tableWidget . setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self . tableWidget . setHorizontalHeaderItem(0 , item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(4, item)
        self . verticalLayout . addWidget(self . tableWidget)
        self . horizontalLayout = QtWidgets . QHBoxLayout()
        self . horizontalLayout . setObjectName("horizontalLayout")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.pushButton = QtWidgets.QPushButton(Dialog)
        self.pushButton.setObjectName("pushButton")
        self.horizontalLayout.addWidget(self.pushButton)
        spacerItem1 = QtWidgets . QSpacerItem( 40 , 20 , QtWidgets . QSizePolicy . Expanding , QtWidgets . QSizePolicy.Minimum)
        self . horizontalLayout . addItem(spacerItem1)
        self . pushButton_2 = QtWidgets . QPushButton (Dialog)
        self . pushButton_2 . setObjectName("pushButton_2")
        self . horizontalLayout . addWidget(self . pushButton_2)
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self . horizontalLayout . addItem ( spacerItem2 )
        self . verticalLayout . addLayout( self . horizontalLayout )
        self . gridLayout . addLayout( self . verticalLayout , 0 , 0 , 1 , 1)

        self . retranslateUi (Dialog)
        QtCore . QMetaObject . connectSlotsByName( Dialog )

    def retranslateUi ( self , Dialog )  :

        _translate = QtCore . QCoreApplication . translate
        Dialog . setWindowTitle(_translate("Dialog" , "Dialog"))
        item = self . tableWidget . horizontalHeaderItem( 0 )
        item . setText(_translate("Dialog" , "姓名"))
        item = self.tableWidget.horizontalHeaderItem(1)
        item.setText(_translate("Dialog", "班级"))
        item = self.tableWidget.horizontalHeaderItem(2)
        item.setText(_translate("Dialog", "学号"))
        item = self.tableWidget.horizontalHeaderItem(3)
        item.setText(_translate("Dialog", "签到时间"))
        item = self.tableWidget.horizontalHeaderItem(4)
        item.setText(_translate("Dialog", "签到地点"))
        self . pushButton . setText(_translate("Dialog" , "导出"))
        self . pushButton_2 . setText(_translate("Dialog" , "取消"))

# class window ( QDialog , Ui_Dialog ) :
#
#     # detect_data_signal = pyqtSignal(bytes)
#
#     def __init__(self, group_id_list = ['class1'] , parent=None):
#         super(window,self).__init__(parent)
#         self.setupUi(self)
#
# if __name__ == '__main__':
#     app = QApplication(sys.argv)
#     ui=window()
#     ui.show()
#     sys.exit(app.exec_())


