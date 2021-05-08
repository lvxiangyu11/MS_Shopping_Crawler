from splinter import Browser
import time
import json
import smtplib

import smtplib
from email.mime.text import MIMEText
from email.header import Header
import smtplib
from email.mime.text import MIMEText
from email.header import Header
import re
import sendmessage

debug = False

friendName = ''


config = {
    "https://www.microsoftstore.com.cn/certified-refurbished-surface-book-2-configurate":{
        'option-label-size-180-item-5510':{
            'option-label-specification-185-item-5643':6000,
        },
        'option-label-size-180-item-5509':{
            'option-label-specification-185-item-5639':0,
            'option-label-specification-185-item-5638':0,
            'option-label-specification-185-item-5650':0,
        }
    },
    "https://www.microsoftstore.com.cn/certified-refurbished-surface-go-configurate":{
        'option-label-specification-185-item-5648':{
            'option-label-specification-185-item-5648':0
        }
    },
    'https://www.microsoftstore.com.cn/certified-refurbished-surface-pro-7-configurate#color=5484':{
        'option-label-color-93-item-5483':{
            'option-label-specification-185-item-5639':0
        },
        'option-label-color-93-item-5484':{
            'option-label-specification-185-item-5639':0
        }

    }
}

def sendEmail(title='test', content='hello world!', receivers=['']):
    mail_host = 'smtp.qq.com'
    mail_user = ''
    mail_pass = ''
    sender = ''

    # 设置email信息
    # 邮件内容设置
    message = MIMEText(content, 'plain', 'utf-8')
    # 邮件主题
    message['Subject'] = title
    # 发送方信息
    message['From'] = sender
    # 接受方信息
    message['To'] = receivers[0]

    # 登录并发送邮件
    try:
        smtpObj = smtplib.SMTP()
        # 连接到服务器
        smtpObj.connect(mail_host, 25)
        # 登录到服务器
        smtpObj.login(mail_user, mail_pass)
        # 发送
        smtpObj.sendmail(
            sender, receivers, message.as_string())
        # 退出
        smtpObj.quit()
    except smtplib.SMTPException as e:
        print('error', e)  # 打印错误

def qqmessage(content):
    qq = sendmessage.CSendQQMsg(friendName, content)
    qq.sendmsg()

def find(config):
    def couldAddTocart():
        add = browser.find_by_id('product-addtocart-button')
        return add.first.visible
    def findByIdWithTry(browser, id):
        def tryFind():
            rnt = None
            try:
                rnt = browser.find_by_id(id)
            except:
                pass
            return rnt

        for i in range(100):
            time.sleep(0.1)
            rnt = tryFind()
            if rnt is not None:
                return rnt
        raise Exception('超时')
    def getPrice(str):
        list = str.split("\n")
        for price in list:
            if not('￥' in price):
                continue
            price = price.split('.')[0]
            price = price[2:]
            price = price.split(',')
            rnt = 0
            for i in price:
                rnt = rnt * 1000 + int(i)
            return rnt


    print('doing your job!')
    browser = Browser()

    while True:
        content = str(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
        count = 0
        for url in config:
            # Visit URL
            browser.visit(url)
            time.sleep(0.5)
            for index in config[url]:
                try:
                    button = findByIdWithTry(browser, index)
                    button.click()
                    for element in config[url][index]:
                        try:
                            count = count+1
                            try:
                                title = findByIdWithTry(browser, 'bundleHeaderSummary').text.split('\n')[0]
                            except:
                                title = ' '
                            print(('-'*7)+str(count)+" : "+title+(' -'*5)+'\n\r')
                            content = content + '\r' + ('-'*5)+str(count)+" : "+title+(' -'*5)+'\r'
                            text = findByIdWithTry(browser, element)
                            textall = text.text
                            text = text.text.replace('\r',' ').replace('\n', ' ')
                            try:
                                text.click()
                            except:
                                pass
                            content = content + text+"\r"
                            if couldAddTocart():
                                print(text)
                                for i in config[url][index]:
                                    if int(config[url][index][i]) < getPrice(textall):
                                        print("太贵了")
                                        content = content + '有货，太贵！\t期望价格：￥'+str(config[url][index][i])+'\r'
                                    else:
                                        print('剁手吧，憨批')
                                        content = content + "剁手啦" * 100
                                        print("剁手！")
                                        # Todo:写邮件提醒，然后吧exit取消掉！
                                        for j in range(20):
                                            try:
                                                qqmessage(content)
                                            except:
                                                pass
                                            try:
                                                sendEmail('快剁手！', content)
                                            except:
                                                pass
                                            time.sleep(10)
                                    break
                            else:
                                print('耍猴ing~:')
                                print(text)
                                content = content + "耍猴ing~\r"

                        except:
                            print(config[url][index], '不存在')

                except:
                    print(index, '不存在')
        if debug:
            sendEmail('Debug', content)
            content = '-DEBUG'*3+'-\r'+content
            qqmessage(content)
            time.sleep(10)
        time.sleep(1)

if __name__ == '__main__':
    find(config)
    # sendEmail('Hello World!')

