# encoding: utf-8
from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)
import codecs
import random
app = Flask(__name__)

line_bot_api = LineBotApi('+YrlgJ1c5YOs8NGIOUOPN2Z/Ya6zmtW2mlrynoKWm64OuqFFYIJ6Gy90AwyTZmg9bTPWUAa8bIA+tJfOgw1ekKR3/RUukTJw+9ppv08wBIF83Hx2FRqaKdcyZcUx2viZe8DXDc6l5ftaAyUNSt7cQQdB04t89/1O/w1cDnyilFU=') #Your Channel Access Token


handler = WebhookHandler('a29dfcc21df2547b09392b7f0a9cabbc') #Your Channel Secret

myquesfile=codecs.open("src/ques1.txt", "r", "utf-8")
myansfile=codecs.open("src/ans1.txt", "r", "utf-8")
ques1=myquesfile.read()
ans1=myansfile.read()
myquesfile.close()
myansfile.close()

ques2=u'我累了，我沒辦法熬過這一次'
ans2=u'相信我，你可以的！我建議你可以先看看【'+'TED'+u'】國際勵志大師安東尼．羅賓：'+'Why we do what we do'+u'。'+'http://www.knowledger.info/2014/07/29/tony-robbins-in-a-tedtalk-why-we-do-what-we-do/'+u'。'
ques3=u'或許一了百了比較輕鬆'
ans3=u'你先可以撥打衛生福利部'+'24'+u'小時安心專線：'+'0800-788-995'+u'、國際生命線協會'+'24'+u'小時電話協談：'+'1995'+u'聊聊看！'
ans4=u'洗洗睡比較快'

happyreply1=u'太棒了！我真是為你開心！'
happyreply2=u'好事可以多跟人分享，快樂會加倍喔！'
happyreply3=u'世界上果然有很多美好的事。'
happyreply4=u'你開心，我窩心。'
happyreply5=u'用心感受每天的快樂。'
happyreply6=u'願你每天笑口常開。'
happyreply7=u'守住你頭頂那片快樂的藍天。'
happyreply8=u'熱愛生命，快樂無所不在！'
happyreply9=u'讓我們一起來唱「快樂崇拜」！'
happyreply10=u'推薦你跟我一起聽首「一百件快樂的事」。'

sadreply1=u'你有的不愉快，讓我來分擔。'
sadreply2=u'每個人都有屬於自己快樂的公式，只是等待你發掘。'
sadreply3=u'盡力就好！'
sadreply4=u'睡個覺起來，明天又是新的一天！'
sadreply5=u'讓我們先一起唱首「煎熬」發洩一下！'
sadreply6=u'一秒前的事，就當它過去了吧。'
sadreply7=u'盡量跟我發洩吧！說完心情會好很多。'
sadreply8=u'多跟我說說，我是你永遠的垃圾桶。'
sadreply9=u'不要排斥不快樂，是它讓你了解快樂的珍貴。'
sadreply10=u'現在出門去運動吧！會讓你心情變好。'

@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'

@handler.add(MessageEvent, message=TextMessage)
def handle_text_message(event):
    text = event.message.text #message from user
    if text == ques1:
        text=ans1
    elif text ==ques2:
        text=ans2
    elif text ==ques3:
        text=ans3
    else:
        condition=0
        num=random.randint(1,10)
        if condition==1  :      #happyreply
            if num==1:
                text=happyreply1
            elif num==2:
                text=happyreply2
            elif num==3:
                text=happyreply3
            elif num==4:
                text=happyreply4
            elif num==5:
                text=happyreply5
            elif num==6:
                text=happyreply6
            elif num==7:
                text=happyreply7
            elif num==8:
                text=happyreply8
            elif num==9:
                text=happyreply9
            else:
                text=happyreply10
        else:                   #sadreply
            if num==1:
                text=sadreply1
            elif num==2:
                text=sadreply2
            elif num==3:
                text=sadreply3
            elif num==4:
                text=sadreply4
            elif num==5:
                text=sadreply5
            elif num==6:
                text=sadreply6
            elif num==7:
                text=sadreply7
            elif num==8:
                text=sadreply8
            elif num==9:
                text=sadreply9
            else:
                text=sadreply10
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text)  ) #reply the same message from user
    

import os
if __name__ == "__main__":
    app.run(host='0.0.0.0',port=os.environ['PORT'])
