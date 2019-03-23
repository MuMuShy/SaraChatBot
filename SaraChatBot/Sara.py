#!/usr/bin/env python
# coding: utf-8

import command_dictionary


#包裝純文字格式
def package_text(unpackage_text):
    unpackage_text = 'text;'+unpackage_text
    return str(unpackage_text)


#包裝圖片格式
def package_img(unpackage_text):
    unpackage_text='img;'+unpackage_text
    return str(unpackage_text)


#包裝按鈕回應格式
def package_button_template(unpackage_text):
    unpackage_text='buttontemplate;'+unpackage_text
    return str(unpackage_text)


#獲得回應 （程式回傳點）
def get_reply(user_message,user_id=0):
    user_message = str(user_message)
    for command in command_dictionary.word.keys():
        if user_message.startswith(command):
            action_command = command_dictionary.word[command]
            return eval(action_command)
    return talk_normal(user_message)


#獲得資料庫的指令
def get_MySql_command(user_MySql,user_message):
    for x in range(len(user_MySql)):
        if user_MySql[x] == '1':
            command_index=str(x)
            action_command=command_dictionary.word_MySQl[command_index]
            return eval(action_command)

# 教Sara 使用者說什麼@Sara應該回應什麼
def teach_Sara(user_message):
    import yaml
    commands=['教你 ','教妳 ']
    for command in commands:
        conversation_say=user_message.replace(command,'').split('@')[0]
        conversation_reply=user_message.replace(command,'').split('@')[-1]
    with open("./chatterbot_corpus /data/chinese/SaraChinese.yml", "r") as yaml_file:
        yaml_obj = yaml.load(yaml_file.read())
        old_conversation = yaml_obj["conversations"]
        dic = [conversation_say, conversation_reply]
        for items in old_conversation:
            if items == dic:
                print('指令已存在')
                yaml_file.close()
                reply = 'Sara好像學過這句話囉 ～～'
                reply = package_text(unpackage_text=reply)
                return reply
        print('指令不存在 新增指令')
        old_conversation.append(dic)
        with open('./chatterbot_corpus /data/chinese/SaraChinese.yml', 'w') as yaml_file:
            yaml_obj["conversations"] = old_conversation
            yaml.dump(yaml_obj, yaml_file, default_flow_style=False, encoding=('utf-8'))
            reply = 'Sara學會新的對話了 ！ 謝謝你～～'
            reply = package_text(unpackage_text=reply)
            return reply


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
            print('訓練完畢')


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
    import os
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
    songs = []
    for key in song_datas.keys():
        songs.append(key)
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


#難產中
def search_ilearnBroadcast(user_message):
    from bs4 import BeautifulSoup
    import re
    from selenium import webdriver
    from selenium.webdriver.chrome.options import Options

    driver = webdriver.Chrome()
    driver.get("https://ilearn2.fcu.edu.tw/login/index.php")
    driver.find_element_by_id("username").click()
    driver.find_element_by_id("username").clear()
    driver.find_element_by_id("username").send_keys("d0440553")
    driver.find_element_by_id("password").click()
    driver.find_element_by_id("password").clear()
    driver.find_element_by_id("password").send_keys("Qazwaxxm3jo3g")
    driver.find_element_by_id("loginbtn").click()
    html = driver.page_source
    driver.close()
    soup = BeautifulSoup(html, 'lxml')
    courses = []
    course_urls = []
    course_summarys = {}
    for course in soup.find_all('a', {'href': re.compile('https://ilearn2.fcu.edu.tw/course/')}):
        try:
            if course.i['class'] == ['fa', 'fa-graduation-cap']:
                courses.append(course.text)
                course_urls.append(course['href'])
        except:
            pass
    for index, url in enumerate(course_urls):
        summarys = []
        driver = webdriver.Chrome()
        driver.get(url)
        driver.find_element_by_id("username").click()
        driver.find_element_by_id("username").clear()
        driver.find_element_by_id("username").send_keys("d0440553")
        driver.find_element_by_id("password").click()
        driver.find_element_by_id("password").clear()
        driver.find_element_by_id("password").send_keys("Qazwaxxm3jo3g")
        driver.find_element_by_id("loginbtn").click()
        driver.find_element_by_xpath(
            u"(.//*[normalize-space(text()) and normalize-space(.)='一般'])[1]/following::span[1]").click()

        html = driver.page_source
        driver.close()
        soup = BeautifulSoup(html, 'lxml')

        for td in soup.find_all('td', 'topic starter'):
            summarys.append(td.text)
        course_summarys[courses[index]] = summarys
    text = ''
    for index, course in enumerate(courses):
        text = text + course + '\n' + course_urls[index] + '\n'
        if course_summarys[course] == []:
            course_summarys[course] = ['沒有公告']
        for summary in course_summarys[course]:
            text += summary + ' '
        text += '\n'


