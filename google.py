#!/usr/bin/python
# encoding: utf-8
import urllib
import urllib2
import execjs  
import requests
class Py4Js():  
      
    def __init__(self):  
        self.ctx = execjs.compile(""" 
        function TL(a) { 
        var k = ""; 
        var b = 406644; 
        var b1 = 3293161072; 
         
        var jd = "."; 
        var $b = "+-a^+6"; 
        var Zb = "+-3^+b+-f"; 
     
        for (var e = [], f = 0, g = 0; g < a.length; g++) { 
            var m = a.charCodeAt(g); 
            128 > m ? e[f++] = m : (2048 > m ? e[f++] = m >> 6 | 192 : (55296 == (m & 64512) && g + 1 < a.length && 56320 == (a.charCodeAt(g + 1) & 64512) ? (m = 65536 + ((m & 1023) << 10) + (a.charCodeAt(++g) & 1023), 
            e[f++] = m >> 18 | 240, 
            e[f++] = m >> 12 & 63 | 128) : e[f++] = m >> 12 | 224, 
            e[f++] = m >> 6 & 63 | 128), 
            e[f++] = m & 63 | 128) 
        } 
        a = b; 
        for (f = 0; f < e.length; f++) a += e[f], 
        a = RL(a, $b); 
        a = RL(a, Zb); 
        a ^= b1 || 0; 
        0 > a && (a = (a & 2147483647) + 2147483648); 
        a %= 1E6; 
        return a.toString() + jd + (a ^ b) 
    }; 
     
    function RL(a, b) { 
        var t = "a"; 
        var Yb = "+"; 
        for (var c = 0; c < b.length - 2; c += 3) { 
            var d = b.charAt(c + 2), 
            d = d >= t ? d.charCodeAt(0) - 87 : Number(d), 
            d = b.charAt(c + 1) == Yb ? a >>> d: a << d; 
            a = b.charAt(c) == Yb ? a + d & 4294967295 : a ^ d 
        } 
        return a 
    } 
    """)  
          
    def getTk(self,text):  
        return self.ctx.call("TL",text)  

headers={
"Host":"translate.google.cn",\
"Referer":"https://translate.google.cn/",\
"User-Agent":"Mozilla/5.0 (X11; Linux x86_64; rv:45.0) Gecko/20100101 Firefox/45.0"}
"""
"Cookie":"NID=101=kqcog2_rDL9JsKJVCH-GIxSO01y538cZsxNtTcHkMfAV5KCdfB1Wq8aGDbGKpspqnIbHIy6QjlezEyuNtC3BeT9GGS3W2dhvCMzeVuygMASpoBx8b7X51TbelLn0xcdl; _ga=GA1.3.1880085423.1492932139",\
"""
class Translate:
	def __init__(self,text):
		self.text=text
	def get_trans(self):
		self.js=Py4Js()
		self.tk=self.js.getTk(self.text)
		print self.tk
		self.t=urllib.quote(self.text)
		self.url="http://translate.google.cn/translate_a/single?client=t&sl=en&tl=zh-CN&hl=zh-CN&dt=at&dt=bd&dt=ex&dt=ld&dt=md&dt=qca&dt=rw&dt=rm&dt=ss&dt=t&ie=UTF-8&oe=UTF-8&source=btn&ssel=3&tsel=3&kc=0&tk=%s&q=%s"%(self.tk,self.t)
		print self.url
		self.r=requests.get(self.url,headers=headers)
		end=self.r.text.find("\",")
		if end>4:
			result=self.r.text[4:end]
			return result

"""
test='i love you too'
js=Py4Js()
tk=js.getTk(test)
print tk

t=urllib.quote(test)
print t
url="http://translate.google.cn/translate_a/single?client=t&sl=en&tl=zh-CN&hl=zh-CN&dt=at&dt=bd&dt=ex&dt=ld&dt=md&dt=qca&dt=rw&dt=rm&dt=ss&dt=t&ie=UTF-8&oe=UTF-8&source=btn&ssel=3&tsel=3&kc=0&tk=%s&q=%s"%(tk,t)
print url

r=requests.get(url,headers=headers)
print r.status_code
print r.text
end=r.text.find("\",")
if end>4:
	result=r.text[4:end]
	print result
"""
trans=Translate('i love you')
trans.get_trans()









