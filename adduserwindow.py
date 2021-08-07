import base64
import sys

import cv2
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QDialog, QApplication
from PyQt5 import QtCore
from PyQt5 import QtGui

from Ui_D import Ui_Dialog


class adduserwindow ( QDialog , Ui_Dialog ) :

    detect_data_signal = pyqtSignal(bytes)

    def __init__(self, group_id_list = ['class1'] , parent=None):
        super(adduserwindow,self).__init__(parent)
        self.setupUi(self)

        self . gengxi(group_id_list)

        self.cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)  # 视频流
        print(2)
        self.CAM_NUM = 0  # 为0时表示视频流来自笔记本内置摄像头
        self.user_id = ''
        self.msg_name = ''
        self.msg_class = ''
        self.group_id = ''

        # self.base64_image
        # self.group_id
        # self.user_id
        # self.msg_name
        # self.msg_class
        self.cameratime = QtCore.QTimer ()
        self.cameratime.start ( 10 )
        self.slot_init()

    def gengxi(self , group_id_list):

        return


    def slot_init(self):

        self.cameratime.timeout.connect(self.camera_show)
        self.pushButton.clicked.connect(self.getcameradata)
        self.pushButton_2 . clicked . connect ( self . queding )
        self.pushButton_3.clicked.connect(self.qvxiao)


    def camera_show(self):

        print(6)

        flag, self.image = self.cap.read()  # 从视频流中读取

        print(7)

        show = cv2.resize(self.image, (440, 370))  # 把读到的帧的大小重新设置为 640x480
        print(8)
        show = cv2.cvtColor(show, cv2.COLOR_BGR2RGB)  # 视频色彩转换回RGB，这样才是现实的颜色
        print(9)
        showImage = QtGui.QImage(show.data, show.shape[1], show.shape[0],
                                 QtGui.QImage.Format_RGB888)  # 把读取到的视频数据变成QImage形式
        print(10)
        try:
            self.label.setPixmap(QtGui.QPixmap.fromImage(showImage))  # 往显示视频的Label里 显示QImage
            print(11)
        except Exception as e:

            print(str(e));

        print(11)

    def getcameradata(self):

        flag, camera_data = self.cap.read()  # 从视频流中读取

        _, enc = cv2.imencode('.jpg', camera_data)

        base64_image = base64.b64encode(enc.tobytes())

        self.base64_image = base64_image

        self.cameratime.stop()

    def queding(self)  :

        # self . group_id = self . lineEdit_3 . text()
        self . user_id = self . lineEdit . text ()
        self . msg_name = self . lineEdit_2 . text ()
        self . msg_class = self . lineEdit_3 . text ()
        self.group_id = self . msg_class
        self . close()

    def qvxiao(self):

        self.close()



# if __name__ == '__main__':
#     app = QApplication(sys.argv)
#     ui=adduserwindow()
#     ui.show()
#     sys.exit(app.exec_())



