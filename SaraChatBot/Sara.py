#!/usr/bin/env python
# coding: utf-8

import command_dictionary


def package_text(unpackage_text):
    unpackage_text = 'text;'+unpackage_text
    return str(unpackage_text)


def get_reply(user_message):
    user_message = str(user_message)
    for command in command_dictionary.word.keys():
        if user_message.startswith(command):
            action_command = command_dictionary.word[command]
            return eval(action_command)
    return "12344"


def talk_normal(user_message):
    reply = str("hello~"+user_message)
    print('Sara 回覆:'+reply)
    return reply


def calculate_dogfood(user_message):
    import re
    import math
    if user_message == '狗糧 ?':
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

