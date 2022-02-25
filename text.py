import json
from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import qrcode, base64, requests, os
from fake_useragent import UserAgent
from threading import Thread
from io import BytesIO
import http.cookiejar as cookielib
from PIL import Image
from typing import List

from Bilibili import schemas, curd
from Bilibili.database import engine, Base, SessionLocal
from Bilibili import schemas, curd
import Bilibili.schemas
from pydantic import BaseModel
from Bilibili.database import engine, Base, SessionLocal
from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks, Request
import urllib.request

'''
txt = "DedeUserID=78&DedeUserID__ckMd5=ba7282a8b10&Expires=155&SESSDATA=948a1a87%%2Ce8be3%2A91&bili_jct=40b9821413c9fd7770f&"
DedeUserID = txt.split('&')[0]
SESSDATA = txt.split('&')[3]
bili_jct = txt.split('&')[4]
headers = {'Content-Type': 'application/json'}
text = {'DedeUserID': 'DedeUserID=11573578', 'SESSDATA': 'SESSDATA=1b52aa9a%2C1647778515%2C8f737%2A91', 'bili_jct': 'bili_jct=d72daf2734e9a648ddec1954a40ccf14', 'email': '2461006717@qq.com'}
print(requests.request('post','http://127.0.0.1:8000/b/create_user/', json=text,headers=headers))
'''
'''
def get_db(): # 数据库依赖
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
Session = requests.session()
temp = Bilibili.schemas.Createuser
temp.DedeUserID = 'DedeUserID=11573578'
temp.SESSDATA = 'SESSDATA=1b52aa9a%2C1647778515%2C8f737%2A91'
temp.bili_jct = 'bili_jct=d72daf2734e9a648ddec1954a40ccf14'
temp.email = '2461006717@qq.com'
text = {'DedeUserID': 'DedeUserID=11573578', 'SESSDATA': 'SESSDATA=1b52aa9a%2C1647778515%2C8f737%2A91', 'bili_jct': 'bili_jct=d72daf2734e9a648ddec1954a40ccf14'}
def xx(db: Session = Depends(get_db)):
    print(curd.create_user_by_code(db=db, user=text))
xx(get_db())
'''
'''
r = requests.get('http://127.0.0.1:8000/b/get_users/spiritlhl?skip=0&limit=100')
ct = 0
for i in r.json():
    user_ck = str(r.json()[ct]['DedeUserID']) + ';' + str(r.json()[ct]['SESSDATA']) + ';' + str(r.json()[ct]['bili_jct']) + ';'
    ct +=1
    t = "{" + "COOKIE: " + "\"" + user_ck + "\"," + "NUMBER: "+str(ct)+",CLEAR: true,WAIT: 60 * 1000,},"
    with open('env.js', 'r', encoding='utf-8') as fp:
        lines = []
        for line in fp:
            lines.append(line)
        fp.close()
        lines.insert(42, '{}\n'.format(t))  # 在第二行插入
        s = ''.join(lines)
    with open('env.js', 'w', encoding='utf-8') as fp:
        fp.write(s)
        fp.close()
'''

"""
with open('env.js', 'r', encoding='utf-8') as fp:
    lines = []
    for line in fp:
        lines.append(line)
    fp.close()
cct = 42
for j in lines[42:]:
    if j == ']\n':
        kill_ct = cct
        cct += 1
    else:
        cct+=1
with open('env.js','w',encoding='utf-8') as fp:
    tplines = lines[0:42]+lines[kill_ct:]
    s = ''.join(tplines)
    fp.write(s)
    fp.close()


r = requests.get('http://127.0.0.1:8000/b/get_users/spiritlhl?skip=0&limit=100')
#r = urllib.request.urlopen('http://127.0.0.1:8000/b/get_users/spiritlhl/')
ct = 0
print(r.json())
for i in r.json():
    user_ck = str(r.json()[ct]['DedeUserID']) + ';' + str(r.json()[ct]['SESSDATA']) + ';' + str(r.json()[ct]['bili_jct']) + ';'
    ct +=1
    t = "    {" +"\n"+"    COOKIE: " + "\"" + user_ck + "\"," +"\n"+"    NUMBER: "+str(ct)+",\n    CLEAR: true,\n    WAIT: 60 * 1000,\n    },"
    with open('env.js', 'r', encoding='utf-8') as fp:
        lines = []
        for line in fp:
            lines.append(line)
        fp.close()
        ttp = 42+(ct-1)*6
        lines.insert(ttp, '{}\n'.format(t))  # 在第二行插入
        s = ''.join(lines)
    with open('env.js', 'w', encoding='utf-8') as fp:
        fp.write(s)
        fp.close()
"""

'''
Session = requests.session()

def get_db(): # 数据库依赖
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_user(db: Session = Depends(get_db)): # 通过DedeUserID查找用户
    db_user = curd.get_user_by_name(db, DedeUserID="DedeUserID=11573578")
    print(db_user)


get_user()
'''

yzurl = "https://api.bilibili.com/nav" #"https://api.bilibili.com/x/web-interface/nav"
ua = UserAgent(path='ua.json')
user_agent = ua.chrome
headers = {
    "cookie": "DedeUserID=20935726;SESSDATA=cb6ed015%2C1641729266%2C7b3e2%2A71;bili_jct=eb4886634421fc2537820ee35dd0d8b3;",
    "referer": "https://space.bilibili.com/",
    "User-Agent": user_agent
}

#code -101 未登陆
#code 0 登陆成功
r = requests.get(yzurl,headers=headers)
print(r.json()["code"] == 0)
