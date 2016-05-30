# -*- coding: utf-8 -*-
import time,pygame,sys,threading,traceback
from pygame.locals import *
import subprocess32 as subprocess
from InfoGet import WeatherInfo,NewsInfo,StockInfo
from userInput import UserInput

class Imgs():
    def __init__(self,screenSize):
        self.curPos=-1
        self.list=[]
        self.weatherList=[]
        self.newsList=[]
        self.stockList=[]
        self.isGetImg=False
        self.screenSize=screenSize
        self.mutex=threading.Lock()
    def getLastCur(self):
        if self.mutex.acquire():
            lastImg=self.list[self.curPos]
            self.nextPos()
            curImg=self.list[self.curPos]
            self.mutex.release()
            return  lastImg,curImg
    def onUpdate(self):
        if self.mutex.acquire():
            self.list=self.weatherList+self.newsList+self.stockList
        self.mutex.release()
        self.isGetImg=True
    def loadWeather(self):
        tmp=[]
        for i in range(1,4):
            p = pygame.image.load(sys.path[0]+"/img/p"+ str(i)+".png").convert()
            p=pygame.transform.smoothscale(p,self.screenSize)
            tmp.append(p)
        if self.mutex.acquire():
            self.weatherList=tmp
        self.mutex.release()
        self.onUpdate()
    def loadNews(self):
        tmp=[]
        for i in range(6):
            p = pygame.image.load(sys.path[0]+"/img/news"+ str(i)+".png").convert()
            p=pygame.transform.smoothscale(p,self.screenSize)
            tmp.append(p)
        if self.mutex.acquire():
            self.newsList=tmp
        self.mutex.release()
        self.onUpdate()
    def loadStock(self):
        tmp=[]
        p = pygame.image.load(sys.path[0]+"/img/stock.png").convert()
        p=pygame.transform.smoothscale(p,self.screenSize)
        tmp.append(p)
        if self.mutex.acquire():
            self.stockList=tmp
        self.mutex.release()
        self.onUpdate()
    def nextPos(self):
        self.curPos+=1
        if self.curPos>=len(self.list):
            self.curPos=0
#####################################################################
class Counter():
    def __init__(self,trigCount,initVal=0):
        self.count=initVal
        self.trigCount=trigCount
        
    def reachTrig(self):
        self.count+=1
        if self.count>=self.trigCount:
            self.count=0
            return True
        return False
####################################################################
class Effect():
    def __init__(self):
        self.pos=-1
        self.outRange=range(212,0,-32)
        self.inRange=range(32,257,32)
        self.pOut=None
        self.pIn=None
        self.working=False
        self.pic=None

    def setFadeWork(self,pOut,pIn):
        self.pOut=pOut
        self.pIn=pIn
        self.working=True
        self.pos=-1
        
    def doFade(self):
        if self.working:
            if not self.pOut == None:
                self.pos+=1
                if self.pos<len(self.outRange):
                    self.pOut.set_alpha(self.outRange[self.pos])
                    return self.pOut
                else:
                    self.pOut=None
                    self.pos=-1
            if not self.pIn == None:
                self.pos+=1
                if self.pos<len(self.inRange):
                    self.pIn.set_alpha(self.inRange[self.pos])
                    return self.pIn
                else:
                    self.pIn=None
                    self.working=False
        else:
            return None

###################################################################

class Note():
    def __init__(self):
        self.working=False
        self.text=None
        self.font=pygame.font.Font(u'/usr/share/fonts/truetype/wqy/wqy-microhei.ttc',128)
        self.cnt=Counter(16)

    def setDrawCmd(self,txt):
        self.working=True
        self.text=self.font.render(txt,True,(0,0,0),(0,200,0))

    def doDraw(self):
        if not self.text==None:
            if self.working:
                if self.cnt.reachTrig():
                    self.working=False
            else:
                self.text=None
        return self.text,self.working

###############################################                
class PlayBorad():
    def __init__(self):
        pygame.init()
        di=pygame.display.Info()
        screenSize = (di.current_w,di.current_h-60)
        screen = pygame.display.set_mode(screenSize,0,32)
        #screen = pygame.display.set_mode(screenSize,FULLSCREEN|HWSURFACE|DOUBLEBUF,32)
        self.screen=screen
        self.screenSize=screenSize
        self.ui=UserInput()

    def proc(self,imgs,li,ci,note,ef,cnt,ui):
        isTrig=False
        if ui.mode=='auto':
            if cnt.reachTrig():
                isTrig=True
        elif ui.mode=='manual':
            cmd=ui.getCmd()
            if cmd=='next':
                isTrig=True
            elif cmd=='manual':
                note.setDrawCmd(u'手动模式')
        if isTrig:
            li,ci=imgs.getLastCur()
            ef.setFadeWork(li,ci)
                
        isUpdate=False
        objList=[]
        pic={'img':None,'loc':(0,0)}
        p=ef.doFade()
        if not p==None:
            pic['img']=p
            isUpdate=True
        else:
            pic['img']=ci
        hasTxt,isWk=note.doDraw()
        if isUpdate:
            objList.append(pic)
        else:
            if hasTxt:
                objList.append(pic)
                if isWk:
                    objList.append({'img':note.text,'loc':(self.screenSize[0]-570,10)})
        self.render(objList)
        return isUpdate
    
    def render(self,imgList):
        if len(imgList)>0:
            self.screen.fill((0,0,0))
            for p in imgList:
                self.screen.blit(p['img'],p['loc'])
            pygame.display.update()#flip()
                
    def play(self,imgs):
        li=None
        ci=None
        cnt=Counter(200,200)
        ef=Effect()
        note=Note()
        while True:
            isUpdate=self.proc(imgs,li,ci,note,ef,cnt,self.ui)
            self.ui.eventCheck(pygame)
            if not isUpdate:
                time.sleep(0.05)    

###################main##########################


#main()

try:
    pb=PlayBorad()
    imgs=Imgs(pb.screenSize)
    
    th=threading.Thread(target=WeatherInfo().runPlan,args=(imgs.loadWeather,))
    th.setDaemon(True)
    th.start()
    time.sleep(5)
    th=threading.Thread(target=NewsInfo().runPlan,args=(imgs.loadNews,))
    th.setDaemon(True)
    th.start()
    th=threading.Thread(target=StockInfo().runPlan,args=(imgs.loadStock,))
    th.setDaemon(True)
    th.start()
    
    while True:
        if imgs.isGetImg:
            pb.play(imgs)
        time.sleep(1)
except Exception,e:
    print e
    with open(sys.path[0]+'/log.txt','a') as fo:
        fo.write(time.asctime()+"---")
        traceback.print_exc(file=fo)
    pb.ui.killIrexecProc()
    pygame.quit()

