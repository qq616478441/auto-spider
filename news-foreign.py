#!/usr/bin/python
# encoding: utf-8
import chardet
import json
import requests
import os
import time
import urllib
import re
import MySQLdb
import sys
import re
import json
from google import *
from scrapy.selector import Selector
from scrapy.http import HtmlResponse
#1491876516
DBUG   = 0
current_time=time.time()
print int(current_time)


reload(sys)
sys.setdefaultencoding('utf-8')
params={"category":"news_society",\
          "utm_source":'toutiao',\
             "widen":'1',\
              "max_behot_time":int(current_time),\
                 "max_behot_time_tmp":int(current_time),\
                 "tadrequire":"true",\
                      "as":"A1E5D8FEEC88ACF",\
                            "cp":"58EC98CACC9F6E1"}




headers={"Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",\
         "Accept-Encoding":"gzip, deflate, sdch, br",\
	   "Accept-Language":"en-US,en;q=0.5",\
	   "Connection":"keep-alive",\
         "Cookie":"bf-browser-language=en-US,en; bf-geo-country=CN; bf_visit=b%26u%3D.lbpzw6Rgn%26v%3D2.0%26c%3D4511909\
; __utma=219708042.2129868372.1492848003.1492848003.1492848003.2; __utmc=219708042; __utmz=219708042\
.1492848003.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); __gads=ID=c19934645d0f1b7e:T=1492848003\
:S=ALNI_MbBHficCNnrtc_cKtrwkLnfGpy-bQ; __utmv=219708042.|6=isRegistered=false=1^7=signupDate=false=1\
^8=facebookConnected=false=1^9=registrationPath=false=1^10=userFlags=false=1^11=allowsEmailUpdates=false\
=1^14=origReferrer=(direct)=1^15=origPageType=Sports=1^18=lastVisit=1492852452=1^28=categoryCounts=11\
%2C11%2C11%2C11%2C11%2C11%2C11%2C11%2C11=1^35=intlEdition=us=1^43=nDHPV=0=1; __qca=P0-587625795-1492848037626\
; __utmb=219708042.82.9.1492853703721",\
 "User-Agent":"Mozilla/5.0 (X11; Linux x86_64; rv:45.0) Gecko/20100101 Firefox/45.0",\
"Host":"www.buzzfeed.com",\
"Referer":	"https://www.buzzfeed.com/sports"}


reBODY =re.compile( r'<body.*?>([\s\S]*?)<\/body>', re.I)
reCOMM = r'<!--.*?-->'
reTRIM = r'<{0}.*?>([\s\S]*?)<\/{0}>'
reTAG  = r'<[\s\S]*?>|[ \t\r\f\v]'

reIMG  = re.compile(r'<img[\s\S]*?src=[\'|"]([\s\S]*?)[\'|"][\s\S]*?>')

class Extractor():
    def __init__(self, url = "", blockSize=3, timeout=5, image=False):
        self.url       = url
        self.blockSize = blockSize
        self.timeout   = timeout
        self.saveImage = image
        self.rawPage   = ""
        self.ctexts    = []
        self.cblocks   = []

    def getRawPage(self):
        try:
            resp = requests.get(self.url,headers=headers, timeout=self.timeout)
        except Exception as e:
            raise e

        if DBUG: print(resp.encoding)

        resp.encoding = "UTF-8"
        info=chardet.detect(resp.content).get('encoding','utf-8')
        html=resp.content.decode(info,'ignore').encode('utf-8')  
        return resp.status_code, html

    def processTags(self):
        self.body = re.sub(reCOMM, "", self.body)
        self.body = re.sub(reTRIM.format("script"), "" ,re.sub(reTRIM.format("style"), "", self.body))
        # self.body = re.sub(r"[\n]+","\n", re.sub(reTAG, "", self.body))
        self.body = re.sub(reTAG, "", self.body)

    def processBlocks(self):
        self.ctexts   = self.body.split("\n")
        self.textLens = [len(text) for text in self.ctexts]

        self.cblocks  = [0]*(len(self.ctexts) - self.blockSize - 1)
        lines = len(self.ctexts)
        for i in range(self.blockSize):
            self.cblocks = list(map(lambda x,y: x+y, self.textLens[i : lines-1-self.blockSize+i], self.cblocks))

        maxTextLen = max(self.cblocks)

        if DBUG: print(maxTextLen)

        self.start = self.end = self.cblocks.index(maxTextLen)
        while self.start > 0 and self.cblocks[self.start] > min(self.textLens):
            self.start -= 1
        while self.end < lines - self.blockSize and self.cblocks[self.end] > min(self.textLens):
            self.end += 1

        return "".join(self.ctexts[self.start:self.end])

    def processImages(self):
        self.body = reIMG.sub(r'{{\1}}', self.body)

    def getContext(self):
        code, self.rawPage = self.getRawPage()
        self.body = re.findall(reBODY, self.rawPage)[0]

        if DBUG: print(code, self.rawPage)

        if self.saveImage:
            self.processImages()
        self.processTags()
        return self.processBlocks()
        # print(len(self.body.strip("\n")))



