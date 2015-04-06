# -*- coding:utf-8 -*-
import urllib
import urllib2
import re
import os 

class Tool:
    '''the processing Tool'''

    removeImg = re.compile('<img.*?>| {1,7}|&nbsp;') #去除img标签,1-7位空格,&nbsp;
    removeAddr = re.compile('<a.*?>|</a>')    #删除超链接标签
    replaceLine = re.compile('<tr>|<div>|</div>|</p>')    #把换行的标签换为\n
    replaceTD= re.compile('<td>')    #将表格制表<td>替换为\t
    replaceBR = re.compile('<br><br>|<br>')    #将换行符或双换行符替换为\n
    removeExtraTag = re.compile('<.*?>')    #将其余标签剔除
    removeNoneLine = re.compile('\n+')    #将多行空行删除
    
    def replace(self,x):
        x = re.sub(self.removeImg,"",x)
        x = re.sub(self.removeAddr,"",x)
        x = re.sub(self.replaceLine,"\n",x)
        x = re.sub(self.replaceTD,"\t",x)
        x = re.sub(self.replaceBR,"\n",x)
        x = re.sub(self.removeExtraTag,"",x)
        x = re.sub(self.removeNoneLine,"\n",x)
        return x.strip()        #strip()将前后多余内容删除
    
class Spider:
    ''' a script reptile taobao mm photo '''
    
    def __init__(self):
        self.user_agent='Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.101 Safari/537.36'
        self.headers={'User-Agent':self.user_agent}
        self.url='http://mm.taobao.com/json/request_top_list.htm'
        self.tool=Tool()

    def getPage(self,pageIndex):
        url=self.url+"?page="+str(pageIndex)
        print url
        request=urllib2.Request(url)
        reponse=urllib2.urlopen(request)
        return reponse.read().decode('gbk','ingore') 

    def getContents(self,pageIndex):
        page=self.getPage(pageIndex)
        pattern=re.compile('<div class="list-item".*?pic-word.*?<a href="(.*?)".*?<img src="(.*?)".*?<a class="lady-name.*?>(.*?)</a>.*?<strong>(.*?)</strong>.*?<span>(.*?)</span>',re.S)
        items=re.findall(pattern,page)
        contents=[]
        for item in items:
            contents.append([item[0],item[1],item[2],item[3],item[4]])
        return contents
            
    def getDetailPage(self,infoURL):
        response = urllib2.urlopen(infoURL)
        return response.read().decode('gbk')
 
    def getBrief(self,page):
        pattern = re.compile('<div class="mm-aixiu-content".*?>(.*?)<!--',re.S)
        result = re.search(pattern,page)
        return self.tool.replace(result.group(1))
    
    def getAllImg(self,page):
        pattern = re.compile('<div class="mm-aixiu-content".*?>(.*?)<!--',re.S)
        content = re.search(pattern,page)
        patternImg = re.compile('<img.*?src="(.*?)"',re.S)
        images = re.findall(patternImg,content.group(1))
        print images[0]
        return images
		

    def saveImgs(self,images,name):
        number = 1
        print u"发现",name,u"共有",len(images),u"张照片"
        for imageURL in images:
            splitPath = imageURL.split('.')
            fTail = splitPath.pop()
            if len(fTail) > 3:
                fTail = "jpg"
            fileName = name + "/" + str(number) + "." + fTail
            self.saveImg(imageURL,fileName)
            number += 1
            
    def saveImg(self,imageURL,fileName):
        u=urllib.urlopen(imageURL)
        data=u.read()
        with open(fileName,"wb") as f:
            f.write(data)

    def saveBrief(self,content,name):
        fileName=name+"/"+name+".txt"
        with open(fileName,"w+") as f:
            f.write(content.encode('utf-8'))

    def saveIcon(self,iconURL,name):
        splitPath = iconURL.split('.')
        fTail = splitPath.pop()
        fileName = name + "/icon." + fTail
        self.saveImg(iconURL,fileName)

    def mkdir(self,path):
        path=path.strip()
        if not os.path.exists(path):
            os.makedirs(path)
            return True
        else:
            return False

    def savePageInfo(self,pageIndex):
        contents = self.getContents(pageIndex)
        for item in contents:
            print u"发现一位模特,名字叫",item[2],u"芳龄",item[3],u",她在",item[4]
            print u"正在偷偷地保存",item[2],"的信息"
            print u"又意外地发现她的个人地址是",item[0]
            detailURL = item[0]
            detailPage = self.getDetailPage(detailURL)
            brief = self.getBrief(detailPage)
            images = self.getAllImg(detailPage)
            self.mkdir(item[2])
            self.saveBrief(brief,item[2])
            self.saveIcon(item[1],item[2])
            self.saveImgs(images,item[2])
    
    def savePages(self,start,end):
        for i in range(start,end+1):
            print u"正在偷偷寻找第",i,u"个地方，看看MM们在不在"
            self.savePageInfo(i)

app=Spider()
app.savePages(1,1)
























