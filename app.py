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

#ml
import operator
import io
from gensim.models.word2vec import Word2Vec
from gensim.models.keyedvectors import KeyedVectors
from sklearn.preprocessing import scale
import numpy as np
#from sklearn.manifold import TSNE
#import matplotlib.pyplot as plt
import jieba
from sklearn.cross_validation import train_test_split
from sklearn.linear_model import SGDClassifier


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
ans4=u'多聊聊你的故事'

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

# Do some very minor text preprocessing
def cleanText(corpus):
    corpus = [z.lower().replace('\n','').split() for z in corpus]
    return corpus

# build word vector for training set by using the average value of all word vectors in the tweet, then scale
def buildWordVector(imdb_w2v,text, size):
    vec = np.zeros(size).reshape((1, size))
    count = 0.
    for word in text:
        try:
            vec += imdb_w2v[word].reshape((1, size))
            count += 1.
        except KeyError:
            continue 
    if count != 0:
        vec /= count
    return vec 

##ML
with open('pos_chinese.txt', 'r') as infile:
    pos_tweets = infile.readlines()

with open('neg_chinese.txt', 'r') as infile:
    neg_tweets = infile.readlines()

# use 1 for positive sentiment, 0 for negative
y = np.concatenate((np.ones(len(pos_tweets)), np.zeros(len(neg_tweets))))

x_train, x_test, y_train, y_test = train_test_split(np.concatenate((pos_tweets, neg_tweets)), y, test_size=0.1)


x_train = cleanText(x_train)
x_test = cleanText(x_test)

n_dim = 300
#Initialize model and build vocab
imdb_w2v = Word2Vec(size=n_dim, min_count=10)
imdb_w2v.build_vocab(x_train)

#Train the model over train_reviews (this may take several minutes)
imdb_w2v.train(x_train)
imdb_w2v.save('chsen.model.bin')

#model = KeyedVectors.load('chsen.model.bin')
train_vecs = np.concatenate([buildWordVector(imdb_w2v,z, n_dim) for z in x_train])
train_vecs = scale(train_vecs)

#Train word2vec on test tweets
imdb_w2v.train(x_test)

#Build test tweet vectors then scale
test_vecs = np.concatenate([buildWordVector(imdb_w2v,z, n_dim) for z in x_test])
test_vecs = scale(test_vecs)

#Use classification algorithm (i.e., Stochastic Logistic Regression) on training set, then assess model performance on test set


lr = SGDClassifier(loss='log', penalty='l2')
#print(train_vecs)
#print(y_train)
lr.fit(train_vecs, y_train)
#print(lr)   


def test_sentance(imdb_w2v,lr,input_sentence):

    # jieba custom setting.
    jieba.set_dictionary('dict.txt')

    # load stopwords set
    stopwordset = set()
    with io.open('stopwords.txt','r',encoding='utf-8') as sw:
        for line in sw:
            stopwordset.add(line.strip('\n'))
    word_list = jieba.cut(input_sentence, cut_all=False)
    pos_result = 0
    neg_result = 0
    for word in word_list:
        if word not in stopwordset:
            if word in imdb_w2v.wv.vocab:
                vector = imdb_w2v.wv[word]
                #print(vector)
                ans = lr.predict([vector])
                anslist = ans.tolist()
                #print(ans)
                if(anslist[0] == 1):
                    print(word)
                    print(anslist[0])
                    print("pos_result += 1")
                    pos_result = pos_result + 1
                elif(anslist[0] == 0):
                    print(word)
                    print(anslist[0])
                    print("neg_result += 1")
                    neg_result = neg_result + 1;
                else:
                    print("do nothing")
                    continue
    return {'pos':pos_result,'neg':neg_result}





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
    condition = -1
    if text == ques1:
        text=ans1
    elif text ==ques2:
        text=ans2
    elif text ==ques3:
        text=ans3
    else:
        condition=0
        '''
        query = text

        result = {}
        result = test_sentance(imdb_w2v,lr,query)
        if(result['pos'] > result['neg']):
            condition=1
        elif(result['neg'] > result['pos']):
            condition=0
        else:
            text=ans4
            condition=2
        '''
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
        elif condition==0 :                   #sadreply
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
        TextSendMessage(text+str(condition))  ) #reply the same message from user
    

import os
if __name__ == "__main__":
    app.run(host='0.0.0.0',port=os.environ['PORT'])