params={"p":1,"z":"5GRI4C","r":"1"}
base_url="https://www.buzzfeed.com/sports"
url=base_url+'?'+urllib.urlencode(params)

while True:
	
	r=requests.get(url,headers=headers)
	print r.status_code
	ul_tag=Selector(text=r.text).xpath(".//*[@class='content']/div/ul/li").extract()
	try:
		for  i in range(len(ul_tag)):
			#try:
			text=ul_tag[i].decode('utf-8','ignore').encode('utf-8')
			content=re.findall(r"rel:data='{(.*?)}'",text)
			if len(content)==0:
				continue
			owner=re.findall(r"rel:owner=\"(.*?)\"",text)
			#print owner
			#print content[0]
			json_content=json.loads('{'+content[0]+'}')
			content_uri=json_content['uri']
			web_url="https://www.buzzfeed.com"+'/'+owner[0]+'/'+content_uri
			r=requests.get(web_url,headers=headers)
			print r.status_code
			http_div=Selector(text=r.text).xpath(".//*[@class='bf_dom c']/div/div/div/div").extract()
			str_temp=''
			for j in range(len(http_div)):
				http_content=http_div[j].decode('utf-8','ignore').encode('utf-8')
				http_div_content=Selector(text=http_content).xpath('.//h2').extract()
				#print re.sub(reTAG,' ',http_div_content[0].decode('utf-8','ignore').encode('utf-8'))
				http_p2_content=Selector(text=http_content).xpath('.//p').extract()
				if len(http_div_content)==0 or len(http_p2_content)==0:
					continue
				if len(http_div_content)!=0:
					http_div_content_str=re.sub(reTAG,' ',http_div_content[0].decode('utf-8','ignore').encode('utf-8'))
				if len(http_p2_content)!=0:
					temp=http_p2_content[0].decode('utf-8','ignore').encode('utf-8')
					http_p2_content_str=re.sub(reTAG,' ',temp)
				
				if http_div_content_str!='':
					#print http_div_content_str
					trans=Translate(http_div_content_str)
					http_div_content_str_trans=trans.get_trans()
					print http_div_content_str_trans.decode('utf-8','ignore').encode('utf-8')
					#print type(http_div_content_str_trans.decode('utf-8','ignore').encode('utf-8'))
					str_temp=str_temp+(http_div_content_str_trans.decode('utf-8','ignore').encode('utf-8'))
					#print str_temp
					 
				if http_p2_content_str!='':
					#print http_p2_content_str
					trans=Translate(http_p2_content_str)
					http_p2_content_str_trans=trans.get_trans()
					print http_p2_content_str_trans
					str_temp=str_temp+http_p2_content_str_trans.decode('utf-8','ignore').encode('utf-8')
					#str_temp=str_temp+http_p2_content_str
				#	str_temp=str_temp+(http_p2_content.decode('utf-8','ignore').encode('utf-8'))
				#print type(http_div_content[0].decode('utf-8','ignore').encode('utf-8'))
			#print str_temp
			s=re.sub(r'查看此图片\\u003e','',str_temp)
			print s
			
			
				#print str_temp
					#print type(http_div_content)
				
				
				#print str_temp
				#sub_h2=re.sub(r'<[^>]+>','',str1)
				#print sub_h2
		
	except:
		continue
		

	
