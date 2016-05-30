import sys,time
import subprocess32 as subprocess
from tts import TTS

class Info(object):
    def __init__(self):
        self.nextTime=0
        self.interval=4
        self.isUseCache=True
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
                    self.nextTime=self.genNextTime(self.interval)
                    self.isUseCache=False
                else:
                    self.nextTime=time.time()+180#retry
                    print 'retry at ' ,time.localtime(self.nextTime)
            elif self.isUseCache:
                update()
                self.nextTime=self.genNextTime(self.interval)
                self.isUseCache=False
                print str(self.__class__) + ' use cache'
            time.sleep(30)
        
class WeatherInfo(Info):
    def __init__(self):
        super(WeatherInfo,self).__init__()
        self.nextTime=time.time()+180
        self.tts=TTS()
    def get(self):
        try:
            print "getWeather",time.asctime()
            out=subprocess.check_output(["casperjs",sys.path[0]+"/weather.js"],timeout=60)
            self.getAlarm(out)
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
        super(NewsInfo,self).__init__()
        self.nextTime=time.time()+220
        self.interval=12
    def get(self):
        out=""
        try:
            print "getNews",time.asctime()
            out=subprocess.check_output(["casperjs",sys.path[0]+"/news.js"],timeout=90)
        except Exception,e:
            print e
            print out
            return False
        return True
        
class StockInfo(Info):
    def __init__(self):
        super(StockInfo,self).__init__()
        self.nextTime=time.mktime((2016,5,30,16,0,0,0,0,0))
        self.interval=24
    def get(self):
        out=""
        try:
            print "getStock",time.asctime()
            out=subprocess.check_output(["casperjs",sys.path[0]+"/stock.js"],timeout=60)
        except Exception,e:
            print 'e',e
            print out
            return False
        return True


def ud():
    print 'ok'
if __name__=="__main__":
    s=StockInfo()
    print s.__class__
