# -*- coding: utf-8 -*-

import urllib
import urllib2
import re

from bs4 import BeautifulSoup
import sys
reload(sys)
sys.setdefaultencoding( "utf-8" )

error = {"error_code": "", "reason": "", "result": []}

LOGIN_URL = 'http://metalib.lib.whu.edu.cn/pds'  # 登录处理链接

SEARCH_URL="http://www.lib.whu.edu.cn/web/index.asp?obj_id=263"

def getcookie(sid, pwd):  # 登录获得cookie字符串
    if sid and pwd:
        postdata = {'func': 'login', 
            'calling_system': 'mrbs', 
            'term1': 'short', 
            'selfreg': '', 
            'bor_id': sid,
            'bor_verification': pwd, 
            'institute': 'WHU',
            'url': 'http://metalib.lib.whu.edu.cn:80/pds?'}  # POST数据
        data = urllib.urlencode(postdata)  # 编码
        #data = data.encode('utf-8')
        #处理请求
        try:
            resultSoup = BeautifulSoup(urllib2.urlopen(urllib2.Request(url=LOGIN_URL, data=data), timeout=4), 'lxml')  # 处理返回链接
        except Exception, e:
            error["error_code"] = 10003
            error["reason"] =u"网络连接错误"
            error["result"] = []
            return error
        else:
            rawLink = resultSoup.find_all("a", attrs={"href": re.compile("pds_handle")})  # 抓取含有pds_handle的链接
            if rawLink:
                href = rawLink[0]["href"]  # 获取链接
                p = re.compile("=(.*)&(.*)&")
                pattern = p.split(href)
                pds_handle = pattern[1]  # 匹配并截取pds_handle的数字部分内容
                cookie = "PDS_HANDLE=" + pds_handle  # 形成cookie字符串
                return cookie
            else:
                error["error_code"] = 10000
                error["reason"] = u"验证错误"
                error["result"] = [
                    {
                        "field": "sid",
                        "error_code": 10001,
                        "reason": u"学号或密码错误"
                    }, {
                        "field": "pwd",
                        "error_code": 10001,
                        "reason": u"学号或密码错误"
                    }
                ]
                return error
    else:
        error["error_code"] = 10000
        error["reason"] = u"验证错误"
        error["result"] = [
            {
                "field": "sid",
                "error_code": 10002,
                "reason": u"数据不完整"
            }, {
                "field": "pwd",
                "error_code": 10002,
                "reason": u"数据不完整"
            }
        ]
        return error

#查询历史借阅
def queryhistory(cookie):
    # 带cookie访问网址，转到登陆界面
    finalbooklist = []

    handpage = 'http://opac.lib.whu.edu.cn:80/F/?func=bor-history-loan&amp;adm_library=WHU50&%s&afedog-flow-item=A8EA28FAD1EB4BECBD4E42B29AF605ED' % cookie  # 历史借阅
    try:
        redirectSoup = BeautifulSoup(urllib2.urlopen(urllib2.Request(url=handpage),timeout=10), 'lxml')
    except Exception, e:
        error["error_code"] = 10003
        error["reason"] =u"网络连接错误"
        error["result"] = []
        return error
    else:
        # 获取自动登录后的信息界面
        js = redirectSoup.find(text=re.compile(r"url\S"))
        p = re.compile(r"http://opac\S+\'")
        # 抓取登陆后要访问的网址
        redirectUrl = p.findall(js)[0]
        try:
            resultSoup = BeautifulSoup(urllib2.urlopen(urllib2.Request(url=redirectUrl), timeout=10), 'lxml')  # 抓取信息界面
        except Exception, e:
            error["error_code"] = 10003
            error["reason"] =u"网络连接错误"
            error["result"] = []
            return error
        else:
            td = resultSoup.find_all('td',{'class':'td1'})  # 抓取图书信息
            if len(td) == 0:
                error["error_code"] = 10004
                error["reason"] = "登录失败"
                error["result"] = []
                return error
            else:
                td=td[1:]  # 删除第一个抓取到的值（没有用）
                #print td
                allinfo = []
                book = {}
                for i in td:
                    if not i.string:
                        i.string = str(0)  # 把空白的罚款数定为0
                        allinfo.append(i.string)
                    else:
                        allinfo.append(i.string)
                while len(allinfo) >= 8:
                    onebook = allinfo[0:10]
                    #print onebook
                    book["编号"] = onebook[0]
                    book["书名"] = onebook[2]
                    book["罚款数目"] = onebook[8]
                    #print book
                    finalbooklist.append(book)
                    book={}
                    allinfo = allinfo[10:]  # 每本书以一个列表的形式存储
                return finalbooklist
