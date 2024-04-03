import time

import telebot
import sqlite3
from telebot import types
import datetime
# Создание объекта бота и передача токена для доступа к Telegram API
bot = telebot.TeleBot('6756523438:AAHdGoxPsqn5JajCLIM3dnwe1m15DmVhNSg')

# Подключение к базе данных SQLite
conn = sqlite3.connect('databasе1.db', check_same_thread=False)
c = conn.cursor()
flag = 1
flag1 = 1
@bot.message_handler(commands=['start'])
def start(message):

    conn = sqlite3.connect('database1.db', check_same_thread=False)
    c = conn.cursor()

    getlog = '''SELECT * FROM loging'''
    c.execute(getlog)
    get = c.fetchall()


    # bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
    user = message.from_user.first_name

    if user == "Ярослав":
        bot.send_message(message.chat.id, f'Здравствуй со-автор, приветственного сообщения не будет, тебе доступны команды: /les, /logs для показа логов и все 😉')
    elif user == '𝓐𝓓𝓥𝓞𝓚𝓐𝓣 𝓓𝓨𝓪𝓥𝓞𝓛𝓐':
        bot.send_message(message.chat.id, f'Здравствуй мой повелитель\nвсего логов: {len(get)}\nбыстый доступ к командам /botstop666, /clear, /show, /send, /update_les666 после него лучше /les1')

    else:
         bot.send_message(message.chat.id,f'привет {user} 👋. Меня создал 𝓐𝓓𝓥𝓞𝓚𝓐𝓣 𝓓𝓨𝓪𝓥𝓞𝓛𝓐, а также соавтором является Горяной Ярослав(IT helper)  \n я выдаю расписание из шп 🥸\nвывести расписание, можно написав "/les"\n ')
    mess_time = datetime.datetime.now()
    datat = mess_time.strftime("%d-%m-%Y %H:%M")
    logings = message.text.strip()
    name_user = message.from_user.first_name
    conn = sqlite3.connect('databasе1.db', check_same_thread=False)
    c = conn.cursor()
    data = (f'{name_user}', f'{logings}', f'{datat}')
    c.execute(f'INSERT OR REPLACE INTO loging (user_name, user_text, datatime) VALUES {data};')
    conn.commit()
    c.close()
    conn.close()


@bot.message_handler(commands=['data_close'])
def a (message):
    global flag1
    flag1 = 0
    bot.send_message(message.chat.id, 'внесения запрещены')

@bot.message_handler(commands=['data_open'])
def open(message):
    global flag1
    flag1 = 1
    bot.send_message(message.chat.id, 'внесения разрешены')


@bot.message_handler(commands=["stop"])
def stopping(message):
    global flag
    flag = 0
    arr = bot.send_message(message.chat.id, text='50%')
    # time.sleep(1)
    acc = bot.edit_message_text("100%", arr.chat.id, arr.message_id)
    time.sleep(1)
    bot.edit_message_text('бот успешно остановлен)',acc.chat.id, acc.message_id )

    bot.stop_polling()

    mess_time = datetime.datetime.now()
    datat = mess_time.strftime("%d-%m-%Y %H:%M")
    logings = message.text.strip()
    name_user = message.from_user.first_name
    conn = sqlite3.connect('databasе1.db', check_same_thread=False)
    c = conn.cursor()
    data = (f'{name_user}', f'{logings}', f'{datat}')
    c.execute(f'INSERT OR REPLACE INTO loging (user_name, user_text, datatime) VALUES {data};')
    conn.commit()
    c.close()
    conn.close()



