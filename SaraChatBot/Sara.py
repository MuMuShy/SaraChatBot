#!/usr/bin/env python
# coding: utf-8

import command_dictionary


def package_text(unpackage_text):
    unpackage_text = 'text;'+unpackage_text
    return str(unpackage_text)


def package_img(unpackage_text):
    unpackage_text='img;'+unpackage_text
    return str(unpackage_text)


def package_button_template(unpackage_text):
    unpackage_text='buttontemplate;'+unpackage_text
    return str(unpackage_text)

def get_reply(user_message):
    user_message = str(user_message)
    for command in command_dictionary.word.keys():
        if user_message.startswith(command):
            action_command = command_dictionary.word[command]
            return eval(action_command)
    return talk_normal(user_message)


def talk_normal(user_message):
    reply = "https://mumu.tw/mumu/image/sara.jpg 標題123 內文 我是按鈕"
    reply = package_button_template(reply)
    print('reply 包裝後:'+reply)
    return reply


def get_Iecs_oldtest(user_message):
    from bs4 import BeautifulSoup
    import requests
    subject = user_message.split(" ")
    if len(subject) < 2:
        reply = 'https://mumu.tw/mumu/image/sara.jpg 考古題 你要的都在這 謝謝 https://drive.google.com/open?id=1F8n4jokD55fwix5zeNRy_Cw4REJUH_RN'
        reply = package_button_template(unpackage_text=reply)
        return reply
    target_subject = subject[1]
    print(target_subject)
    r = requests.get('http://mumu.tw/mumu/Iecstest/1/grade1.html')
    soup = BeautifulSoup(r.content, 'html.parser')
    print(soup)
    if soup.find('a', id=target_subject) == None:
        reply = '找不到此科目 可能資料庫沒有或是輸入錯誤\n如想提供考古題 可聯絡開發者～\nhttps://line.me/ti/p/SoDXl-PPop'
        reply = package_text(unpackage_text=reply)
        return reply
    url = soup.find('a', id=target_subject)['href']
    print(url)
    reply='找到關於:'+target_subject+'的考古題: '+url
    reply = package_text(unpackage_text=reply)
    return reply





def calculate_dogfood(user_message):
    import re
    import math
    print(user_message)
    if user_message == '狗糧 ?' or user_message == '狗糧 ？':
        reply = package_text(unpackage_text='請依照：\n「狗糧 二星滿等白蛋(包含三星20等白蛋),二星滿等(包含三星1|20等),三星滿等(包含四星1|25等),四星滿等(包含五星)」\n 方式輸入')
        return reply
    kind_of_dog_food = []
    for message in user_message[re.search('\d+,\d+,\d+,\d+',user_message).span()[0]:re.search('\d+,\d+,\d+,\d+',user_message).span()[1]].split(','):
        kind_of_dog_food.append(int(message))
    total_exp = 17047390
    special_exp = kind_of_dog_food[0]*95710
    exp_twenty = kind_of_dog_food[1]*150000
    exp_twentyfive = (kind_of_dog_food[0]+kind_of_dog_food[2])*170710
    exp_thirty = kind_of_dog_food[3]*340070
    now_have_Exp = (exp_thirty+exp_twenty+exp_twentyfive)-special_exp
    print('now you have exp:',now_have_Exp)
    still_need_exp = math.ceil((total_exp - now_have_Exp)/5374)
    content = '以探索28困難計算:\n(月卡):' + str(math.ceil(still_need_exp/1.15)) + '\n(月卡,50%):' + str(math.ceil(still_need_exp/1.15/1.5)) + '\n(月卡,50%,100%):' + str(math.ceil(still_need_exp/1.15/1.5/2)) + '\n(月卡,50%,100%,陰陽寮):' + str(math.ceil(still_need_exp/1.15/1.5/2/1.1))
    content = content + '\n(月卡,50%,100%,陰陽寮,好友組隊):' + str(math.ceil(still_need_exp/1.15/1.5/2/1.1/1.3))
    reply = package_text(unpackage_text=content)
    return reply
