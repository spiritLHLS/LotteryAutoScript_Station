from fastapi import APIRouter, Depends, HTTPException, Request, Form, BackgroundTasks
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fake_useragent import UserAgent
from threading import Thread
from io import BytesIO
from PIL import Image
from typing import List
from imbox import Imbox


import http.cookiejar as cookielib
import qrcode, base64, requests, random, time, datetime, re


import schemas, curd
from database import engine, Base, SessionLocal

Base.metadata.create_all(bind=engine)


application = APIRouter()


templates = Jinja2Templates(directory='./templates')

#application.mount("/static", StaticFiles(directory="static"), name="static")


requests.packages.urllib3.disable_warnings()


urlip = 'http://127.0.0.1:8000/' #部署的在服务器，将127.0.0.1换成对应外网ip或域名，端口记得在服务器开放，可自己改为其他端口
admin = 'admin' # 后端一些接口操作所需的验证权限码
qqurl = "" # go-cqhttp机器人发送消息的路径，一般是http://服务器外网ip:5700/
zqq = "" # 自己的Q号，推送失败接受信息的Q号
imap_url = '' # 腾讯云企业邮箱或qq邮箱的imap服务器地址，与my_config邮箱推送对应
zzemail = '' # 对应的邮箱
zzemail_password = '' # 邮箱对应的授权码，腾讯云企业邮箱则是密码即可
group_id=  # Q群号，推送到指定Q群，推送后会删除邮箱中中转的邮件


status_qr = 0
Session = requests.session()
ua = UserAgent(path='ua.json')
user_agent = ua.chrome
headers = {'User-Agent': user_agent, 'Referer': "https://www.bilibili.com/"}
headerss = {'User-Agent': user_agent,  'Host': 'passport.bilibili.com','Referer': "https://passport.bilibili.com/login"}
qrcodedata = '0'

class showpng(Thread): # 生成图片模板
    def __init__(self, data):
        Thread.__init__(self)
        self.data = data

    def run(self):
        img = Image.open(BytesIO(self.data))
        img.show()


def islogin(Session): # 判定是否已经登陆成功
    try:
        Session.cookies.load(ignore_discard=True)
    except Exception:
        pass
    loginurl = Session.get("https://api.bilibili.com/x/web-interface/nav", verify=False, headers=headers).json()
    if loginurl['code'] == 0:
        print('Cookies值有效，',loginurl['data']['uname'],'，已登录！')
        return Session, True
    else:
        print('Cookies值已经失效，请重新扫码登录！')
        return Session, False

def save_ck(text): # 判定扫码结果是否保存
    try:
        tokenurl = 'https://passport.bilibili.com/qrcode/getLoginInfo'
        qrcodedata = Session.post(tokenurl, data={'oauthKey': oauthKey, 'gourl': 'https://www.bilibili.com/'},
                                  headers=headerss).json()
        if '-4' in str(qrcodedata['data']):
            return '二维码未失效，请扫码！'
        elif '-5' in str(qrcodedata['data']):
            return '已扫码，请确认！'
        elif '-2' in str(qrcodedata['data']):
            return '二维码已失效，请刷新页面再扫码！'
        elif 'True' in str(qrcodedata['status']):
            Session.get(qrcodedata['data']['url'], headers=headers)
            #with open('bilcookies.txt', 'a') as fp:
            #    fp.write(str(qrcodedata['data']['url'][42:-39])+'\n')
            txt = str(qrcodedata['data']['url'][42:-39])
            DedeUserID = txt.split('&')[0]
            SESSDATA = txt.split('&')[3]
            bili_jct = txt.split('&')[4]
            text["DedeUserID"] = DedeUserID
            text["SESSDATA"] = SESSDATA
            text["bili_jct"] = bili_jct
            return text
        else:
            return '未知错误'
    except:
        return '未知错误, 录入失败, 大概率未扫码或扫码失败，也有可能是请求频繁了'

def write_ck():#配置文件写入ck
    #先清空文件记录
    global kill_ct
    kill_ct = 42
    with open('env.js', 'r', encoding='utf-8') as fp:
        lines = []
        for line in fp:
            lines.append(line)
        fp.close()
    cct = 42
    for j in lines[42:]:
        if j == '    ],\n':
            kill_ct = cct
            cct += 1
        else:
            cct += 1
    with open('env.js', 'w', encoding='utf-8') as fp:
        tplines = lines[0:42] + lines[kill_ct:]
        s = ''.join(tplines)
        fp.write(s)
        fp.close()
    #写入新数据
    temp_url = urlip+'b/get_users/'+admin+'/'
    r = requests.get(temp_url)
    ct = 0
    for i in r.json():
        print(i)
        user_ck = str(r.json()[ct]['DedeUserID']) + ';' + str(r.json()[ct]['SESSDATA']) + ';' + str(r.json()[ct]['bili_jct']) + ';'
        ct += 1
        t = "        {\n" + "         COOKIE: " + "\"" + user_ck + "\",\n" + "         NUMBER: " + str(ct) + ",\n"+"         CLEAR: true,\n"+"         WAIT: 70 * 1000,\n"+"    },\n"
        with open('env.js', 'r', encoding='utf-8') as fp:
            lines = []
            for line in fp:
                lines.append(line)
            fp.close()
            lines.insert(42 + (ct-1)*6, '{}\n'.format(t))  # 在42行插入
            s = ''.join(lines)
        with open('env.js', 'w', encoding='utf-8') as fp:
            fp.write(s)
            fp.close()


