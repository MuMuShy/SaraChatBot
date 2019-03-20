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

def get_reply(user_message,user_id=0):
    user_message = str(user_message)
    for command in command_dictionary.word.keys():
        if user_message.startswith(command):
            action_command = command_dictionary.word[command]
            return eval(action_command)
    return talk_normal(user_message)


def get_MySql_command(user_MySql,user_message):
    for x in range(len(user_MySql)):
        if user_MySql[x] == '1':
            command_index=str(x)
            action_command=command_dictionary.word_MySQl[command_index]
            return eval(action_command)


#普通回話
def talk_normal(user_message):
    from chatterbot import ChatBot
    from chatterbot.trainers import ChatterBotCorpusTrainer
    from googletrans import Translator
    class Sara:
        # 建立一個 ChatBot
        chatbot = ChatBot(
            # 這個 ChatBot 的名字叫做 Sara
            "Sara",
            storage_adapter="chatterbot.storage.SQLStorageAdapter",
            
        )

        def __init__(self):
            self.trainer = ChatterBotCorpusTrainer(self.chatbot)
            self.trainer.train("./chatterbot_corpus /data/chinese/SaraChinese.yml")


        def getResponse(self, message=""):
            return self.chatbot.get_response(message)

    bot=Sara()
    reply = bot.getResponse(user_message)
    translator = Translator()
    reply = translator.translate(str(reply), dest='zh-TW').text
    reply = package_text(str(reply))
    return reply

#查詢IECS考古題
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




#計算狗糧剩餘場數
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
#搜尋御魂配置
def search_roiyarusupiritto(user_message):
    from bs4 import BeautifulSoup
    import requests
    import re
    from googletrans import Translator
    import re
    res = requests.get('http://news.4399.com/yyssy/shishenlu/')
    soup = BeautifulSoup(res.content, 'lxml')
    ShiKiGaMi = {}
    for li in soup.find_all('a', href=re.compile('http://news.4399.com/yyssy/shishenlu/\w')):
        ShiKiGaMi[li.text] = [li['href'], 'https://mumu.tw/mumu/image/onmyoji/' + li.text + '.jpg']
    shikigami_name_TW = user_message.split(' ')[-1]
    translator = Translator()
    shikigami_name = translator.translate(shikigami_name_TW,dest='zh-CN').text
    res2 = requests.get(ShiKiGaMi[shikigami_name][0])
    soup2 = BeautifulSoup(res2.content,'lxml')
    roiyarusupiritto_name=[]
    roiyarusupiritto_place=[]
    for con_hd in soup2.select('div .con .hd'):
        roiyarusupiritto_name.append(con_hd.text)
    for con_bd in soup2.select('div .con .bd'):
        roiyarusupiritto_place.append(con_bd.text)
    imageurl = ShiKiGaMi[shikigami_name][1]
    title = shikigami_name
    text = ''
    for i in range(0,len(roiyarusupiritto_name)):
        text = text + roiyarusupiritto_name[i] + '\n'
        if i != len(roiyarusupiritto_name)-1:
            text+='\n'
    label = '查看'
    actionurl = ShiKiGaMi[shikigami_name][0]
    reply = imageurl + ' ' + title + ' ' + text + ' ' + label + ' ' + actionurl
    reply = package_button_template(unpackage_text=reply)
    return reply

