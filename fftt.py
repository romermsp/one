# -*- coding: utf-8 -*-
from __future__ import division
import matplotlib.pyplot as pl
import numpy as np
from scipy.signal import butter, lfilter
import scipy
import wave
import struct
import time,pygame,sys
from pygame.locals import *
import pyaudio


def init():
    pygame.init()
    screen_size = (800,600)
    screen = pygame.display.set_mode(screen_size,0,32)
    return screen
def eventCheck():
    for event in pygame.event.get():
            if event.type in [QUIT ,KEYDOWN]:
                unInit()

def unInit():
    stream.stop_stream()  
    stream.close()   
    p.terminate()
    pygame.quit()
    sys.exit()
                
def freq_amp(sig,N,Fs):
    fft_sig = np.fft.rfft(sig)/len(sig)

    freqs=np.arange(len(fft_sig))*Fs/N
    #freqs=np.fft.fftshift(freqs)
    amp=np.abs(fft_sig)
    
    fa=scipy.log10(amp)*60
    #fa=np.where(fa>0,fa,0)
    #pl.plot(freqs,fa)
    #pl.show()
    #aa=[int(am) for am in fa[100:138] ]
    #print aa
    return fa
def cmpr(fa,seg):
    segLen=int(len(fa)/seg)
    amp= [np.average(fa[segLen*s:segLen*(s+1)]) for s in range(0,seg)]
    #print amp
    amps=[]
    for s in range(0,seg):
        avg=np.average(fa[segLen*s:segLen*(s+1)])
        if avg<0:
            avg=0
        amps.append(avg)    
    #print amps  
    return amps   
    
def open(path):
    wav_file= wave.open(path, 'rb')
    params = wav_file.getparams()
    nchannels, sampwidth, framerate, nframes = params[:4]
    print nchannels, sampwidth, framerate, nframes 
    #nframes=N 
    data=wav_file.readframes(nframes)
    wav_file.close()
    return data,framerate,sampwidth,nchannels

if __name__ == '__main__':

    N=4096
    datas,fr,sw,nch=open('e:\\bak\\HOW_Secrets_of_the_Forest1.wav')#Kalimba HOW_Secrets_of_the_Forest
    p = pyaudio.PyAudio()
    stream = p.open(format = p.get_format_from_width(sw),  
                channels = nch,  
                rate = fr,
                output = True)
    scr=init()
    
    d=datas[:N]

    i=1
    while True:
        time.sleep(0.02)
        
        if len(d)>0:
            sig=np.fromstring(d, dtype=np.int16)
            sig.shape = -1, 2
            sig = sig.T
            freq=freq_amp(sig[0],256,fr)
            f=cmpr(freq,8)
            scr.fill((0,0,0))
            for j in range(0,len(f)):               
                pygame.draw.line(scr, (0,111,22), (j*60,500), (j*60,500-f[j]),16)
            pygame.display.update()
            stream.write(d)
            d=datas[i*N:(i+1)*N]
            i+=1
        
        eventCheck()
        
##    sigs=np.fromstring(data, dtype=np.int16)
##    scr=init()
     
##    for nth in range(0,222):
##        sig=sigs[N*nth:N*(nth+1)]
##        freq=freq_amp(sig,N,fr)
##        f=cmpr(freq,8)
##
##        #print freq
##        scr.fill((0,0,0))
##        for i in range(0,len(f)):               
##            pygame.draw.line(scr, (255,0,255), (i*60,500), (i*60,500-f[i]),16)
##        pygame.display.update()
    #eventCheck()
    #time.sleep(0.05)
    #while True:
        #eventCheck()
        #time.sleep(1)
  
