import sys,threading
import subprocess,time

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
        if self.irexecProc!=None and self.irexecProc.poll()==None:
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
            time.sleep(10)
        
    def eventCheck(self,pygame):
        for event in pygame.event.get():
            if event.type in [pygame.MOUSEBUTTONDOWN]:
                #with open(sys.path[0]+'/log.txt','a') as fo:
                    #fo.write(str(event.key)+'\n')
                self.killIrexecProc()
                pygame.quit()
                sys.exit() 
