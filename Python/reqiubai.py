# -*- coding:utf-8 -*-
import urllib
import urllib2
import re
import thread
import time 
 

class qsbk:
    def __init__(self):
        self.pageIndex=1
        self.user_agent='Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.101 Safari/537.36'
        self.headers={'User-Agent':self.user_agent}
        self.stories=[]
        self.enable=False

    def getPage(self,pageIndex):
        try:
            url='http://www.qiushibaike.com/hot/page/'+str(pageIndex)
            request=urllib2.Request(url,headers=self.headers)
            response=urllib2.urlopen(request)
            page=response.read().decode('utf-8')
            return page
        except urllib2.URLError,e:
            if hasattr(e,"reason"):
                print u"连接百科失败，错误原因",e.reason
            return None
                
    def getPageItems(self,pageIndex):
        page=self.getPage(pageIndex)
        if not page:
            print "页面加载失败"
	    return None
        pattern = re.compile('<div.*?class="article block untagged mb15".*?<div.*?class="author.*?>.*?<a.*?</a>.*?<a.*?>(.*?)</a>.*?<div.*?class'+
                         '="content".*?title="(.*?)">(.*?)</div>(.*?)<div class="stats.*?class="number">(.*?)</i>',re.S)
        items=re.findall(pattern,page)
        pageStories=[]
        for item in items:
            havImg=re.search("img",item[3])
            if not havImg:
                pageStories.append([item[0],item[1],item[4],item[2]])
        return pageStories		
		
    def loadPage(self):
        if self.enable==True:
            if len(self.stories)<2:
                pageStories=self.getPageItems(self.pageIndex)
                if pageStories:
                    self.stories.append(pageStories)
                    self.pageIndex+=1

    def getOnestory(self,pageStories,page):
        for story in pageStories:
	    print u"正在读取糗事百科,按回车查看新段子，Q退出"
            input=raw_input()
            if input =="Q":
                self.enable=False
                return
            print u"第%d页\t发布人:%s发布时间:%s\t赞:%s%s\n" %(page,story[0],story[1],story[2],story[3])
				
    def start(self):

        self.enable=True
        self.loadPage()
        nowPage=0
        while self.enable:
             if len(self.stories)>0:
                pageStories=self.stories[0]
                nowPage+=1
                del self.stories[0]
                self.getOnestory(pageStories,nowPage)
                self.loadPage()
					
spider=qsbk()
spider.start()
                
		
		
		
		
		
		
		
		
		
		