#查询当前借阅信息
def queryloan(cookie):
    # 带cookie访问网址，转到登陆界面
    handpage = 'http://opac.lib.whu.edu.cn:80/F/?func=bor-loan&amp;adm_library=WHU50&%s&afedog-flow-item=A8EA28FAD1EB4BECBD4E42B29AF605ED' % cookie  # 历史借阅
    req = urllib2.Request(url=handpage)
    try:
        soup = BeautifulSoup(urllib2.urlopen(req, timeout=4), 'lxml')
    except Exception, e:
        error["error_code"] = 10003
        error["reason"] = u"网络连接错误"
        error["result"] = []
        return error
    else:
        page = str(soup)  # 获取自动登录后的信息界面
        js = soup.find(text=re.compile(r"url\S"))
        p = re.compile(r"http://opac\S+\'")
        url_ = p.findall(js)[0]
        req2 = urllib2.Request(url=url_)  # 抓取登陆后要访问的网址
        try:
            soup2 = BeautifulSoup(urllib2.urlopen(req2, timeout=4), 'lxml')  # 抓取信息界面
        except Exception, e:
            error["error_code"] = 10003
            error["reason"] = u"网络连接错误"
            error["result"] = []
            return error
        else:
            td = soup2.find_all(class_=re.compile("td1"))  # 抓取图书信息
            if len(td) == 0:
                error["error_code"] = 10004
                error["reason"] = u"登录信息错误"
                error["result"] = []
                return error
            allinfo = []  # 初始抓取的所有信息存在该列表
            rawbooklist = []  # 原始书籍信息
            finalbooklist = []  # 经过删减的最终书籍信息
            book = {}  # 每本书以一个字典存储
            for i in td:
                if not i.string:
                    i.string = str(0)  # 把空白的罚款数定为0
                    allinfo.append(i.string)
                else:
                    allinfo.append(i.string)
            while len(allinfo) >= 12:
                onebook = allinfo[0:12]
                rawbooklist.append(onebook)
                allinfo = allinfo[12:]  # 每本书以一个列表的形式存储
            for each in rawbooklist:
                del each[1]  # 删去checkbox
                del each[1]  # 删去作者
                del each[2]  # 删去出版年份
                del each[3]  # 删去出版年份
                del each[4]
                del each[4]
                del each[4]
                del each[4]
                book["编号"] = each[0]
                book["书名"] = each[1]
                book["应还日期"] = each[2]
                book["罚款数目"] = each[3]
                finalbooklist.append(book)
                book = {}
        return finalbooklist