def image_recognition(imagefilepath):
    reply=""
    import base64
    import json
    outputfile = 'data.json'
    requestlist = []
    feature_json_obj = []
    features = "FACE_DETECTION WEB_DETECTION"
    with open(imagefilepath, 'rb')as image_file:
        content_json_obj = {
            "content": base64.b64encode(image_file.read()).decode('UTF-8')
        }
    for word in features.split(' '):
        feature_json_obj.append({
            "type": word,
            "maxResults": "10"
        })

    requestlist.append({
        "features": feature_json_obj,
        "image": content_json_obj,
    })

    with open(outputfile, 'w') as output_file:
        json.dump({"requests": requestlist}, output_file)

    print('Send requests...')

    import requests
    data = open('./data.json', 'rb').read()
    response = requests.post(
        url='https://vision.googleapis.com/v1/images:annotate?key=AIzaSyBSscdPQsM_AFZapsFOHK66U-TgHjdX_8M',
        data=data,
        headers={'Content-Type': 'application/json'})
    response = response.text
    response_json = json.loads(response)
    face_response = response_json['responses'][0]
    peoplecount = 1
    emotions = ["喜悅 joyLikelihood", "難過 sorrowLikelihood", "生氣 angerLikelihood", "驚訝 surpriseLikelihood",
                "備感壓力 underExposedLikelihood", "憂鬱 blurredLikelihood", "戴帽子 headwearLikelihood"]
    compare_result = ["非常低的可能 VERY_UNLIKELY", "低可能 UNLIKELY", "可能 LIKELY", "非常可能 VERY_LIKELY","吻合 POSSIBLE"]
    if 'faceAnnotations' in response_json['responses'][0]:
        for face_result in face_response['faceAnnotations']:
            print('第', peoplecount, "個人看起來: \n")
            counttemp=str(peoplecount)
            reply += '第'+counttemp+"個人看起來: \n"
            for emotion in emotions:
                emotion_chinese = emotion.split(' ')[0]
                emotion_compare = emotion.split(' ')[1]
                for result in compare_result:
                    result_chinese = result.split(' ')[0]
                    result_compare = result.split(' ')[1]
                    if face_result[emotion_compare] == result_compare:
                        face_result[emotion_compare] = result_chinese
                print(emotion_chinese, ": ", face_result[emotion_compare])
                reply += str(emotion_chinese)+": "+str(face_result[emotion_compare])+"\n"
            peoplecount += 1
            print('\n')
            reply += '\n'
    else:
        reply+='你似乎給了我一張沒有人的照片呢 不過我還是幫你找一下網路上有沒有這張圖片\n'
    print('網頁分析')
    if 'fullMatchingImages' in response_json['responses'][0]['webDetection']:
        print(response_json['responses'][0]['webDetection']['fullMatchingImages'])
        print('\n')
        web_response_fullmatch = response_json['responses'][0]['webDetection']['fullMatchingImages']
        web_response_pagesmatch = response_json['responses'][0]['webDetection']['pagesWithMatchingImages']
        for url in web_response_fullmatch:
            print("找到與圖片吻合的網址: ", url['url'])
            urltemp=str(url['url'])
            reply += "找到與圖片吻合的網址: "+urltemp+'\n'
        for url_item in web_response_pagesmatch:
            print('找到有出現圖片的網站: '+url_item['url'])
            urltemp = str(url_item['url'])
            reply += '找到有出現圖片的網站:'+urltemp+'\n'
    else:
        print('沒有圖片出現吻合的網站資料')
        reply+='沒有圖片出現吻合的網站資料'+'\n'
    if 'visuallySimilarImages' in response_json['responses'][0]['webDetection']:
        web_response_simullar = response_json['responses'][0]['webDetection']['visuallySimilarImages']
        simullar_max = 3  # 最多列出五個相似
        for items in web_response_simullar:
            if simullar_max <= 0:
                break
            else:
                print("找到與圖片相似的網站: ", items['url'])
                urltemp=str(items['url'])
                reply += "找到與圖片相似的網站: "+urltemp+'\n'
                simullar_max -= 1
    else:
        print('沒有相似圖片的網站資料')
        reply += '沒有相似圖片的網站資料'+'\n'

    reply=package_text(reply)
    return reply
