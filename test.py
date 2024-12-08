from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.models import MessageEvent, TextMessage, TextSendMessage
import random

app = Flask(__name__)

# 設定 LineBot API
line_bot_api = LineBotApi("HeY7xErJxPUD2+UrUyfikjhpi5XsB6rykrc06AwGheydfuCkjQQ6IjbJi60g/WamRk2DHX+0Sk18MLKwD1+anucjjVDDdjSHK4EfMNqv/Tn4eCOn2/zsy0heZod+FqdbAhiXoI95VuoBSnbsKKmvAgdB04t89/1O/w1cDnyilFU=")
handler = WebhookHandler("84678552c0bbd4a3026ee16c8cb8d4a7")

# 儲存用戶的運勢結果
user_horoscope_dict = {}

# 星座日期對應（包含跨年處理）
Constellation_date = {
    "牡羊座": ((3, 21), (4, 19)),
    "金牛座": ((4, 20), (5, 20)),
    "雙子座": ((5, 21), (6, 20)),
    "巨蟹座": ((6, 21), (7, 22)),
    "獅子座": ((7, 23), (8, 22)),
    "處女座": ((8, 23), (9, 22)),
    "天秤座": ((9, 23), (10, 22)),
    "天蠍座": ((10, 23), (11, 21)),
    "射手座": ((11, 22), (12, 21)),
    "摩羯座": ((12, 22), (1, 19)),  # 跨年處理
    "水瓶座": ((1, 20), (2, 18)),
    "雙魚座": ((2, 19), (3, 20)),
}

# 星座運勢生成
def get_horoscope():
    career_coss = random.randint(1, 10)
    love_coss = random.randint(1, 10)
    wealth_coss = random.randint(1, 10)

    career_point = {
        1: "大凶",
        2: "大凶",
        3: "凶。",
        4: "凶。",
        5: "良好",
        6: "良好",
        7: "優良",
        8: "優良",
        9: "大吉",
        10: "大吉"
    }

    love_point = career_point
    wealth_point = career_point
    
    career = career_point[career_coss]
    love = love_point[love_coss]
    wealth = wealth_point[wealth_coss]

    total_coss = (career_coss + love_coss + wealth_coss) // 3
    if total_coss <= 3:
        total_point = "您今天的運勢是很差的，一言難盡。"
    elif total_coss <= 7:
        total_point = "您今天的運勢是良好，可保持平常心。"
    else:
        total_point = "您今天的運勢超棒的，無所畏懼！勇往直前！！！"        

    return {
        "career_coss": career_coss,
        "love_coss": love_coss,
        "wealth_coss": wealth_coss,
        "career": career,
        "love": love,
        "wealth": wealth,
        "total_coss": total_coss,
        "total_point": total_point
    }

# 處理回調函數
@app.route("/callback", methods=["POST"])
def callback():
    signature = request.headers["X-Line-Signature"]
    body = request.get_data(as_text=True)
    print(f"Received body:{body}")
    try:
        handler.handle(body, signature)
    except Exception as e:
        print(f"Error handling the request:{e}")
        abort(400)
    return "OK"

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    print("收到訊息:", event.message.text)
    user_message = event.message.text
    user_id = event.source.user_id  # 提取用戶的 user_id

    try:
        birthday_month, birthday_day = map(int, user_message.split("/"))
        print(f"您的生日是:{birthday_month}/{birthday_day}")  # 確認生日解析結果
    except ValueError:
        # 如果格式錯誤，回覆提示訊息
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text="請輸入正確的生日格式 (MM/DD)，例如 08/15"))
        return

    user_zodiac = None

    # 星座匹配邏輯
    for zodiac, (start, end) in Constellation_date.items():
        start_month, start_day = start
        end_month, end_day = end

        # 處理跨年星座邏輯
        if start_month < end_month:  # 當星座的開始月份小於結束月份（如金牛座 4/20 - 5/20）
            if (start_month < birthday_month < end_month) or\
               (birthday_month == start_month and birthday_day >= start_day) or\
               (birthday_month == end_month and birthday_day <= end_day):
                user_zodiac = zodiac
                break
        else:  # 處理跨年的星座（如摩羯座 12/22 - 1/19）
            if (birthday_month > start_month or (birthday_month == start_month and birthday_day >= start_day)) or\
               (birthday_month < end_month or (birthday_month == end_month and birthday_day <= end_day)):
                user_zodiac = zodiac
                break

    # 檢查該 user_id 是否已有運勢結果
    if user_id in user_horoscope_dict:
        # 如果已有運勢結果，直接返回
        horoscope = user_horoscope_dict[user_id]
        response_message = f"您的星座是:{horoscope['zodiac']}\n"
        response_message += f"事業運勢:{horoscope['career']}\n"
        response_message += f"感情運勢:{horoscope['love']}\n"
        response_message += f"財運運勢:{horoscope['wealth']}\n"
        response_message += f"今天總體運勢:{horoscope['total_point']}"
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=response_message))
        print(f"Sending response (cached):{response_message}")
        return

    if user_zodiac:
        print(f"User zodiac found:{user_zodiac}")
        horoscope = get_horoscope()

        response_message = f"您的星座是:{user_zodiac}\n"
        response_message += f"事業運勢:{horoscope['career_coss']}分-{horoscope['career']}\n"
        response_message += f"感情運勢:{horoscope['love_coss']}分-{horoscope['love']}\n"
        response_message += f"財運運勢:{horoscope['wealth_coss']}分-{horoscope['wealth']}\n"
        response_message += f"今天總體運勢:{horoscope['total_point']}"

        # 將結果存入字典
        horoscope["zodiac"] = user_zodiac
        user_horoscope_dict[user_id] = horoscope

        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=response_message))
        print(f"Sending response (new):{response_message}")
    else:
        print("Zodiac not found")
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text="您輸入的星座無法識別，請檢查日期"))

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
