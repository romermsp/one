
import time
from xmlrpclib import ServerProxy
import base64
from pyaudio import PyAudio, paInt16
from Queue import Queue
import threading

#audioBuffer=["",""]
#curPlayBufferId=0


NUM_SAMPLES = 16000
SAMPLING_RATE = 16000
pa=None
sp=None
stream=None
audioString=Queue()
isNeedGet=True
mutex=threading.Lock()

    
def init():
    global stream,sp
    pa = PyAudio()
    stream = pa.open(format =paInt16,  channels = 1,rate = SAMPLING_RATE,output = True)
    sp=ServerProxy('http://:8083',verbose=False,allow_none=True,encoding='ascii')

def main():
    global stream,sp,audioString,isNeedGet,mutex
    th=threading.Thread(target=getAudio)
    th.setDaemon(True)
    th.start()
    while True:
        if audioString.qsize()>0:
            bs=audioString.get()
            if audioString.qsize()==0:
                if mutex.acquire():
                    isNeedGet=True
                    mutex.release()
            stream.write(bs)
        

def getAudio():
    global sp,isNeedGet,audioString,mutex
    while True:
        try:
            if isNeedGet:
                s=sp.live()
                if s!="":
                    s=base64.standard_b64decode(s)
                    audioString.put(s)
                    if mutex.acquire():
                        isNeedGet=False
                        mutex.release()
        except Exception,e:
            print e
        time.sleep(0.5)

init()
main()

