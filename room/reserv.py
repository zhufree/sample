#  -*-coding: utf-8-*-

from sgmllib import SGMLParser
import urllib
import urllib2
from bs4 import BeautifulSoup
import xml.etree.ElementTree as ET
import re
import datetime

now = datetime.datetime.now()

#  抓取空闲研修室的方法，输出格式见API文档

error = {"error_code": "", "reason": "", "result": ""}


class Reservelib(SGMLParser):

    def getroominfo(self, year, month, day, region):
        # 获取空闲研修室信息，参数为年月日和学部（1是本部，2是医学部）
        self.year = year
        self.month = month
        self.day = day
        self.region = region
        nump = re.compile("room=\d+")
        dic = {}
        # 返回字典格式见文档
        # 返回四个时间段分别空闲的房间号, 按时间存储
        # 本部
        if self.region == '1':
            dic['B1.2'] = {}   # area=6
            dic['B1.4'] = {}   # area=8
            dic['B1.8'] = {}   # area=8
            dic['B2.2'] = {}   # area=9
            url_1_6 = 'http://reserv.lib.whu.edu.cn/day.php?year=%s&month=%s&day=%s&area=6' % (
                year, month, day)
            url_1_8 = 'http://reserv.lib.whu.edu.cn/day.php?year=%s&month=%s&day=%s&area=8' % (
                year, month, day)
            url_1_9 = 'http://reserv.lib.whu.edu.cn/day.php?year=%s&month=%s&day=%s&area=9' % (
                year, month, day)
            # 根据日期和area访问相应页面（6，8，9是本部的三个区域）
            try:
                soup_1_6 = BeautifulSoup(
                    urllib2.urlopen(url_1_6, timeout=4), 'lxml')
                soup_1_8 = BeautifulSoup(
                    urllib2.urlopen(url_1_8, timeout=4), 'lxml')
                soup_1_9 = BeautifulSoup(
                    urllib2.urlopen(url_1_9, timeout=4), 'lxml')
            except Exception, e:
                error["error_code"] = 10003
                error["reason"] = e
                error["result"] = []
                return error
            else:
                s_1_6 = soup_1_6.find_all('a', {'class': 'new_booking'})
                s_1_8 = soup_1_8.find_all('a', {'class': 'new_booking'})
                s_1_9 = soup_1_9.find_all('a', {'class': 'new_booking'})
                # 抓取可以预订的空闲研修室链接
                rooms_2 = {}
                rooms_2['1'] = []
                rooms_2['2'] = []
                rooms_2['3'] = []
                rooms_2['4'] = []
                for i in s_1_6:
                    room = nump.findall(str(i))[0]
                    hour = re.search("hour=..", str(i)).group()
                    if hour == "hour=08":
                        rooms_2['1'].append(room[5:])
                    elif hour == "hour=11":
                        rooms_2['2'].append(room[5:])
                    elif hour == "hour=15":
                        rooms_2['3'].append(room[5:])
                    elif hour == "hour=18":
                        rooms_2['4'].append(room[5:])
            # 判断空闲时间段，并加入该研修室列表中，下同
                dic['B1.2'] = rooms_2
                rooms_4 = {}
                rooms_4['1'] = []
                rooms_4['2'] = []
                rooms_4['3'] = []
                rooms_4['4'] = []
                rooms_8 = {}
                rooms_8['1'] = []
                rooms_8['2'] = []
                rooms_8['3'] = []
                rooms_8['4'] = []
                for i in s_1_8:
                    room = nump.findall(str(i))[0]
                    hour = re.search("hour=..", str(i)).group()
                    if room == "room=105":
                        if hour == "hour=08":
                            rooms_8['1'].append(room[5:])
                        elif hour == "hour=11":
                            rooms_8['2'].append(room[5:])
                        elif hour == "hour=15":
                            rooms_8['3'].append(room[5:])
                        elif hour == "hour=18":
                            rooms_8['4'].append(room[5:])
                        dic['B1.8'] = rooms_8
                    else:
                        if hour == "hour=08":
                            rooms_4['1'].append(room[5:])
                        elif hour == "hour=11":
                            rooms_4['2'].append(room[5:])
                        elif hour == "hour=15":
                            rooms_4['3'].append(room[5:])
                        elif hour == "hour=18":
                            rooms_4['4'].append(room[5:])
                        dic['B1.4'] = rooms_4
                rooms_2 = {}
                rooms_2['1'] = []
                rooms_2['2'] = []
                rooms_2['3'] = []
                rooms_2['4'] = []
                for i in s_1_9:
                    room = nump.findall(str(i))[0]
                    hour = re.search("hour=..", str(i)).group()
                    if hour == "hour=08":
                        rooms_2['1'].append(room[5:])
                    elif hour == "hour=11":
                        rooms_2['2'].append(room[5:])
                    elif hour == "hour=15":
                        rooms_2['3'].append(room[5:])
                    elif hour == "hour=18":
                        rooms_2['4'].append(room[5:])
                dic['B2.2'] = rooms_2
                return dic
        # 医学部
        elif self.region == '2':
            dic['Y2.1'] = {}   # area=12
            dic['Y1.4'] = {}   # area=14
            dic['Y1.8'] = {}   # area=14
            url_2_14 = 'http://reserv.lib.whu.edu.cn/day.php?year=%s&month=%s&day=%s&area=14' % (
                year, month, day)
            url_2_12 = 'http://reserv.lib.whu.edu.cn/day.php?year=%s&month=%s&day=%s&area=12' % (
                year, month, day)
            try:
                soup_2_14 = BeautifulSoup(
                    urllib2.urlopen(url_2_14, timeout=4), 'lxml')
                soup_2_12 = BeautifulSoup(
                    urllib2.urlopen(url_2_12, timeout=4), 'lxml')
            except Exception, e:
                error["error_code"] = 10003
                error["reason"] = u"网络连接错误"
                error["result"] = []
                return error
            else:
                s_2_14 = soup_2_14.find_all('a', {'class': 'new_booking'})
                s_2_12 = soup_2_12.find_all('a', {'class': 'new_booking'})
                rooms_2 = {}
                rooms_2['1'] = []
                rooms_2['2'] = []
                rooms_2['3'] = []
                rooms_2['4'] = []
                for i in s_2_12:
                    room = nump.findall(str(i))[0]
                    hour = re.search("hour=..", str(i)).group()
                    if hour == "hour=08":
                        rooms_2['1'].append(room[5:])
                    elif hour == "hour=11":
                        rooms_2['2'].append(room[5:])
                    elif hour == "hour=15":
                        rooms_2['3'].append(room[5:])
                    elif hour == "hour=18":
                        rooms_2['4'].append(room[5:])
                dic['Y2.1'] = rooms_2
                rooms_4 = {}
                rooms_4['1'] = []
                rooms_4['2'] = []
                rooms_4['3'] = []
                rooms_4['4'] = []
                rooms_8 = {}
                rooms_8['1'] = []
                rooms_8['2'] = []
                rooms_8['3'] = []
                rooms_8['4'] = []
                for i in s_2_14:
                    room = nump.findall(str(i))[0]
                    hour = re.search("hour=..", str(i)).group()
                    if room == "room=101" or room == "room=102":
                        if hour == "hour=08":
                            rooms_4['1'].append(room[5:])
                        elif hour == "hour=11":
                            rooms_4['2'].append(room[5:])
                        elif hour == "hour=15":
                            rooms_4['3'].append(room[5:])
                        elif hour == "hour=18":
                            rooms_4['4'].append(room[5:])
                    else:
                        if hour == "hour=08":
                            rooms_8['1'].append(room[5:])
                        elif hour == "hour=11":
                            rooms_8['2'].append(room[5:])
                        elif hour == "hour=15":
                            rooms_8['3'].append(room[5:])
                        elif hour == "hour=18":
                            rooms_8['4'].append(room[5:])
                dic['Y1.4'] = rooms_4
                dic['Y1.8'] = rooms_8
                return dic
        else:
            error["error_code"] = 10001
            error["reason"] = u"不合法的数据"
            error["result"] = [{
                "field": "region",
                "error_code": 10002,
                "reason": u"数据不完整"
            }]
            return error

    def getcookie(self, sid, pwd):
        # 登录获得cookie字符串
        if sid and pwd:
            self.sid = sid
            self.pwd = pwd
            login_path = 'http://metalib.lib.whu.edu.cn/pds'  # 登录处理链接
            postdata = {
                'func': 'login',
                'calling_system': 'mrbs',
                'term1': 'short',
                'selfreg': '',
                'bor_id': self.sid,
                'bor_verification': self.pwd,
                'institute': 'WHU',
                'url': 'http://metalib.lib.whu.edu.cn:80/pds?'
            }  # Post数据
            data = urllib.urlencode(postdata)  # 编码
            data = data.encode('utf-8')
            req = urllib2.Request(url=login_path, data=data)  # 处理请求
            try:
                soup = BeautifulSoup(
                    urllib2.urlopen(req, timeout=4), 'lxml')  # 处理返回链接
            except Exception, e:
                error["error_code"] = 10003
                error["reason"] = u"网络连接错误"
                error["result"] = []
                return error
            else:
                # 抓取含有pds_handle的链接
                raw = soup.find_all(
                    "a", attrs={"href": re.compile("pds_handle")})
                if raw:
                    href = raw[0]["href"]  # 获取链接
                    p = re.compile("=(.*)&(.*)&")
                    pattern = p.split(href)
                    pds_handle = pattern[1]   # 匹配并截取pds_handle的数字部分内容
                    cookie = "PDS_HANDLE=" + pds_handle + \
                        '''; path="/"; domain=".lib.whu.edu.cn"; path_spec; domain_dot; expires="2015-08-21 04:24:11Z"; version=0'''   # 形成cookie字符串
                    self.cookie = cookie
                    self.getuserinfo(cookie)
                    return cookie
                else:
                    error["error_code"] = 10000
                    error["reason"] = u"验证错误"
                    error["result"] = [{
                        "field": "sid",
                        "error_code": 10001,
                        "reason": u"不合法的数据"
                    }, {
                        "field": "pwd",
                        "error_code": 10001,
                        "reason": u"不合法的数据"
                    }]
                    return error
        else:
            error["error_code"] = 10000
            error["reason"] = u"验证错误"
            error["result"] = [{
                "field": "sid",
                "error_code": 10002,
                "reason": u"数据不完整"
            }, {
                "field": "pwd",
                "error_code": 10002,
                "reason": u"数据不完整"
            }]
            return error

    def getuserinfo(self, cookie):  # 获取用户信息（主要是name和ID）, 需要cookie
        req = urllib2.Request(
            "http://metalib.lib.whu.edu.cn/pds?func=Bor-info")
        if cookie:
            req.add_header('Cookie',  cookie)
            try:
                root = ET.parse(
                    urllib2.urlopen(req, timeout=4)).getroot()  # 获取根节点
            except Exception, e:
                error["error_code"] = 10003
                error["reason"] = e
                error["result"] = []
                return error
            else:
                name = root.getiterator("name")[0].text.encode('utf-8')
                ID = root.getiterator("id")[0].text.encode('utf-8')
                self.name = name
                self.ID = ID
                return name, ID
        else:
            error["error_code"] = 10001
            error["reason"] = u"不合法的数据"
            error["result"] = [{
                "field": "cookie",
                "error_code": 10002,
                "reason": u"数据不完整"
            }]
            return error

    def reservbyroom(self, room, time):  # 需要cookie
        if str(room).isdigit() and str(time).isdigit():
            if int(room) not in range(16, 41) and int(room) not in range(70, 106):
                error["error_code"] = 10001
                error["reason"] = u"不合法的数据"
                error["result"] = [{
                    "field": "room",
                    "error_code": 13002,
                    "reason": u"房间号错误（超出范围）"
                }]
                return error
            if time == '1':
                time = 8
            elif time == '2':
                time = 11.5
            elif time == '3':
                time = 15
            elif time == '4':
                time = 18.5
            else:
                error["error_code"] = 10001
                error["reason"] = u"不合法的数据"
                error["result"] = [{
                    "field": "time",
                    "error_code": 13002,
                    "reason": u"时间段错误（超出范围）"
                }]
                return error
        else:
            error["error_code"] = 10001
            error["reason"] = u"不合法的数据"
            error["result"] = [{
                "field": "room",
                "error_code": 10002,
                "reason": u"数据不完整"
            }, {
                "field": "time",
                "error_code": 10002,
                "reason": u"数据不完整"
            }]
            return error
        self.room = room
        handpage = 'http://reserv.lib.whu.edu.cn/edit_entry_handler.php'
        if hasattr(self, "name") and hasattr(self, "sid") and hasattr(self, "ID"):
            postdata = {
                'name': self.name,
                'description': 'description',
                'start_day': self.day,
                'start_month': self.month,
                'start_year': now.year,
                'start_seconds': str(time*3600),
                'all_day': 'no',
                'end_day': self.day,
                'end_month': self.month,
                'end_year': now.year,
                'end_seconds': str(time*3600+12600),
                'area': '',
                'rooms[]': room,
                'type': 'I',
                'confirmed': '1',
                'f_bor_id': self.sid,
                'f_entry_tel': 'tel',
                'f_entry_email': 'email',
                'f_entry_person1': '',
                'f_entry_person2': '',
                'f_entry_person3': '',
                'returl': 'http://reserv.lib.whu.edu.cn/day.php?year=%s&month=%s&day=%s' % (now.year, self.month, self.day),
                'create_by': self.ID,
                'rep_id': '0',
                'edit_type': 'series'
            }
            req = urllib2.Request(
                url=handpage, data=urllib.urlencode(postdata))
            req.add_header('Cookie',  self.cookie)
            try:
                soup = BeautifulSoup(urllib2.urlopen(req, timeout=4), 'lxml')
            except Exception, e:
                error["error_code"] = 10003
                error["reason"] = e
                error["result"] = []
                return error
            else:
                pageinfo = str(soup)  # 以下代码为获取预订的房间id
                if 'Fatal error' in pageinfo:
                    error["error_code"] = 13004
                    error["reason"] = u"其他未知错误"
                    error["result"] = []
                    return error
                elif 'repeat reservation' in pageinfo:
                    error["error_code"] = 13000
                    error["reason"] = u"重复预订研修室"
                    error["result"] = []
                    return error
                elif 'The new booking will conflict with the following entries' in pageinfo:
                    error["error_code"] = 13001
                    error["reason"] = u"该研修室已被他人预订"
                    error["result"] = []
                    return error
                else:
                    links = soup.find_all(
                        'a', attrs={'href': re.compile('view_entry')})  # 抓取已预订的房间链接
                    # str                 # 将gb2312编码为utf-8
                    for link in links:
                        if link.renderContents() == self.name:
                            linkofid = link['href']  # 获得链接中的网址部分（id包含在其中）
                            linkstr = str(linkofid)
                            numid = re.compile("id=\d+")
                            roomid = numid.findall(linkstr)[0][3:]  # 正则匹配出id
                            self.roomid = roomid
                            return int(roomid)
        else:
            error["error_code"] = 10001
            error["reason"] = u"不合法的数据"
            error["result"] = [{
                "field": "name",
                "error_code": 10002,
                "reason": u"数据不完整"
            }, {
                "field": "sid",
                "error_code": 10002,
                "reason": u"数据不完整"
            }, {
                "field": "ID",
                "error_code": 10002,
                "reason": u"数据不完整"
            }]
            return error

    def cancel(self):
        if hasattr(self,  "roomid"):
            handpage = "http://reserv.lib.whu.edu.cn/del_entry.php?id=%s" % (
                self.roomid)
            req = urllib2.Request(url=handpage)
            if hasattr(self, "cookie"):
                req.add_header('Cookie',  self.cookie)
                try:
                    soup = BeautifulSoup(
                        urllib2.urlopen(req, timeout=4), 'lxml')
                except Exception, e:
                    error["error_code"] = 10003
                    error["reason"] = u"网络连接错误"
                    error["result"] = []
                    return error
                else:
                    pageinfo = str(soup)
                    if 'do not have access' in pageinfo:
                        error["error_code"] = 10001
                        error["reason"] = u"不合法的数据"
                        error["result"] = [{
                            "field": "name",
                            "error_code": 14000,
                            "reason": u"没有可以取消的研修室"
                        }]
                        return error
                    elif 'Go To Today' in pageinfo:
                        return int(self.roomid)  # 取消预约成功，返回房间ID
                    else:
                        error["error_code"] = 10001
                        error["reason"] = u"unknow error"
                        error["result"] = [{
                            "field": "name",
                            "error_code": 14001,
                            "reason": u"'unknow error'"
                        }]
                        return error
            else:
                error["error_code"] = 10001
                error["reason"] = u"不合法的数据"
                error["result"] = [{
                    "field": "name",
                    "error_code": 10002,
                    "reason": u"数据不完整"
                }]
                return error

if __name__ == '__main__':
    test = Reservelib()
    print test.getcookie('', '')
    print test.getroominfo(2015, 10, 13, 1)
    print test.reservbyroom('30', '1')
    print test.cancel()
