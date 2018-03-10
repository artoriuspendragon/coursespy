#!/usr/bin/python
# -*- coding:utf-8 -*-
import requests
from bs4 import BeautifulSoup
import re
import urllib
from sys import argv
import codecs,sys
import datetime


fpurl='xxxx'
ccurl='xxxx'
cturl='xxxx'
ctterm='20171'
cttermno = urllib.parse.unquote(
        '2017-2018%EF%BF%BD%EF%BF%BD%D2%BB%D1%A7%EF%BF%BD%EF%BF%BD%5B%EF%BF%BD%EF%BF%BD%C7%B0%D1%A7%EF%BF%BD%EF%BF%BD%5D')
def makecourselist(html):
    trresult = BeautifulSoup(html, 'html5lib').find_all('td', {'class': 'PuTongCell'})
    resultlist = []

    for item in trresult:
        reresult = re.sub(r'<[^>]+>', ' ', str(item))
        listresult = []
        for litem in reresult.split(' '):
            if litem != '':
                listresult.append(litem)
        resultlist.append(listresult)
    if resultlist == []:
        return []
    weekcourselist = []
    for j in range(0, 7):
        daycourselist = []
        for i in range(0, 5):
            courseposition = i * 7 + j
            if resultlist[courseposition] != []:
                singlecourse = {
                    "name": resultlist[courseposition][0],
                    "teacher": resultlist[courseposition][1],
                    "location": resultlist[courseposition][2],
                    "times": resultlist[courseposition][3],
                    "classes": resultlist[courseposition][4],
                }
				
                daycourselist.append(singlecourse)
            else:
                daycourselist.append({})
        weekcourselist.append(daycourselist)
    return weekcourselist

def makepostdata(html,myaccount,mypassword,checkcode):
    soup = BeautifulSoup(html.text, 'html5lib')
    checkdata = {}
    checkdata['viewstate'] = soup.find(id='__VIEWSTATE')['value']
    checkdata['eventvalidation'] = soup.find(id='__EVENTVALIDATION')['value']
    checkdata['callback'] = soup.find(id='gridNew_CallbackState')['value']
    lgpostdata = {
        '__EVENTARGUMENT': '',
        '__EVENTTARGET': '',
        '__EVENTVALIDATION': checkdata['eventvalidation'],
        '__LASTFOCUS': '',
        '__VIEWSTATE': checkdata['viewstate'],
        'Button1': '+',
        'cobRole': '%D1%A7%C9%FA',
        'cobRole%24CVS': '',
        'cobRole%24DDD%24L': 'bdfeb86e-3c29-4696-a19d-6c428850cea3',
        'cobRole%24DDD%24L%24CVS': '',
        'cobRole_DDD_LCustomCallback': '',
        'cobRole_DDD_LDeletedItems': '',
        'cobRole_DDD_LInsertedItems': '',
        'cobRole_DDDWS': '0%3A0%3A-1%3A0%3A0%3A0%3A0%3A0%3A',
        'cobRole_VI': 'bdfeb86e-3c29-4696-a19d-6c428850cea3',
        'gridNew%24CallbackState': checkdata['callback'],
        'gridNew%24DXSelInput': '',
        'txtVolidate': checkcode,
        'User_ID': myaccount,
        'User_Pass': mypassword
    }
    return lgpostdata

def getstarttime(currentweek):
    now = datetime.datetime.today()
    now = now.replace(hour=0, minute=0, second=0, microsecond=0)
    delttime = datetime.timedelta(days=(int(currentweek) - 1) * 7 + now.weekday())
    starttime = now - delttime
    return (str(starttime))

def startspy(myaccount,mypassword):
    log(myaccount+','+mypassword)
    uphead = {'Connection': 'Keep-Alive'}
    s = requests.session()
    s.headers.update(uphead)
    r = s.get(url=fpurl)
    checkcode= s.get(url=ccurl).cookies['CheckCode']
    logindata=makepostdata(r,myaccount,mypassword,checkcode)
    nr = s.post(url=fpurl, data=logindata)
    falsetext='判断用户名、密码不能为空'
    if(nr.text.find(falsetext)>0):
        return 'error: login failed'
    ctr = s.get(url=cturl)
    ctsoup = BeautifulSoup(ctr.text, 'html5lib')
    eventvalidation = ctsoup.find(id='__EVENTVALIDATION')['value']
    viewstate = ctsoup.find(id='__VIEWSTATE')['value']
    ctddw = ctsoup.find(id='cobTermNo_DDDWS')['value']
    currentweek = ctsoup.find(id="txtweeks_I")['value']

    currentweekcourse = makecourselist(ctr.text)
    ctpostdata = {
        '__EVENTTARGET': 'txtweeks',
        '__EVENTARGUMENT': '',
        '__VIEWSTATE': viewstate,
        '__EVENTVALIDATION': eventvalidation,
        'cobTermNo_VI': ctterm,
        'cobTermNo': cttermno,
        'cobTermNo_DDDWS': ctddw,
        'cobTermNo$DDD$L': ctterm,
        'cobTermNo$DDD$L$CVS': '',
        'cobTermNo$CVS': '',
        'txtweeks': currentweek,
        'txtweeks$CVS': ''
    }
    alltimetable = []
    for week in range(0, 25):
        ctpostdata['txtweeks'] = week + 1
        ctpage = s.post(url=cturl, data=ctpostdata)
        currentweekct = makecourselist(ctpage.text)
        alltimetable.append(currentweekct)
    alltimetable[int(currentweek) - 1] = currentweekcourse
    alltimetable.append({"starttime":getstarttime(currentweek)})
    return alltimetable
def log(text):
    f=open('log.txt','a')
    f.write('\n')
    temp=str(str(text).encode('utf-8'))
    f.write(temp)
    f.close()
def test():
   return 'hello'

#script,stuID,stuPwd = argv
#result=str(startspy(stuID,stuPwd))
#result=result.replace("\'","\"")
#print(result)

