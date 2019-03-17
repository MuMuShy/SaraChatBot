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


def calculate_dogfood(usermessage):
    reply = '狗糧萬歲'
    reply = package_text(unpackage_text=reply)
    print("處理結果"+reply)
    return reply


def get_Iecs_oldtest(user_message):
    from bs4 import BeautifulSoup
    import requests
    target_subject = '線性代數'
    r = requests.get('http://mumu.tw/mumu/Iecstest/1/grade1.html')
    soup = BeautifulSoup(r.content, 'html.parser')
    print(soup)
    url = soup.select("a")['href']
    print(url)
    reply = package_text(unpackage_text=url)
    return reply
