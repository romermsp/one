from pygame.locals import *
from InfoGet import Info
import threading,time,pygame,sys

class Effect():
    def fade(self,screen,p,rg):
        for alpha in rg:
            p.set_alpha(alpha)
            screen.fill((0,0,0))
            screen.blit(p,(0,0))
            pygame.display.flip()
            pygame.time.delay(10)         
    def fadeIn(self,screen,p):
        rg=range(0,257,32)
        self.fade(screen,p,rg)
    def fadeOut(self,screen,p):
        rg=range(255,0,-32)
        self.fade(screen,p,rg)

class Imgs():
    def __init__(self,scrsz):
        self.curPos=0
        #self.lastPos=0
        self.list=[]
        self.isGetImg=False
        self.screenSize=scrsz
    def getLastCur(self):
        self.lastImg=self.list[self.curPos]
        self.curPos+=1
        if self.curPos>=len(self.list):
            self.curPos=0
        self.curImg=self.list[self.curPos]  
        return self.lastImg,self.curImg
    def update(self):
        pt = pygame.image.load(sys.path[0]+"/img/p1.png").convert()
        p0=pygame.transform.smoothscale(pt,self.screenSize)
        pt = pygame.image.load(sys.path[0]+"/img/p2.png").convert()
        p1=pygame.transform.smoothscale(pt,self.screenSize)
        pt = pygame.image.load(sys.path[0]+"/img/p3.png").convert()
        p2=pygame.transform.smoothscale(pt,self.screenSize)
        self.list=[p0,p1,p2]
        self.isGetImg=True

def eventCheck():
    for event in pygame.event.get():
        if event.type == QUIT or event.type==KEYDOWN:
            pygame.quit()
            #sys.exit()

def timeTodelay(s):
    s+=1
    if s>5:
        s=0
    return s

def init():
    pygame.init()
    vi=pygame.display.Info()
    screen_size = (int(vi.current_w),int(vi.current_h*0.94))
    screen = pygame.display.set_mode(screen_size,FULLSCREEN,32)#FULLSCREEN|HWSURFACE
    screen.fill((0,0,0))
    return screen,screen_size

def playboard(screen,imgs):        
    t=0
    ef=Effect()
    while True:   
        if t==0:
            li,ci=imgs.getLastCur()
            ef.fadeOut(screen,li)    
            ef.fadeIn(screen,ci)
        t=timeTodelay(t)
        eventCheck()
        pygame.time.delay(3000)

try:    
    ig=Info()
    screen,size=init()
    imgs=Imgs(size)
    th=threading.Thread(target=ig.runPlan,args=(imgs.update,))
    th.setDaemon(True)
    th.start()
    
    while True:
        if imgs.isGetImg:
            playboard(screen,imgs)
        time.sleep(3)
        
except Exception,e:
    print e
    pygame.quit()
    #sys.exit()        




        
