#匯入模組
from flask import Flask,request,abort
from linebot import LineBotApi,WebhookHandler
from linebot.models import MessageEvent,TextMessage,TextSendMessage
from datetime import datetime
import random


app=Flask(__name__)
#---------------------------------------------------------------------
#匯入聯動ID
line_bot_api=LineBotApi("HeY7xErJxPUD2+UrUyfikjhpi5XsB6rykrc06AwGheydfuCkjQQ6IjbJi60g/WamRk2DHX+0Sk18MLKwD1+anucjjVDDdjSHK4EfMNqv/Tn4eCOn2/zsy0heZod+FqdbAhiXoI95VuoBSnbsKKmvAgdB04t89/1O/w1cDnyilFU=")
handler=WebhookHandler("84678552c0bbd4a3026ee16c8cb8d4a7") 
#---------------------------------------------------------------------
#設定星座
Constellation_date={"牡羊座":((3,21),(4,19)),
                    "金牛座":((4,20),(5,20)),
                    "雙子座":((5,21),(6,20)),
                    "巨蟹座":((6,21),(7,22)),
                    "獅子座":((7,23),(8,22)),
                    "處女座":((8,23),(9,22)),
                    "天秤座":((9,23),(10,22)),
                    "天蠍座":((10,23),(11,21)),
                    "射手座":((11,22),(12,21)),
                    "摩羯座":((12,22),(1,19)),
                    "水瓶座":((1,20),(2,18)),
                    "雙魚座":((2,19),(3,20))}

def get_horoscope():

    career_coss=random.randint(1,10)
    love_coss=random.randint(1,10)
    wealth_coss=random.randint(1,10)


    career_point={
        1:"你很爛",
        2:"你很差",
        3:"我覺得不行",
        4:"很不好",
        5:"勉強",
        6:"好像還可以",
        7:"不錯奧",
        8:"很棒",
        9:"很可以",
        10:"超棒的啦"
    }

    love_point={
        1:"你很爛",
        2:"你很差",
        3:"我覺得不行",
        4:"很不好",
        5:"勉強",
        6:"好像還可以",
        7:"不錯奧",
        8:"很棒",
        9:"很可以",
        10:"超棒的啦"
    }

    wealth_point={
        1:"你很爛",
        2:"你很差",
        3:"我覺得不行",
        4:"很不好",
        5:"勉強",
        6:"好像還可以",
        7:"不錯奧",
        8:"很棒",
        9:"很可以",
        10:"超棒的啦"
    }
    
    career=career_point[career_coss]
    love=love_point[love_coss]
    wealth=wealth_point[wealth_coss]

    total_coss=(career_coss+love_coss+wealth_coss)//3
    if total_coss<=3:
        total_point="你實在是不行"
    
    elif total_coss<=7:
        total_point="你好像還可以"

    else:
        total_point="你很棒奧你贏了"        
    
    return{
        "career_coss":career_coss,
        "love_coss":love_coss,
        "wealth_coss":wealth_coss,
        "career":career,
        "love":love,
        "wealth":wealth,
        "total_coss":total_coss
    }



@app.route("/callback",methods=["POST"])

def callback():
    signature=request.headers["X-Line-Signature"]
    body=request.get_data(as_text=True)
    try:
        handler.handle(body,signature)
    except Exception as e:
        abort(400)
    return"OK"        



@handler.add(MessageEvent,message=TextMessage)
def handle_message(event):
    user_message=event.message.text
    today=datetime.today()
    user_month=today.month
    user_day=today.day
    
    try:
        birthday_month,birthday_day=map(int,user_message.split("/"))
    except ValueError:
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text="請輸入正確的生日格式"))

        return  

    user_zodiac=None
    for zodiac,(start,end) in Constellation_date.items():
        start_month,start_day=start
        end_month,end_day=end
        if(birthday_month>start_month or (birthday_month==start_month and birthday_day>=start_day)) and\
          (birthday_month<end_month or(birthday_month==end_month and birthday_day<=end_day)):
           user_zodiac=zodiac
           break
    if user_zodiac:
        shingzuoyunshi=get_horoscope()
        
        response_message=f"您的星座是:{user_zodiac}\n"
        response_message+=f"事業運勢:{shingzuoyunshi["career_coss"]}分-{shingzuoyunshi["career"]}\n"
        response_message+=f"感情運勢:{shingzuoyunshi["love_coss"]}分-{shingzuoyunshi["love"]}\n"
        response_message+=f"財運運勢:{shingzuoyunshi["wealth_coss"]}分-{shingzuoyunshi["wealth"]}\n"
        response_message+=f"今天總體運勢:{shingzuoyunshi['total_point']}"


    line_bot_api.reply_message(event.reply_token,TextSendMessage(text=response_message))




    









