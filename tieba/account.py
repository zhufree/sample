#-*- coding:utf-8 -*-

import cookielib
import urllib
import urllib2
import re
import gzip
import json
import hashlib

from bs4 import BeautifulSoup
from StringIO import StringIO

from tieba_settings import *

import sys
default_encoding = 'utf-8'
if sys.getdefaultencoding() != default_encoding:
    reload(sys)
    sys.setdefaultencoding(default_encoding)


class Account(object):

    """Login Baidu Account And Collect Info"""

    def __init__(self, username, password):

        """ login """

        self.username = username
        self.password = password
        self.login_baidu()

    def login_baidu(self):

        """
        use username and password to login
        :param username: baidu ID, not phonenumber or email
        :param password: pasword
        :return: True or False
        """

        # prepare:load cookiejar to save cookies
        cookie_jar = cookielib.LWPCookieJar()
        cookie_support = urllib2.HTTPCookieProcessor(cookie_jar)
        opener = urllib2.build_opener(cookie_support, urllib2.HTTPHandler)
        urllib2.install_opener(opener)
        # print u'Login...'

        # first:visit index page to get the BAIDUID,save in the cookiejar
        indexRequest = urllib2.Request(url=INDEX_URL)
        urllib2.urlopen(indexRequest, timeout=5)

        # second:get token(with BAIDUID)
        tokenRequest = urllib2.Request(url=TOKEN_URL)
        tokenResponse = urllib2.urlopen(tokenRequest, timeout=5)

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
        rawData = {
            'charset': 'UTF-8',
            'token': tokenVal,
            'isPhone': 'false',
            'u': 'https://passport.baidu.com/',
            'loginType': '1',
            'username': self.username,
            'password': self.password,
            'tpl': 'pp',
            'staticpage': 'https://passport.baidu.com/static/passpc-account/html/v3Jump.html',
            'verifycode': 'nlvv',
            'callback': "parent.bd__pcbs__ra48vi"
        }

        self.post_data(rawData)

    def post_data(self, rawData):
        """ 
        post data to login
        :param rawData: raw data dict.
        :return: True or False
        """
        postData = urllib.urlencode(rawData)
        loginRequest = urllib2.Request(LOGIN_URL, postData, HEADERS)
        loginResponse = urllib2.urlopen(loginRequest, timeout=5)
        # several ways to know whether login successful

        # first:make sure PTOKEN,STOKEN,SAVEUSERID,PASSID are in response info
        # print loginResponse.info()

        # second:the response self is a gzip file,unzip file and get the link
        buffer_ = StringIO(loginResponse.read())
        f = gzip.GzipFile(fileobj=buffer_)
        loginResponse = f.read()
        # print loginResponse
        URL_matcher = re.search(u"encodeURI\('(?P<URL>.*?)'\)", loginResponse)
        redirectURL = URL_matcher.group('URL')
        # print redirectURL

        # "error=0",that means login successful.
        if 'error=0' in redirectURL:
            # print rawData['username']+u' logged in!'
            return True
        #'error=257'，need to input verifycode
        elif 'error=257' in redirectURL:
            # print redirectURL
            # match verify code
            vcodeMatch = re.search(r'codestring=\S+&username', redirectURL)
            # cut the string
            vcodeNum = vcodeMatch.group(0)[11:-9]
            print vcodeNum
            # add into the post data
            rawData['codestring'] = vcodeNum
            # get vcode img url
            vcodeUrl = 'https://passport.baidu.com/cgi-bin/genimage?' + \
                vcodeNum
            # print vcodeUrl
            vcodeRequest = urllib2.Request(vcodeUrl)
            vcodeResponse = urllib2.urlopen(vcodeRequest)
            # download the vcode img
            with open('vcode.jpg', 'wb') as out:
                out.write(vcodeResponse.read())
                out.flush()
            # input vcode
            vcode = raw_input(u'input vcode:')
            rawData['verifycode'] = vcode
            # post data again
            self.post_data(rawData)
        else:
            # print u'登录失败'
            return False

    def get_bars(self):
        """
        get bars that account like
        :need login first
        :return: a list contain tieba that user likes, each format is :
        {
            'name': 'XXXXXX',
            'link': 'http://tieba.baidu.com/?f=xxxxxx'
        }
        """

        def has_title_but_no_class(tag):
            return tag.has_attr('title') and not tag.has_attr('class')
        page_count = 1
        self.like_tiebas = []    
        while True:
            like_tieba_url = 'http://tieba.baidu.com/f/like/mylike?&pn=%d' % page_count
            fetchRequest = urllib2.Request(like_tieba_url)
            fetchResponse = urllib2.urlopen(fetchRequest).read()
            fetchPage = BeautifulSoup(fetchResponse, "lxml")
            bar_boxs = fetchPage.find_all(has_title_but_no_class)
            # print bar_boxs
            temp_like_tieba = [{
                'name': bar['title'].encode('utf-8'),
                'link':'http://tieba.baidu.com'+bar['href']
            } for bar in bar_boxs]
            # each bar is a tuple with name and link
            if not temp_like_tieba:
                break
            if not self.like_tiebas:
                self.like_tiebas = temp_like_tieba
            else:
                self.like_tiebas += temp_like_tieba
            page_count += 1
        return self.like_tiebas

    def fetch_tieba_info(self):
        """
        get info about each tieba and sign
        :need login first
        :param self.like_tiebas:
        :return: list contains info of a bar, each format like:
        {
            'name': 'XXXXXX',
            'link': 'http://tieba.baidu.com/?f=xxxxxx'
            'sign_status':[] or ['xxxx'],
            'tbs': 'xxxxxx',
            'fid': 'xxxxxx'
        }
        """
        self.like_tiebas_info = []
        for tieba_info in self.like_tiebas:
            tieba_wap_url = "http://tieba.baidu.com/mo/m?kw=" + tieba_info['name']
            wap_resp = urllib2.urlopen(tieba_wap_url).read()
            re_already_sign = '<td style="text-align:right;"><span[ ]>(.*?)<\/span><\/td><\/tr>'
            if re.findall(re_already_sign, wap_resp):
                tieba_info['sign_status'] = True
            else:
                tieba_info['sign_status'] = False
            re_fid = '<input type="hidden" name="fid" value="(.+?)"\/>'
            _fid = re.findall(re_fid, wap_resp)
            tieba_info['fid'] = _fid and _fid[0] or None
            re_tbs = '<input type="hidden" name="tbs" value="(.+?)"\/>'
            _tbs = re.findall(re_tbs, wap_resp)
            tieba_info['tbs'] = _tbs and _tbs[0] or None
            self.like_tiebas_info.append(tieba_info)
        return self.like_tiebas_info

    def auto_sign(self):
        """ 
        auto sign function 
        :need login first
        :param self.like_tiebas_info:
        :return self.like_tiebas_info: change the sign_status in self.like_tiebas_info
        """
        for tieba_info in self.like_tiebas_info:
            if tieba_info['sign_status']:
                pass
            else:
                tieba_info['sign_status'] = self.sign(
                    tieba_info['fid'], 
                    tieba_info['tbs'], 
                    tieba_info['name']
                    )
        return self.like_tiebas_info

    def sign(self, fid, tbs, kw):
        sign_post_data = {
            "_client_id": "03-00-DA-59-05-00-72-96-06-00-01-00-04-00-4C-43-01-00-34-F4-02-00-BC-25-09-00-4E-36",
            "_client_type": "4",
            "_client_version": "1.2.1.17",
            "_phone_imei": "540b43b59d21b7a4824e1fd31b08e9a6",
            "fid": fid,
            "kw": kw,
            "net_type": "3",
            'tbs': tbs
        }

        sign_post_data = self._decode_uri_post(sign_post_data)
        postData = urllib.urlencode(sign_post_data)

        signRequest = urllib2.Request(SIGN_URL, postData)
        signResponse = urllib2.urlopen(signRequest, timeout=5)
        signResponse = json.load(signResponse)
        # print signResponse
        error_code = signResponse['error_code']
        sign_bonus_point = 0
        try:
            # Don't know why but sometimes this will trigger key error.
            sign_bonus_point = int(
                signResponse['user_info']['sign_bonus_point'])
        except KeyError:
            pass
        if error_code == '0':
            return True
            # print tieba_info['kw']+u"吧 签到成功,经验+%d" % sign_bonus_point
        else:
            # print u'签到失败'
            # print "Error:" + unicode(error_code) + " " +
            # unicode(error_msg)
            return "Error:" + unicode(error_code)


    def _decode_uri_post(self, postData):
        """
        decode post data
        tool function, use when sign.
        :param postData: data to post when sign.
        :return: decoded data.
        """

        SIGN_KEY = "tiebaclient!!!"
        s = ""
        keys = postData.keys()
        keys.sort()
        for i in keys:
            s += i + '=' + postData[i]
        sign = hashlib.md5(s + SIGN_KEY).hexdigest().upper()
        postData.update({'sign': str(sign)})
        return postData


if __name__ == '__main__':
    def auto(user):
        account = Account(user['username'], user['password'])
        account.get_bars()
        account.fetch_tieba_info()
        account.auto_sign()
        for tieba_info in account.like_tiebas_info:
            print tieba_info['name'],tieba_info['sign_status']
        print 'end a user:'+user['username']
