# -*- coding: utf-8 -*-

import mechanize
import bs4
import telebot
from config import *

bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(commands=["start"])
def start(message):
    bot.send_message(message.chat.id, "Привіт! Я можу надіслати тобі розклад занять Волинського національного університету імені Лесі Українки.\nПросто напишіть назву своєї групи нижче👇")

@bot.message_handler(content_types=["text"])
def text(message):

    browser = mechanize.Browser()
    browser.open(URL)

    browser.select_form(name="setVedP")
    browser["group"] = message.text
    response = browser.submit()

    html_raw = response.read().decode(DECODE_TYPE)

    soup = bs4.BeautifulSoup(html_raw, "lxml")
    if soup.find("div", {"class": "alert alert-info"}):
        bot.send_message(message.chat.id, "За вашим запитом записів не знайдено")
    else:
        h4 = soup.find("h4", {"class": "hidden-xs"})
        rows = soup.find_all("div", {"class": "col-md-6"})
        msg = h4.text
        for row in rows:
            if not row.h4 is None:
                data = []
                table = row.find("table")
                trows = table.find_all('tr')
                for trow in trows:
                    cols = trow.find_all('td')
                    cols = [ele.text.strip() for ele in cols]
                    data.append([ele for ele in cols if ele])
                nl = "\n"
                msg = f"{msg}{nl}{row.h4.text}{nl}{nl.join([' '.join(d) for d in data])}"
        bot.send_message(message.chat.id, msg)

bot.polling()