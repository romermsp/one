# -*- coding: utf-8 -*-
import numpy as np
import wave,pyaudio
import struct,scipy
import time,pygame,sys
from pygame.locals import *
from pwm import Led

def init():
    pass
    '''
    pygame.init()
    screen_size = (800,600)
    screen = pygame.display.set_mode(screen_size,0,32)
    return screen
    '''
def eventCheck():
    for event in pygame.event.get():
            if event.type in [QUIT ,KEYDOWN]:
                unInit()
def unInit():
    stream.stop_stream()  
    stream.close()   
    p.terminate()
    pygame.quit()

                
def freq_amp(sig,N,Fs):
    fft_sig = np.fft.rfft(sig)/len(sig)
    #freqs=np.arange(len(fft_sig))*Fs/N
    #freqs=np.fft.fftshift(freqs)
    amp=np.abs(fft_sig)
    fa=scipy.log10(amp+0.0001)
    #fa=np.where(fa>0,fa,0)
    #pl.plot(freqs,fa)
    #pl.show()
    #aa=[int(am) for am in fa[100:138] ]
    return fa
def cmpr(fa,seg):
    segLen=int(len(fa)/seg)
    amp= [np.average(fa[segLen*s:segLen*(s+1)]) for s in range(0,seg)]
    amps=[]
    for s in range(0,seg):
        avg=np.average(fa[segLen*s:segLen*(s+1)])
        if avg<0:
            avg=0
        amps.append(avg)    
    return amps   
    
def open(path):
    wav_file= wave.open(path, 'rb')
    params = wav_file.getparams()
    nchannels, sampwidth, framerate, nframes = params[:4]
    print nchannels, sampwidth, framerate, nframes 
    data=wav_file.readframes(nframes)
    wav_file.close()
    return data,framerate,sampwidth,nchannels

def setStepSampleCount(fr,sw,nch=1):
    print fr,sw,nch
    stepRate=fr*sw*nch/8
    print stepRate
    sc=512
    while sc<=32768:
        if stepRate<sc:
            break
        sc*=2
    return sc

if __name__ == '__main__':
    datas,fr,sw,nch=open(sys.path[0]+'/ambient.wav')
    N=setStepSampleCount(fr,sw,nch)
    print N
    N= 4096
    p = pyaudio.PyAudio()#Kalimba HOW_Secrets_of_the_Forest1  ambient
    stream = p.open(format = p.get_format_from_width(sw),  
                channels = nch,  
                rate = fr,
                output = True)
    #scr=init()
    led=Led([{4:'b'},{17:'b'},{27:'g'},{22:'g'},{18:'g'},{23:'w'},{24:'y'},{25:'r'}])
    d=datas[:N]

    i=1
    while True:
        #time.sleep(0.5)
        #print time.time()
        if len(d)<=0:
            break
        sig=np.fromstring(d, dtype=np.int16)
        #sig.shape = -1, 2
        #sig = sig.T
        #freq=freq_amp(sig[0],256,fr)
        freq=freq_amp(sig,0,fr)
        f=cmpr(freq,8)
        for id in range(len(led.pins)):
            pw=f[id]
            if pw>0.3:
                #pw=(pw-1)*50
                pw=pw*22
                #print pw,
                led.pwm(id,pw)
                #led.output(id,1)
            else:
                led.output(id,0)
        #print ''
        
        #print pw
       
        stream.write(d)
        d=datas[i*N:(i+1)*N]
        i+=1
        
        #eventCheck()
        
   
