from telethon import TelegramClient, events
from googlesearch import search
import requests, re, wikipedia, json, pytz, cryptocompare, random, qrcode,socket, platform, speedtest, psutil, subprocess, netifaces, nmap, distro, os, sys, glob, warnings, feedparser, dns.resolver
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import pytz
import cryptocompare
import translators as ts
from io import BytesIO
from deep_translator import GoogleTranslator
from uuid import uuid4
from uuid import uuid4
from datetime import datetime, timedelta
from bs4 import BeautifulSoup, GuessedAtParserWarning
from telethon import TelegramClient, events
from telethon.tl.types import InputWebDocument


API_ID = 'secret'
API_HASH = 'secret'
BOT_TOKEN = 'secret'
WEATHER_API_KEY = 'secret'

bot = TelegramClient('bot_session', API_ID, API_HASH).start(bot_token=BOT_TOKEN)
wikipedia.set_lang("ru")
def clean_text(text):
    text = re.sub(r'\s+', ' ', text)
    text = re.sub(r'Перейти к.*?(?=\w)', '', text)
    text = re.sub(r'(Пройти тест|Материал из.*?энциклопедии)', '', text)
    return text.strip()

@bot.on(events.InlineQuery)
async def inline_handler(event):
    builder = event.builder
    query = event.text.lower()
    results = []

    if query.startswith('ask '):
        search_query = query[4:]
        try:
            wiki_summary = wikipedia.summary(search_query, sentences=3)
            search_results = []
            for url in search(search_query, num_results=3):
                try:
                    response = requests.get(url, timeout=5)
                    soup = BeautifulSoup(response.text, 'html.parser')
                    text = clean_text(soup.get_text())
                    search_results.append({
                        'text': text[:300],
                        'url': url
                    })
                except:
                    continue

            answer = f"🔎 По запросу «{search_query}»:\n\n📚 Из Википедии:\n{wiki_summary}\n\n"
            for result in search_results:
                answer += f"📍 {result['text']}...\n"
                answer += f"➜ {result['url']}\n\n"

            results.append(builder.article(
                title=f'Поиск: {search_query}',
                text=answer,
                id=str(uuid4())
            ))
        except:
            results.append(builder.article(
                title='Поиск не дал результатов',
                text="🔍 Попробуйте другой запрос",
                id=str(uuid4())
            ))
    elif query.startswith('weather '):
        city = query[8:]
        try:
            url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={WEATHER_API_KEY}&units=metric&lang=ru'
            response = requests.get(url)
            data = response.json()
            weather_text = (
                f"🌤 Погода в {city}:\n"
                f"🌡 Температура: {data['main']['temp']}°C\n"
                f"☁️ {data['weather'][0]['description'].capitalize()}\n"
                f"💧 Влажность: {data['main']['humidity']}%\n"
                f"💨 Ветер: {data['wind']['speed']} м/с"
            )
            results.append(builder.article(
                title=f'Погода в {city}',
                text=weather_text,
                id=str(uuid4())
            ))
        except:
            results.append(builder.article(
                title='Город не найден',
                text="Город не найден",
                id=str(uuid4())
            ))
    
    elif query.startswith('netinfo'):
        try:
            import netifaces
            interfaces = netifaces.interfaces()
            net_info = "🌐 Сетевые интерфейсы:\n\n"
            
            for iface in interfaces:
                addrs = netifaces.ifaddresses(iface)
                if netifaces.AF_INET in addrs:
                    ip = addrs[netifaces.AF_INET][0]['addr']
                    mask = addrs[netifaces.AF_INET][0]['netmask']
                    net_info += f"📡 {iface}:\n"
                    net_info += f"  IP: {ip}\n"
                    net_info += f"  Маска: {mask}\n"
                    if netifaces.AF_LINK in addrs:
                        mac = addrs[netifaces.AF_LINK][0]['addr']
                        net_info += f"  MAC: {mac}\n"
                    net_info += "\n"
            
            results.append(builder.article(
                title='Сетевая информация',
                text=net_info,
                id=str(uuid4())
            ))
        except Exception as e:
            results.append(builder.article(
                title='Ошибка',
                text=f"⚠️ Ошибка получения сетевой информации: {str(e)}",
                id=str(uuid4())
            ))

    
    elif query.startswith('scan '):
        target = query[5:]
        try:
            nm = nmap.PortScanner()
            nm.scan(target, arguments='-F -sV')
            
            scan_result = f"🔍 Результаты сканирования {target}:\n\n"
            
            for host in nm.all_hosts():
                scan_result += f"📡 Host: {host}\n"
                for proto in nm[host].all_protocols():
                    scan_result += f"\nПротокол: {proto}\n"
                    ports = nm[host][proto].keys()
                    for port in ports:
                        state = nm[host][proto][port]['state']
                        service = nm[host][proto][port]['name']
                        version = nm[host][proto][port]['version']
                        scan_result += f"  Порт {port}: {state} ({service} {version})\n"
            
            results.append(builder.article(
                title='Результаты сканирования',
                text=scan_result,
                id=str(uuid4())
            ))
        except Exception as e:
            results.append(builder.article(
                title='Ошибка',
                text=f"⚠️ Ошибка сканирования: {str(e)}",
                id=str(uuid4())
            ))
    elif query.startswith('ip '):
        ip = query[3:]
        try:
            response = requests.get(f'http://ip-api.com/json/{ip}')
            data = response.json()
            if data['status'] == 'success':
                info = (
                    f"📍 IP информация: {ip}\n\n"
                    f"🌍 Страна: {data['country']}\n"
                    f"🏢 Регион: {data['regionName']}\n"
                    f"🌆 Город: {data['city']}\n"
                    f"🏢 Провайдер: {data['isp']}\n"
                    f"🌐 Организация: {data['org']}\n"
                    f"📌 Координаты: {data['lat']}, {data['lon']}"
                )
            else:
                info = "❌ IP не найден"
            results.append(await builder.article(
                title=f'IP инфо: {ip}',
                text=info,
                id=str(uuid4())
            ))
        except:
            results.append(await builder.article(
                title='Ошибка',
                text="❌ Ошибка получения информации",
                id=str(uuid4())
            ))

    elif query.startswith('whois '):
        domain = query[6:]
        try:
            result = subprocess.run(['whois', domain], capture_output=True, text=True)
            whois_info = result.stdout[:4000] + "..." if len(result.stdout) > 4000 else result.stdout
            results.append(await builder.article(
                title=f'WHOIS: {domain}',
                text=f"🔍 WHOIS информация для {domain}:\n\n{whois_info}",
                id=str(uuid4())
            ))
        except:
            results.append(await builder.article(
                title='Ошибка',
                text="❌ Ошибка получения WHOIS",
                id=str(uuid4())
            ))

    elif query.startswith('trace '):
        host = query[6:]
        try:
            result = subprocess.run(['traceroute', host], capture_output=True, text=True)
            results.append(await builder.article(
                title=f'Трассировка: {host}',
                text=f"🛤 Трассировка до {host}:\n{result.stdout}",
                id=str(uuid4())
            ))
        except:
            results.append(await builder.article(
                title='Ошибка',
                text="❌ Ошибка выполнения трассировки",
                id=str(uuid4())
            ))

    elif query.startswith('ssl '):
        domain = query[4:]
        try:
            result = subprocess.run(['openssl', 's_client', '-connect', f'{domain}:443', '-servername', domain], 
                                  input='Q\n', capture_output=True, text=True)
            cert_info = result.stdout
            
            valid_from = re.search(r'notBefore=(.+?)\n', cert_info)
            valid_to = re.search(r'notAfter=(.+?)\n', cert_info)
            issuer = re.search(r'issuer=(.+?)\n', cert_info)
            
            ssl_info = (
                f"🔒 SSL информация для {domain}:\n\n"
                f"📅 Действителен с: {valid_from.group(1) if valid_from else 'Н/Д'}\n"
                f"📅 Действителен до: {valid_to.group(1) if valid_to else 'Н/Д'}\n"
                f"🏢 Выдан: {issuer.group(1) if issuer else 'Н/Д'}"
            )
            results.append(await builder.article(
                title=f'SSL: {domain}',
                text=ssl_info,
                id=str(uuid4())
            ))
        except:
            results.append(await builder.article(
                title='Ошибка',
                text="❌ Ошибка проверки SSL",
                id=str(uuid4())
            ))
    elif query.startswith('pass '):
        length = int(query[5:]) if query[5:].isdigit() and int(query[5:]) <= 50 else 12
        chars = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*'
        password = ''.join(random.choice(chars) for _ in range(length))
        results.append(await builder.article(
            title='Генератор паролей',
            text=f"🔐 Сгенерированный пароль:\n`{password}`\n\nДлина: {length} символов",
            id=str(uuid4())
        ))

    elif query.startswith('morse '):
        text = query[6:]
        MORSE_CODE = {
            'А': '.-', 'Б': '-...', 'В': '.--', 'Г': '--.', 'Д': '-..', 'Е': '.', 'Ж': '...-',
            'З': '--..', 'И': '..', 'Й': '.---', 'К': '-.-', 'Л': '.-..', 'М': '--', 'Н': '-.',
            'О': '---', 'П': '.--.', 'Р': '.-.', 'С': '...', 'Т': '-', 'У': '..-', 'Ф': '..-.',
            'Х': '....', 'Ц': '-.-.', 'Ч': '---.', 'Ш': '----', 'Щ': '--.-', 'Ъ': '.--.-.',
            'Ы': '-.--', 'Ь': '-..-', 'Э': '..-..', 'Ю': '..--', 'Я': '.-.-',
            'A': '.-', 'B': '-...', 'C': '-.-.', 'D': '-..', 'E': '.', 'F': '..-.',
            'G': '--.', 'H': '....', 'I': '..', 'J': '.---', 'K': '-.-', 'L': '.-..',
            'M': '--', 'N': '-.', 'O': '---', 'P': '.--.', 'Q': '--.-', 'R': '.-.',
            'S': '...', 'T': '-', 'U': '..-', 'V': '...-', 'W': '.--', 'X': '-..-',
            'Y': '-.--', 'Z': '--..', '0': '-----', '1': '.----', '2': '..---',
            '3': '...--', '4': '....-', '5': '.....', '6': '-....', '7': '--...',
            '8': '---..', '9': '----.', ' ': ' '
        }
        morse = ' '.join(MORSE_CODE.get(c.upper(), c) for c in text)
        results.append(await builder.article(
            title='Морзе код',
            text=f"📡 Текст в морзе:\n`{morse}`",
            id=str(uuid4())
        ))

    elif query.startswith('bin '):
        text = query[4:]
        binary = ' '.join(format(ord(c), '08b') for c in text)
        results.append(await builder.article(
            title='Бинарный код',
            text=f"💻 Текст в бинарном виде:\n`{binary}`",
            id=str(uuid4())
        ))

    elif query.startswith('hash '):
        text = query[5:]
        import hashlib
        hashes = {
            'MD5': hashlib.md5(text.encode()).hexdigest(),
            'SHA1': hashlib.sha1(text.encode()).hexdigest(),
            'SHA256': hashlib.sha256(text.encode()).hexdigest()
        }
        result = "🔒 Хеши:\n\n"
        for name, hash_value in hashes.items():
            result += f"{name}: `{hash_value}`\n"
        results.append(await builder.article(
            title='Хеширование',
            text=result,
            id=str(uuid4())
        ))
    elif query.startswith('json '):
        text = query[5:]
        try:
            parsed = json.loads(text)
            formatted = json.dumps(parsed, indent=2, ensure_ascii=False)
            results.append(await builder.article(
                title='JSON форматирование',
                text=f"📝 Форматированный JSON:\n\n`{formatted}`",
                id=str(uuid4())
            ))
        except:
            results.append(await builder.article(
                title='JSON валидация',
                text="❌ Невалидный JSON",
                id=str(uuid4())
            ))

    elif query.startswith('unit '):
        value = query[5:]
        try:
            size_bytes = float(value)
            sizes = ['B', 'KB', 'MB', 'GB', 'TB', 'PB']
            result = "🔄 Конвертация размеров:\n\n"
            for i, unit in enumerate(sizes):
                converted = size_bytes / (1024 ** i)
                result += f"{converted:.2f} {unit}\n"
            results.append(await builder.article(
                title='Конвертер единиц',
                text=result,
                id=str(uuid4())
            ))
        except:
            results.append(await builder.article(
                title='Ошибка',
                text="❌ Неверный формат числа",
                id=str(uuid4())
            ))

    elif query.startswith('code '):
        code = query[5:]
        try:
            # выполнение кода в изоляции
            restricted_globals = {"__builtins__": {"print": print, "len": len, "str": str, "int": int, "float": float}}
            output = eval(code, restricted_globals, {})
            results.append(await builder.article(
                title='Python Eval',
                text=f"💻 Результат выполнения:\n\n`{output}`",
                id=str(uuid4())
            ))
        except Exception as e:
            results.append(await builder.article(
                title='Ошибка выполнения',
                text=f"❌ Ошибка: {str(e)}",
                id=str(uuid4())
            ))

    elif query.startswith('color '):
        color = query[6:]
        try:
            # поддержка HEX и RGB
            if color.startswith('#'):
                hex_color = color
                rgb = tuple(int(color.lstrip('#')[i:i+2], 16) for i in (0, 2, 4))
            else:
                rgb = tuple(map(int, color.split(',')))
                hex_color = '#{:02x}{:02x}{:02x}'.format(*rgb)
            
            results.append(await builder.article(
                title='Конвертер цветов',
                text=f"🎨 Информация о цвете:\n\nHEX: `{hex_color}`\nRGB: `{rgb}`",
                id=str(uuid4())
            ))
        except:
            results.append(await builder.article(
                title='Ошибка',
                text="❌ Неверный формат цвета",
                id=str(uuid4())
            ))

    elif query.startswith('cron '):
        expression = query[5:]
        try:
            from cron_descriptor import get_description
            description = get_description(expression)
            results.append(await builder.article(
                title='CRON парсер',
                text=f"⏰ Расшифровка CRON выражения:\n\n`{expression}`\n\n{description}",
                id=str(uuid4())
            ))
        except:
            results.append(await builder.article(
                title='Ошибка',
                text="❌ Неверное CRON выражение",
                id=str(uuid4())
            ))
    elif query.startswith('phone '):
        phone = query[6:]
        formatted = f"📱 Форматы номера {phone}:\n\n"
        # чистим номер от лишнего
        clean = ''.join(filter(str.isdigit, phone))
        if len(clean) >= 10:
            formatted += f"Международный: +{clean}\n"
            formatted += f"Локальный: {clean[-10:]}\n"
            formatted += f"С пробелами: {' '.join(clean)}\n"
            formatted += f"Через тире: {'-'.join(clean)}"
        results.append(await builder.article(
            title='Форматирование номера',
            text=formatted,
            id=str(uuid4())
        ))

    elif query.startswith('age '):
        date = query[4:]
        try:
            from datetime import datetime
            birth_date = datetime.strptime(date, '%d.%m.%Y')
            today = datetime.now()
            age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
            days = (today - birth_date).days
            
            results.append(await builder.article(
                title='Калькулятор возраста',
                text=f"🎂 Возраст:\n\nПолных лет: {age}\nДней всего: {days}\nМесяцев всего: {days//30}\nНедель всего: {days//7}",
                id=str(uuid4())
            ))
        except:
            results.append(await builder.article(
                title='Ошибка',
                text="❌ Используйте формат ДД.ММ.ГГГГ",
                id=str(uuid4())
            ))

    elif query.startswith('timer '):
        minutes = query[6:]
        try:
            mins = int(minutes)
            from datetime import datetime, timedelta
            end_time = datetime.now() + timedelta(minutes=mins)
            results.append(await builder.article(
                title='Таймер',
                text=f"⏰ Таймер на {mins} минут\n\nЗакончится в: {end_time.strftime('%H:%M')}",
                id=str(uuid4())
            ))
        except:
            results.append(await builder.article(
                title='Ошибка',
                text="❌ Укажите количество минут числом",
                id=str(uuid4())
            ))

    elif query.startswith('note '):
        from datetime import datetime
        text = query[5:]
        now = datetime.now().strftime('%d.%m.%Y %H:%M')
        results.append(await builder.article(
            title='Заметка',
            text=f"📝 Заметка от {now}:\n\n{text}",
            id=str(uuid4())
        ))

    elif query.startswith('split '):
        parts = query[6:].split('|')
        if len(parts) == 2:
            try:
                amount = float(parts[0])
                people = int(parts[1])
                per_person = amount / people
                results.append(await builder.article(
                    title='Делим счёт',
                    text=f"💰 Делим {amount} на {people} человек:\n\nС каждого: {per_person:.2f}",
                    id=str(uuid4())
                ))
            except:
                results.append(await builder.article(
                    title='Ошибка',
                    text="❌ Формат: сумма|количество людей",
                    id=str(uuid4())
                ))

    elif query.startswith('rate '):
        currency = query[5:].upper()
        try:
            response = requests.get(f'https://api.exchangerate-api.com/v4/latest/USD')
            rates = response.json()['rates']
            if currency in rates:
                rate = rates[currency]
                results.append(await builder.article(
                    title='Курс валют',
                    text=f"💵 Курс {currency}:\n\n1 USD = {rate} {currency}\n1 {currency} = {1/rate:.4f} USD",
                    id=str(uuid4())
                ))
        except:
            results.append(await builder.article(
                title='Ошибка',
                text="❌ Не удалось получить курс валюты",
                id=str(uuid4())
            ))
    elif query.startswith('status'):
        from datetime import datetime
        import psutil
        uptime = datetime.now() - datetime.fromtimestamp(psutil.boot_time())
        memory = psutil.virtual_memory()
        status_info = (
            f"🤖 Статус бота:\n\n"
            f"✨ Бот активен\n"
            f"⏱ Аптайм: {str(uptime).split('.')[0]}\n"
            f"💾 RAM: {memory.percent}%\n"
            f"🔄 CPU: {psutil.cpu_percent()}%"
        )
        results.append(await builder.article(
            title='Статус бота',
            text=status_info,
            id=str(uuid4())
        ))



    elif query.startswith('about'):
        about_text = (
            "ℹ️ О боте:\n\n"
            "🤖 Многофункциональный инлайн-бот\n"
            "✨ Версия: 1.0\n"
            "👨‍💻 Разработчик: @dontkillmyvibe31006\n\n"
            "📚 Возможности:\n"
            "• Поиск информации\n"
            "• Конвертация данных\n"
            "• Системные утилиты\n"
            "• Сетевые инструменты\n\n"
            "🔗 Исходный код: пока не выкладывал p.s мне лень)\n"
        )
        results.append(await builder.article(
            title='О боте',
            text=about_text,
            id=str(uuid4())
        ))

    elif query.startswith('usage'):
        usage_text = (
            "📝 Как использовать бота:\n\n"
            "1️⃣ Введите @it_halper_bot в любом чате\n"
            "2️⃣ Добавьте команду и параметры\n"
            "3️⃣ Выберите результат из списка\n\n"
            "Примеры:\n"
            "• @it_halper_bot weather москва\n"
            "• @it_halper_bot translate hello\n"
            "• @it_halper_bot calc 2+2\n\n"
            "❔ Для помощи: @it_halper_bot help"
        )
        results.append(await builder.article(
            title='Инструкция',
            text=usage_text,
            id=str(uuid4())
        ))

    elif query.startswith('feedback'):
        feedback_text = (
            "📬 Обратная связь:\n\n"
            "Для связи с разработчиком:\n"
            "• Telegram: @dontkillmyvibe31006\n"
            "• Email: egorg666good@gmail.com\n\n"
            "🐛 Нашёл баг? Сообщи!\n"
            "💡 Есть идеи? Напиши!\n"
            "👍 Понравился бот? Поделись(быстроооо)! хы"
        )
        results.append(await builder.article(
            title='Обратная связь',
            text=feedback_text,
            id=str(uuid4())
        ))
    elif query.startswith('news'):
        try:
            import feedparser
            # use RSS ленту РИА Новостей
            feed = feedparser.parse('https://ria.ru/export/rss2/archive/index.xml')
            news_text = "📰 Последние новости:\n\n"
            # берём 5 последних новостей
            for i, entry in enumerate(feed.entries[:5], 1):
                news_text += f"{i}. {entry.title}\n\n"
            results.append(await builder.article(
                title='Новости',
                text=news_text,
                id=str(uuid4())
            ))
        except:
            results.append(await builder.article(
                title='Новости',
                text="📰 Последние новости временно недоступны",
                id=str(uuid4())
            ))


    elif query.startswith('movie '):
        movie = query[6:]
        try:
            response = requests.get(f'http://www.omdbapi.com/?t={movie}&apikey=b6faaa5')
            data = response.json()
            if data['Response'] == 'True':
                movie_info = (
                    f"🎬 {data['Title']} ({data['Year']})\n\n"
                    f"⭐️ Рейтинг: {data['imdbRating']}\n"
                    f"📽 Жанр: {data['Genre']}\n"
                    f"⏱ Длительность: {data['Runtime']}\n"
                    f"📝 Сюжет: {data['Plot']}"
                )
            else:
                movie_info = "❌ Фильм не найден"
            results.append(await builder.article(
                title='Информация о фильме',
                text=movie_info,
                id=str(uuid4())
            ))
        except:
            results.append(await builder.article(
                title='Фильмы',
                text="🔄 Попробуйте позже",
                id=str(uuid4())
            ))

    elif query.startswith('recipe '):
        dish = query[7:]
        try:
            response = requests.get(f'https://api.spoonacular.com/recipes/search?query={dish}&apiKey=42fc6e30ef9047178757cc82225c61ac ')
            recipes = response.json()['results'][:3]
            recipe_text = f"🍳 Рецепты по запросу '{dish}':\n\n"
            for recipe in recipes:
                recipe_text += f"📝 {recipe['title']}\n⏱ Время готовки: {recipe['readyInMinutes']} мин\n\n"
            results.append(await builder.article(
                title='Рецепты',
                text=recipe_text,
                id=str(uuid4())
            ))
        except:
            results.append(await builder.article(
                title='Рецепты',
                text="🔄 Попробуйте позже",
                id=str(uuid4())
            ))
    elif query.startswith('sysinfo'):
        import platform
        import psutil
        
        
        system = platform.system()
        release = platform.release()
        machine = platform.machine()
        processor = platform.processor()
        
       
        memory = psutil.virtual_memory()
        memory_total = round(memory.total / (1024 * 1024 * 1024), 2)  
        memory_used = round(memory.used / (1024 * 1024 * 1024), 2)    
        
        
        disk = psutil.disk_usage('/')
        disk_total = round(disk.total / (1024 * 1024 * 1024), 2)      
        disk_used = round(disk.used / (1024 * 1024 * 1024), 2)        
        
        sysinfo_text = (
            f"💻 Системная информация:\n\n"
            f"🖥 Система: {system} {release}\n"
            f"⚙️ Архитектура: {machine}\n"
            f"🔄 Процессор: {processor}\n\n"
            f"📊 Память:\n"
            f"Всего: {memory_total} GB\n"
            f"Использовано: {memory_used} GB\n"
            f"Загрузка: {memory.percent}%\n\n"
            f"💾 Диск:\n"
            f"Всего: {disk_total} GB\n"
            f"Использовано: {disk_used} GB\n"
            f"Загрузка: {disk.percent}%"
        )
        
        results.append(await builder.article(
            title='Системная информация',
            text=sysinfo_text,
            id=str(uuid4())
        ))
    elif query.startswith('server'):
        from datetime import datetime
        import psutil
        hostname = socket.gethostname()
        local_ip = socket.gethostbyname(hostname)
        uptime = str(datetime.now() - datetime.fromtimestamp(psutil.boot_time())).split('.')[0]
        
        server_info = (
            f"🖥 Информация о сервере:\n\n"
            f"📌 Hostname: {hostname}\n"
            f"🌐 Local IP: {local_ip}\n"
            f"⚡️ Uptime: {uptime}\n"
            f"👥 Active Users: {len(psutil.users())}"
        )
        results.append(await builder.article(
            title='Сервер',
            text=server_info,
            id=str(uuid4())
        ))

    elif query.startswith('monitor'):
        import psutil
        processes = []
        for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent']):
            pinfo = proc.info
            if pinfo['cpu_percent'] > 0:
                processes.append(pinfo)
        
        processes = sorted(processes, key=lambda x: x['cpu_percent'], reverse=True)[:5]
        
        monitor_text = "📊 Топ процессов:\n\n"
        for proc in processes:
            monitor_text += (
                f"📌 {proc['name']}\n"
                f"PID: {proc['pid']}\n"
                f"CPU: {proc['cpu_percent']}%\n"
                f"RAM: {round(proc['memory_percent'], 1)}%\n\n"
            )
        
        results.append(await builder.article(
            title='Мониторинг',
            text=monitor_text,
            id=str(uuid4())
        ))

    elif query.startswith('network'):
        import psutil
        net_io = psutil.net_io_counters()
        bytes_sent = round(net_io.bytes_sent / (1024 * 1024), 2)
        bytes_recv = round(net_io.bytes_recv / (1024 * 1024), 2)
        
        network_text = (
            f"🌐 Сетевая статистика:\n\n"
            f"📤 Отправлено: {bytes_sent} MB\n"
            f"📥 Получено: {bytes_recv} MB\n"
            f"📊 Пакетов отправлено: {net_io.packets_sent}\n"
            f"📊 Пакетов получено: {net_io.packets_recv}\n"
            f"❌ Ошибок: {net_io.errin + net_io.errout}\n"
            f"⚠️ Dropped: {net_io.dropin + net_io.dropout}"
        )
        
        results.append(await builder.article(
            title='Сеть',
            text=network_text,
            id=str(uuid4())
        ))

    elif query.startswith('logs'):
        from datetime import datetime
        import subprocess
        
    
        result = subprocess.run(['tail', '-n', '10', '/var/log/syslog'], capture_output=True, text=True)
        log_content = result.stdout
        
        logs_text = (
            "📋 Последние системные события:\n\n"
            f"{log_content}\n\n"
            "Используйте:\n"
            "logs error - поиск ошибок\n"
            "logs warn - поиск предупреждений"
        )
        
        results.append(await builder.article(
            title='Системные логи',
            text=logs_text,
            id=str(uuid4())
        ))

    elif query.startswith('stats'):
 
        stats_file = 'bot_stats.json'
        if os.path.exists(stats_file):
            with open(stats_file, 'r') as f:
                stats = json.load(f)
                stats['users'] = set(stats['users'])  
        else:
            stats = {
                'commands': {
                    'help': 0,
                    'weather': 0,
                    'translate': 0,
                    'calc': 0,
                    'status': 0,
                    'server': 0,
                    'monitor': 0,
                    'network': 0,
                    'stats': 0
                },
                'users': set(),
                'total_queries': 0
            }
            
       
        current_command = query.split()[0]
        if current_command in stats['commands']:
            stats['commands'][current_command] += 1
        stats['users'].add(str(event.sender_id))
        stats['total_queries'] += 1
        
    
        with open(stats_file, 'w') as f:
            stats_to_save = stats.copy()
            stats_to_save['users'] = list(stats['users'])
            json.dump(stats_to_save, f)
            
       
        top_commands = sorted(stats['commands'].items(), key=lambda x: x[1], reverse=True)[:5]
        
        stats_info = (
            "📊 Статистика бота:\n\n"
            f"📈 Всего команд: {stats['total_queries']}\n"
            f"👥 Пользователей: {len(stats['users'])}\n\n"
            "Топ команд:\n"
        )
        
        for cmd, count in top_commands:
            if count > 0:  
                stats_info += f"• {cmd}: {count} раз\n"
        
        results.append(await builder.article(
            title='Статистика',
            text=stats_info,
            id=str(uuid4())
        ))


    elif query.startswith('quote'):
        try:
          
            quotes = [
                {"text": "Жизнь — это то, что с тобой происходит, пока ты строишь планы.", "author": "Джон Леннон"},
                {"text": "Будущее зависит от того, что ты делаешь сегодня.", "author": "Махатма Ганди"},
                {"text": "Чтобы дойти до цели, надо идти.", "author": "Оноре де Бальзак"},
                {"text": "Самый лучший способ предсказать будущее — создать его.", "author": "Питер Друкер"},
                {"text": "Если ты не знаешь, куда идешь, то как поймешь, что ты туда пришел?", "author": "Джордж Харрисон"},
                {"text": "Единственный способ делать великие дела — любить то, что ты делаешь.", "author": "Стив Джобс"},
                {"text": "Успех — это способность идти от неудачи к неудаче, не теряя энтузиазма.", "author": "Уинстон Черчилль"},
                {"text": "Жизнь измеряется не количеством наших вдохов, а количеством моментов, когда захватывает дух.", "author": "Майя Энджелоу"},
                {"text": "Если вы можете мечтать об этом, вы можете это сделать.", "author": "Уолт Дисней"},
                {"text": "Лучший способ начать делать — перестать говорить и начать делать.", "author": "Уолт Дисней"}
            ]
            quote = random.choice(quotes)
            quote_text = f"💭 {quote['text']}\n\n— {quote['author']}"
            results.append(await builder.article(
                title='Цитата дня',
                text=quote_text,
                id=str(uuid4())
            ))
        except:
            results.append(await builder.article(
                title='Цитата',
                text="💭 Попробуйте ещё раз",
                id=str(uuid4())
            ))


    elif query.startswith('help'):
        help_text = """
🤖 Inline команды бота:

Поиск и информация:
📍 ask <запрос> - Поиск в интернете
📍 weather <город> - Погода(из openweathermap.org)
📍 (time <город> - Время и дата)
📍 crypto <монета> - Курсы криптовалют

Инструменты:
📍 translate <текст> - Переводчик
📍 (qr <текст> - QR код)
📍 (calc <выражение> - Калькулятор)
📍 short <ссылка> - Сократить ссылку

Системные инструменты:
📍 netinfo - Информация о сетевых интерфейсах
📍 sysinfo - Детальная информация о системе
📍 scan <хост> - Сканирование портов и сервисов
Сетевые инструменты:
📍 ip <ip> - Информация об IP
📍 whois <домен> - WHOIS информация
📍 trace <хост> - Трассировка маршрута
📍 ssl <домен> - Проверка SSL сертификата
Кодирование и безопасность:
📍 pass <длина> - Генератор паролей
📍 morse <текст> - Перевод в код Морзе
📍 bin <текст> - Перевод в бинарный код
📍 hash <текст> - Хеширование текста
Инструменты разработчика:
📍 json <текст> - Форматирование JSON
📍 unit <число> - Конвертер единиц измерения
📍 code <код> - Выполнение Python кода
📍 color <hex/rgb> - Конвертер цветов
📍 cron <выражение> - Парсер CRON выражений
Полезные инструменты:
📍 phone <номер> - Форматирование телефона
📍 age <дата> - Калькулятор возраста
📍 timer <минуты> - Установка таймера
📍 note <текст> - Создание заметки
📍 split <сумма|люди> - Разделить счёт
📍 rate <валюта> - Курс валют(результат может быть не точным)
Управление ботом:
📍 status - Статус бота
📍 about - О боте
📍 usage - Как использовать
📍 feedback - Обратная связь
Развлечения и информация:
📍 news - Последние новости
📍 movie <название> - Информация о фильме(в разработке)
📍 recipe <блюдо> - Поиск рецептов(в разработке)
📍 quote - Случайная цитата

Мониторинг системы:
📍 server - Информация о сервере
📍 monitor - Мониторинг процессов
📍 network - Сетевая статистика
📍 logs - Просмотр логов
📍 stats - Просмотр статистики используемых команд

Используйте: @it_halper_bot команда
"""
        results.append(builder.article(
            title='Помощь',
            text=help_text,
            id=str(uuid4())
        ))

    await event.answer(results)

if __name__ == '__main__':
    print('о чудо, запустился с толкоча')
    bot.run_until_disconnected()
