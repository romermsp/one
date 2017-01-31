#!/usr/bin/python
# -*- coding: utf-8 -*-
import time,sys,subprocess,MySQLdb,json

class TvboxUsage():
    def getCurSta(self):
        try:
            with open(sys.path[0]+"/statu.txt","r") as f:
                l=f.readline()
                if l[0]=="on":
                    return l
                else:
                    return "off"
        except Exception,e:
            return "error"
    
    def getLog(self):
        p=subprocess.Popen(['tail','/home/pi/tvbox/log3.txt','-n30'],stdout=subprocess.PIPE)
        out=p.communicate()
        return out[0]

    def tDiv(self,h,m):
        return h*2+m/30

    def getStruct(self,s,f='%y-%m-%d %H:%M'):
        return time.strptime(s,f)

    def newDayLine(self):
        t=[]
        for i in range(48):
            t.append('_')
        return t

    def addSec(self,t,s):
        ts=time.mktime(t)+s
        tt=time.localtime(ts)
        return time.strftime('%y-%m-%d %H:%M',tt)

    def genGrahLog(self):
        i=0
        curDay=''
        dl='<td>0</td>^^^^^<td>3</td>^^^^^<td>6</td>^^^^^<td>9</td>^^^^^<td>1</td><td>2</td>^^^^<td>1</td><td>5</td>^^^^<td>1</td><td>8</td>^^^^<td>2</td><td>1</td>^^^^'
        rslt=""
        log=self.getLog()[:-1].split('\n')
        isLineDone=True
        while True:
            if isLineDone:
                t=log[i].split(',')
                timeBegin,timeEnd=t[0],t[1]
                i=i+1
            if timeBegin>=timeEnd:
                continue         
            logDay=timeBegin.split(' ')[0]
            logEndDay=timeEnd.split(' ')[0]
            
            if logDay!=curDay:
                rslt+= '<tr><td>'+curDay+'</td>'+''.join(dl)+'</tr>'
                dl=self.newDayLine()
                curDay=logDay
                
            ts=self.getStruct(timeBegin)
            if logDay == logEndDay:
                te=self.getStruct(timeEnd)
                isLineDone=True
            else:
                te=self.getStruct(logDay+" 23:59")
                isLineDone=False
                timeBegin=self.addSec(te,60)
            s=self.tDiv(ts.tm_hour,ts.tm_min)
            e=self.tDiv(te.tm_hour,te.tm_min)
            for j in range(s,e+1):
                dl[j]='@'
            if i>=len(log) and isLineDone:
                break
        rslt+= '<tr><td>'+curDay+'</td>'+''.join(dl)+'</tr>'
        rslt=rslt.replace('_','<td style="background-color:#eeeeee">_</td>')
        rslt=rslt.replace('@','<td style="background-color:#22dd33">_</td>')
        rslt=rslt.replace('^','<td>-</td>')
        rslt='<table>'+rslt+'</table>'
        rslt+='<br/>'
        rslt+='<p>curSta: '+self.getCurSta()+"</p>"
        for l in log[-5:]:
            rslt+=l.replace(',','----')+'<br/>'
        rslt="<p>"+rslt+"</p>"
        rslt="<hr/><h1>Tvbox Usage</h1>"+rslt
        return rslt
        
