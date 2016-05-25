import pigpio

class Led():
    def __init__(self,pins=[]):
        self.max=90
        self.min=0
        self.pins=pins
        self.fixColor={'r':-3.2,'y':-2,'g':0,'w':2.1,'b':1.4}
        self.pi=pigpio.pi()
        for p in pins:
            id=p.items()[0][0]
            #color=p.items()[0][1]
            self.pi.set_PWM_range(id,100)
            self.pi.set_mode(id,pigpio.OUTPUT)
            self.pi.set_PWM_frequency(id,50)
            self.pi.write(id,0)

    def pwm(self,id,dc):
        dc+=self.fixColor[self.pins[id].items()[0][1]]*10
        if dc>self.max:
            dc=self.max
        elif dc<self.min:
             dc=self.min
        self.pi.set_PWM_dutycycle(self.pins[id].items()[0][0],dc)

    def output(self,id,b):
        self.pi.write(self.pins[id].items()[0][0],b)

#pi.write(pin,0)
#pi.stop()
'''
l=Led([{4:'b'},{17:'b'},{27:'g'},{22:'g'},{18:'g'},{23:'w'},{24:'w'},{25:'r'}])
for i in range(8):   
    l.pwm(i,10)
'''
