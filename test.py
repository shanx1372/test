from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.models import MessageEvent, TextMessage, TextSendMessage
import random

app = Flask(__name__)

# 匯入LINE bot API
line_bot_api = LineBotApi("你的LINE Bot的Channel Access Token")
handler = WebhookHandler("你的LINE Bot的Channel Secret")

# 設定星座範圍
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
    "摩羯座": ((12, 22), (1, 19)),
    "水瓶座": ((1, 20), (2, 18)),
    "雙魚座": ((2, 19), (3, 20))
}

# 生成運勢數據
def get_horoscope():
    career_coss = random.randint(1, 10)
    love_coss = random.randint(1, 10)
    wealth_coss = random.randint(1, 10)

    career_point = {
        1: "你很爛", 2: "你很差", 3: "我覺得不行", 4: "很不好", 5: "勉強", 6: "好像還可以", 7: "不錯奧", 8: "很棒", 9: "很可以", 10: "超棒的啦"
    }
    love_point = {
        1: "你很爛", 2: "你很差", 3: "我覺得不行", 4: "很不好", 5: "勉強", 6: "好像還可以", 7: "不錯奧", 8: "很棒", 9: "很可以", 10: "超棒的啦"
    }
    wealth_point = {
        1: "你很爛", 2: "你很差", 3: "我覺得不行", 4: "很不好", 5: "勉強", 6: "好像還可以", 7: "不錯奧", 8: "很棒", 9: "很可以", 10: "超棒的啦"
    }

    career = career_point[career_coss]
    love = love_point[love_coss]
    wealth = wealth_point[wealth_coss]

    total_coss = (career_coss + love_coss + wealth_coss) // 3
    if total_coss <= 3:
        total_point = "你實在是不行"
    elif total_coss <= 7:
        total_point = "你好像還可以"
    else:
        total_point = "你很棒奧你贏了"

    return {
        "career_coss": career_coss,
        "love_coss": love_coss,
        "wealth_coss": wealth_coss,
        "career": career,
        "love": love,
        "wealth": wealth,
        "total_coss": total_coss
    }

# 根據生日來判斷星座
def get_zodiac(birthday_month, birthday_day):
    for zodiac, (start, end) in Constellation_date.items():
        start_month, start_day = start
        end_month, end_day = end

        if start_month < end_month:  # 星座在同一年內
            if start_month < birthday_month < end_month or \
               (birthday_month == start_month and birthday_day >= start_day) or \
               (birthday_month == end_month and birthday_day <= end_day):
                return zodiac
        else:  # 星座橫跨年底
            if birthday_month >= start_month or birthday_month <= end_month:
                if (birthday_month == start_month and birthday_day >= start_day) or \
                   (birthday_month == end_month and birthday_day <= end_day) or \
                   (start_month < birthday_month < end_month):
                    return zodiac
    return None

@app.route("/callback", methods=["POST"])
def callback():
    signature = request.headers["X-Line-Signature"]
    body = request.get_data(as_text=True)
    try:
        handler.handle(body, signature)
    except Exception as e:
        print(f"Error handling the request: {e}")
        abort(400)
    return "OK"


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    user_message = event.message.text
    try:
        birthday_month, birthday_day = map(int, user_message.split("/"))
    except ValueError:
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text="請輸入正確的生日格式（MM/DD）"))
        return

    user_zodiac = get_zodiac(birthday_month, birthday_day)
    if user_zodiac:
        horoscope = get_horoscope()
        response_message = f"您的星座是: {user_zodiac}\n"
        response_message += f"事業運勢: {horoscope['career_coss']}分 - {horoscope['career']}\n"
        response_message += f"感情運勢: {horoscope['love_coss']}分 - {horoscope['love']}\n"
        response_message += f"財運運勢: {horoscope['wealth_coss']}分 - {horoscope['wealth']}\n"
        response_message += f"今天總體運勢: {horoscope['total_point']}"
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=response_message))
    else:
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text="無法匹配您的星座，請檢查日期"))


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)
