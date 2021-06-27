# -*- coding:utf-8 -*-
from tkinter import *
from PIL import Image,ImageDraw
import numpy as np
import pickle
import socket
import sys

def send_from(arr, dest):
  view = memoryview(arr).cast('B')
  while len(view):
    nsent = dest.send(view)
    view = view[nsent:]
 
def recv_into(arr, source):
  view = memoryview(arr).cast('B')
  while len(view):
    nrecv = source.recv_into(view)
    view = view[nrecv:]


class Window:
    def __init__(self,win,ww,wh,client):
        self.win=win
        self.ww=ww
        self.wh=wh
        self.client=client
        self.win.geometry("%dx%d+%d+%d" %(ww,wh,500,100))
        self.win.title("手写数字识别软件---by 20180620李洧臣")
        self.can=Canvas(self.win,width=ww-130,height=wh-32,bg='white')
        self.can.place(x=0,y=0)
        self.can.bind("<B1-Motion>",self.paint)
        
        self.entry1=Entry(self.win,width=16)
        self.entry1.place(x=405,y=200)
        self.entry2=Entry(self.win,width=16)
        self.entry2.place(x=405,y=260)
        
        self.label1=Label(self.win,text="识别结果:",font=('微软雅黑',20))
        self.label1.place(x=405,y=0)
        self.label2=Label(self.win,width=6,height=2,text='',font=('微软雅黑',20),
                          background="white",relief="ridge",borderwidth=10)
        self.label2.place(x=405,y=50)
        self.label3=Label(self.win, text="用户名:",font=('微软雅黑',10))
        self.label3.place(x=405,y=170)
        self.label4=Label(self.win, text="密码：",font=('微软雅黑',10))
        self.label4.place(x=405,y=230)

        self.button1=Button(self.win,text="Predict",width=10,height=1,bg='gray',command=self.predict)
        self.button1.place(x=10,y=wh-30)
        self.button2=Button(self.win,text="Clear",width=10,height=1,bg='white',command=self.clear)
        self.button2.place(x=100,y=wh-30)
        self.button3=Button(self.win,text="Exit", width=10,height=1,bg='white',command=self.exit_)
        self.button3.place(x=200,y=wh-30)
        self.button4=Button(self.win,text="Log in", width=10,height=1,bg='white',command=self.log_in)
        self.button4.place(x=280,y=wh-30)

        self.image=Image.new("RGB",(ww-130,wh-30),color=(0,0,0))#(0,0,0)表示黑色背景
        self.draw=ImageDraw.Draw(self.image)
        self.valid_flag = 0
        
        self.client2 = socket.socket()
        # 访问服务器的IP和端口
        self.ip_port2= ('192.168.43.31', 8889)
        # 连接主机
        self.client2.connect(self.ip_port2)
        
    def log_in(self):
        user=self.entry1.get().encode()
        password=self.entry2.get().encode()
        self.client2.send(user)
        self.client2.send(password)
        _data=self.client2.recv(1024)
        self.valid_flag=pickle.loads(_data)       
        if self.valid_flag == 1:    
            messagebox.showinfo(title='登陆成功', message='欢迎！')
        else: 
            messagebox.showwarning(title='登录失败', message='用户名或密码错误！')
            
    def paint(self,event):
        self.x1,self.y1=event.x-12,event.y-12
        self.x2,self.y2=(self.x1+24),(self.y1+24)
        self.can.create_rectangle(self.x1, self.y1, self.x2, self.y2, fill="black")
        self.draw.rectangle(((self.x1,self.y1),(self.x2,self.y2)),(255,255,255))#(255,255,255)表示白色字

    def predict(self):
        if self.valid_flag== 0 :
            messagebox.showwarning(title='警告', message='请先登录')
        else:
            if np.array(self.image).sum()==0:#检测到还没进行手写就预测,显示预测结果为空
                self.display('')
            else:
                self._image=self.image.resize((28,28),Image.ANTIALIAS).convert('L')
                self._image=np.array(self._image).reshape(1,28,28,1).astype(float)#训练时shape为(-1,28,28,1)
                #self.rec=self.model.predict_classes(self._image.astype(float))[0]
                send_from(self._image, self.client)
                _data = self.client.recv(1024)
                data = pickle.loads(_data)
                #self.client.send(pickle.dumps(self._image))
                self.display(data)#显示预测结果
                self.draw=ImageDraw.Draw(self.image)

    def clear(self):
        self.can.delete("all")
        self.image=Image.new("RGB",(self.ww-130,self.wh-30),(0,0,0))#(0,0,0)表示黑色背景
        self.draw=ImageDraw.Draw(self.image)
        self.display('')

    def display(self,string):
        self.label2=Label(self.win,width=6,height=2,text=string,font=('微软雅黑',20),
                          background="white",relief="ridge",borderwidth=10)
        self.label2.place(x=405,y=50)

    def exit_(self):
        if self.valid_flag ==1:
            _image=np.zeros(784).reshape(1,28,28,1).astype(float)
            send_from(_image, self.client)
        self.client2.close()
        self.win.destroy()

    def closeEvent():
        Window.win.destroy()
        sys.exit()