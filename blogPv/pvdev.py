# -*- coding: utf-8 -*-
import httplib,time,sys,subprocess
#from mail import mail 
import MySQLdb
#reload(sys)
#sys.set
#select c.dt,c.id,c.pv-p.pv from blog_pv p inner join blog_pv c on c.dt=date_add(p.dt,interval 1 day) and c.id=p.id  where c.dt='2017-1-10';
def execSql(cmd):
    precmd="mysql -uroot -ppassword -e \"use stat;"
    p=subprocess.Popen(precmd+cmd+"\"",stdout=subprocess.PIPE,shell=True)
    global out
    out=p.communicate()
    return out[0]

def readArticleId():
    db=MySQLdb.connect('localhost','root','password','stat')
    cs=db.cursor()
    sql="select id,aid from blog_article"
    #sql="select * from blog_article"
    global rs
    cs.execute(sql)
    rs=cs.fetchall()
    d={}
    for r in rs:
        d[r[1]]=r[0]
    db.close()
    return d

def addToDb(sql,ld):
    db=MySQLdb.connect('localhost','root','password','stat',charset='utf8')
    cs=db.cursor()
    #cs.executemany(sql,ld)
    cs.execute(sql)
    db.commit()
    db.close()

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
listData=[]
sql="insert into blog_pv (dt,id,pv) values (%s,%s,%s)"  
while True:
    pos=0
    dt=time.strftime("%y-%m-%d")
    cont=getInfo()
    print "go"
    if cont!="":
        global listData
        listData=[]
        #dictAid=readArticleId()
        #break
        while True:
            aid,pv,pos=findData(cont,pos+1)
            if aid==0:
                break
            #id=int(dictAid[aid])
            title=getStrByBorder(cont,aid+'">',"</a>")
            
            #listData.append((str(dt),str(id),str(pv)))
            #sql="update blog_article set title='%s' where id=%d"%(title.strip(),int(id))
            sql="insert into blog_article (aid,title) values ('%s','%s')"%(str(aid),title.strip())
            print sql
            addToDb(sql,'listData')
    
    time.sleep(60*60*24)


