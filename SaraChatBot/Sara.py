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
    return talk_normal()


def talk_normal():
    reply = 'hi~ i  am Sara'
    reply = package_text(unpackage_text=reply)
    return reply


def calculator_dogfood():
    reply = '狗糧萬歲'
    reply = package_text(unpackage_text=reply)
    print("處理結果"+reply)
    return reply


