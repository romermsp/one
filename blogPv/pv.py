# -*- coding: utf-8 -*-
import httplib,time,sys

def getStrByBorder(src,border0,border1):
    pos0=src.find(border0)
    if pos0==-1:
        return ''
    pos1=src.find(border1,pos0+len(border0))
    if pos1==-1:
        return ''
    return src[(pos0+len(border0)):pos1]

def getInfo():
    try:
        conn = httplib.HTTPConnection("blog.csdn.net")
        conn.request("GET", "/romermsp")
        res = conn.getresponse()
        return res.read()
    except Exception,e:
        print e
        return ''

def findData(cont,lastPos):
    p=cont.find('class="link_view"',lastPos)
    if p>=0:
        aid=getStrByBorder(cont[p:],'/romermsp/article/details/','"')
        pv=getStrByBorder(cont[p:],'(',')')
        return aid,pv,p
    else:
        return 0,0,0
    

while True:
    pos=0
    txt=""
    cont=getInfo()
    if cont!="":
        while True:
            aid,pv,pos=findData(cont,pos+1)
            if aid==0:
                break
            txt=txt+aid+","+pv+";"
        if txt!="":
            txt=time.strftime("%y-%m-%d")+";"+txt+"\n"    
            with open(sys.path[0]+"\pv.txt", "a") as fo:
                fo.write(txt)
    time.sleep(60*60*6)

