# -*- coding:utf-8 -*-
from tkinter import Tk
from Window import Window
import socket

if __name__ == '__main__':
    win=Tk()
    ww = 530#窗口宽设定530
    wh = 430#窗口高设定430
    # 服务端为TCP方式，客户端也采用TCP方式，默认参数即为TCP
    client = socket.socket()
        # 访问服务器的IP和端口
    ip_port= ('192.168.43.31', 8888)
        # 连接主机
    client.connect(ip_port)
    Window(win,ww,wh,client)
    win.protocol("WM_DELETE_WINDOW",Window.closeEvent)
    win.mainloop()