#全部续借
def renewall(cookie):
    # 带cookie访问网址，转到登陆界面
    handpage = 'http://opac.lib.whu.edu.cn:80/F/?func=bor-loan&amp;adm_library=WHU50&%s&afedog-flow-item=A8EA28FAD1EB4BECBD4E42B29AF605ED' % cookie  # 历史借阅
    req1 = urllib2.Request(url=handpage)
    req1.add_header('Cookie', cookie)
    try:
        soup1 = BeautifulSoup(urllib2.urlopen(req1, timeout=4), 'lxml')
    except Exception, e:
        error["error_code"] = 10003
        error["reason"] = u"网络连接错误"
        error["result"] = []
        return error
    else:
        page = str(soup1)  # 获取自动登录后的信息界面
        js = soup1.find(text=re.compile(r"url\S"))
        p = re.compile(r"http://opac\S+\'")
        url1 = p.findall(js)[0]
        req2 = urllib2.Request(url=url1)  # 抓取登陆后要访问的网址
        try:
            soup2 = BeautifulSoup(urllib2.urlopen(req2, timeout=4), 'lxml')  # 抓取信息界面
        except Exception, e:
            error["error_code"] = 10003
            error["reason"] = u"网络连接错误"
            error["result"] = []
            return error
        else:
            #page2 = str(soup2)
            link= soup2.find("a", attrs={"href": re.compile("javascript:replacePage")})#抓取全部续借的链接
            url2=p.findall(link["href"])[0]
            req3 = urllib2.Request(url=url2) 
            try:
                soup3 = BeautifulSoup(urllib2.urlopen(req3, timeout=4), 'lxml')  # 访问链接抓取页面
            except Exception, e:
                error["error_code"] = 10003
                error["reason"] = u"网络连接错误"
                error["result"] = []
                return error
            else:
                page3=str(soup3)#根据页面信息判断情况
                #print page3
                info=soup3.find("div",attrs={"class":"title"}).string
                if "续借不成功" in info:
                    error["error_code"] = 10005
                    error["reason"] = u"已达到续借限制"
                    error["result"] = []
                    return error
                elif "续借的单册" in info:
                    return u"续借成功"
                else:
                    error["error_code"] = 10006
                    error["reason"] = u"未知错误"
                    error["result"] = []
                    return error

def renew(cookie,number):#需要续借的图书编号，在查询时有提供
    # 带cookie访问网址，转到登陆界面
    handpage = 'http://opac.lib.whu.edu.cn:80/F/?func=bor-loan&amp;adm_library=WHU50&%s&afedog-flow-item=A8EA28FAD1EB4BECBD4E42B29AF605ED' % cookie  # 历史借阅
    req1 = urllib2.Request(url=handpage)
    req1.add_header('Cookie', cookie)
    try:
        soup1 = BeautifulSoup(urllib2.urlopen(req1, timeout=4), 'lxml')
    except Exception, e:
        error["error_code"] = 10003
        error["reason"] = u"网络连接错误"
        error["result"] = []
        return error
    else:
        page = str(soup1)  # 获取自动登录后的信息界面
        js1= soup1.find(text=re.compile(r"url\S"))
        p = re.compile(r"http://opac\S+\'")
        url1 = p.findall(js1)[0]
        req2 = urllib2.Request(url=url1)  # 抓取登陆后要访问的网址
        try:
            soup2 = BeautifulSoup(urllib2.urlopen(req2, timeout=4), 'lxml')  # 抓取信息界面
        except Exception, e:
            error["error_code"] = 10003
            error["reason"] = u"网络连接错误"
            error["result"] = []
            return error
        else:
            js2= soup2.find(text=re.compile(r"strData\S"))#抓取续借的链接
            books=soup2.find_all("input",attrs={"type":"checkbox"})
            bookid=books[number-1]["name"]
            p = re.compile(r"http://opac\S+50")
            url2 = p.findall(js2)[0]+"&"+bookid+"=Y"
            req3 = urllib2.Request(url=url2) 
            try:
                soup3 = BeautifulSoup(urllib2.urlopen(req3, timeout=4), 'lxml')  # 访问链接抓取页面
            except Exception, e:
                error["error_code"] = 10003
                error["reason"] = u"网络连接错误"
                error["result"] = []
                return error
            else:
                page3=str(soup3)#根据页面信息判断情况
                #print page3
                info=soup3.find("div",attrs={"class":"title"}).string
                if "续借不成功" in info:
                    error["error_code"] = 10005
                    error["reason"] = u"已达到续借限制"
                    error["result"] = []
                    return error
                elif "续借的单册" in info:
                    return u"续借成功"
                else:
                    error["error_code"] = 10006
                    error["reason"] = u"未知错误"
                    error["result"] = []
                    return error
