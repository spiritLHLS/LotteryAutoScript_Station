from imbox import Imbox
from email.mime.text import MIMEText
import datetime, re, smtplib


with Imbox('imap.exmail.qq.com', '', '', ssl=True) as imbox:
    # 获取全部邮件
    inbox_message_after = imbox.messages(date__on=datetime.date.today())
    for uid, message in inbox_message_after:
        #print(message.subject)  # 邮件主题
        if message.body['plain'][0][:4] == "发生时间":
            body = message.body['plain'][0]
            body = body.replace("   ", '\n')
            body = body.replace('{ "content": "', '\n').replace(' {"content":"', '\n')
            body = body.replace(' "}', '\n').replace('" }', '\n')
            id = re.findall(r"私信你(.*?)说", body)[0][1:-1]
        else:
            imbox.delete(uid)

#设置服务器所需信息

mail_host = 'smtp.exmail.qq.com'

mail_user = ''
#密码(部分邮箱为授权码)
mail_pass = ''
#邮件发送方邮箱地址
sender = ''
#邮件接受方邮箱地址，注意需要[]包裹，这意味着你可以写多个邮件地址群发
receivers = ['']

#设置email信息
#邮件内容设置
message = MIMEText(body,'plain','utf-8')
#邮件主题
message['Subject'] = 'title'
#发送方信息
message['From'] = sender
#接受方信息
message['To'] = receivers[0]

#登录并发送邮件
try:
    smtpObj = smtplib.SMTP()
    #连接到服务器
    smtpObj.connect(mail_host,25)
    #登录到服务器
    smtpObj.login(mail_user,mail_pass)
    #发送
    smtpObj.sendmail(sender,receivers,message.as_string())
    #退出
    smtpObj.quit()
    print('success')
except smtplib.SMTPException as e:
    print('error',e) #打印错误
