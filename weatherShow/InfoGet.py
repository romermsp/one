import sys,time
import subprocess32 as subprocess
from tts import TTS
class Info():
    def __init__(self):
        self.nextTime=0
        self.tts=TTS()
    def get(self):
        try:
            print "get",time.localtime()
            out=subprocess.check_output(["casperjs",sys.path[0]+"/weather.js"],timeout=60)
            print out
            self.getAlarm(out)
        except Exception,e:
            print e
            return False
        return True
    def genNextTime(self,hAdd):
        t=time.time()+hAdd*3600
        if time.localtime(t).tm_hour>1 or time.localtime(t).tm_hour<6:
            t=self.genNextTime(hAdd+1)
        return t
    def runPlan(self,update):
        while True:
            if self.nextTime<time.time():
                isOK=self.get()
                if isOK:
                    update()
                    self.nextTime=self.genNextTime(3)
                else:
                    self.nextTime=time.time()+180#retry
                #print time.localtime(self.nextTime)
            time.sleep(60)
    def getAlarm(self,out):
        try:
            msg=''
            ls=out.split('\n')
            for l in ls:
                if l.find('alarm:')>=0:
                    msg=l.split('alarm:')[1]
                    break
            if not msg=='':
                subprocess.check_output(['mplayer',sys.path[0]+'/pre.wav'])
                tts.playTTS(msg)
            return True
        except Exception,e:
            print e
            return False
        
info=Info()
info.get()
        
