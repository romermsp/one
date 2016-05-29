import sys,time
import subprocess32 as subprocess
from tts import TTS

class Info():
    def __init__(self):
        #self.nextTime=0
        pass
    def get(self):
        pass
    def genNextTime(self,hAdd):
        t=time.time()+hAdd*3600
        if time.localtime(t).tm_hour>1 and time.localtime(t).tm_hour<6:
            t=self.genNextTime(hAdd+1)
        return t
    def runPlan(self,update):
        while True:
            if self.nextTime<time.time():
                isOK=self.get()
                if isOK:
                    update()
                    self.nextTime=self.genNextTime(4)
                else:
                    self.nextTime=time.time()+180#retry
            time.sleep(60)
    
class WeatherInfo(Info):
    def __init__(self):
        self.nextTime=0
        self.tts=TTS()
    def get(self):
        try:
            print "getWeather",time.localtime()
            out=subprocess.check_output(["casperjs",sys.path[0]+"/weather.js"],timeout=60)
            #self.getAlarm(out)
        except Exception,e:
            print e
            return False
        return True

    def getAlarm(self,out):
        try:
            msg=''
            ls=out.split('\n')
            for l in ls:
                if l.find('alarm:')>=0:
                    msg=l.split('alarm:')[1]
                    break
            if not msg=='':
                subprocess.check_output(['mplayer',sys.path[0]+'/pre.wav','-af','volume=-3'])
                self.tts.playTTS(msg)
            return True
        except Exception,e:
            print e
            return False

class NewsInfo(Info):
    def __init__(self):
        self.nextTime=0
    def get(self):
        out=""
        try:
            print "getNews",time.localtime()
            out=subprocess.check_output(["casperjs",sys.path[0]+"/news.js"],timeout=60)
        except Exception,e:
            print e
            print out
            return False
        return True
        
