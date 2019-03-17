from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *
import Sara


app = Flask(__name__)

# Channel Access Token
line_bot_api = LineBotApi('1OIbKHpoQ6M7tHdTgwyi3SIfHMq8aC5LPa/M+QYp/2mCOlPWxQgKX6JkBXjBuC3ZRhYKLWPN+D8uFdBN/nxTvT+exrdhpLvJPTQqPKLdzhJJa/t2cQSiF6SNgMbf1JqUEkGEmCYwhLZZha2omMuX6wdB04t89/1O/w1cDnyilFU=')
# Channel Secret
handler = WebhookHandler('0fa53597780a6097e5a73f0219c4925d')

# 監聽所有來自 /callback 的 Post Request
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

# 處理訊息
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    user_message = str(event.message.text)
    sara_reply = Sara.get_reply(user_message)
    print("訊息長度" + str(len(sara_reply)))
    for sara_reply_index in range(len(sara_reply)):
        print("索引"+str(sara_reply_index))
        print('Sara回覆:未處理:'+sara_reply[sara_reply_index])
        reply_type = str(sara_reply[sara_reply_index].split(';')[0])
        reply_message=str(sara_reply[sara_reply_index].split(';')[1])
        print('sara回覆:處理結果'+reply_message)
        if reply_type == 'text':
            print('文字回覆格式 開始回覆')
            line_bot_api.reply_message(event.reply_token, TextSendMessage(text=reply_message))
        else:
            line_bot_api.reply_message(event.reply_token, TextSendMessage(text="其他格式回覆"))
        #回傳字串


import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