#按关键词检索图书
def searchbook(cookie,searchword):
    searchRequest=urllib2.Request(SEARCH_URL)
    try:
        redirectSoup = BeautifulSoup(urllib2.urlopen(searchRequest, timeout=10), 'lxml')
    except Exception, e:
        error["error_code"] = 10003
        error["reason"] = u"网络连接错误"
        error["result"] = []
        return error
    else:
        redirectJs = redirectSoup.find(text=re.compile(r"url\S"))
        p = re.compile(r"http://opac\S+\?")
        redirectUrl = p.findall(redirectJs)[0]
        resultUrl=redirectUrl+"func=find-b&%s&request=%s" % (cookie,searchword)
        resultRequest = urllib2.Request(url=resultUrl)  # 抓取登陆后要访问的网址
        try:
            resultResponse=urllib2.urlopen(resultRequest, timeout=10)
            #print resultResponse.read()
        except Exception, e:
            error["error_code"] = 10003
            error["reason"] = u"网络连接错误"
            error["result"] = []
            return error
        else:
            resultSoup = BeautifulSoup(resultResponse, 'lxml')  # 抓取信息界面
            #print resultSoup
            divs_1=resultSoup.find_all('div',{'class':'itemtitle'})
            conditions_1=resultSoup.find_all('u')
            cover_all_1=resultSoup.find_all('td',{'class':'cover'})#封面图片+二维码
            cover_extra_1=resultSoup.find_all('td',{'class':'cover','id':'opac_qr'})#二维码
            covers_1=[c for c in cover_all_1 if c not in cover_extra_1]#封面
            #for c in covers:
                #print c.next.nextSibling.nextSibling.next['src']
            books_1=[{'Num':str(i),
                    'name':divs_1[i].next.string,
                    'condition':conditions_1[i].string,
                    'cond_link':conditions_1[i].parent['href'],
                    'book_cover':covers_1[i].next.nextSibling.nextSibling.next['src']
                    } for i in range(len(divs_1))]
            nextpageUrl=redirectUrl+"func=short-jump&jump=11"
            nextpageRequest=urllib2.Request(nextpageUrl)#抓取头两页
            try:
                nextpageSoup=BeautifulSoup(urllib2.urlopen(nextpageRequest,timeout=10), 'lxml')
            except Exception, e:
                error["error_code"] = 10003
                error["reason"] = u"网络连接错误"
                error["result"] = []
                return error
            else:
                #print nextPageSoup
                divs_2=nextpageSoup.find_all('div',{'class':'itemtitle'})

                conditions_2=resultSoup.find_all('u')
                cover_all_2=resultSoup.find_all('td',{'class':'cover'})
                cover_extra_2=resultSoup.find_all('td',{'class':'cover','id':'opac_qr'})
                covers_2=[c for c in cover_all_2 if c not in cover_extra_2]
                books_2=[{'Num':str(i),
                        'name':divs_2[i].next.string.encode('utf-8'),
                        'condition':conditions_2[i].string,
                        'cond_link':conditions_2[i].parent['href'],
                        'book_cover':covers_2[i].next.nextSibling.nextSibling.next['src']
                        } for i in range(len(divs_2))]
                for book in books_2:
                    if book not in books_1:
                        books_1.append(book)
                if len(books_1)>0:
                    return books_1
                else:
                    return "no result"
                    
                
#按编号预约书籍
def orderbook(cookie,book_to_order):
    check_orderUrl=book_to_order['cond_link']
    checkorderRequest=urllib2.Request(check_orderUrl+'&%s' % cookie)
    checkorderSoup=BeautifulSoup(urllib2.urlopen(checkorderRequest,timeout=10), 'lxml')
    #print checkorderSoup
    order=checkorderSoup.find('a',{'href':re.compile('func=item-hold-request')})
    if order:
        orderUrl=order['href']
        orderSoup=BeautifulSoup(urllib2.urlopen(urllib2.Request(orderUrl),timeout=10), 'lxml')
        orderForm=orderSoup.find('form')
        rootUrl_1=orderForm['action']
        input_data_1=orderSoup.find_all('input')
        orderData={inp['name']:inp['value'] for inp in input_data_1[:-1]}
        orderData['PICKUP']=orderSoup.find('option')['value']
        orderData=urllib.urlencode(orderData)
        orderRequest=urllib2.Request(rootUrl_1+'&%s' % cookie,data=orderData)
        resultSoup=BeautifulSoup(urllib2.urlopen(orderRequest,timeout=10))
        if u'预约请求细节' in str(resultSoup):
            return 'order succeed'
        else:
            return 'order failed'
    else:
        error["error_code"] = 10007
        error["reason"] =u"no aviliable order"
        error["result"] = []
        return error
