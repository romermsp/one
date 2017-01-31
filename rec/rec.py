
from pyaudio import PyAudio, paInt16
from SimpleXMLRPCServer import SimpleXMLRPCServer
import base64,time,wave,threading

isLive=False
audioString=[]

def bufferAppend(bf):
    global audioString
    audioString.append("".join(bf))

lastBeatTime=0
def heartBeat():
    global lastBeatTime,isLive,pa
    while isLive:
        if time.time()-lastBeatTime>10:
            isLive=False
        time.sleep(1)

pa=None        
stream=None
  
def recStart(p):
    global isLive,bufferAppend,stream,pa
    NUM_SAMPLES = 32000
    SAMPLING_RATE = 16000
    stream = pa.open(format=paInt16, channels=1,rate=SAMPLING_RATE,
                     input=True,frames_per_buffer=NUM_SAMPLES,input_device_index=0)
    save_count = 0
    save_buffer = []
    while isLive:
        string_audio_data = stream.read(16000)
        save_buffer.append( string_audio_data )
        save_count=save_count+1
        if save_count >2:
            #print save_count,time.time(),len(save_buffer)
            bufferAppend(save_buffer)
            #save_wave_file('E:\\project\\rec\\rec.wav',save_buffer)
            save_buffer = []
            save_count=0
    #while not isLive:
    stream.stop_stream()
    stream.close()
    global audioString
    audioString=[]

def live():
    global audioString,isLive,lastBeatTime
    lastBeatTime=time.time()
    if not isLive:
        isLive=True
        th=threading.Thread(target=recStart,args=("bufferAppend",))
        th.setDaemon(True)
        th.start()
        th1=threading.Thread(target=heartBeat)
        th1.setDaemon(True)
        th1.start()
        time.sleep(6)
    if len(audioString)>0:
        a=audioString.pop(0)
        return base64.standard_b64encode(a)
    else:
        return ""

def init():
    global pa
    pa = PyAudio()
    s=SimpleXMLRPCServer(('0.0.0.0',8083),allow_none=True)
    s.register_function(live)
    s.serve_forever()


init()
