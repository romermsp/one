# -*- coding: utf-8 -*-
import time,pygame,sys,threading,traceback
from pygame.locals import *
import subprocess32 as subprocess
from InfoGet import Info

class Imgs():
    def __init__(self,screenSize):
        self.curPos=-1
        self.list=[]
        self.isGetImg=False
        self.screenSize=screenSize
    def getLastCur(self):
        lastImg=self.list[self.curPos]
        self.nextPos()
        curImg=self.list[self.curPos]  
        return  lastImg,curImg
    def update(self):
        self.list=[]
        p = pygame.image.load(sys.path[0]+"/img/p1.png").convert()
        p=pygame.transform.smoothscale(p,self.screenSize)
        self.list.append(p)
        p = pygame.image.load(sys.path[0]+"/img/p2.png").convert()
        p=pygame.transform.smoothscale(p,self.screenSize)
        self.list.append(p)
        p = pygame.image.load(sys.path[0]+"/img/p3.png").convert()
        p=pygame.transform.smoothscale(p,self.screenSize)
        self.list.append(p)
        self.isGetImg=True
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
class UserInput():
    def __init__(self):
        self.mode='auto'#'manual'
        self.cmdList=[]
        self.lastCmdTime=0
        self.irexecProc=None
        th=threading.Thread(target=self.remoteRecv,args=(self.cmdAction,))
        th.setDaemon(True)
        th.start()
        

    def remoteRecv(self,cmdAction):
        p=subprocess.Popen('irexec',stdout=subprocess.PIPE)
        self.irexecProc=p
        while True:
            cmd=p.stdout.readline()[:-1]
            c=cmd.split(' ')
            if c[0]=='c':
                cmdAction(c[1])
            time.sleep(0.01)
    def killIrexecProc(self):
        if self.irexecProc.poll()==None:
            self.irexecProc.kill()
    def cmdAction(self,cmd):
        if cmd=='blue':
            self.lastCmdTime=time.time()
            if self.mode=='auto':
                self.mode='manual'
                self.cmdList.append('manual')
                th=threading.Thread(target=self.checkIsActive)
                th.setDaemon(True)
                th.start()
            elif self.mode=='manual':
                self.cmdList.append('next')
    def getCmd(self):
        if len(self.cmdList)>0:
            return self.cmdList.pop(0)
        else:
            return ''

    def checkIsActive(self):
        while True:
            if time.time()-self.lastCmdTime>120:
                self.mode='auto'
                break
            time.sleep(5)
        
    def eventCheck(self):
        for event in pygame.event.get():
            if event.type in [MOUSEBUTTONDOWN]:
                #with open(sys.path[0]+'/log.txt','a') as fo:
                    #fo.write(str(event.key)+'\n')
                self.killIrexecProc()
                pygame.quit()
                sys.exit()    
#################################################
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
        screenSize = (di.current_w,di.current_h)
        screen = pygame.display.set_mode(screenSize,FULLSCREEN|HWSURFACE|DOUBLEBUF,32)
        self.screen=screen
        self.screenSize=screenSize

    def proc(self):
        pass
    
    def render(self,imgList):
        if len(imgList)>0:
            self.screen.fill((0,0,0))
            for p in imgList:
                self.screen.blit(p['img'],p['loc'])
            pygame.display.flip()
                
    def play(self,imgs):
        li=None
        ci=None
        screen=self.screen
        cnt=Counter(180,180)
        ef=Effect()
        ui=UserInput()
        note=Note()
        while True:
            
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
            
            ui.eventCheck()
            if not isUpdate:
                time.sleep(0.05)    

###################main##########################
        
def main():
    try:
        pb=PlayBorad()
        imgs=Imgs(pb.screenSize)
        th=threading.Thread(target=Info().runPlan,args=(imgs.update,))
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

main()