class BlogPv():
    def genDtSql(self,endDate,days):
        curDay=endDate-(days-1)*3600*24
        sql="select '%s' as dt "%(time.strftime('%Y-%m-%d',time.localtime(curDay)))
        while True:   
            if curDay>=endDate:
                break
            curDay+=3600*24
            sql+="union all select '%s' "%(time.strftime('%Y-%m-%d',time.localtime(curDay)))       
        return sql

    def genPvSql(self,endDate,days):    
        sql='''select t1.id,t1.dt,ifnull(p.pv,0) as pv,t1.title
            from (select id,dt,title from blog_article a cross join (%s) t) t1 
            left join  blog_pv p on p.id=t1.id and p.dt=t1.dt
            order by id,dt
            '''%(self.genDtSql(endDate,days))
        return sql 

    def genChartRslt(self,x,y,name):
            rslt='''
            <h1>%s</h1>
            <div id="blog%sChart" style="align:left;width: 550px; height: 400px; margin: 0"></div>
            <script language="JavaScript">
            $(document).ready(function() {
               var title = {
                   text: ''   
               };
               var xAxis = {
                   categories: %s
               };
               var yAxis = {
                  title: {text: 'PV'},
                  plotLines: [{
                     value: 0,
                     width: 1,
                     color: '#808080'
                  }]
               };   
               var legend = {
                  layout: 'vertical',
                  align: 'right',
                  verticalAlign: 'middle',
                  borderWidth: 1
               };
               var series =  %s;
               var json = {};
               json.title = title;
               json.xAxis = xAxis;
               json.yAxis = yAxis;
               //json.legend = legend;
               json.series = series;
               $('#blog%sChart').highcharts(json);
            });
            </script>
            '''%(name,name,json.dumps(x),json.dumps(y,encoding='utf8'),name)
            return '<hr/>'+rslt

    def genPvRslt(self,days=10):
        db=MySQLdb.connect('localhost','root','password','stat',charset='utf8')
        cs=db.cursor()
        sql=self.genPvSql(time.time()-24*3600,days)
        cs.execute(sql)
        rs=cs.fetchall()
        xData=[]
        for i in range(days):
            xData.append(rs[i][1])
        yData=[]
        i=0
        for r in rs:
            if i % days==0:
                ds={}
                ds['name']=r[3]
                dp=[]
            dp.append(int(r[2]))
            if i % days ==(days-1):
                ds['data']=dp
                yData.append(ds)
            i+=1
        db.close()
        rslt=self.genChartRslt(xData,yData,'Pv')
        return rslt
    
    def genPvDeltaSql(self,endDate,days):    
        sql='''select tc.id,tc.dt,case when tc.pv is null or ty.pv is null then 0 when tc.pv-ty.pv<1 then 0 else (tc.pv-ty.pv) end as pvd,tc.title
            from 
            (select t1.id,t1.dt,p.pv,t1.title from 
            (select id,dt,title from blog_article a  
            cross join (%s) t) t1  
            left join  blog_pv p on p.id=t1.id and p.dt=t1.dt) tc
            left join 
            (select t1.id,t1.dt,p.pv,t1.title from 
            (select id,dt,title from blog_article a  
            cross join (%s) t) t1  
            left join blog_pv p on p.id=t1.id and p.dt=t1.dt) ty
            on tc.dt=date_add(ty.dt, interval 1 day) and tc.id=ty.id
            order by id,dt
            '''%(self.genDtSql(endDate,days),self.genDtSql(endDate-24*3600,days))
        return sql
    
    def genPvDeltaRslt(self,days=10):
        db=MySQLdb.connect('localhost','root','password','stat',charset='utf8')
        cs=db.cursor()
        sql=self.genPvDeltaSql(time.time()-24*3600,days)
        cs.execute(sql)
        rs=cs.fetchall()
        xData=[]
        for i in range(days):
            xData.append(rs[i][1])
        yData=[]
        i=0
        for r in rs:
            if i % days==0:
                ds={}
                ds['name']=r[3]
                dp=[]
            dp.append(int(r[2]))
            if i % days ==(days-1):
                ds['data']=dp
                yData.append(ds)
            i+=1
        db.close()
        rslt=self.genChartRslt (xData,yData,'DeltaPv')
        return rslt
    def genRslt(self):
        return self.genPvRslt()+self.genPvDeltaRslt()

class Temp():       
    def genChartRslt(self,x,y):
        rslt='''
        <h1>Temperature</h1>
        <div id="container" style="align:left;width: 550px; height: 400px; margin: 0"></div>
        <script language="JavaScript">
        $(document).ready(function() {
           var title = {
               text: ''};
           var xAxis = {
               categories: %s};
           var yAxis = {
              title: {
                 text: 'Temperature (\\'C)'},
              plotLines: [{
                 value: 0,
                 width: 1,
                 color: '#808080'}]
           };   
           var series =  [
              {'name': 'current',
                 'data': %s}];
           var json = {};
           json.title = title;
           json.xAxis = xAxis;
           json.yAxis = yAxis;
           json.series = series;
           $('#container').highcharts(json);
        });
        </script>
        '''%(x,y)
        return '<hr/>'+rslt

    def getHisTemp(self):
        cmd="mysql -uroot -ppassword -e \"use stat;select * from airtemp where dt>date_add(now(),interval -5 day) \""
        p=subprocess.Popen(cmd,stdout=subprocess.PIPE,shell=True)
        out=p.communicate()[0]
        timeX,dataY=[],[]
        data=out.split('\n')[7:-1]
        for d in data:
            d=d.split('\t')
            timeX.append(d[0])
            dataY.append(float(d[1]))
        return self.genChartRslt(timeX,dataY)    

class RecentActivity():
    def __init__(self):
        imgCnt=3
        
    def getRslt(self):
        p=subprocess.Popen(['ls','/var/www/cam1'],stdout=subprocess.PIPE)
        p=subprocess.Popen(['tail','-n3'],stdin=p.stdout,stdout=subprocess.PIPE)
        p=subprocess.Popen(['sort','-r'],stdin=p.stdout,stdout=subprocess.PIPE)
        out=p.communicate()[0]
        imgs=out.split('\n')[:-1]
        rslt=""
        for img in imgs:
            rslt+='<div><img src="/cam1/'+img+ '" width="400px"/></div>'
        return '<hr/><h1>Recent Activity</h1>'+rslt
    
print "Content-Type:text/html\n\n"
print """
<head>
<meta charset='utf-8'/>
<script src='/js/jquery.min.js'></script>
<script src='/js/highcharts.js'></script>
</head>
"""
print "query time: " + time.strftime('%m-%d %H:%M')+"<br/>"
print RecentActivity().getRslt()
print Temp().getHisTemp()
print TvboxUsage().genGrahLog()
print BlogPv().genRslt()
