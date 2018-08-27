#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
Required
- requests
Info
- author : "lee-zeicai"
- email  : "2925168463@qq.com"
- date   : "2018.8.27"
- waring : "Code for learning only, do not do illegal use！"
'''

import requests
from bs4 import BeautifulSoup
import queue
import threading
import re
import pymysql

q = queue.Queue()
header={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.167 Safari/537.36'}
main_url = "http://kaijiang.500.com/shtml/ssq/18099.shtml"

r = requests.get(main_url,header)
r.encoding = r.apparent_encoding
soup = BeautifulSoup(r.content, "html.parser")
for a in soup.find('div',attrs = {'class':'iSelectList'}).children:
    try:
        q.put(a.get_text())
    except:
        continue

def get_info():
    while True:
        term = q.get()
        data=[]
        data.append(term)
        url = "http://kaijiang.500.com/shtml/ssq/%s.shtml"%term
        r = requests.get(url,header)
        r.encoding = r.apparent_encoding
        soup = BeautifulSoup(r.text, 'html.parser')
        date = soup.find('span', attrs={'class':"span_right"}).string
        date = date.split(' ')[0].split('：')[1].replace('年',"-").replace('月',"-").replace('日',"")
        data.append(date)
        soup = BeautifulSoup(r.text,'html.parser')
        balls = soup.find('table',attrs={'cellpadding':'1'})
        red_ball = balls('td')[-1].string.strip().split(' ')
        for i in red_ball:
            data.append(i)
        blue_ball = soup.find('li',attrs={'class':"ball_blue"}).string
        data.append(blue_ball)
        insert('data',data)
        if q.empty():
            break
            
def insert(db,values):
    try: 
        sql='insert into %s values (%s)'% (db,','.join("'%s'" % x for x in values))
        print (sql)
        conn=pymysql.connect(host='localhost',user='root',passwd="******", db="lottery",port=3306,charset='utf8')
        cur=conn.cursor()
        cur.execute(sql)
        conn.commit()
        cur.close()
        conn.close()
    except Exception as e:
        with open('db_fail.txt','a')as f:
            f.write('%s    %s\n'%(db,e))         
        
if __name__ == '__main__':
    r = requests.get(main_url,header)
    r.encoding = r.apparent_encoding
    soup = BeautifulSoup(r.content, "html.parser")
    for a in soup.find('div',attrs = {'class':'iSelectList'}).children:
        try:
            q.put(a.get_text())
        except:
            continue    
    p=threading.Thread(target=get_info)
    d=threading.Thread(target=get_info)
    e=threading.Thread(target=get_info)
    p.start()
    d.start()
    e.start()
    p.join()
    d.join()
    e.join()