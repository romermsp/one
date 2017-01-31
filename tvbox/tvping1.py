import subprocess as sp
import time,sys

lastState="off"
timeOn=""
timeOff=""

def work():
    global lastState,timeOn,timeOff
    p=sp.Popen(["ping","192.168.1.123","-c","1"],stdout=sp.PIPE,stderr=sp.PIPE)
    out,err=p.communicate()
    isPingOn=False
    if "1 received" in out:
        isPingOn=True
    if isPingOn and lastState=="off":
        timeOn=time.strftime("%y-%m-%d %H:%M")
        lastState="on"
        print lastState,timeOn
    elif not isPingOn and lastState=="on":
        timeOff=time.strftime("%y-%m-%d %H:%M")
        lastState="off"
        with open(sys.path[0]+"/log3.txt","a") as f:
            f.write(timeOn+","+timeOff+"\n")
        print lastState,timeOff
    
print time.strftime("%y-%m-%d %H:%M")        
while True:
    work()
    time.sleep(60)
