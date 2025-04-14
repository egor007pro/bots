import requests
from bs4 import BeautifulSoup
import telebot
bot = telebot.TeleBot('secret')

@bot.message_handler(commands=['start'])
def hello(message):
    bot.send_message(message.chat.id, 'привет👋 я бот погодник + новостник, меня создал 𝓐𝓓𝓥𝓞𝓚𝓐𝓣 𝓓𝓨𝓪𝓥𝓞𝓛𝓐, а также соавтором является Горяной Ярослав(IT helper)')
    bot.send_message(message.chat.id, 'мои основные команды: /weather, /news'"\n" 'погода выводится в формате "Сейчас", простая цифра без ничего это uv')


@bot.message_handler(commands=['news'])
def news(message):
    URL = "https://ria.ru"
    page = requests.get(URL)
    # print(page)
    soup = BeautifulSoup(page.content, "html.parser")
    news = soup.find_all('a', class_='cell-list__item-link color-font-hover-only')
    ss=len(news)
    bot.send_message(message.chat.id, f'Всего новостей: {ss} показать?(да, нет) предупреждение! все новости выводятся отдельными сообщениями, ответ писать с маленькой буквы')

    bot.register_next_step_handler(message, yes_or_no)

def yes_or_no(message):

    user=message.text
    if user == 'да':
        URL = "https://ria.ru"
        page = requests.get(URL)
        # print(page)
        soup = BeautifulSoup(page.content, "html.parser")
        news = soup.find_all('a', class_='cell-list__item-link color-font-hover-only')
        for new in news:

            bot.send_message(message.chat.id, new.text)
        bot.send_message(message.chat.id, 'новости взяты с (https://ria.ru) ')
    elif user=='нет':
        bot.send_message(message.chat.id, 'отмена отправки выполнена ')
    else:
        bot.send_message(message.chat.id, 'пожалуйста, ответьте да или нет')



@bot.message_handler(commands=['weather'])
def weather(message):

    url='https://pogoda.mail.ru/prognoz/chekhov/'
    page = requests.get(url)
    # print(page)
    soup= BeautifulSoup(page.content, "html.parser")
    temper_now=soup.find('div', class_='information__content__additional information__content__additional_temperature')

    temper_now=temper_now.text
    a = temper_now.replace("\n", " ")
    b = a.split()
    temper_now = " ".join(b)
    # print(f'Сейчас {temper_now}')

    dir=soup.find('div', class_='information__content__additional information__content__additional_first')
    dir=dir.text
    a = dir.replace("\n", " ")
    b = a.split()
    dir_f = " ".join(b)
    # print(dir_f)

    feels=soup.find('div', class_='information__content__additional information__content__additional_second')
    feels=feels.text
    a = feels.replace("\n", " ")
    b = a.split()
    feels_f = " ".join(b)
    # print(feels_f)


    evening=soup.find('div', class_='information__content__wrapper information__content__wrapper_right')

    evening=evening.text
    a = evening.replace("\n", " ")
    b = a.split()
    evening_f = " ".join(b)
    # print(evening_f)
    bot.send_message(message.chat.id, f'Сейчас {temper_now} {dir_f}\n{feels_f}\n{evening_f}' )
    for i in range(2, 12):
        i = soup.find('a', href=f'/prognoz/chekhov/14dney/#day{i}')

        day = i.text
        a = day.replace("\n", " ")
        b = a.split()
        day_print = " ".join(b)

        bot.send_message(message.chat.id, day_print)
@bot.message_handler(commands=["botstop666"])
def stopping(message):
    bot.send_message(message.chat.id, text='50%')
    bot.send_message(message.chat.id, text='100%')
    bot.send_message(message.chat.id, text='бот успешно остановлен)')
    bot.stop_polling()

bot.polling()
