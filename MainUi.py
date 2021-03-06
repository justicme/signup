# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ceshi.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.
import sys

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPalette
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtWidgets import QMainWindow, QWidget


class Ui_MainWindow(QWidget):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 630)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        # 定义按钮
        self.close_pushButton = QtWidgets.QPushButton(self.centralwidget)
        # 设置按钮位置(x,y,width,height)
        self.close_pushButton.setGeometry(QtCore.QRect(771, 0, 28, 28))
        # 设置按钮内容
        # self.close_pushButton.setText("")
        # 设置按钮对象名（不是显示内容
        self.close_pushButton.setObjectName("close_pushButton")
        # 设置按钮圆角
        self.close_pushButton.setStyleSheet('background-color: rgb(255, 0 , 0);border-radius: 10px; border: 2px groove gray;border-style: outset;')

        # 定义按钮
        self.min_pushButton = QtWidgets.QPushButton(self.centralwidget)
        # 设置按钮位置(x,y,width,height)
        self.min_pushButton.setGeometry(QtCore.QRect(741, 0, 28, 28))
        # 设置按钮内容
        # self.close_pushButton.setText("")
        # 设置按钮对象名（不是显示内容
        self.min_pushButton.setObjectName("min_pushButton")
        # 设置按钮圆角
        self.min_pushButton.setStyleSheet('background-color: rgb(255, 255 , 0);border-radius: 10px; border: 2px groove gray;border-style: outset;')

        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        self.tabWidget.setGeometry(QtCore.QRect(0, 30, 801, 601))
        self.tabWidget.setObjectName("tabWidget")
        self.tab = QtWidgets.QWidget()
        self.tab.setObjectName("tab")
        # self.pushButton = QtWidgets.QPushButton(self.tab)
        # self.pushButton.setGeometry(QtCore.QRect(50, 430, 93, 28))
        # self.pushButton.setObjectName("pushButton")
        '''
        添加菜单栏
        '''
        self.menuBar = QtWidgets.QMenuBar(self.tab)
        self.menuBar.setGeometry(QtCore.QRect(0, 3, 800, 26))
        self.menu = QtWidgets.QMenu(self.menuBar)
        self.menu.setObjectName("menu")
        self.menu_2 = QtWidgets.QMenu(self.menuBar)
        self.menu_2.setObjectName("menu_2")
        self.menu_3 = QtWidgets.QMenu(self.menuBar)
        self.menu_3.setObjectName("menu_3")
        # self.setMenuBar(self.menuBar)
        # MainWindow.setMenuBar(self.menuBar)
        self.tianjiayonghuzu = QtWidgets.QAction(self.tab)
        self.tianjiayonghuzu.setObjectName("tianjiayonghuzu")
        self.shanchuyonghuzu = QtWidgets.QAction(self.tab)
        self.shanchuyonghuzu.setObjectName("shanchuyonghuzu")
        # self.chaxunyonghuzu = QtWidgets.QAction(self.tab)
        # self.chaxunyonghuzu.setObjectName("chaxunyonghuzu")
        self.tianjiayonghu = QtWidgets.QAction(self.tab)
        self.tianjiayonghu.setObjectName("tianjiayonghu")
        self.shanchuyonghu = QtWidgets.QAction(self.tab)
        self.shanchuyonghu.setObjectName("shanchuyonghu")
        self.gengxinyonghu = QtWidgets.QAction(self.tab)
        self.gengxinyonghu.setObjectName("gengxinyonghu")
        self.startqiandao = QtWidgets.QAction(self.tab)
        self.startqiandao.setObjectName("startqiandao")
        self.endqiandao = QtWidgets.QAction(self.tab)
        self.endqiandao.setObjectName("endqiandao")
        self.menu.addAction(self.startqiandao)
        self.menu.addAction(self.endqiandao)
        self.menu_2.addAction(self.tianjiayonghuzu)
        self.menu_2.addAction(self.shanchuyonghuzu)
        # self.menu_2.addAction(self.chaxunyonghuzu)
        self.menu_3.addAction(self.tianjiayonghu)
        self.menu_3.addAction(self.shanchuyonghu)
        self.menu_3.addAction(self.gengxinyonghu)
        self.menuBar.addAction(self.menu.menuAction())
        self.menuBar.addAction(self.menu_2.menuAction())
        self.menuBar.addAction(self.menu_3.menuAction())
        '''
            摄像头屏幕    
        '''
        self.camshowarea = QtWidgets.QLabel(self.tab)
        self.camshowarea.setGeometry(QtCore.QRect(10, 40, 491, 481))
        self.camshowarea.setText("")
        self.camshowarea.setObjectName("camshowarea")
        # self.camshowarea.setFrameShape(QtWidgets.QFrame.Box)
        # self.camshowarea.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.camshowarea.setStyleSheet("QWidget#camshowarea{background-image: url(./231.png);border-radius:30px;}")
        '''
            信息模块                
        '''
        self.plainTextEdit = QtWidgets.QPlainTextEdit(self.tab)
        self.plainTextEdit.setGeometry(QtCore.QRect(520, 130, 261, 191))
        self.plainTextEdit.setObjectName("plainTextEdit")
        # self.plainTextEdit_2 = QtWidgets.QPlainTextEdit(self.tab)
        # self.plainTextEdit_2.setGeometry(QtCore.QRect(520, 360, 261, 171))
        # self.plainTextEdit_2.setObjectName("plainTextEdit_2")
        self.dingweiarea  =  QWebEngineView(self.tab)
        self.dingweiarea . setGeometry(QtCore.QRect(520, 360, 261, 171))
        self.dingweiarea . setObjectName("dingweiarea")

        '''
        信息提示         
        '''
        self.label = QtWidgets.QLabel(self.tab  )
        self.label.setGeometry(QtCore.QRect(530, 330, 101, 16))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.tab)
        self.label_2.setGeometry(QtCore.QRect(530, 100, 101, 16))
        self.label_2.setObjectName("label_2")
        '''
            时间模块
        '''
        # self.label_2.setStyleSheet('''QLabel{color:darkGray;background:white;border:2px solid #F3F3F5;border-radius:45px;font-size:14pt; font-weight:400;font-family: Roman times;}''')
        self.riqi = QtWidgets.QLabel(self.tab)
        self.riqi.setGeometry(QtCore.QRect(570, 30, 161, 21))
        self.riqi.setText("")
        self.riqi.setObjectName("riqi")
        self.shijian = QtWidgets.QLabel(self.tab          )
        self.shijian.setGeometry(QtCore.QRect(570, 70, 161, 20))
        self.shijian.setText("")
        self.shijian.setObjectName("shijian")
        self.tabWidget.addTab(self.tab, "")
        self.tab_2 = QtWidgets.QWidget()
        self.tab_2.setObjectName("tab_2")
        # self.pushButton_2 = QtWidgets.QPushButton(self.tab_2)wwwwwww
        # self.pushButton_2.setGeometry(QtCore.QRect(90, 460, 93, 28))
        # self.pushButton_2.setObjectName("pushButton_2")
        '''
            摄像头屏幕    
        '''
        self.camshowarea_2 = QtWidgets.QLabel(self.tab_2)
        self.camshowarea_2.setGeometry(QtCore.QRect(10, 40, 491, 481))
        self.camshowarea_2.setText("")
        self.camshowarea_2.setObjectName("camshowarea_2")
        '''
            录音按钮    
        '''
        self.luyinanniu = QtWidgets.QPushButton ( self . tab_2 )
        self.luyinanniu . setGeometry ( QtCore . QRect( 636 , 500 , 93 , 28  )  )
        self . luyinanniu . setText("")
        self . luyinanniu . setObjectName (  "luyinanniu"  )

        '''
            信息模块    
        '''

        self.plainTextEdit_3 = QtWidgets.QPlainTextEdit(self.tab_2)
        self.plainTextEdit_3.setGeometry(QtCore.QRect(520, 300, 261, 171))
        self.plainTextEdit_3.setObjectName("plainTextEdit_3")
        '''
            添加菜单栏
        '''
        self.menuBar_1 = QtWidgets.QMenuBar(self.tab_2)
        self.menuBar_1.setGeometry(QtCore.QRect(0, 3, 800, 26))
        self.menu_4 = QtWidgets.QMenu(self.menuBar)
        self.menu_4.setObjectName("menu_4")
        self . tianjiakouling = QtWidgets . QAction ( self . tab_2 )
        self . tianjiakouling . setObjectName( "tianjiakouling" )
        self . menu_4 . addAction ( self . tianjiakouling )
        self . menuBar_1 . addAction ( self . menu_4 . menuAction() )

        self.tabWidget.addTab(self.tab_2, "")
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        # self.pushButton.setText(_translate("MainWindow", "1"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("MainWindow", "打卡签到"))
        # self.pushButton_2.setText(_translate("MainWindow", "2"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), _translate("MainWindow", "自动登陆"))
        self.label.setText(_translate("MainWindow", "学生签到位置"))
        self.label_2.setText(_translate("MainWindow", "学生签到情况"))

        self.menu.setTitle(_translate("MainWindow", "签到"))
        self.menu_2.setTitle(_translate("MainWindow", "班级"))
        self.menu_3.setTitle(_translate("MainWindow", "学生"))
        self . menu_4 . setTitle(_translate("MainWindow" , "口令"))
        self . tianjiakouling . setText(_translate("MainWindow" , "添加口令"))
        self.tianjiayonghuzu.setText(_translate("MainWindow", "添加班级"))
        self.shanchuyonghuzu.setText(_translate("MainWindow", "删除班级"))
        # self.chaxunyonghuzu.setText(_translate("MainWindow", "查询用户组"))
        self.tianjiayonghu.setText(_translate("MainWindow", "添加学生"))
        self.shanchuyonghu.setText(_translate("MainWindow", "删除学生"))
        self.gengxinyonghu.setText(_translate("MainWindow", "更新学生"))
        self.startqiandao.setText(_translate("MainWindow", "启动签到"))
        self.endqiandao.setText(_translate("MainWindow", "关闭签到"))
        self.luyinanniu.setText(_translate("MainWindow", "验证"))
        self.setWindowOpacity(0.9)  # 设置窗口透明度
        # Ui_CamShow.setAttribute(QtCore.Qt.WA_TranslucentBackground) # 设置窗口背景透明
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)  # 隐藏边框
        pe = QPalette()
        self.setAutoFillBackground(True)
        pe.setColor(QPalette.Window, Qt.lightGray)  # 设置背景色
        # pe.setColor(QPalette.Background,Qt.blue)
        self.setPalette(pe)


# class CamShow2(QMainWindow,Ui_MainWindow):
#
#     # detect_data_signal = pyqtSignal ( bytes )
#     #
#     # group_id = pyqtSignal ( str )
#     #
#     # camera_status = False
#
#     def __init__(self,parent=None):
#         super(CamShow2,self).__init__(parent)
#         self.setupUi(self)
#
# if __name__ == '__main__':
#     app = QtWidgets.QApplication(sys.argv)
#     ui=CamShow2()
#     ui.show()
#     sys.exit(app.exec_())
