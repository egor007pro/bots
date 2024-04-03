import telebot
import requests
from bs4 import BeautifulSoup
bot=telebot.TeleBot('6756523438:AAHdGoxPsqn5JajCLIM3dnwe1m15DmVhNSg')
flag = 1
@bot.message_handler(commands=(['start']))
def start(message):
    user = message.from_user.first_name


    bot.send_message(message.chat.id, f"Привет{user} для вывода новостей напиши /news, а для вывода погоды /weather")
@bot.message_handler(commands=['news'])
def news(message):
    URL = "https://ria.ru/"
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, "html.parser")
    news = soup.find_all('div', class_='cell-list__item m-no-image')

    for j in news:
        ss = j.text
        # print('\n')
        bot.send_message(message.chat.id, ss)
    bot.send_message(message.chat.id, "новости взяты с источника (https://ria.ru/)")

@bot.message_handler(commands=['weather'])
def weath(message):

    url = 'https://pogoda.mail.ru/prognoz/chekhov/'
    response = requests.get(url)
    bs = BeautifulSoup(response.content,"html.parser")
    # print(bs.prettify())
    weath = bs.find('div', class_='days__wrapper')
    # cloud =bs.find('span', class_='text text_block text_light_normal text_fixed')
    # feel = bs.find('span', class_='text text_block text_light_normal text_fixed color_gray')
    # vlaga = bs.find('span', class_='link link_block link_icon')
    # clo = cloud.text
    weather = weath.text
    wea = weather.replace('\n', ' ')
    wea2 = wea.replace('\t', '')
    wea3 = wea2.replace(' ', '\n')
    wea4 = wea3.replace('', '')
    bot.send_message(message.chat.id, wea2)
    # print(wea2)
    yesterday = bs.find('div', class_='information__content__additional information__content__additional_temperature')
    yes = yesterday.text
    yes_cor = yes.replace('\n', '.')
    yes_cor2 = yes_cor.replace('\t', '')
    cloud = bs.find('div', class_='information__content__additional information__content__additional_first')
    # ss = cloud._find_one('div',class_='information__content__additional__item' )
    test = cloud.text
    test1 = test.replace('\n', '')
    test2 = test1.replace('\t', '')
    test3=test2.replace('', '')
    # print(f'Сейчас{yes_cor2}')
    # print(test3)
    # bot.send_message(message.chat.id,ss)

    bot.send_message(message.chat.id, f'сейчас{yes_cor2}')
    # night_day=bs.find('div', class_='information__content__period__temperature')
    # print(f'Ночью {night_day.text}')
    day = bs.find('div', class_='information__content__wrapper information__content__wrapper_right')
    day1 = day.text
    day_cor1 = day1.replace('\n', ' ')
    day_cor2 = day_cor1.replace('\t', '')
    day_cor_fin = day_cor2.replace('', '')
    # print(day_cor2)
    bot.send_message(message.chat.id, day_cor_fin)
@bot.message_handler(commands=["botstop666"])
def stopping(message):
    global flag
    flag = 0
    bot.send_message(message.chat.id, text='50%')
    bot.send_message(message.chat.id, text='100%')
    bot.send_message(message.chat.id, text='бот успешно остановлен)')

    bot.stop_polling()

while flag:
    try:
        bot.polling(none_stop=True, interval=0)

    except Exception as e:
        print('❌❌❌❌❌ Сработало исключение! ❌❌❌❌❌')
