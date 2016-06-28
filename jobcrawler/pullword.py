# -*- coding: utf-8 -*-  
import httplib, urllib
import string, time, sys, sqlite3


class Info():
    def __init__(self):
        self.httpClient = None
        self.headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain"}

    def get(self, txt):
        rt = ''
        try:
            self.httpClient = httplib.HTTPConnection("api.pullword.com", 80, timeout=8)
            self.httpClient.request("GET", "/get.php?source=" + urllib.quote(
                txt) + "&param1=0&param2=1", '', self.headers)
            response = self.httpClient.getresponse()
            print response.status == 200

            r = response.read()
            rs = r.split()  # "\n"
            for e in rs:
                l = e.split(':')
                if string.atof(l[1]) > 0.8:
                    rt += l[0] + '##'

        except Exception, e:
            print 'e', e
        finally:
            if self.httpClient:
                self.httpClient.close()
            return rt


class Saver():
    def __init__(self):
        self.tmpRslt = ''
        self.filePath = 'e:\\bak\\pytmp\\rs.txt'

    def save(self):
        with open(self.filePath, "a") as fo:
            fo.write(self.tmpRslt)

    def readFile(self):
        with open('e:\\bak\\pytmp\\r.txt', "r") as fo:
            return fo.read()



class DB():
    def __init__(self):
        self.conn = sqlite3.connect(sys.path[0] + '/t1.db')
    def connect(self):
        self.conn = sqlite3.connect(sys.path[0] + '/t1.db')

    def insert(self, job, keywords):
        try:
            stmt = "insert into job(name,salary) values ('" + job[0] + "','" + job[1] + "')"
            self.conn.execute(stmt)
            cursor = self.conn.execute('SELECT last_insert_rowid()')
            lastId = cursor.fetchone()[0]
            print lastId
            for kw in keywords:
                stmt="insert into keyword(id,name) values (" +str(lastId)+ ",'" + kw  +"')"
                self.conn.execute(stmt)

            self.conn.commit()
        except Exception, e:
            print e
            self.conn.rollback()

    def select(self, st):
        cursor = self.conn.execute(st)
        return cursor

    def close(self):
        self.conn.close()

    def creat(self):
        conn = sqlite3.connect(sys.path[0] + '/t1.db')
        conn.execute('CREATE TABLE keyword (id INTEGER ,name TEXT)')
        conn.execute('CREATE TABLE job (id INTEGER PRIMARY KEY AUTOINCREMENT,name TEXT,salary TEXT)')
        conn.close()



def seg():
    s = Saver()
    info = Info()
    ori = s.readFile()
    j = ori.split('#NL#')
    for i in range(600, len(j) - 1):
        print i
        f = j[i].split('#$$#')
        if len(f[2]) > 1020:
            f[2] = f[2][:1020]
        fc = info.get(f[2])
        s.tmpRslt += f[0] + '#$$#' + f[1] + '#$$#' + fc + '#$$#' + f[3] + '#NL#'
        time.sleep(0.2)
    s.save()


def main():
    filterWords=["职位","描述","岗位","职责","任职","资格","职能","类别","关键字","要求","举报","分享"]
    i=0
    d = DB()
    with open('e:\\bak\\pytmp\\rs.txt', "r") as fo:
        oriData=fo.read()
    rows= oriData.split('#NL#')[:-1]
    for r in rows:
        cols=r.split('#$$#')
        name=cols[0]
        #salary
        keywords=cols[2].split('##')[:-1]
        kws=[]
        for kw in keywords:
            if not isFilterWordrFound(filterWords,kw):
                kws.append(kw)
        d.insert([name,''],kws)
        i+=1
        if i>993:
            break
    d.close()

def isFilterWordrFound(filterWords,kw):
    for f in filterWords:
        if kw.find(f)>-1:
            return True
    return False

def bla():
    d=sqlite3.connect(sys.path[0] + '/t1.db')
    '''
    d.execute('delete from keyword')
    d.commit()
    '''
    c = d.execute('SELECT job.name,keyword.name from job join keyword on job.id=keyword.id')
    for r in c:
        print r[0],r[1]

    d.close()


main()