# -*- coding:utf-8 -*-
import urllib
import urllib2
import re
import thread
import time 
import re


# config
PROXY=False
BASEURL = 'http://tieba.baidu.com/p/3138733512'

PROXYNAME='http://num:password@proxy.fudan.edu.cn:8080' 
PROXYHANDLER=urllib2.ProxyHandler({'http':PROXYNAME})

class Tool:
    removeImg = re.compile('<img.*?>| {7}|')            #去除img标签,7位长空格
    removeAddr = re.compile('<a.*?>|</a>')              #删除超链接标签
    replaceLine = re.compile('<tr>|<div>|</div>|</p>')  #把换行的标签换为\n
    replaceTD= re.compile('<td>')                       #将表格制表<td>替换为\t
    replacePara = re.compile('<p.*?>')                  #把段落开头换为\n加空两格
    replaceBR = re.compile('<br><br>|<br>')             #将换行符或双换行符替换为\n
    removeExtraTag = re.compile('<.*?>')                #将其余标签剔除
    def replace(self,x):
        x = re.sub(self.removeImg,"",x)
        x = re.sub(self.removeAddr,"",x)
        x = re.sub(self.replaceLine,"\n",x)
        x = re.sub(self.replaceTD,"\t",x)
        x = re.sub(self.replacePara,"\n    ",x)
        x = re.sub(self.replaceBR,"\n",x)
        x = re.sub(self.removeExtraTag,"",x)
        return x.strip()

class bdtb:
    def __init__(self,baseURL,seeLz,floorTag):
        self.baseUrl=baseURL
        self.seeLz='?see_lz='+str(seeLz)
        self.user_agent='Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.101 Safari/537.36'
        self.headers={'User-Agent':self.user_agent}
        self.tool=Tool()
        self.file=None
        self.floorTag=floorTag
        self.floor=1
		
    def getPage(self,pageNum):
	try:
	    url=self.baseUrl+self.seeLz+'&pn='+str(pageNum)
	    if  PROXY:
	        opener = urllib2.build_opener(PROXYHANDLER)
	        urllib2.install_opener(opener)	
	        request=urllib2.Request(url,headers=self.headers)
	        response=opener.open(request)
	    else:
	        request=urllib2.Request(url,headers=self.headers)
	        response=urllib2.urlopen(request)
	    
		page=response.read().decode('utf-8')
	    return page
	except urllib2.URLError,e:
	    if hasattr(e,"reason"):
                print u"连接百度贴吧失败,错误原因",e.reason
	        return None 
			
    def getTitle(self,page):
        pattern=re.compile('<h1.*?class="core_title_txt.*?".*?>(.*?)</h1>',re.S)
        title=re.search(pattern,page)
        if title:
            return title.group(1)
        else:
            return None

    def setFileTitle(self,title):
        if title is not None:
            print title
            self.file = open(title + ".txt","w+")
        else:
            self.file = open(self.defaultTitle + ".txt","w+")			

    def getPageNum(self,page):
        pattern = re.compile('<li class="l_reply_num.*?</span>.*?<span.*?>(.*?)</span>',re.S)
        title=re.search(pattern,page)
        if title:
            return title.group(1)
        else:
            return None			
			
    def getContent(self,page):
        pattern = re.compile('<div id="post_content_.*?>(.*?)</div>',re.S)
        items = re.findall(pattern,page)
        contents=[] 
        for item in items:
            print u"正在读取百度贴吧,按回车查看新帖子，Q退出"
            input=raw_input()
            #if input =="Q":

            content="\n"+self.tool.replace(item)+"\n"
            floorLine = "\n"+str(self.floor)+u"楼---------------------------------------------------------------"
            print floorLine
            print content

            contents.append(floorLine.encode('utf-8'))
            contents.append(content.encode('utf-8'))
            self.floor+=1

        return contents
	
    def writeData(self,contents):
        for item in contents:
            self.file.write(item)

    def start(self):
        indexPage = self.getPage(1)
        pageNum = self.getPageNum(indexPage)
        title = self.getTitle(indexPage)
        self.setFileTitle(title)
        if pageNum == None:
            print u"URL已失效，请重试"
            return
        try:
            print u"该帖子共有" + str(pageNum) + u"页"
            for i in range(1,int(pageNum)+1):
                print u"正在写入第" + str(i) + u"页数据"
                page = self.getPage(i)
                contents = self.getContent(page)
                if self.floorTag=='1':
                    self.writeData(contents)
        except IOError,e:
            print u"写入异常，原因" + e.message
        finally:
            print u"写入任务完成"			
			
print u"请输入帖子代号\n"
baseURL = 'http://tieba.baidu.com/p/' + str(raw_input(u'http://tieba.baidu.com/p/'))	
	
print u"是否只获取楼主发言，是输入1，否输入0\n"	
seeLZ = raw_input()

print u"是否写入楼层信息，是输入1，否输入0\n"
floorTag = raw_input()			

app=bdtb(BASEURL,seeLZ,floorTag)
app.start()
				
				
				
				
				