#推薦吃什麼
def recommend_food(user_message):
    import re
    from bs4 import BeautifulSoup
    import requests
    import random
    from selenium import webdriver
    cities = ['台北市', '新北市', '桃園市', '台中市', '台南市', '高雄市', '基隆市', '新竹市', '嘉義市', '新竹縣',
              '苗栗縣', '彰化縣', '南投縣', '雲林縣', '嘉義縣', '屏東縣', '宜蘭縣', '花蓮縣', '台東縣', '澎湖縣']

    try:
        if type(user_message) == str:
            url = 'https://www.foodpanda.com.tw/' + user_message
        else:
            lat = user_message.latitude
            lng = user_message.longitude
            address = user_message.address
            for c in cities:
                if re.search(c, address) != None:
                    city = c
            url = 'https://www.foodpanda.com.tw/restaurants/lat/' + str(lat) + '/lng/' + str(
                lng) + '/city/' + city + '/address/' + address
        print(url)
        res = requests.get(url)
        soup = BeautifulSoup(res.content, 'lxml')
        stores = []
        summarys = []
        costs = []
        pictures = []
        food_datas = {}
        for store in soup.find_all('span', 'name fn'):
            stores.append(store.text.replace(' ', ''))
        for summary in soup.find_all('li', 'vendor-characteristic'):
            summarys.append(summary.text[1:-1].replace('\n', ','))
        for cost in soup.find_all('ul', 'extra-info mov-df-extra-info'):
            costs.append(cost.text.replace('\n', '').replace(' ', ''))
        for picture in soup.find_all('div', 'vendor-picture b-lazy'):
            pictures.append(picture['data-src'].split('|')[0])
        for index, key in enumerate(stores):
            food_datas[key] = [summarys[index], costs[index], pictures[index]]
        which_one = random.randint(0, len(stores)-1)
        imageurl = food_datas[stores[which_one]][2]
        title = stores[which_one]
        text = food_datas[stores[which_one]][0] + '\n' + food_datas[stores[which_one]][1]
        label = '下一個'
        actionurl = url.replace('https://www.foodpanda.com.tw/', '')
    except:
        if type(user_message) == str:
            url = 'https://www.ipeen.com.tw/search/all/000/1-0-0-0/?adkw=' + user_message + '&so=sat'
        else:
            for c in cities:
                if re.search(c, address) != None:
                    x = c
            city = address[re.search(x[0], address).span()[0]:re.search('區', address).span()[1]]
            url = 'https://www.ipeen.com.tw/search/all/000/1-0-0-0/?adkw=' + city + '&so=sat'
        print(url)
        res = requests.get(url)
        soup = BeautifulSoup(res.content, 'lxml')
        stores = []
        summarys = []
        pictures = []
        for store in soup.find_all('a', {'data-label': '店名'}):
            stores.append(store.text.replace(' ', ''))
        for summary in soup.find_all('li', 'cate'):
            summarys.append(summary.text.replace('\xa0', '').replace('\n', '').replace(' ', ''))
        for picture in soup.find_all('img', 'lazy'):
            pictures.append(picture['src'])
        which_one = random.randint(0, len(stores)-1)
        print(which_one)
        imageurl = pictures[which_one]
        title = stores[which_one]
        text = summarys[which_one]
        label = '下一個'
        actionurl = url.replace('https://www.ipeen.com.tw/search/all/000/1-0-0-0/?adkw=', '').replace('&so=sat', '')
    reply = imageurl + ' ' + title + ' ' + text + ' ' + label + ' ' + actionurl
    reply = package_button_template(unpackage_text=reply)
    return reply


# 查詢食物 第一次執行將資料庫某指令設為true
def set_MySqlfood(user_message,user_id):
    print('更新使用者食物查詢狀態:'+user_id)
    id=user_id
    import requests
    data={'id':id,'command':'recommend_food(user_message)'}
    r = requests.post('http://mumu.tw/mumu/php/Sara/SetCommand.php', data=data)
    print(r.text)
    reply='按左下角的+ 發送位置訊息給我 我就能推薦你食物呦！'
    reply=package_text(reply)
    return reply

#推薦歌曲
def recommend_music():
    import json
    import random
    with open('./music.json', 'r') as load_f:
        song_datas = json.load(load_f)
    songs = song_datas.keys()
    choose_one = songs[random.randint(0, len(song_datas)-1)]
    imageurl = song_datas[choose_one][1]
    title = song_datas[choose_one][0]
    text = song_datas[choose_one][3]
    label = 'MUSIC'
    actionurl = song_datas[choose_one][2]
    reply = imageurl + ' ' + title + ' ' + text + ' ' + label + ' ' + actionurl
    reply = package_button_template(unpackage_text=reply)
    return reply

#查詢傳說對決基本資料
def search_ArenaofValor(user_message):
    from bs4 import BeautifulSoup
    import requests
    what_to_search = user_message.split(' ')[-1]
    res = requests.get('https://pro.moba.garena.tw/heroList')
    soup = BeautifulSoup(res.content,'lxml')
    hero_urls=[]
    hero_names=[]
    hero_pictures=[]
    hero_datas={}
    for hero in soup.find_all('a','herolist-list__item-a'):
        hero_names.append(hero.text.replace('\t','').replace('\n',''))
        hero_urls.append(hero['href'])
    for hero in soup.find_all('img'):
        hero_pictures.append('https:'+hero['src'])
    for index in range(0,len(hero_names)):
        hero_datas[hero_names[index]] = [hero_urls[index],hero_pictures[index]]
    imageurl = hero_datas[what_to_search][1]
    title = what_to_search
    text = what_to_search
    label = '查看'
    actionurl = hero_datas[what_to_search][0]
    reply = imageurl + ' ' + title + ' ' + text + ' ' + label + ' ' + actionurl
    reply = package_button_template(unpackage_text=reply)
    return reply



