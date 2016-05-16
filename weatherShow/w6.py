import time,pygame,sys,threading
from pygame.locals import *
import subprocess32 as subprocess

class Info():
    def __init__(self):
        self.nextTime=0
    def get(self):
        try:
            pass
            #out=subprocess.check_output(["casperjs",sys.path[0]+"/weather.js"],timeout=60)
        except Exception,e:
            return False#need manual stop
        return True
    
    def runPlan(self,updateImg):
        while True:
            if self.nextTime<time.time():
                isOK=self.get()
                if isOK:
                    updateImg()
                    self.nextTime=time.time()+3*60*60
                else:
                    self.nextTime=time.time()+180#retry
                #print 'nextTime',time.localtime(self.nextTime)
            time.sleep(60)
######################################################################
class Imgs():
    def __init__(self):
        self.curPos=-1
        self.list=[]
        self.isGetImg=False
    def getLastCur(self):
        lastImg=self.list[self.curPos]
        self.nextPos()
        curImg=self.list[self.curPos]  
        return  lastImg,curImg
    def update(self):
        self.list=[]
        p = pygame.image.load(sys.path[0]+"/img/p1.png").convert()
        self.list.append(p)
        p = pygame.image.load(sys.path[0]+"/img/p2.png").convert()
        self.list.append(p)
        #......
        self.isGetImg=True
    def nextPos(self):
        self.curPos+=1
        if self.curPos>=len(self.list):
            self.curPos=0
#####################################################################
class Counter():
    def __init__(self,trigCount):
        self.count=0
        self.trigCount=trigCount
        
    def reachTrig(self):
        self.count+=1
        if self.count>=self.trigCount:
            self.count=0
            return True
        return False
####################################################################
class Effect():
    def fade(self,screen,p,rg):
        for alpha in rg:
            p.set_alpha(alpha)         
            screen.fill((0,0,0))
            screen.blit(p,(0,0))
            pygame.display.update()
            time.sleep(0.01)
            
    def fadeIn(self,screen,p):
        rg=range(0,257,32)
        self.fade(screen,p,rg)
        
    def fadeOut(self,screen,p):
        rg=range(255,0,-32)
        self.fade(screen,p,rg)
###################################################################
class UserInput():
    def __init__(self):
        self.mode='auto'#'manual'
        self.cmdList=[]
        th=threading.Thread(target=self.remoteRecv,args=(self.cmdAction,))
        th.setDaemon(True)
        th.start()

    def remoteRecv(self,cmdAction):
        p=subprocess.Popen('irexec',stdout=subprocess.PIPE)
        while True:
            cmd=p.stdout.readline()[:-1]
            c=cmd.split(' ')
            if c[0]=='c':
                cmdAction(c[1])
            time.sleep(0.1)
    def cmdAction(self,cmd):
        if cmd=='blue':
            if self.mode=='auto':
                self.mode='manual'
                #self.cmdList.append('manual')
            elif self.mode=='manual':
                self.cmdList.append('next')
    def getCmd(self):
        if len(self.cmdList)>0:
            return self.cmdList.pop(0)
        else:
            return ''
    
    def eventCheck(self):
        for event in pygame.event.get():
            if event.type in [QUIT ,KEYDOWN]:
                pygame.quit()
                sys.exit()    
#################################################
class PlayBorad():
    def __init__(self):
        pygame.init()
        screenSize = (1280,720)
        screen = pygame.display.set_mode(screenSize,0,32)
        self.screen=screen

                
    def play(self,imgs):
        screen=self.screen
        cnt=Counter(4)
        ef=Effect()
        ui=UserInput()
        while True:
            cmd=ui.getCmd()
            isTrig=False
            if ui.mode=='auto':
                if cnt.reachTrig():
                    isTrig=True
            elif ui.mode=='manual':
                if cmd=='next':
                    isTrig=True
            if isTrig:
                li,ci=imgs.getLastCur()
                ef.fadeOut(screen,li)  
                ef.fadeIn(screen,ci)

            ui.eventCheck()
            time.sleep(1)    

###################main##########################
        
def main():
    pb=PlayBorad()
    imgs=Imgs()
    th=threading.Thread(target=Info().runPlan,args=(imgs.update,))
    th.setDaemon(True)
    th.start()

    while True:
        if imgs.isGetImg:
            pb.play(imgs)
        time.sleep(1)

   
main()
        
