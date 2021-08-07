import base64
import json
import math
import os
import sqlite3
from threading import Timer
from urllib import request

import requests as requests
from PyQt5.QtWebChannel import QWebChannel
from PyQt5.QtWebEngineWidgets import QWebEnginePage, QWebEngineView
from PyQt5.QtWidgets import QMainWindow, QMessageBox, QInputDialog

# from ClientThread import ClientThread
from addcommand import addcommandwindow           #  添加口令 时 的 窗口
from MainUi import Ui_MainWindow                 # 主界面显示
import sys
from PyQt5 import QtCore,QtGui,QtWidgets

from PyQt5.QtCore import QTimer, QCoreApplication, QDate, QTime, pyqtSignal, QUrl
from PyQt5.QtGui import QPixmap
import cv2
import qimage2ndarray
import time

from adduserwindow import adduserwindow        # 添加学生信息和更新学生信息的窗口加载
from detect import detect_thread             #  与百度人脸识别 AI 交互 的线程

import pyaudio
import wave

from MySharedObject import MySharedObject     # 用于网页和我们客户端的交互

from PyQt5.QtWebChannel import QWebChannel, QWebChannelAbstractTransport

import datetime

#引入selenium库中的 webdriver 模块
from selenium import webdriver
#引入time库
import time




