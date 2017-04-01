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
        text=ans4
    #textlength=len(text)
    #texttype=type(text)
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text)  ) #reply the same message from user
    

import os
if __name__ == "__main__":
    app.run(host='0.0.0.0',port=os.environ['PORT'])