old = None
dot = None
opd = None
@bot.message_handler(commands=['les'])
def les_command(message):

    conn = sqlite3.connect('database1.db', check_same_thread=False)
    c = conn.cursor()

    user = message.from_user.first_name
    global old, dot, opd
    try:
        bot.delete_message(chat_id=message.chat.id, message_id=old.message_id)
        bot.delete_message(chat_id=message.chat.id, message_id=old.message_id)

    except:
        dot = bot.send_message(message.chat.id, 'Нахожу расписание.')
        time.sleep(1)
        #
        dot1 = bot.edit_message_text("Нахожу расписание..", dot.chat.id, dot.message_id)
        time.sleep(0.5)
        dot2 = bot.edit_message_text("Нахожу расписание...", dot1.chat.id, dot1.message_id)
        time.sleep(1)
        bot.edit_message_text('готово', dot2.chat.id, dot2.message_id)

    keyboard = create_schedule_keyboard()
    old = bot.send_message(message.chat.id, text=f'Добрый день {user}\nВас приветствует карманный портал🧐', reply_markup=keyboard)
    bot.delete_message(chat_id=message.chat.id, message_id=opd.message_id)

    mess_time = datetime.datetime.now()
    datat = mess_time.strftime("%d-%m-%Y %H:%M")
    logings = message.text.strip()
    name_user = message.from_user.first_name
    conn = sqlite3.connect('databasе1.db', check_same_thread=False)
    c = conn.cursor()
    data = (f'{name_user}', f'{logings}', f'{datat}')
    c.execute(f'INSERT OR REPLACE INTO loging (user_name, user_text, datatime) VALUES {data};')
    conn.commit()
    c.close()
    conn.close()

    # log(message)

    # bot.register_next_step_handler(message, text)




@bot.message_handler(commands=['les1'])
def les_command(message):
    global old, dot, opd
    try:
        bot.delete_message(chat_id=message.chat.id, message_id=old.message_id)
        bot.delete_message(chat_id=message.chat.id, message_id=old.message_id)

    except:
        dot = bot.send_message(message.chat.id, 'Соединение....')
        opd =  bot.edit_message_text('Соединение установлено', dot.chat.id, dot.message_id)
        bot.edit_message_text('Готово', opd.chat.id, opd.message_id)

    keyboard = create_schedule_keyboard()
    old = bot.send_message(message.chat.id, text='Вас приветствует карманный портал🧐', reply_markup=keyboard)
    # bot.delete_message(chat_id=message.chat.id, message_id=opd.message_id)

    mess_time = datetime.datetime.now()
    datat = mess_time.strftime("%d-%m-%Y %H:%M")
    logings = message.text.strip()
    name_user = message.from_user.first_name
    conn = sqlite3.connect('databasе1.db', check_same_thread=False)
    c = conn.cursor()
    data = (f'{name_user}', f'{logings}', f'{datat}')
    c.execute(f'INSERT OR REPLACE INTO loging (user_name, user_text, datatime) VALUES {data};')
    conn.commit()
    c.close()
    conn.close()
# Функция для обработки команды /upd
@bot.message_handler(commands=['update'])
def upd_command(message):

    mess_time = datetime.datetime.now()
    datat = mess_time.strftime("%d-%m-%Y %H:%M")
    logings = message.text.strip()
    name_user = message.from_user.first_name
    conn = sqlite3.connect('databasе1.db', check_same_thread=False)
    c = conn.cursor()
    data = (f'{name_user}', f'{logings}', f'{datat}')
    c.execute(f'INSERT OR REPLACE INTO loging (user_name, user_text, datatime) VALUES {data};')
    conn.commit()
    c.close()
    conn.close()
    keyboard = create_schedule_keyboard_upd()
    bot.send_message(message.chat.id, text='Че будем обновлять?🤔', reply_markup=keyboard)

    # log(message)

