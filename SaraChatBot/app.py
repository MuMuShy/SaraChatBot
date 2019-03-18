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
@handler.add(MessageEvent, message=LocationMessage)
@handler.add(MessageEvent, message=StickerMessage)
def handle_message(event):
    user_message_type=event.message.type
    #使用者傳送了 地理位置類型
    if user_message_type == 'location':
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text="我知道你在哪！"))
        user_message=event.message
    # 使用者傳送了一般文字訊息
    elif user_message_type == 'text':
        user_message = str(event.message.text)
    # 使用者傳送了貼圖訊息
    elif user_message_type == 'sticker':
        print('收到貼圖訊息')
        line_bot_api.reply_message(event.reply_token, StickerSendMessage(package_id='1',sticker_id=410))
    print(user_message)
    sara_reply = Sara.get_reply(user_message)
    reply_type = sara_reply.split(';')[0]
    reply_message = sara_reply.split(';')[1]

    #回覆給使用者的格式
    if reply_type == 'text':
        print('文字回覆格式 開始回覆')
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=reply_message))
    elif reply_type == 'img':
        sara_reply=sara_reply.split(';')[1]
        original_img_url=sara_reply.split(' ')[0]
        print('大圖: '+original_img_url)
        preview_img_url=sara_reply.split(' ')[1]
        print('小圖: '+preview_img_url)
        message = ImageSendMessage(
            original_content_url=original_img_url,
            preview_image_url=preview_img_url
        )
        line_bot_api.reply_message(event.reply_token, message)
    elif reply_type == 'greeting':
        print('greeting!~')
        buttons_template = TemplateSendMessage(
            alt_text='Buttons Template',
            template=ButtonsTemplate(
                title='Sara',
                text='妳好～ 我是萬用的小助理 Sara',
                thumbnail_image_url='https://mumu.tw/mumu/image/sara.jpg',
                actions=[
                    MessageTemplateAction(
                        label='我愛你',
                        text='我愛Sara'
                    )
                ]
            )
        )
        line_bot_api.reply_message(event.reply_token, buttons_template)
    elif reply_type == 'buttontemplate':
        sara_reply = sara_reply.split(';')[1]
        messageobject = sara_reply.split(' ')
        _imageurl = messageobject[0]
        _title = messageobject[1]
        _text = messageobject[2]
        _label = messageobject[3]
        print('imageurl:'+_imageurl)
        print('title: '+_title)
        print('text: '+_text)
        print('label: '+_label)
        if len(messageobject)==5:
            _actionurl=messageobject[4]
            print('acitonurl: '+_actionurl)
        else:
            _actionurl=' '
        # 圖片文字回覆格式:圖片網址 標題 內文 按鈕 [目標網站(選填)]
        buttons_template = TemplateSendMessage(
            alt_text='Buttons Template',
            template=ButtonsTemplate(
                title=_title,
                text=_text,
                thumbnail_image_url=_imageurl,
                actions=[
                    MessageTemplateAction(
                        label=_label,
                        text=_actionurl
                    )
                ]
            )
        )
        line_bot_api.reply_message(event.reply_token, buttons_template)




import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
