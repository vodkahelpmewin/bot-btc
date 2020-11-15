import requests
from bs4 import BeautifulSoup
import csv
import subprocess
import re
import sqlalchemy
import config
import random
import telebot
from telebot import types
import json
from time import sleep

bot = telebot.TeleBot(config.token)


@bot.message_handler(commands=["start"])
def cmd_start(message):
    bot.send_message(message.chat.id, "Новости: \nhabr - GO \nkanobu - KA")


@bot.message_handler(content_types=['text'])
def get_text_messages_go(message):
    if message.text == "GO":
        headers = ({
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.80 Safari/537.36'})

        habr_page = 'https://habr.com/ru/news/'
        # response = requests.get(main_page)
        # print(response)
        # html = response.content

        full_page = requests.get(habr_page, headers=headers)
        page = full_page.text
        # забераем всю страницу
        soup = BeautifulSoup(page, "lxml")

        print("_________________________________________________")

        result1 = {}
        for item in soup.find_all("a", class_="post__title_link"):
            item_links = item.get('href')
            item_tags = item.getText()

            result1[item_tags] = item_links
            msg = result1[item_tags]
            bot.send_message(message.chat.id, msg)

        with open("all_news_habr.json", "w") as file:
            json.dump(result1, file, indent=4, ensure_ascii=False)

        subprocess.call("/Users/a17760485/Desktop/telegrambot/sendDocumentJSON.sh", shell=True)
    elif message.text == "KA":
        bot.send_message(message.from_user.id, "comming soon...")
        keyboard = types.InlineKeyboardMarkup()
        course = types.InlineKeyboardButton(text='Сourse $', callback_data='course')
        # добавляем кнопку на экран
        keyboard.add(course)
        habr_news = types.InlineKeyboardButton(text='Habr news', callback_data='habr')
        keyboard.add(habr_news)
        alll_habr_news = types.InlineKeyboardButton(text='All habr news', callback_data='alllnews')
        keyboard.add(alll_habr_news)
        mific = types.InlineKeyboardButton(text='Mific', callback_data='grade')
        keyboard.add(mific)
        bot.send_message(message.from_user.id, text='Выберай ;)', reply_markup=keyboard)

    elif message.text != "KA":
        bot.send_message(message.from_user.id, "Новости: \nHabr - GO \nMenu - KA")


@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    if call.data == "habr":
        headers = ({
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.80 Safari/537.36'})

        main_page = 'https://habr.com/ru/news/'

        full_page = requests.get(main_page, headers=headers)
        page = full_page.text
        # забераем всю страницу
        soup = BeautifulSoup(page, "lxml")

        print("_________________________________________________")

        result1 = {}
        for item in soup.find_all("a", class_="post__title_link"):
            item_links = item.get('href')
            item_tags = item.getText()

            result1[item_tags] = item_links
            msg = result1[item_tags] = item_links
            bot.send_message(call.message.chat.id, msg)

        with open("all_news_habr.json", "w") as file:
            json.dump(result1, file, indent=4, ensure_ascii=False)

        subprocess.call("/Users/a17760485/Desktop/telegrambot/sendDocumentJSON.sh", shell=True)

        msg = "habr news"
        # Отправляем текст в Телеграм
        bot.send_message(call.message.chat.id, msg)

    if call.data == "course":

        DOLLAR_RUB = 'https://www.google.com/search?sxsrf=ALeKk01NWm6viYijAo3HXYOEQUyDEDtFEw%3A1584716087546&source=hp&ei=N9l0XtDXHs716QTcuaXoAg&q=%D0%B4%D0%BE%D0%BB%D0%BB%D0%B0%D1%80+%D0%BA+%D1%80%D1%83%D0%B1%D0%BB%D1%8E&oq=%D0%B4%D0%BE%D0%BB%D0%BB%D0%B0%D1%80+&gs_l=psy-ab.3.0.35i39i70i258j0i131l4j0j0i131l4.3044.4178..5294...1.0..0.83.544.7......0....1..gws-wiz.......35i39.5QL6Ev1Kfk4'
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.80 Safari/537.36'}

        full_page = requests.get(DOLLAR_RUB, headers=headers)
        soup = BeautifulSoup(full_page.content, 'html.parser')
        convert = soup.findAll("span", {"class": "DFlfde", "class": "SwHCTb", "data-precision": 2})
        print(convert[0].text)

        msg = "Course $: " + convert[0].text
        bot.send_message(call.message.chat.id, msg)


    if call.data == "alllnews":
        headers = ({
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.80 Safari/537.36'})

        # n = 1
        # while n <= 50:
        for item in range(1, 51):
            habr_all_page = 'https://habr.com/ru/news/page'
            full_page = requests.get(habr_all_page + f"{item}", headers=headers)
            page = full_page.text
            # забераем всю страницу
            soup = BeautifulSoup(page, "lxml")
            link = soup.find_all("a", class_="post__title_link")

            #   file = '/Users/a17760485/Desktop/telegrambot/output-pars' + str(n) + '.html'
            file = f"/Users/a17760485/Desktop/telegrambot/habr-news-{item}.html"
            myfile1 = open(file, mode='w', encoding='UTF-8')
            myfile1.write(str(page))
            myfile1.close()
            print(f'Итерация {item} звершилась')
            sleep(1)
            msg = link
            bot.send_message(call.message.chat.id, msg)


bot.polling(none_stop=True, interval=0)