# Функция для создания встроенной клавиатуры с расписанием
def create_schedule_keyboard():
    keyboard = types.InlineKeyboardMarkup()
    keyboard.row(types.InlineKeyboardButton("Пн", callback_data='пн'),
                 types.InlineKeyboardButton("Вт", callback_data='вт'))
    keyboard.row(types.InlineKeyboardButton("Ср", callback_data='ср'),
                 types.InlineKeyboardButton("Чт", callback_data='чт'))
    keyboard.row(types.InlineKeyboardButton("Пт", callback_data='пт'),
                 types.InlineKeyboardButton("изменения", callback_data='upd'))
    keyboard.row(types.InlineKeyboardButton("Куратор", callback_data='less'),
                 types.InlineKeyboardButton("звонки", callback_data='alarms'))

    return keyboard

# Функция для создания встроенной клавиатуры с возможностью обновления информации
def create_schedule_keyboard_upd():
    keyboard = telebot.types.InlineKeyboardMarkup()
    keyboard.row(types.InlineKeyboardButton("Пн", callback_data='upd_пн'),
                 types.InlineKeyboardButton("Вт", callback_data='upd_вт'))
    keyboard.row(types.InlineKeyboardButton("Ср", callback_data='upd_ср'),
                 types.InlineKeyboardButton("Чт", callback_data='upd_чт'))
    keyboard.row(types.InlineKeyboardButton("Пт", callback_data='upd_пт'),
                 types.InlineKeyboardButton("изменения", callback_data='upd_upd'))
    keyboard.row(types.InlineKeyboardButton("Куратор", callback_data='upd_less'),
                 types.InlineKeyboardButton("звонки", callback_data='upd_alarms'))

    return keyboard

# Функция обработки нажатия на кнопку в клавиатуре
@bot.callback_query_handler(func=lambda call: True)
def button_click(call):
    selected_day = call.data
    conn = sqlite3.connect('database1.db', check_same_thread=False)
    c = conn.cursor()
    if selected_day.startswith('upd_'):  # Если кнопка для обновления информации
        handle_update_message(call.message, selected_day.split('_')[1])
    else:  # Если кнопка для вывода расписания
        query = "SELECT schedule_text FROM schedule WHERE day = ?"
        c.execute(query, (selected_day,))
        selected_schedule = c.fetchone()
        if selected_schedule:
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                  text=selected_schedule[0])
        else:
            bot.send_message(chat_id=call.message.chat.id, text="Расписание не найдено")
            # bot.register_next_step_handler(call, handle_update_message)

# Функция для обработки текстовых сообщений для обновления информации
def handle_update_message(message, day):
# global day
    bot.send_message(message.chat.id, text='Напишите текст для обновления информации')

    try:
        bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
        bot.delete_message(chat_id=message.chat.id, message_id=message.message_id - 1)
    except:
        bot.send_message(message.chat.id, '.')
        # bot.register_next_step_handler(message, update_schedule)
    # @bot.message_handler(func=lambda m: m.chat.id == message.chat.id)
# Функция для обработки текстовых сообщений для обновления информации
# def handle_update_message(message, day):
#     bot.send_message(message.chat.id, text='Напишите текст для обновления информации')

    @bot.message_handler(func=lambda m: m.chat.id == message.chat.id)


    def handle_update_text(message):
        mess_time = datetime.datetime.now()
        datat = mess_time.strftime("%d-%m-%Y %H:%M")
        logings = message.text.strip()
        name_user = message.from_user.first_name
        conn = sqlite3.connect('databasе1.db', check_same_thread=False)
        c = conn.cursor()
        data = (f'{name_user}', f'{logings}', f'{datat}')
        c.execute(f'INSERT OR REPLACE INTO loging (user_name, user_text, datatime) VALUES {data};')
        conn.commit()
        c.close()
        conn.close()

        if flag1 == 1:

            update_schedule(day, message.text)
            bot.send_message(message.chat.id, text='Информация обновлена')
        else:
            bot.send_message(message.chat.id, 'изменения запрещены сначала разблокируйте внесения по команде /data_open ')

       #на случай случайных вводов
        # bot.register_next_step_handler(message, les_command)
        # bot.register_next_step_handler(message, les_command)
        # bot.register_next_step_handler(message, les_command)

    mess_time = datetime.datetime.now()
    datat = mess_time.strftime("%d-%m-%Y %H:%M")
    logings = message.text.strip()
    name_user = message.from_user.first_name
    conn = sqlite3.connect('databasе1.db', check_same_thread=False)
    c = conn.cursor()
    data = (f'{name_user}', f'{logings}', f'{datat}')
    c.execute(f'INSERT OR REPLACE INTO loging (user_name, user_text, datatime) VALUES {data};')
    conn.commit()
    c.close()
    conn.close()
    # bot.register_next_step_handler(message, d)
