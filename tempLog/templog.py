import time,sys,subprocess

def logTemp():
    p=subprocess.Popen(['cat','/sys/bus/w1/devices/28-000006b3f065/w1_slave'],stdout=subprocess.PIPE)
    out=p.communicate()[0]
    t=int(out.split('t=')[1][:-1])/100
    temp=str(float(t)/10)
    dt=time.strftime('%Y-%m-%d %H:%M:%S')
    cmd="mysql -uroot -ppassword -e \"use stat;insert into airtemp (dt,temp) values ('"+ dt + "',"+ temp +")\""
    p=subprocess.Popen(cmd,stdout=subprocess.PIPE,shell=True)
    out=p.communicate()

while True:
    logTemp()
    time.sleep(1800)


