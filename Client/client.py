import socket
import threading
import subprocess as sub
class Client(threading.Thread):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    address=('127.0.0.1',5022)
    data=[]
    dataLock=threading.Lock()
    def getData(self):
        with self.dataLock:
            return self.data

    def updateData(self, i):
        with self.dataLock:
            #print("self.data length was: " + str(len(self.data)))
            for x in range(i):
                self.data.pop(0)
            #print ("self.data length is now: "+str(len(self.data)))

    def run(self):
        while True:
            #make data a list? and delete when processed each entry???
            d=self.s.recv(1)
            with self.dataLock:
                self.data.append(d)
               #print (d)
            #print (len(self.data))
            if not d:
                break

    def sendMsg(self, message):
        self.s.send(message)


    def __init__(self):
        self.s.connect(self.address)
        threading.Thread.__init__(self)


        #cThread = threading.Thread(target=self.sendMsg, args=(b"t",))
        #cThread.daemon = True
        #cThread.start()

        #mThread = threading.Thread(target=self.handler)
        #mThread.daemon = True
        #mThread.start()