#
# Функция для обновления информации в базе данных
def update_schedule(day, text):
    conn = sqlite3.connect('databasе1.db', check_same_thread=False)
    c = conn.cursor()
    query = "UPDATE schedule SET schedule_text = ? WHERE day = ?"
    c.execute(query, (text, day))
    conn.commit()


    



@bot.message_handler(commands=['logs'])
def get_logs(message):
    conn = sqlite3.connect('databasе1.db', check_same_thread=False)
    c = conn.cursor()

    getlog = '''SELECT * FROM loging'''
    c.execute(getlog)
    get = c.fetchall()

    bot.send_message(message.chat.id, f'всего {len(get)} записей')
    bot.send_message(message.chat.id, 'для дальнейшего взаимодействия есть команды (/clear, /show, /send')
#log
    mess_time = datetime.datetime.now()
    datat = mess_time.strftime("%d-%m-%Y %H:%M")
    logings = message.text.strip()
    name_user = message.from_user.first_name
    conn = sqlite3.connect('databaseeeeee.db', check_same_thread=False)
    c = conn.cursor()
    data = (f'{name_user}', f'{logings}', f'{datat}')
    c.execute(f'INSERT OR REPLACE INTO loging (user_name, user_text, datatime) VALUES {data};')
    conn.commit()
    c.close()
    conn.close()
@bot.message_handler(commands=['show'])
def reg_yes (message):
        conn = sqlite3.connect('databasе1.dbdatabasе1.db')
        c = conn.cursor()
        tet = '''SELECT * FROM loging'''
        exe = c.execute(tet)

        for row in exe:
            infa = f' Время: {row[0]}\nИмя - {row[1]}:\nтекст: {row[2]} '

            bot.send_message(message.chat.id, infa)
@bot.message_handler(commands=['send'])
def send (message):
    bot.send_document(message.chat.id, document=open("databasе1.db", "rb"))

@bot.message_handler(commands=['clear'])
def delete (message):
        conn = sqlite3.connect('databasе1.db')
        c = conn.cursor()
        delete = '''DELETE FROM loging'''
        c.execute(delete)
        conn.commit()
        bot.send_message(message.chat.id, 'База данных очищена!')
# @bot.message_handler(content_types=['text'])
# def d (message):
#     # text = message.text
#     # if text == text:
#         bot.send_message(message.chat.id, 'твоя моя не понима')


create_table_query = '''CREATE TABLE IF NOT EXISTS schedule
                        (day TEXT PRIMARY KEY, schedule_text TEXT)'''
c.execute(create_table_query)

create_table_logs = '''CREATE TABLE IF NOT EXISTS loging
                       (user_name TEXT, user_text TEXT, datatime TEXT)'''
c.execute(create_table_logs)

conn.commit()

while flag:
    try:
        bot.polling(none_stop=True, interval=0)
        # если возникла ошибка — сообщаем про исключение и продолжаем работу
    except Exception as e:
        print('❌❌❌❌❌ Сработало исключение! ❌❌❌❌❌')


@bot.message_handler(commands=["stop"])
def stopping(message):
    global flag
    flag = 0
    bot.send_message(message.chat.id, text='50%')
    bot.send_message(message.chat.id, text='100%')
    bot.send_message(message.chat.id, text='бот успешно остановлен)')

    bot.stop_polling()




conn.close()