def get_db(): # 数据库依赖
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@application.get("/")
async def home(request: Request):
    return templates.TemplateResponse(
        "home.html",
        {
            "request": request
        }
    )

@application.get("/ckpush/")
async def ckpush(request: Request):
    return templates.TemplateResponse('index.html', {'request': request})


@application.post("/inputck/")
def files(
                    #request:           Request,
                    db: Session = Depends(get_db),
                    DedeUserID: str  = Form(...),
                    SESSDATA: str    = Form(...),
                    bili_jct: str    = Form(...),
                    email: str       = Form(...)
                ):
    cookie = {
  "DedeUserID": "DedeUserID="+DedeUserID,
  "SESSDATA": "SESSDATA="+SESSDATA,
  "bili_jct": "bili_jct="+bili_jct,
  "email": email
            }
    db_user = curd.get_user_by_name(db, DedeUserID=cookie["DedeUserID"])  # 查询是否在库
    if (db_user != None):
        curd.change_user_by_code(db=db, user=cookie)  # 在库更新ck
    else:
        curd.create_user_by_code(db=db, user=cookie)  # 不在库创建ck
    write_ck()
    return "录入成功，ck记录为{}".format(cookie)

@application.get("/login") # 生成base64流图片
def login():
    global oauthKey,Session,status_qr
    #if not os.path.exists('cookies.txt'):
    #    with open("cookies.txt", 'w') as f:
    #        f.write("")
    Session = requests.session()
    Session.cookies = cookielib.LWPCookieJar(filename='bzcookies.txt')
    Session, status = islogin(Session)
    if not status:
        getlogin = Session.get('https://passport.bilibili.com/qrcode/getLoginUrl', headers=headers).json()
        loginurl = requests.get(getlogin['data']['url'], headers=headers).url
        oauthKey = getlogin['data']['oauthKey']
        qr = qrcode.QRCode()
        qr.add_data(loginurl)
        img = qr.make_image()
        a = BytesIO()
        img.save(a, 'png')
        png = a.getvalue()
        a.close()
        base64_data = base64.b64encode(png)  # 使用base64进行加密
        text = 'data:image/gif;base64,'+str(base64_data)[2:-1]
        status_qr = 1
        return text

@application.get('/readme')
async def readme(): # 说明
    text = "1.二维码加载失败或二维码失效请刷新页面更新;" \
           "2.保存ck如若见到录入失败，刷新页面再次扫码录入;" \
           "3.扫码登陆占用网页端，日常有使用网页端的请手动录入;" \
           "4.手动录入浏览器抓ck请跳转手动录入页面后仔细查看说明;" \
           "5.最下端有手动录入按钮，跳转后输入cookie值录入;" \
           "6.暂时没做好配置界面，默认只转已关注的up的动态。"
    return text

@application.get('/login/sucess/{email}') # {email} # 保存ck到数据库并修改对应文件
def login_sucess(email: int, db: Session = Depends(get_db)):
    text = {
  "DedeUserID": "string",
  "SESSDATA": "string",
  "bili_jct": "string",
  "email": "string"
            }
    text = save_ck(text)
    if type(text) == type(dict()):
        text["email"] = email
        db_user = curd.get_user_by_name(db, DedeUserID=text["DedeUserID"]) # 查询是否在库
        if (db_user != None):
            curd.change_user_by_code(db=db, user=text) # 在库更新ck
        else:
            curd.create_user_by_code(db=db, user=text) # 不在库创建ck
        write_ck()
        return "录入成功"
    else:
        return "错误原因：{}".format(text)


@application.post("/create_user", response_model=schemas.Readuser)
def create_user(user: schemas.Createuser, db: Session = Depends(get_db)): # json格式创建用户
    db_user = curd.get_user_by_name(db, DedeUserID=user.DedeUserID)
    if db_user:
        raise HTTPException(status_code=400, detail="user already registered")
    return curd.create_user(db=db, user=user)


@application.get("/get_user/{DedeUserID}", response_model=schemas.Readuser)
def get_user(DedeUserID: str, db: Session = Depends(get_db)): # 通过DedeUserID查找用户
    db_user = curd.get_user_by_name(db, DedeUserID=DedeUserID)
    if db_user is None:
        raise HTTPException(status_code=404, detail="user not found")
    return db_user


@application.get("/get_users/{admin}", response_model=List[schemas.Readuser])
def get_users(admin: str, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)): # 查找所有用户数据
    if admin == admin:
        users = curd.get_users(db, skip=skip, limit=limit)
        return users
    else:
        return


