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
    text=ans1
    textlength=len(text)
    texttype=type(text)
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=text+str(textlength)+str(texttype))  ) #reply the same message from user
    

import os
if __name__ == "__main__":
    ques1=codecs.open("ques1.txt", "r", "utf-8")
    ans1=codecs.open("ans1.txt", "r", "utf-8")
    app.run(host='0.0.0.0',port=os.environ['PORT'])
