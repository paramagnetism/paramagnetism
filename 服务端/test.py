import socket
import pickle
import numpy
import pymysql
from tensorflow import keras

# 默认tcp方式传输
sk = socket.socket()
sk2 = socket.socket()
# 绑定IP与端口
ip_port = ('192.168.43.31', 8888)
ip_port2 = ('192.168.43.31', 8889)
# 绑定监听
sk.bind(ip_port)
sk2.bind(ip_port2)
# 最大连接数
sk.listen(5)
sk2.listen(5)
#加载训练好的cnn模型
model=keras.models.load_model("cnn.h5")
#连接至本地数据库
con = pymysql.connect(host='localhost',
                       user='root',
                       password='0208',
                       db='client_list',
                       charset='utf8')
cursor = con.cursor()
log_in = 0

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

# 不断循环接收数据
while True:
    # 提示信息
    print("正在等待接收数据。。。。。。。")
    # 接收数据  连接对象和客户地址
    con2, address = sk2.accept()
    while True:
        user = con2.recv(1024).decode()
        sql = "select password from password where username = '" + user + "'"
        cursor.execute(sql)
        #print("searching")
        password=con2.recv(1024).decode()
        for i in cursor.fetchall():#返回一个tuple
            #print(i)
            if password in i:
                log_in = 1
        con2.send(pickle.dumps(log_in))
        if log_in == 1:
            break
    
    
    #登录过程
    conn, address = sk.accept()
    # 不断接收客户发来的消息
    while True:
        # 接收客户端消息
        if log_in == 1:
            print('receiving data')
            data=numpy.zeros(784).reshape(1,28,28,1).astype(float)
            recv_into(data, conn)
            #print(data)
        # 接收到退出指令
            if data.sum() == 0:
                print('EXIT')
                log_in = 0
                break

            rec = model.predict_classes(data)[0]
            conn.send(pickle.dumps(rec))
        
    # 主动关闭连接
    conn.close()
