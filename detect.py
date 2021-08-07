import base64
import sqlite3
from urllib import request

import requests
from PyQt5.QtCore import QThread, pyqtSignal, QDateTime
from PyQt5.QtWidgets import QFileDialog


class detect_thread(QThread) :

    transmit_data = pyqtSignal ( dict )

    search_data = pyqtSignal ( str  )

    OK = True

    sign_list =  {}

    def __init__(self , token , group_id )  :

        super ( detect_thread , self ) . __init__ ()

        self . access_token = token

        self . group_id = group_id

        self . condition = False

        self . add_status = 0



    def run (  self  )  :

        while self . OK  :

            if self . condition  :

                self . detect_face ( self.base64_image)

                self . condition = False

    def get_base64 ( self , base64_image   )  :

        self . base64_image = base64_image

        self . condition = True

        con = sqlite3 . connect ( r"stu_data.db" )

        c = con.cursor ()

    def detect_face ( self , base64_image )  :

        # path , ret = QFileDialog . getOpenFileName ( self , "open picture" , "." , "图片格式(*.jpg)" )
        #
        # fp = open ( path , 'rb' )
        #
        # base64_image = base64.b64encode ( fp . read (  ) )

        request_url = "https://aip.baidubce.com/rest/2.0/face/v3/detect"

        params = {

            "image" : base64_image ,
            "image_type" : "BASE64"  ,
            "face_field" : "gender,age,beauty,expression,face_shape,glasses,emotion,mask"  ,
            "max_face_num" : 1

        }

        access_token = self . access_token

        request_url = request_url + "?access_token=" + access_token

        headers = {  'content-type' : 'application/json'  }

        response = requests.post ( request_url , data = params , headers = headers   )

        if response  :

            data = response . json (    )

            if data [ 'error_code' ] != 0  :

                # self . transmit_data . emit ( data )

                self . search_data . emit ( '学生签到状态\n学生信息 : ' + "没有检测到人脸" )

                return

            if data [ 'result' ] [ 'face_num' ]  >  0  :

                # self . transmit_data . emit ( dict(data) )

                self . face_search ( self.group_id )

    def face_search ( self , group_id )  :

        request_url = "https://aip.baidubce.com/rest/2.0/face/v3/search"

        params = {

            "image" : self.base64_image  ,

            "image_type" : "BASE64"  ,

            "group_id_list" : group_id

        }

        access_token = self . access_token

        request_url = request_url + "?access_token=" + access_token

        headers = {  'content-type' : 'application/json'  }

        response = requests.post ( request_url , data = params , headers = headers   )

        if response  :

            data = response . json ()

            # print(group_id)

            # print ( data )

            if data['error_code'] == 0:

                if data['result']['user_list'][0]['score'] > 90:

                    del ( data [ 'result' ] [ 'user_list' ] [ 0 ] [ 'score' ] )

                    datetime = QDateTime.currentDateTime()

                    # print ( datetime )

                    datetime = QDateTime.toString(datetime)

                    # print(datetime)

                    data['result']['user_list'][0]['datetime'] = datetime

                    key = data [ 'result' ] [ 'user_list' ] [ 0 ] [ 'group_id' ] + data [ 'result' ] [ 'user_list' ] [ 0 ] [ 'user_id' ]

                    if key not in self.sign_list.keys() :

                        self.sign_list[key] = data [ 'result' ] [ 'user_list' ] [ 0 ]

                    # print(data [ 'result' ] [ 'user_list' ] [ 0 ] [ 'user_info' ])

                    self . search_data . emit ( "学生签到状态\n学生信息 : " + data [ 'result' ] [ 'user_list' ] [ 0 ] [ 'user_info' ]+"\n"+data[ 'result' ] [ 'user_list' ] [ 0 ]['user_id'] )
                    # print(data [ 'result' ] [ 'user_list' ] [ 0 ])

                    # stu_data = data [ 'result' ] [ 'user_list' ] [ 0 ] [ 'user_info' ]
                    #
                    # info = stu_data . split('\n')
                    #
                    # # print ( info )
                    #
                    # _ , info_name = info [ 0 ] . split( ':' )
                    #
                    # _ , info_class = info [ 1 ] . split( ':' )
                    #
                    # # print (  info_name  +  "    "  +  info_class  )
                    #
                    # id = data [ 'result' ] [ 'user_list' ] [ 0 ] [ 'user_id' ]
                    #
                    # try  :
                    #
                    #     self . search_sqlite ( id )
                    #
                    # except        :
                    #
                    #     self  .  create_sqlite  (    )
                    #
                    #     self  .  search_sqlite ( id )
                    #
                    # search_id = 0
                    #
                    # for i in self.values :
                    #
                    #     search_id = i[0]
                    #
                    # if search_id == id  :
                    #
                    #     self . update_sqlite ( id , info_name , info_class , datetime   )
                    #
                    # else  :
                    #
                    #     self .add_sqlite ( id , info_name , info_class , datetime   )

                else  :

                    self . search_data . emit ( "学生签到状态\n学生信息 : " + "姓名:none\n班级:none" )

    # def create_sqlite ( self )  :
    #
    #     con = sqlite3 . connect ( r"stu_data.db" )
    #
    #     c = con.cursor (    )
    #
    #     c.execute ( "create table student(id primary key, name, stu_class, datetime)" )
    #
    #     print ( "创建成功" )
    #
    # def add_sqlite ( self, id, name, stu_class, datetime)    :
    #
    #     con = sqlite3 . connect ( r"stu_data.db" )
    #
    #     c = con.cursor (    )
    #
    #     value = ( id , name , stu_class , datetime )
    #
    #     sql = "insert into student (id, name, stu_class, datetime) values ( ? , ? , ? , ? )"
    #
    #     c . execute ( sql , value )
    #
    #     print ( "添加成功" )
    #
    #     con . commit (    )
    #
    # def update_sqlite ( self , id , name , stu_class , datetime )  :
    #
    #     con = sqlite3.connect(r"stu_data.db")
    #
    #     c = con.cursor()
    #
    #     sql = "update student set name = ? , stu_class = ? , datetime = ? where id = ?"
    #
    #     c.execute ( sql , ( name , stu_class , datetime ,id ) )
    #
    #     con . commit ()
    #
    #     print ( "更新成功" )
    #
    # def search_sqlite ( self , id  )  :
    #
    #     con = sqlite3.connect(r"stu_data.db")
    #
    #     c = con.cursor()
    #
    #     sql = "select * from student where id = ?"
    #
    #     self.values = c . execute ( sql , (id,) )
