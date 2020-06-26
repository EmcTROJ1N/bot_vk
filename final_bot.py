#! /usr/bin/env python3
# -*- coding: utf-8 -*-
from vk_api.utils import get_random_id
import vk
from bs4 import BeautifulSoup as BS
from selenium import webdriver
import time
from pyvirtualdisplay import Display

url = 'https://www.youtube.com/channel/UCXZBrkds6XdSOfH6--Y3Fug/videos'
token = '486ecea181ee5467cf628c6eca2c70ff2dd134521faddf0ed1906381aa5120fe6ab475f0c9fc2e58ab19c'

def parse_url(URL):
    while True:
        with Display():
            driver = webdriver.Chrome('/home/omon/python/chromedriver')
            driver.get(URL)
            time.sleep(10)  #Можно ждать до загрузки страницы, но проще подождать 10 секунд, их хватит с запасом
            html = driver.page_source
        soup = BS(html, "html.parser")
        videos = soup.find_all("ytd-grid-video-renderer",{"class":"style-scope ytd-grid-renderer"})
        a = videos[0].find("a",{"id":"video-title"})
        link = "https://www.youtube.com" + a.get("href")
        with open('last_url.log', 'r') as last_url:
            url = last_url.read()
            if url != link:
                with open('last_url.log', 'w') as last_url:
                    last_url.write(link)
                auto_send_wall(token, link)
                print('Вышел новый видосик!')
            else:
                print('Все нормуль, все чисто')
    sleep(180)


def auto_send_wall(tok, URL):
    import vk
    session = vk.Session(access_token = tok)
    vk = vk.API(session, scope = 'messages', v ='5.62')
    followers = vk.groups.getMembers(group_id = '355860713')
    msg = '''
            Новое видео на канале наркомана!!!
            Рекомендуется всем к просмотру!!!


            {0}
            {0}
            {0}

            '''.format(URL)
    for i in followers['items']:
        vk.messages.send(user_id = str(i), random_id = get_random_id(), message = msg)


while True:
    parse_url(url)
