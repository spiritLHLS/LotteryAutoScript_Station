![fastapi - 0.68.1](https://img.shields.io/static/v1?label=fastapi&message=0.68.1&color=success&logo=fastapi)

# B站抽奖站点

本站点前后端由 [spiritlhl](https://github.com/spiritLHL) 开发

感谢 [shanmiteko](https://github.com/shanmiteko) 开发并维护的抽奖脚本

配套脚本仓库链接： [https://github.com/shanmiteko/LotteryAutoScript](https://github.com/shanmiteko/LotteryAutoScript)

本仓库文件为本地展示版本，服务器部署请看下方部署方式

仓库文件项目匹配脚本2.3.5版本

## 前端页面

![](https://i.loli.net/2021/10/06/RmapSE8uMd4vKIj.png)

![](https://i.loli.net/2021/10/08/LRCyVTzfGAsJr9Y.png)

## 后端页面

![](https://i.loli.net/2021/10/06/BkE7oMjYTCsZf3q.png)

## 功能

- [x] 扫码添加cookie到Bilibili.sqlite3数据库
- [x] 添加cookie后刷新脚本的env配置文件
- [x] 多次扫码cookie更新替换
- [x] 匹配DedeUserID删除数据库内的cookie
- [x] 增加手动录入ck页面，方便自己浏览器抓ck录入
- [x] 删除同时刷新脚本配置文件内的ck记录
- [x] 检查库内所有cookie后删除所有过期cookie
- [x] 一对一通知推送(已更改为群内指定群成员@的方式推送，直接一对一容易QQ风控)
- [ ] 个人自定义配置
- [ ] 账号管理面板

## 部署方式

自用配置，其他配置自行探索

### step 1

部署好本项目对应的大佬docker版本的脚本，然后将本仓库文件上传到docker版本的```env.js```文件所在文件夹，覆盖原有文件。

注意对应的版本号！！！

### step 2

安装python3.6以上版本的环境，ubuntu20版本自带python环境符合，其他环境自行测试，没有环境自行下载

环境安装完成后，在管理员权限下终端输入

```bash
pip install -r requirement.txt
```

等待依赖包安装完成

配置QQ推送，后续需要用到go-cqhttp机器人的http发信息端口

具体配置详见：[https://docs.go-cqhttp.org/](https://docs.go-cqhttp.org/)

### step 3

安装完成后修改```run.py```,```main.py```,```home.html```，```env.js```文件，按照注释修改

```python
#run.py
docs_url='/docs',     # 后端接口路径，可自行修改
redoc_url='/redocs',  # 后端接口文档接口路径，可自行修改
```

```python

#一些重要自定义参数
urlip = 'http://127.0.0.1:8000/' #部署的在服务器，将127.0.0.1换成对应外网ip或域名，端口记得在服务器开放，可自己改为其他端口
admin = 'admin' # 后端一些接口操作所需的验证权限码
qqurl = "" # go-cqhttp机器人发送消息的路径，一般是http://服务器外网ip:5700/
zqq = "" # 自己的Q号，推送失败接受信息的Q号
imap_url = '' # 腾讯云企业邮箱或qq邮箱的imap服务器地址，与my_config邮箱推送对应
zzemail = '' # 对应的邮箱
zzemail_password = '' # 邮箱对应的授权码，腾讯云企业邮箱则是密码即可
```

```html
<script>
//home.html
    var urlip="http://127.0.0.1:8000/"    //服务器外网地址，和main中的urlip相同
</script>
```

```env.js```文件对应大佬仓库说明修改，注意和```main.py```文件配置对应

```
//env.js
        SMTP_HOST: "", //必填
        SMTP_PORT: "", //必填
        SMTP_USER: "", //必填
        SMTP_PASS: "", //必填
```

记得填对，而且对应端口开放！

### step4 

修改完毕，直接使用screen窗口挂起，管理员权限在```run.py```对应文件夹路径下执行

```bash
python3 run.py
```

然后站点就启用了

### step5

站点正常使用会自动修改```env.js```文件，记得同样用screen窗口挂起大佬的脚本执行

如果是宝塔界面，docker管理器方便管理，执行后不需要再通过screen窗口看日志了，直接在管理器中看即可

**站点不会自动运行大佬的脚本！站点只负责ck维护以及相关推送！**

### step6

具体大佬脚本如何部署docker版本，请去他的仓库查看，这里不再赘述

脚本仓库链接： [https://github.com/shanmiteko/LotteryAutoScript](https://github.com/shanmiteko/LotteryAutoScript)

ck录入后如果脚本有卡住，提示有ck过期，后端docs页面请求一下check接口，自动删除过期ck并通知对应号主，再次运行脚本即可

如果有宝塔面板，直接管理器里点运行即可

相关接口如何使用请站点运行后，访问对应的 ```http://你的ip:对应端口/docs```或```http://你的ip:对应端口/redocs```查看

## 不要将本项目用于收费代挂，一经发现直接删库跑路