#查询已预约书籍
def queryorder(cookie):
    orderPage='http://opac.lib.whu.edu.cn/F/?func=bor-hold&adm_library=WHU50&%s&afedog-flow-item=A8EA28FAD1EB4BECBD4E42B29AF605ED' % cookie
    orders=[]
    singleOrder={}
    try:
        RedirectSoup=BeautifulSoup(urllib2.urlopen(urllib2.Request(orderPage)), 'lxml')
    except Exception, e:
        error["error_code"] = 10003
        error["reason"] =u"网络连接错误"
        error["result"] = []
        return error
    else:
        #page = str(RedirectSoup)  # 获取自动登录后的信息界面
        js = RedirectSoup.find(text=re.compile(r"url\S"))
        p = re.compile(r"http://opac\S+\'")
        url_ = p.findall(js)[0]
        req2 = urllib2.Request(url=url_)  # 抓取登陆后要访问的网址
        try:
            querySoup = BeautifulSoup(urllib2.urlopen(req2, timeout=4), 'lxml')  # 抓取信息界面
        except Exception, e:
            error["error_code"] = 10003
            error["reason"] =u"网络连接错误"
            error["result"] = []
            return error
        else:
            #print querySoup
            rawInfo=querySoup.find_all('td',{'class':'td1'})#抓取所有预约相关信息
            allorderInfo=rawInfo[1:]#去掉开头的无关信息
            #print allorderInfo
            while len(allorderInfo)>=13:#每13条为一条预约信息
                singleOrderL=allorderInfo[:13]
                singleOrder={'Num':singleOrderL[0].next.string.rstrip(),
                            'cancel_link':singleOrderL[0].next['href'],
                            'name':singleOrderL[2].string,
                            'from':singleOrderL[3].string,
                            'to':singleOrderL[4].string,
                            'location':singleOrderL[6].string,
                            'return_time':singleOrderL[7].string}#列表中重要信息对应存储在字典中
                orders.append(singleOrder)#单个预约信息加入列表中
                allorderInfo=allorderInfo[13:]
            return orders
#删除预约请求
def deleteorder(cookie,order_to_delete):
    infoUrl=order_to_delete['cancel_link']
    try:
        infoSoup=BeautifulSoup(urllib2.urlopen(urllib2.Request(infoUrl), timeout=10), 'lxml')
    except Exception, e:
        error["error_code"] = 10003
        error["reason"] =u"网络连接错误"
        error["result"] = []
        return error
    else:
        #print infoSoup
        delete_link=infoSoup.find('a',{'href':re.compile(r'DELETE')})['href']
        #print delete_link
        try:
            resultSoup=BeautifulSoup(urllib2.urlopen(urllib2.Request(delete_link), timeout=10), 'lxml')
        except Exception, e:
            error["error_code"] = 10003
            error["reason"] =u"网络连接错误"
            error["result"] = []
            return error
        else:
            #print resultSoup
            if u'管理库' in str(resultSoup):
                return 'cancel succeed'
            else:
                return 'cancel failed'



if __name__ == '__main__':

    cookie=getcookie('2013302480033','114028')

    booksinfo= searchbook(cookie,'编程珠玑')
    # print booksinfo
    # print booksinfo[0]['condition']+booksinfo[0]['cond_link']
    #             book_to_order=None
    #             for book in booksinfo:
    #                 if book['Num']=='2':
    #                     book_to_order=book
    #                 else:
    #                     pass
    #             #print book_to_order
    #             if book_to_order:
    #                 print orderbook(cookie,book_to_order)
    #             print  queryorder(cookie)
    #             orders=queryorder(cookie)
    #             order_to_delete=None
    #             for order in orders:
    #                 if order['Num']=='1':
    #                     order_to_delete=order
    #
    #             if order_to_delete:
    #                 print deleteorder(cookie,order_to_delete)
