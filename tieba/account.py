# -*- coding:utf-8 -*-
# login baidu

import cookielib
import urllib
import urllib2
import re
import gzip
from bs4 import BeautifulSoup
from StringIO import StringIO
from tieba_settings import *


class Account(object):
    """Login Baidu Account And Collect Info"""
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.login_baidu()
        
    def login_baidu(self):
        """use username and password to login"""
        # prepare:load cookiejar to save cookies
        cookie_jar = cookielib.LWPCookieJar()
        cookie_support = urllib2.HTTPCookieProcessor(cookie_jar)
        opener = urllib2.build_opener(cookie_support, urllib2.HTTPHandler)
        urllib2.install_opener(opener)
        print u'Login...'

        # first:visit index page to get the BAIDUID,save in the cookiejar
        indexRequest = urllib2.Request(url=INDEX_URL)
        while True:
            try:
                urllib2.urlopen(indexRequest, timeout=10)
            except Exception, e:
                print e
                continue
            else:
                break
        

        # second:get token(with BAIDUID)
        tokenRequest = urllib2.Request(url=TOKEN_URL)
        while True:
            try:
                tokenResponse = urllib2.urlopen(tokenRequest, timeout=10)
            except Exception, e:
                print e
                continue
            else:
                break

        tokenInfo = tokenResponse.read()
        # print tokenInfo

        # the response forms like following
        # {"errInfo":{ "no": "0" },
        #   "data": { "rememberedUserName" : "", 
        #             "codeString" : "",
        #             "token" : "5b576b5d5a4afc302633c1a65d990f7a", 
        #             "cookie" : "1", "usernametype":"",
        #             "spLogin" : "rate", 
        #             "disable":"", 
        #             "loginrecord":{ 'email':[ ], 'phone':[ ] }
        #           }
        # }

        matchVal = re.search(u'"token" : "(?P<tokenVal>.*?)"', tokenInfo)
        tokenVal = matchVal.group('tokenVal')
        # print '=======token is '+tokenVal+'========='

        # visit login url and post data
        rawdata = {
            'charset': 'UTF-8',
            'token': tokenVal,
            'isPhone': 'false',  
            'u': 'https://passport.baidu.com/',
            'loginType': '1',          
            'username': self.username.encode('utf-8'),
            'password': self.password, 
            'tpl': 'pp',
            'staticpage': 'https://passport.baidu.com/static/passpc-account/html/v3Jump.html',
            'verifycode': 'nlvv',       
            'callback': "parent.bd__pcbs__ra48vi"
        }

        self.post_data(rawdata)

    def post_data(self, rawdata):
        postData = urllib.urlencode(rawdata)
        loginRequest = urllib2.Request(LOGIN_URL, postData, HEADERS)
        loginResponse = urllib2.urlopen(loginRequest, timeout=5)
        #several ways to know whether login successful


        #first:make sure PTOKEN,STOKEN,SAVEUSERID,PASSID are in response info
        #print loginResponse.info()
        '''
        Set-Cookie: PTOKEN=deleted; expires=Sun, 20-Apr-2014 03:40:38 GMT; path=/; domai
        n=baidu.com; httponly
        Set-Cookie: PTOKEN=63cd1940a5de3737de5a8cbd02154a26; expires=Fri, 07-Jul-2023 03
        :40:39 GMT; path=/; domain=passport.baidu.com; httponly
        Set-Cookie: STOKEN=8abaecc88b5d709807e4ee18cb3589435ef9e45e511cef05689dbf5eb0aba
        291; expires=Fri, 07-Jul-2023 03:40:39 GMT; path=/; domain=passport.baidu.com; h
        ttponly
        Set-Cookie: SAVEUSERID=665821d9ac7537beb4e699e036423b36df2af9; expires=Fri, 07-J
        ul-2023 03:40:39 GMT; path=/; domain=passport.baidu.com; httponly
        Set-Cookie: USERNAMETYPE=1; expires=Fri, 07-Jul-2023 03:40:39 GMT; path=/; domai
        n=passport.baidu.com; httponly
        Set-Cookie: UBI=fi_PncwhpxZ%7ETaJc0i8bafLQmtE9sCuuORhjfZ4TYw64bmf%7EtepJH3mB3dVK
        6QPpXsNJanEq66CJo8oMEqPZl8AphK%7EMrqKcYCDyBs67DmqTaolBJTxRsSqI85Qwa7o0JZ%7E0q-aT
        67RdMT1OBBCLDCKU1e7; expires=Fri, 07-Jul-2023 03:40:39 GMT; path=/; domain=passp
        ort.baidu.com; httponly
        Set-Cookie: PASSID=SXsQAD; expires=Sun, 20-Apr-2014 03:40:39 GMT; path=/; domain
        =passport.baidu.com; httponly
        '''



        # second:the response self is a gzip file,unzip file and get the link
        bufferr = StringIO(loginResponse.read())
        f = gzip.GzipFile(fileobj=bufferr)
        loginResponse = f.read()
        # print loginResponse
        URL_matcher = re.search(u"encodeURI\('(?P<URL>.*?)'\)", loginResponse)
        redirectURL = URL_matcher.group('URL')
        # print redirectURL
        # the link is like following
        '''
        https://passport.baidu.com/static/passpc-account/html/v3Jump.html?hao123Param=Zz
        JhSGQzVkhjNGNGUlBNRVZMYlV0YVNYazVTa2xMUWtRdE1FTnJRblZuT1dkeVRXRlBOMlZYU2tsQlZuaF
        dRVUZCUVVGQkpDUUFBQUFBQUFBQUFBRUFBQUJYbTk4aXdhTFd2cmUwMDZiSzFBQUFBQUFBQUFBQUFBQU
        FBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFFaD
        BORlZJZERSVmRq&callback=parent.bd__pcbs__ra48vi&index=0&codestring=&username=%E7
        %AB%8B%E5%BF%97%E5%8F%8D%E5%BA%94%E8%AF%95&phonenumber=&mail=&tpl=pp&u=https%3A%
        2F%2Fpassport.baidu.com%2F&needToModifyPassword=0&gotourl=&auth=&error=0
        '''
        # and notice the last "error=0",that means login successful.
        if 'error=0' in redirectURL:
            # print rawdata['username']+u' logged in!'
            return True
        # 'error=257'，need to input verifycode
        elif 'error=257' in redirectURL:
            # match verify code
            vcodeMatch = re.search(r'codestring=tcIcaptchaservice\S+&username', redirectURL)
            # cut the string
            vcodeNum = vcodeMatch.group(0)[11:-9]
            # add into the post data
            rawdata['codestring'] = vcodeNum
            # get vcode img url
            vcodeUrl = 'https://passport.baidu.com/cgi-bin/genimage?' + vcodeNum
            # print vcodeUrl
            vcodeRequest = urllib2.Request(vcodeUrl)
            vcodeResponse = urllib2.urlopen(vcodeRequest)
            # down the vcode img
            with open('vcode.jpg','wb') as out:
                out.write(vcodeResponse.read())
                out.flush()
            # input vcode
            vcode = raw_input(u'input vcode:')
            rawdata['verifycode'] = vcode
            # post data again
            self.post_data(rawdata)
        else:
            # print u'登录失败'
            return False

    def get_bars(self):
        """get bars that account like"""
        # visit the user's info center
        infoRequest = urllib2.Request(url=INFO_URL)
        infoResponse = urllib2.urlopen(infoRequest, timeout=5)
        with open('test.html', 'w') as out:
           out.write(infoResponse.read())# output the page to see
        infoPage=BeautifulSoup(infoResponse, "lxml")
        # print infoPage
        # m=infoPage.find('a',attrs={'class':'ibx-uc-nick'})
        page_count = 1
        like_tieba = []

        def has_title_but_no_class(tag):
            return tag.has_attr('title') and not tag.has_attr('class')
        while True:
            like_tieba_url = 'http://tieba.baidu.com/f/like/mylike?&pn=%d' % page_count
            fetchRequest = urllib2.Request(like_tieba_url)
            fetchResponse = urllib2.urlopen(fetchRequest).read()
            fetchPage = BeautifulSoup(fetchResponse, "lxml")

            bar_boxs = fetchPage.find_all(has_title_but_no_class)
            # print bar_boxs
            temp_like_tieba = [{'name': bar['title'].encode('utf-8'), 'link':'http://tieba.baidu.com'+bar['href']} for bar in bar_boxs]
            # each bar is a tuple with name and link
            if not temp_like_tieba:
                break
            if not like_tieba:
                like_tieba = temp_like_tieba
            else:
                like_tieba += temp_like_tieba
            page_count += 1
        return like_tieba


#if __name__ == '__main__':
    # user=USER_LIST[0]
    # account = Account(user['username'],user['password'])
    # bars = account.get_bars()
    # print bars
