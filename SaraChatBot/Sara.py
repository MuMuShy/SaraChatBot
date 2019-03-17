#!/usr/bin/env python
# coding: utf-8
# In[ ]:

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


def normal_talk(user_message):
    reply = str("hello~"+user_message)
    print('Sara 回覆:'+reply)
    return reply


def calculator_dogfood():
    reply = '狗糧萬歲'
    reply = package_text(unpackage_text=reply)
    print("處理結果"+reply)
    return reply


