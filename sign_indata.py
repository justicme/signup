import sqlite3
import sys

from PyQt5.QtWidgets import QAbstractItemView, QDialog, QTableWidgetItem, QFileDialog, QApplication

from Ui_Dialog import Ui_Dialog


class sign_data(Ui_Dialog , QDialog )  :
    def __init__ (self , parent = None )  :
        super ( sign_data , self ) . __init__ ( parent )
        self . setupUi ( self )
        con = sqlite3.connect(r"f:\\pyqtui\\signin_data.db")

        c = con.cursor()

        signdata = c . execute ( "select * from signinhis" )
        self . signdata = signdata
        self . tableWidget . setEditTriggers ( QAbstractItemView . NoEditTriggers )
        for i in self . signdata  :

            rowcount = self . tableWidget . rowCount ()
            self . tableWidget . insertRow ( rowcount )
            self . tableWidget . setItem ( rowcount , 0 , QTableWidgetItem( i [ 0 ] ))
            self . tableWidget . setItem( rowcount , 1 , QTableWidgetItem( i [ 1 ] ))
            self.tableWidget.setItem(rowcount, 2, QTableWidgetItem( i [ 2 ] ))
            self.tableWidget.setItem(rowcount, 3, QTableWidgetItem( i [ 3 ] ))
            self.tableWidget.setItem(rowcount, 4, QTableWidgetItem( i [ 4 ] ))

        self . pushButton . clicked . connect ( self . save_data )

        self . pushButton_2 . clicked . connect ( self . close_window )

    def close_window(self):

        self . close()

    def save_data (self)  :

        filename , ret = QFileDialog . getSaveFileName ( self , "导出数据" , "." , "TXT(*.txt)")

        f = open(filename , "w")

        con = sqlite3.connect(r"f:\\pyqtui\\signin_data.db")

        c = con.cursor()

        signdata = c.execute("select * from signinhis")
        self.signdata = signdata

        for i in self . signdata  :

            f . write ( str(i[ 0 ])+" " + str(i[ 1 ]) + " " + str(i[ 2 ]) + " " + str(i[ 3 ]) + " " + str(i[ 4 ]) + "\n")

        f . close (    )

        self . accept  (    )

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ui=sign_data()
    ui.show()
    sys.exit(app.exec_())
