#-*- coding:utf-8 -*-
import httplib, urllib,socket
import sys,time,re

params = dict(
    login_token="",
    format="json",
    domain_id=, # Domain.List 
    record_id=, #Record.List
    sub_domain="fac", 
    record_line="默认"
)
current_ip = '.'

def ddns(ip):
    params.update(dict(value=ip))
    headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/json"}
    conn = httplib.HTTPSConnection("dnsapi.cn")
    conn.request("POST", "/Record.Ddns", urllib.urlencode(params), headers)
    response = conn.getresponse()
    print response.status, response.reason
    data = response.read()
    conn.close()
    return response.status == 200

def getStrByBorder(src,border0,border1):
    pos0=src.find(border0)
    if pos0==-1:
        return ''
    pos1=src.find(border1,pos0+len(border0))
    if pos1==-1:
        return ''
    return src[(pos0+len(border0)):pos1]

def getIp_dnspod():
    try:
        sock = socket.create_connection(('ns1.dnspod.net', 6666),20)
        #sock.settimeout(30)
        ip = sock.recv(16)
        sock.close()
        return ip
    except Exception,e:
        return ''

def getIp_ip138():
    try:
        conn = httplib.HTTPConnection("1212.ip138.com",timeout=20)
        conn.request("GET", "/ic.asp")
        res = conn.getresponse()
        s= res.read()
        return getStrByBorder(s,'[',']')
    except Exception,e:
        return ''

def getIp_sohu():
    try:
        conn = httplib.HTTPConnection("pv.sohu.com",timeout=20)
        conn.request("GET", "/cityjson")
        res = conn.getresponse()
        s= res.read()
        return getStrByBorder(s,'cip": "','"')
    except Exception,e:
        return ''
    

def getIp():
    global mId
    ip=methods[mId]()
    if re.match('.*\..*\..*\..*',ip)==None:
        mId+=1
        if mId>len(methods):
            mId=1
        time.sleep(10)
        ip,mId=getIp()
    return ip,mId
    
#http://ipip.yy.com/get_ip_info.php
#http://whois.pconline.com.cn/ipJson.jsp
mId=2
methods={1:getIp_ip138,2:getIp_dnspod,3:getIp_sohu}    
logPath=sys.path[0]+"/log.txt"

while True:
    try:
        ip,siteId = getIp()
        if current_ip != ip:
            with open(logPath, "a") as fo:
                fo.write("%s %s %d\n"%(time.strftime("%m-%d %H:%M "),ip,siteId))
            
            if ddns(ip):
                current_ip = ip
            else:
                with open(logPath, "a") as fo:
                    fo.write('update fail' + '\n')
                   
    except Exception, e:
        #print e
        with open(logPath, "a") as fo:
            fo.write(time.strftime("%m-%d %H:%M ")+str(e) + '\n')
            
    time.sleep(600)