@application.post("/delete_user/")
def get_users(admin: str, DedeUserID: str, db: Session = Depends(get_db)): # 指定用户数据删除
    if admin == admin:
        delete_user = curd.delete_user_by_code(db, DedeUserID=DedeUserID)
        write_ck()
        return delete_user
    else:
        return

def check_real_users(db):
    temp_url = urlip + 'b/get_users/' + admin + '/'
    r = requests.get(temp_url)
    yzurl = "https://api.bilibili.com/nav"  # "https://api.bilibili.com/x/web-interface/nav"
    ua = UserAgent(path='ua.json')
    ct = 0
    for i in r.json():
        user_agent_t = ua.chrome
        user_ck_t = str(r.json()[ct]['DedeUserID']) + ';' + str(r.json()[ct]['SESSDATA']) + ';' + str(
            r.json()[ct]['bili_jct']) + ';'
        headers = {
            "cookie": user_ck_t,
            "referer": "https://space.bilibili.com/",
            "User-Agent": user_agent_t
        }
        ct += 1
        res = requests.get(yzurl, headers=headers)
        time.sleep(random.uniform(2.1,5.1))#增加间隔
        if res.json()["code"] == 0:
            continue
        elif res.json()["code"] == -101:
            ttpp = r.json()[ct - 1]['DedeUserID']
            id = str(ttpp)[11:]
            resttpp = requests.get("https://space.bilibili.com/" + str(id) + "/")
            name = re.findall(r"<title>(.*?)的个人空间_哔哩哔哩_Bilibili", resttpp.text)[0]
            try:
                qq = curd.get_user_by_name(db, "DedeUserID=" + str(id)).email
                data = {
                    'user_id': qq,
                    'message': "你的账号  昵称：{}  uid：{}\n 记录已过期，请重行录入".format(name, id)
                }
                requests.post(qqurl + 'send_private_msg', data)
            except:
                data = {
                    'user_id': zqq,
                    'message': '账号id{}，昵称{} 过期推送失败'.format(id, name)
                }
                requests.post(qqurl + 'send_private_msg', data)
            curd.delete_user_by_code(db, DedeUserID=ttpp)
            write_ck()
        else:
            continue

@application.post("/check_user/")
def check_users(admin: str, background_tasks: BackgroundTasks, db: Session = Depends(get_db)): # 检查所有ck并删除过期ck
    if admin == admin:
        background_tasks.add_task(check_real_users, db)
        return "检查完毕并删除过期ck"
    else:
        return "未知错误"

def push_msg_QQ(db):
    with Imbox(imap_url, zzemail, zzemail_password, ssl=True) as imbox:
        # 获取全部邮件
        inbox_message_after = imbox.messages()
        for uid, message in inbox_message_after:
            if message.body['plain'][0][:4] == "## 私" or message.body['plain'][0][:4] ==  "## [":
                body = message.body['plain'][0]
                body = body.replace("   ", '\n')
                body = body.replace('{ "content": "', '\n').replace(' {"content":"', '\n')
                body = body.replace(' "}', '\n').replace('" }', '\n')
                body = body.replace('奖', 'j').replace("抽", "c").replace("中","z").replace("恭","g").replace("喜","x")
                try:
                    id = re.findall(r"私信你(.*?)说", body)[0][1:-1]
                except:
                    id = re.findall(r"了你\((.*?)\)", body)[0]
                res = requests.get("https://space.bilibili.com/" + str(id) + "/")
                name = re.findall(r"<title>(.*?)的个人空间_哔哩哔哩_Bilibili", res.text)[0]
                try:
                    qq = curd.get_user_by_name(db, "DedeUserID="+str(id)).email
                    headers = {'Content-Type': 'application/json'}
                    data = {
                        'group_id': group_id,
                        'message': [
                            {
                                "type": "at",
                                "data": {
                                    "qq": qq,
                                    "name": zqq          
                                    }
                            },
                            {
                                "type" : "text",
                                "data": {
                                    "text": " 账号  昵称：{}  uid：{}可能zhong了\n".format(name, id)+body
                                    }
                            }        
                        ]
                    }
                    requests.post(qqurl+'send_group_msg', headers=headers, json=data)
                    imbox.delete(uid)
                    time.sleep(random.uniform(2.1,5.1))
                except:
                    data = {
                        'group_id': group_id,
                        'message': '账号id{}，昵称{}推送失败'.format(id, name)
                    }
                    requests.post(qqurl+'send_group_msg', data)
                    imbox.delete(uid)
                    time.sleep(random.uniform(2.1,5.1))
            elif message.body['plain'][0][:4] == "COOK":
                body = message.body['plain'][0]
                data = {
                        'group_id': group_id,
                        'message': "@"+ str(qq) +" "+body.replace("失效", "sx")
                    }
                requests.post(qqurl+'send_group_msg', data)
                imbox.delete(uid)
                time.sleep(random.uniform(2.1,5.1))
            else:
                pass
                #imbox.delete(uid)

@application.get("/push_msg/")
def push_msg(background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    background_tasks.add_task(push_msg_QQ, db)
    return "发送完毕"