class CamShow(QMainWindow,Ui_MainWindow):
    BaiduAK = 'sNaGelApjNkQOiQwnw5pKkDqvnelXFCu'

    EARTH_REDIUS = 6378.137

    detect_data_signal = pyqtSignal ( bytes )

    group_id = pyqtSignal ( str )

    trand_data_signal = pyqtSignal ( str )

    camera_status = False

    def __init__(self,parent=None):
        super(CamShow,self).__init__(parent)
        print(1)
        self.cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)  # 视频流
        print(2)
        self.CAM_NUM = 0  # 为0时表示视频流来自笔记本内置摄像头
        print(3)
        self.setupUi(self)
        self.timer_camera = QtCore.QTimer()  # 定义定时器，用于控制显示视频的帧
        self.timer_camera_1 = QtCore.QTimer()
        self.timer_luyin = QtCore.QTimer()
        self.datatime = QtCore.QTimer()
        self.datatime.start ( 10 )
        self.slot_init()  # 初始化槽函数

        self.dingweiarea.page().featurePermissionRequested.connect(self.permissionRequested)

        path = "file:\\" + os.getcwd() + "\\ding.html"
        path = path.replace('\\', '/')
        print(path)
        self.dingweiarea . load(QUrl(path))

        self.channel = QWebChannel()
        self.shared = MySharedObject()
        self.channel.registerObject("bridge", self.shared)
        self.dingweiarea.page().setWebChannel(self.channel)
        self.sharedtimer = QtCore.QTimer()
        self.sharedtimer.timeout.connect(self.text)
        # self.sharedtimer.start(1000)


        self . get_accesstoken ()      #获取语音识别的token

        self . Gettokent ()           #获取人脸识别的token

    def text(self):

        print(self.shared.strval)

    def permissionRequested(self, frame, feature):
        self.dingweiarea.page().setFeaturePermission(frame, feature, QWebEnginePage.PermissionGrantedByUser)

    def Gettokent(self):
        baidu_server = "https://openapi.baidu.com/oauth/2.0/token?"
        grant_type = "client_credentials"
        # API Key
        client_id = "rAz2sh5IaxjWiGvF5d2Zbobh"
        # Secret Key
        client_secret = "MIBKp3V2afnt2XN8Y3zkNeuPjW3jQMmL"

        # 拼url
        url = 'https://openapi.baidu.com/oauth/2.0/token?grant_type=client_credentials&client_id={}&client_secret={}'.format(
            client_id, client_secret)
        # print(url)
        # 获取token
        res = requests.post(url)
        # print(res.text)
        token = json.loads(res.text)["access_token"]
        # print(token)

        self.luyintoken = token

    def get_accesstoken (self)  :

        API_KEY = '02VY7U2GcZuGVTlGs7GHNOUK'
        SECRET_KEY = 'rPbAc1ZsZzc4LlGxpwcSyiD95U2PqTaX'

        host = 'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id=' + API_KEY + '&client_secret=' + SECRET_KEY

        print ( " dads " )

        response = requests . get ( host )

        print(  " dads "  )

        if response  :

            print(" dads ")

            data = response . json ()

            self . access_token = data . get ( 'access_token' )

    def slot_init(self):
        self.startqiandao.triggered.connect(self.button_open_camera_clicked)    #若该按键被点击，则调用button_open_camera_clicked()
        self.timer_camera.timeout.connect(self.show_camera) #若定时器结束，则调用show_camera()
        self.endqiandao.triggered.connect(self.button_close_camera_clicked)#若该按键被点击，则调用close()，注意这个close是父类QtWidgets.QWidget自带的，会关闭程序
        self.datatime.timeout.connect(self.updatedatatime)     # 用于实时更新时间并显示
        self.tianjiayonghuzu . triggered . connect ( self . add_group )      #     用于数据维护
        self . shanchuyonghuzu . triggered . connect ( self . del_group)      #     用于数据维护
        # self . chaxunyonghuzu . triggered . connect ( self . getlist )      #     用于数据维护
        self . tianjiayonghu . triggered . connect ( self . add_user )      #     用于数据维护
        self . shanchuyonghu . triggered . connect ( self . del_user )      #     用于数据维护
        self . gengxinyonghu . triggered . connect ( self . update_userd )      #     用于数据维护
        self . tabWidget . currentChanged . connect ( self . tabchange )      #     用于数据维护
        self . timer_camera_1 . timeout . connect ( self . show_camera_1 )    #     网页登录模块 的 摄像头 图像 显示
        self . luyinanniu . pressed . connect ( self . luyinstart )             #      按钮按下开始录音
        self . luyinanniu . clicked . connect ( self . luyinend )           #    按钮释放结束录音
        self . timer_luyin . timeout . connect ( self . luyin )             #    录音
        self . min_pushButton . clicked . connect ( self.showMinimized )    #   自小化 窗口
        self.close_pushButton.clicked.connect(self.close)                   #   关闭窗口
        self.tianjiakouling.triggered.connect ( self . addcommand )         #    用于 添加 登录 口令
        #     self.tianjia_yonghu.triggered.connect(self.xianshi)  # 若该按键被点击，则调用close()，注意这个close是父类QtWidgets.QWidget自带的，会关闭程序
    #
    # def xianshi(self)  :
    #
    #     msg = QtWidgets.QMessageBox.warning(self, 'warning', "显示", buttons=QtWidgets.QMessageBox.Ok)

    def addcommand ( self )    :

        window = addcommandwindow()
        window_status = window.exec_ ()
        # if window_status != 1    :
        #     return
        con = sqlite3.connect(r"f:\\pyqtui\\login_data.db")

        c = con.cursor()

        value = (window.username_txt, window.password_txt,
                 window.website_txt , window.userwidget_txt ,
                 window.passwordwidget_txt , window.loginwidget_txt , window.comm_txt )

        # sql = "insert into task (class_name , start_datatime , end_datatime , location) values ( ? , ? , ? , ? )"
        sql = "insert into login2 (username , password , website , usernamewidget , passwordwidget , loginwidget , command) values ( ? , ? , ? , ? , ? , ? , ? )"

        c.execute(sql, value)

        print("创建成功")

        c.execute("select * from login2")

        print(c.fetchall())

        con.commit()


    def tabchange(self):

        if self . tabWidget . currentIndex() == 1  :

            self . timer_camera_1 . start ( 10 )

        elif self . tabWidget . currentIndex() == 0  :

            self . timer_camera_1 . stop ()

    '''
        按钮按住时 ， 触发这个函数        
        录音声音采集参数准备   
    '''
    def luyinstart(self):

        self.CHUNK = 1024  # wav文件是由若干个CHUNK组成的，CHUNK我们就理解成数据包或者数据片段。
        self.FORMAT = pyaudio.paInt16  # 这个参数后面写的pyaudio.paInt16表示我们使用量化位数 16位来进行录音。
        self.CHANNELS = 1  # 代表的是声道，这里使用的单声道。
        self.RATE = 16000  # 采样率16k
        # RECORD_SECONDS = Time  # 采样时间
        self.WAVE_OUTPUT_FILENAME = "text.wav"  # 输出文件名

        self.p = pyaudio.PyAudio()

        self . stream = self.p.open(format=self.FORMAT,
                                    channels=self.CHANNELS,
                                    rate=self.RATE,
                                    input=True,
                                    frames_per_buffer=self.CHUNK)

        print("* 录音开始")

        self . frames = []

        self.timer_luyin . start( 10 )       #开始录音声音采集

    '''
        录音声音采集开始
    '''
    def luyin(self):

        data = self.stream.read(1024)
        self.frames.append(data)

    '''
        当按钮释放时 ， 触发这个函数    
        录音声音采集结束
    '''
    def luyinend(self)  :

        self . if_clear = False

        self.timer_luyin . stop ()

        self.stream.stop_stream()
        self.stream.close()
        self.p.terminate()

        wf = wave.open(self.WAVE_OUTPUT_FILENAME, 'wb')
        wf.setnchannels(self.CHANNELS)
        wf.setsampwidth(self.p.get_sample_size(self.FORMAT))
        wf.setframerate(self.RATE)
        wf.writeframes(b''.join(self.frames))
        wf.close()

        try:
            RATE = "16000"  # 采样率16KHz
            FORMAT = "wav"  # wav格式
            CUID = "wate_play"
            DEV_PID = "1536"  # 无标点普通话
            token = self.luyintoken

            # 以字节格式读取文件之后进行编码
            with open(self.WAVE_OUTPUT_FILENAME, "rb") as f:
                speech = base64.b64encode(f.read()).decode('utf8')

            size = os.path.getsize(self.WAVE_OUTPUT_FILENAME)
            headers = {'Content-Type': 'application/json'}
            url = "https://vop.baidu.com/server_api"
            data = {
                "format": FORMAT,
                "rate": RATE,
                "dev_pid": DEV_PID,
                "speech": speech,
                "cuid": CUID,
                "len": size,
                "channel": 1,
                "token": token,
            }
            req = requests.post(url, json.dumps(data), headers)
            result = json.loads(req.text)
            print(result)
            self . kouling = result["result"][0][:-1]
            print(self.kouling)
            # self.plainTextEdit_3.appendPlainText( result["result"][0][:-1] )
            self . if_clear = True
        except:
            # self.plainTextEdit_3.appendPlainText( '识别不清' )
            self . if_clear = False
            self.kouling = ""
        self . get_luyindata ()        # 读取摄像头的图像

        self . search_face_luyin ()      # 搜索图像的信息 ， 确认是否为本人



    '''
        读取摄像头的图像    
    '''
    def get_luyindata ( self )  :

        flag, camera_data = self.cap.read()  # 从视频流中读取

        _, enc = cv2.imencode('.jpg', camera_data)

        self . luyin_base64_image = base64.b64encode(enc.tobytes())



    '''
        搜索图像的信息 ， 确认是否为本人
    '''
    def search_face_luyin ( self )  :

        self.if_self = False
        self.commandvalid = False

        request_url = "https://aip.baidubce.com/rest/2.0/face/v3/search"

        params = {

            "image": self.luyin_base64_image,

            "image_type": "BASE64",

            "group_id_list": "class2"

        }

        access_token = self.access_token

        request_url = request_url + "?access_token=" + access_token

        headers = {'content-type': 'application/json'}

        response = requests.post(request_url, data=params, headers=headers)

        if response:

            data = response.json()

            # print(group_id)

            print(data)

            if data['error_code'] == 0 and data['result']['user_list'][0]['score'] > 90:

                self . user_id = data['result']['user_list'][0]['user_id']

                # self.plainTextEdit_3.appendPlainText(self . user_id)

                if str(self.user_id) == "20194047"    :

                    self . if_self = True

            if self . if_self and self . if_clear    :

                con = sqlite3.connect(r"f:\\pyqtui\\login_data.db")

                c = con.cursor()

                sql = "select * from login2 where command = ?"

                values = c.execute( sql , (self . kouling , ))

                for i in values    :

                    self . commandvalid = True
                    self.username = i[0]
                    self.password = i[1]
                    self.website = i[2]
                    self.usernamewidget = i[3]
                    self.passwordwidget = i[4]
                    self.loginwidget = i[5]
                    self.command = i[6]

                if self . commandvalid:
                    self.plainTextEdit_3.clear()
                    self.plainTextEdit_3.appendPlainText( "人脸登陆认证结果：" + "\n" + "认证成功" + "\n" + "口令确认：" + "\n" + self.kouling + "\n" + "口令有效" )
                    driver = webdriver.Chrome()
                    # 打开智慧树学习平台
                    driver.get(self.website)
                    '''
                    考虑到网页打开的速度取决于每个人的电脑和网速，
                    使用time库sleep()方法，让程序睡眠5秒
                    '''
                    time.sleep(10)
                    # #在主页面点击登录按钮，进入登录页面
                    # driver.find_element_by_xpath('//*[@id="notLogin"]/span/a[1]').click()
                    # 输入账号和密码
                    driver.find_element_by_xpath(self.usernamewidget).send_keys(self.username)
                    driver.find_element_by_xpath(self.passwordwidget).send_keys(self.password)
                    # 点击登录按钮
                    driver.find_element_by_xpath(self.loginwidget).click()

                else    :

                    self.plainTextEdit_3.clear()

                    self.plainTextEdit_3.appendPlainText("人脸登陆认证结果：" + "\n" + "认证成功" + "\n" + "口令确认：" + "\n" + self.kouling + "\n" + "口令无效")

            elif self . if_self == False and self . if_clear    :

                self.plainTextEdit_3 . clear  ()

                self.plainTextEdit_3.appendPlainText("人脸登陆认证结果：" + "\n" + "认证失败" + "\n" + "口令确认：" + "\n" + self.kouling)
            elif self . if_self and self . if_clear == False    :
                self.plainTextEdit_3.clear()

                self.plainTextEdit_3.appendPlainText("人脸登陆认证结果：" + "\n" + "认证成功" + "\n" + "口令确认：" + "\n" + "口令模糊")

            else    :

                self.plainTextEdit_3.clear()

                self.plainTextEdit_3.appendPlainText("人脸登陆认证结果：" + "\n" + "认证失败" + "\n" + "口令确认：" + "\n" + "口令模糊")

    '''
        tab_2的页面 的 摄像头 视频 显示 
    '''
    def show_camera_1(self):

        print(6)

        flag, self.image = self.cap.read()  # 从视频流中读取

        print(7)

        show = cv2.resize(self.image, (480, 470))  # 把读到的帧的大小重新设置为 640x480
        print(8)
        show = cv2.cvtColor(show, cv2.COLOR_BGR2RGB)  # 视频色彩转换回RGB，这样才是现实的颜色
        print(9)
        showImage = QtGui.QImage(show.data, show.shape[1], show.shape[0],
                                 QtGui.QImage.Format_RGB888)  # 把读取到的视频数据变成QImage形式
        print(10)
        try:
            self.camshowarea_2.setPixmap(QtGui.QPixmap.fromImage(showImage))  # 往显示视频的Label里 显示QImage
            print(11)
        except Exception as e:

            print(str(e));

        print(11)

    '''
        开始签到的处理函数
    '''
    def button_open_camera_clicked(self):

        list = self . getlist()

        print (list['result']['group_id_list'])

        self . group_id , ret = QInputDialog . getText ( self , "请输入所在班级" , "班级信息\n" + str( list['result']['group_id_list'] ) )

        if self . group_id == ''  :

            QMessageBox . about ( self , "签到失败" , "班级不能为空" )

            return

        # self . group_id = list [ 'result' ] [ 'group_id_list'] [ 0 ]

        group_status = 0

        for i in list['result']['group_id_list']  :

            if i == self . group_id  :

                group_status = 1

                break

        if group_status == 0  :

            QMessageBox . about ( self , "签到失败" , "该班级不存在" )

            return



        if self.timer_camera.isActive() == False:  # 若定时器未启动
            print( 4 )
            flag = self.cap.open(self.CAM_NUM)  # 参数是0，表示打开笔记本的内置摄像头，参数是视频文件路径则打开视频
            print( 5 )
            if flag == False:  # flag表示open()成不成功
                msg = QtWidgets.QMessageBox.warning(self, 'warning', "请检查相机于电脑是否连接正确", buttons=QtWidgets.QMessageBox.Ok)
            else:
                '''
                    开始 摄像头 图像 显示 
                '''
                self.timer_camera.start(10)  # 定时器开始计时30ms，结果是每过30ms从摄像头中取一帧显示
                # self.pushButton.setText('关闭相机 ')

                '''
                    创建线程 进行 用于发送图像数据连接到百度AI 的 接口 获取 人脸信息和数据 
                '''
                self . detectThread = detect_thread ( self . access_token , self . group_id )

                self . detectThread . start (    )

                self . facedetecttime = QTimer ( self )

                self . facedetecttime . start ( 500 )

                self . facedetecttime . timeout.connect ( self . get_cameradata )

                '''
                    传出数据到线程中
                '''
                self . detect_data_signal . connect ( self . detectThread . get_base64 )

                '''
                    将线程中的数据传回给到函数处理
                '''
                self . detectThread . transmit_data . connect ( self . get_detectdata )

                self . detectThread . search_data . connect ( self . get_search_data )

                # '''
                #     创建客户端联系服务器的线程
                # '''
                # self.client_thread = ClientThread()
                #
                # self.client_thread.start()
                # self.trand_data_signal.connect(self.client_thread.get_start)
                #
                # self.client_thread.transmit_data.connect(self.get_search_data_print)

    '''
        获取摄像头的图像  并传给线程处理     
    '''
    def get_cameradata ( self )  :

        flag , camera_data = self.cap.read()  # 从视频流中读取

        _ , enc = cv2 . imencode ( '.jpg' , camera_data )

        base64_image = base64 . b64encode ( enc.tobytes() )

        self . detect_data_signal . emit ( bytes ( base64_image ) )

    '''
        接收线程的处理后的数据并加载 ， 人脸年龄等数据 ， （现在不用显示了 ， 因为该模块已经被地图模块代替 ）        ；               
    '''
    def get_detectdata ( self , data )  :

        if data['error_code'] != 0  :

            self . plainTextEdit_2 . setPlainText ( str( data['error_code'] ) + " \n " + data['error_msg'] )

            return

        elif data['error_msg'] == "SUCCESS"  :

            self . plainTextEdit_2 . clear ()

            face_num = data['result']['face_num']

            if face_num == 0  :

                self . plainTextEdit_2 . appendPlainText( "未检测到人脸" )

                return

            else  :

                self . plainTextEdit_2 . appendPlainText( "检测到人脸" )

            for i in range ( face_num ) :

                age = data['result']['face_list'][ i ]['age']

                beauty = data['result']['face_list'][ i ]['beauty']

                gender = data['result']['face_list'][i]['gender'] [ 'type' ]

                expression = data['result']['face_list'][i]['expression'][ 'type' ]

                face_shape = data['result']['face_list'][i]['face_shape'][ 'type' ]

                glasses = data['result']['face_list'][i]['glasses'][ 'type' ]

                emotion = data['result']['face_list'][i]['emotion'][ 'type' ]

                mask = data['result']['face_list'][i]['mask'][ 'type' ]

                self . plainTextEdit_2 . appendPlainText( "年龄 = " + str ( age ) )

                self.plainTextEdit_2.appendPlainText("相貌 = " + str(beauty) )

                self.plainTextEdit_2.appendPlainText("性别 = " + str(gender))

                self.plainTextEdit_2.appendPlainText("年龄 = " + str(expression) )

                self.plainTextEdit_2.appendPlainText("年龄 = " + str(face_shape))

                self.plainTextEdit_2.appendPlainText("年龄 = " + str(glasses))

                self.plainTextEdit_2.appendPlainText("年龄 = " + str(emotion))

                self.plainTextEdit_2.appendPlainText("年龄 = " + str(mask))

    def Pos2Coord( self ,  name):
        '''
            @func: 通过百度地图API将地理名称转换成经纬度
            @note: 官方文档 http://lbsyun.baidu.com/index.php?title=webapi/guide/webservice-geocoding
            @output:
                lng: 经度
                lat: 纬度
                conf: 打点绝对精度（即坐标点的误差范围）
                comp: 描述地址理解程度。分值范围0-100，分值越大，服务对地址理解程度越高
                level: 能精确理解的地址类型
        '''
        url = 'http://api.map.baidu.com/geocoding/v3/?address=%s&output=json&ak=%s' % (name, self.BaiduAK)
        res = requests.get(url)
        if res.status_code == 200:
            val = res.json()
            if val['status'] == 0:
                retVal = {'lng': val['result']['location']['lng'], 'lat': val['result']['location']['lat'], \
                          'conf': val['result']['confidence'], 'comp': val['result']['comprehension'],
                          'level': val['result']['level']}
            else:
                retVal = None
            return retVal
        else:
            print('无法获取%s经纬度' % name)

    def Coord2Pos(self , lng, lat, town='true'):
        '''
            @func: 通过百度地图API将经纬度转换成地理名称
            @input:
                lng: 经度
                lat: 纬度
                town: 是否获取乡镇级地理位置信息，默认获取。可选参数（true/false）
            @output:
                address:解析后的地理位置名称
                province:省份名称
                city:城市名
                district:县级行政区划名
                town: 乡镇级行政区划
                adcode: 县级行政区划编码
                town_code: 镇级行政区划编码
        '''
        url = 'http://api.map.baidu.com/reverse_geocoding/v3/?output=json&ak=%s&location=%s,%s&extensions_town=%s' % (
        self.BaiduAK, lat, lng, town)
        res = requests.get(url)
        if res.status_code == 200:
            val = res.json()
            if val['status'] == 0:
                val = val['result']
                retVal = {'address': val['formatted_address'], 'province': val['addressComponent']['province'], \
                          'city': val['addressComponent']['city'], 'district': val['addressComponent']['district'], \
                          'town': val['addressComponent']['town'], 'adcode': val['addressComponent']['adcode'],
                          'town_code': val['addressComponent']['town_code']}
            else:
                retVal = None
            return retVal
        else:
            print('无法获取(%s,%s)的地理信息！' % (lat, lng))

    # lat lon - > distance

    # 计算经纬度之间的距离，单位为千米

    def rad(self,d):
        pi = 3.14
        return d * pi / 180.0

    def getDistance(self,lat1, lng1, lat2, lng2):
        radLat1 = self.rad(lat1)
        radLat2 = self.rad(lat2)
        a = radLat1 - radLat2
        b = self.rad(lng1) - self.rad(lng2)
        s = 2 * math.asin(math.sqrt(
            math.pow(math.sin(a / 2), 2) + math.cos(radLat1) * math.cos(radLat2) * math.pow(math.sin(b / 2), 2)))
        s = s * self.EARTH_REDIUS
        return s

    def get_search_data(self, data)  :

        self.findtask = False
        self . success = False
        self.stu_signined = False
        stu = data . split('学生签到状态\n学生信息 : ')
        # print(stu)
        # stu = stu[1].split('\n')

        # _ , stu_name = stu [0] . split(':')
        # _ , stu_class = stu[1] . split(':')

        if ( stu[1] == "没有检测到人脸" )  :

            self.plainTextEdit.clear()

            self.plainTextEdit.appendPlainText("没有检测到人脸")

        elif(stu[1] == "姓名:none\n班级:none")  :

            self.plainTextEdit.clear()

            self.plainTextEdit.appendPlainText("该学生不指定班级中")

        else  :

            stu = stu[1].split('\n')
            _ , stu_name = stu [0] . split(':')
            _ , stu_class = stu [1] . split(':')
            stu_id = stu[2]
            print(stu_id)
            con = sqlite3.connect(r"f:\\pyqtui\\task_data.db")

            c = con.cursor()
            sql = "select * from task where class_name = ?"

            value = c.execute(sql, (stu_class,))

            for i in value :
                self.findtask = True
                # print(i)
                # print(i[1])
                self.start_datatime = i[1]
                self.end_datatime = i[2]
                self.location = i[3]
                print(self.start_datatime)
                print(self.start_datatime)

                self . start_datatime = self.start_datatime.split(' ')
                self.start_data = self . start_datatime[0]
                self.start_time = self . start_datatime[1]

                self.end_datatime = self.end_datatime.split(' ')
                self.end_data = self.end_datatime[0]
                self.end_time = self.end_datatime[1]


            if self.findtask  :

                task_start_time = datetime.datetime.strptime(str(self.start_data) + str(self.start_time),
                                                        '%Y-%m-%d%H:%M:%S')
                # 开始时间
                print(task_start_time)
                task_end_time = datetime.datetime.strptime(str(self.end_data) + str(self.end_time),
                                                      '%Y-%m-%d%H:%M:%S')
                # 结束时间
                print(task_end_time)
                # 当前时间
                self.now_time = datetime.datetime.now()
                if task_start_time < self.now_time < task_end_time  :

                    val = self.Pos2Coord(self.location)
                    location_lng = val['lng']
                    location_lat = val['lat']

                    now_lng = float(self.shared.strval.split('\n')[0])
                    now_lat = float(self.shared.strval.split('\n')[1])

                    self.now_location = self . Coord2Pos ( now_lng , now_lat )

                    sd = self.getDistance( location_lat , location_lng , now_lat , now_lng )

                    if sd <= 2  :
                        self.plainTextEdit.clear()
                        self.plainTextEdit.appendPlainText("签到学生："+ stu_name + "\n" + "距离目标签到地址：" + str(sd) + " KM" + "\n" +"签到情况："+ "\n" +"签到成功")
                        self . success = True

                    else  :
                        self.plainTextEdit.clear()
                        self.plainTextEdit.appendPlainText("签到学生："+ stu_name + "\n" + "距离目标签到地址：" + str(sd) + " KM" + "\n" +"签到情况："+ "\n" +"签到失败\n签到位置不再目标签到地点")

                else  :
                    self.plainTextEdit.clear  ()
                    self.plainTextEdit.appendPlainText("签到学生："+ stu_name + "\n"  +"签到情况："+ "\n" +"签到失败\n不能在非签到时间段签到")

            else  :

                self . plainTextEdit . clear ()

                self . plainTextEdit . appendPlainText ( "签到学生："+ stu_name +  "\n" +"签到情况："+ "\n" +"签到失败\n所在班级没有签到任务")

            if self . success    :

                con = sqlite3 . connect ( r"f:\\pyqtui\\signin_data.db" )

                c = con . cursor ()

                sql = "select * from signinhis where stu_name = ?"

                stu_signinhis =  c . execute ( sql , (stu_name,) )

                for i in stu_signinhis    :

                    self . stu_signined = True

                if self . stu_signined    :

                    con = sqlite3 . connect ( r"f:\\pyqtui\\signin_data.db" )

                    c = con . cursor  ()

                    sql = " update signinhis set stu_class = ? , stu_id = ? , stu_datetime = ? , stu_location = ? where stu_name = ?"

                    c . execute ( sql , ( stu_class , stu_id , str(self.now_time) , self.now_location['address'] , stu_name))

                    c . execute ( " select * from signinhis " )

                    print( c.fetchall () )

                    con . commit ()

                else    :

                    con = sqlite3.connect(r"f:\\pyqtui\\signin_data.db")

                    c = con.cursor()

                    sql = " insert into signinhis ( stu_name , stu_class , stu_id , stu_datetime , stu_location ) values ( ? , ? , ? , ? , ? ) "

                    c.execute(sql, ( stu_name , stu_class, stu_id, str(self.now_time), self.now_location['address']))

                    c.execute(" select * from signinhis ")

                    print(c.fetchall())

                    con.commit()




















                    # def get_search_data_print(self,  data):
    #
    #
    #     self . plainTextEdit . appendPlainText( data )





    def button_close_camera_clicked(self):

        if self.timer_camera.isActive() == True  :
            self.timer_camera.stop()  # 关闭定时器
            # self.cap.release()  # 释放视频流
            # self.camshowarea.clear()  # 清空视频显示区域
            # # self.pushButton.setText('打开相机')
            self.facedetecttime . stop  ()

    def updatedatatime(self)  :

        date = QDate.currentDate ()

        self.riqi.setText( date . toString (  ) )

        time = QTime . currentTime (  )

        self . shijian . setText ( time . toString (  )  )



    def show_camera(self):

        # print( 6 )

        flag, self.image = self.cap.read()  # 从视频流中读取

        # print( 7 )

        show = cv2.resize(self.image, (480, 470))  # 把读到的帧的大小重新设置为 640x480
        # print( 8 )
        show = cv2.cvtColor(show, cv2.COLOR_BGR2RGB)  # 视频色彩转换回RGB，这样才是现实的颜色
        # print( 9 )
        showImage = QtGui.QImage(show.data, show.shape[1], show.shape[0],
                                 QtGui.QImage.Format_RGB888)  # 把读取到的视频数据变成QImage形式
        # print( 10 )
        try:
            self.camshowarea.setPixmap(QtGui.QPixmap.fromImage(showImage))  # 往显示视频的Label里 显示QImage
            # print(11)
        except Exception as e  :

            print ( str( e ) ) ;

        # print( 11 )

    def add_group ( self )  :

        group , ret = QInputDialog . getText ( self , "添加班级" , "请输入班级（由数字、字母、下划线组成）" )

        request_url = "https://aip.baidubce.com/rest/2.0/face/v3/faceset/group/add"

        params = {

            "group_id" : group

        }

        access_token = self . access_token

        request_url = request_url + "?access_token=" + access_token

        headers = {  'content-type' : 'application/json'  }

        response = requests . post ( request_url , data = params , headers = headers )

        if response  :

            message = response . json ()

            if message [ 'error_msg' ] == 'SUCCESS'  :

                QMessageBox . about ( self , "班级创建结果" , "班级创建成功" )

            else  :

                QMessageBox . about ( self , "班级创建结果" , "班级创建失败\n" + message [ 'error_msg' ] )

    def del_group ( self )  :

        request_url = "https://aip.baidubce.com/rest/2.0/face/v3/faceset/group/delete"

        list = self . getlist ()

        group , ret = QInputDialog . getText ( self , "班级列表" , "班级信息\n" + str ( list [ 'result' ][ 'group_id_list' ] ) )

        params = {

            "group_id" : group

        }

        access_token = self.access_token

        request_url = request_url + "?access_token=" + access_token

        headers = {  'content-type' : 'application/json'  }

        response = requests.post ( request_url , data = params , headers = headers )

        if response  :

            data = response . json ()

            if data[  'error_msg'  ] == 'SUCCESS'  :

                QMessageBox . about ( self , "班级删除结果" , "班级删除成功" )

            else  :

                QMessageBox . about ( self , "班级删除结果" , "班级删除失败\n" + data [ 'error_msg' ] )

    def getlist ( self )  :

        request_url = "https://aip.baidubce.com/rest/2.0/face/v3/faceset/group/getlist"

        params = {

            "start" : 0 , "length" : 100

        }

        access_token = self . access_token

        request_url = request_url + "?access_token=" + access_token

        headers = {  'content-type' : 'application/json'  }

        response = requests . post ( request_url , data = params , headers = headers )

        if response  :

            data = response . json ()

            if data['error_msg'] == 'SUCCESS'  :

                return data

            else  :

                QMessageBox . about ( self , "获取班级结果" , "获取班级失败\n" + data [ 'error_msg' ] )

    def add_user ( self )  :

        request_url = "https://aip.baidubce.com/rest/2.0/face/v3/faceset/user/add"

        if self . camera_status  :

            QMessageBox .about ( self , "摄像头状态" , "摄像头已打开 , 正在进行人脸签到\n请关闭签到 , 再添加用户" )

            return

        list = self . getlist ()

        window = adduserwindow ( list [ 'result' ] [ 'group_id_list' ] , self )

        window_status = window.exec_()

        print("window_status = " + str(window_status) )

        print(window.user_id)
        print(window.group_id)
        print(window.msg_name)
        print(window.msg_class )

        # if window_status != 1:
        #
        #     return

        if(window.group_id == '')  :
            QMessageBox.about(self, "人脸创建结果", "人脸创建失败\n" )
            return

        params = {

            "image" : window . base64_image ,
            "image_type" : "BASE64" ,
            "group_id"  :  window . group_id  ,
            "user_id"  : window . user_id ,
            "user_info" : '姓名:' + window. msg_name + '\n' + '班级:' + window.msg_class

        }

        access_token = self . access_token

        request_url = request_url + "?access_token=" + access_token

        headers = {  'content-type' : 'application/json'  }

        response = requests.post ( request_url , data = params , headers = headers )

        if response  :

            data = response . json ()

            if data [ 'error_msg' ] == 'SUCCESS'  :

                QMessageBox . about ( self , "人脸创建结果" , "人脸创建成功" )

            else  :

                QMessageBox . about ( self , "人脸创建结果" , "人脸创建失败\n" + data [ 'error_msg' ] )

    def update_userd(self):

        request_url = "https://aip.baidubce.com/rest/2.0/face/v3/faceset/user/update"

        if self . camera_status  :

            QMessageBox .about ( self , "摄像头状态" , "摄像头已打开 , 正在进行人脸签到\n请关闭签到 , 再添加用户" )

            return

        list = self . getlist ()

        window = adduserwindow ( list [ 'result' ] [ 'group_id_list' ] , self )

        window_status = window . exec_()

        # if window_status != 1  :
        #
        #     return

        params = {

            "image" : window . base64_image ,
            "image_type" : "BASE64" ,
            "group_id"  :  window . group_id  ,
            "user_id"  : window . user_id ,
            "user_info" : '姓名:' + window. msg_name + '\n' + '班级:' + window.msg_class

        }

        access_token = self . access_token

        request_url = request_url + "?access_token=" + access_token

        headers = {  'content-type' : 'application/json'  }

        response = requests.post ( request_url , data = params , headers = headers )

        if response  :

            data = response . json ()

            if data [ 'error_msg' ] == 'SUCCESS'  :

                QMessageBox . about ( self , "人脸更新结果" , "人脸更新成功" )

            else  :

                QMessageBox . about ( self , "人脸更新结果" , "班级更新失败\n" + data [ 'error_msg' ] )

    def get_userlist(self , group)  :

        request_url = "https://aip.baidubce.com/rest/2.0/face/v3/faceset/group/getusers"

        params = {

            "group_id" : group

        }

        access_token = self.access_token

        request_url = request_url + "?access_token=" + access_token

        headers = {'content-type': 'application/json'}

        response = requests.post(request_url, data=params, headers=headers)

        if response  :

            data = response . json ()

            if data [ 'error_msg' ] == 'SUCCESS'  :

                # QMessageBox . about ( self , "人脸创建结果" , "人脸更新成功" )

                return data

            else  :

                QMessageBox . about ( self , "获取用户列表结果" , "获取用户列表失败\n" + data [ 'error_msg' ] )

    def user_face_list( self, group , user ):

        request_url = "https://aip.baidubce.com/rest/2.0/face/v3/faceset/face/getlist"

        params = {

            "user_id"  :  user  ,

            "group_id": group

        }

        access_token = self.access_token

        request_url = request_url + "?access_token=" + access_token

        headers = {'content-type': 'application/json'}

        response = requests.post(request_url, data=params, headers=headers)

        if response:

            data = response.json()

            if data['error_msg'] == 'SUCCESS':

                # QMessageBox . about ( self , "人脸创建结果" , "人脸更新成功" )

                return data

            else:

                QMessageBox.about(self, "获取用户人脸列表结果", "获取用户人脸列表失败\n" + data['error_msg'])

    def del_face_token( self, group , user , face_token ):

        request_url = "https://aip.baidubce.com/rest/2.0/face/v3/faceset/face/delete"

        params = {

            "user_id"  :  user  ,

            "group_id"  :  group  ,

            "face_token"  :  face_token

        }

        access_token = self.access_token

        request_url = request_url + "?access_token=" + access_token

        headers = {'content-type': 'application/json'}

        response = requests.post(request_url, data=params, headers=headers)

        if response:

            data = response.json()

            if data['error_msg'] == 'SUCCESS':

                QMessageBox . about ( self , "人脸删除结果" , "人脸删除成功" )

                # return data

            else:

                QMessageBox.about(self, "人脸删除结果", "人脸删除失败\n" + data['error_msg'])

    def del_user(self):

        list = self.getlist()
        group,ret = QInputDialog.getText(self,"班级获取","班级信息\n"+str(list['result']['group_id_list']))
        group_status = 0
        if group == ''  :
            QMessageBox.about(self,"删除失败","班级不能为空\n")
            return
        for i in list['result']['group_id_list']  :
            if i == group  :
                group_status = 1
                break

        if group_status == 0  :
            QMessageBox.about(self,"删除失败","班级不存在\n")
            return

        userlist = self.get_userlist(group)
        user,ret = QInputDialog.getText(self,"用户获取" , "用户信息\n" + str(userlist['result']['user_id_list']))

        user_status  =  0
        if user  == ''  :
            QMessageBox.about(self,"删除失败","用户不能为空")
            return
        for i in userlist['result']['user_id_list']  :

            if i == user  :

                user_status = 1

                break

        if user_status == 0  :
            QMessageBox.about(self, "删除失败", "用户不存在")
            return

        face_list = self.user_face_list(group , user)
        for i in face_list['result']['face_list']  :
            self.del_face_token( group , user , i['face_token'])

    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            self.m_flag = True
            self.m_Position = event.globalPos() - self.pos()  # 获取鼠标相对窗口的位置
            event.accept()
            self.setCursor(QtGui.QCursor(QtCore.Qt.OpenHandCursor))  # 更改鼠标图标

    def mouseMoveEvent(self, QMouseEvent):
        if QtCore.Qt.LeftButton and self.m_flag:
            self.move(QMouseEvent.globalPos() - self.m_Position)  # 更改窗口位置
            QMouseEvent.accept()

    def mouseReleaseEvent(self, QMouseEvent):
        self.m_flag = False
        self.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))




if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    ui=CamShow()
    # t = Timer(1,ui.text)
    # t.start()
    ui.show()
    sys.exit(app.exec_())






