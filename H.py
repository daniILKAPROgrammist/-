from telebot import TeleBot, types
import requests
from datetime import datetime, date, time, timedelta
import json
from pydantic import BaseModel
from time import sleep
from threading import Thread
import random
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
from email.mime.text import MIMEText
import smtplib

t = TeleBot("6370938616:AAGKNWr66eB3e36e7a2CI90LAQmXhpfGB-o")

@t.message_handler(commands=["start"])
def h(message):
    r = json.load(open("Гавно.json","r"))
    if str(message.from_user.id) not in r:
        r[str(message.from_user.id)] = {"v": 0, "gyg": "", "f":False}
    t.send_message(message.chat.id, "Введи имя пользователя и пароль через пробел")
    r[str(message.from_user.id)]["v"] = 1
    json.dump(r, open("Гавно.json", "w"))
    t.register_next_step_handler(message, b)

def r0(message):
    r = json.load(open("Гавно.json","r"))
    return r[str(message.from_user.id)]["v"] == 1

@t.message_handler(func=r0, type=["text"])
def b(message):
    g = requests.get("http://127.0.0.1:8000/us").json()
    r = json.load(open("Гавно.json","r"))
    l = message.text.split()
    print(g)
    if len(l) != 2:
        t.send_message(message.chat.id, "Неверный формат сообщения. Введи имя пользователя и пароль через пробел. Для повторной повытки - /start")
    elif l[0] in g and g[l[0]]["gam"]:
        t.send_message(message.chat.id, "Похоже кто - то уже в аккаунте")
    elif l[0] in g and l[1] == g[l[0]]["passs"]:
        if r[str(message.from_user.id)]["gyg"]:
            g[r[str(message.from_user.id)]["gyg"]]["gam"] = False
        r[str(message.from_user.id)]["gyg"] = l[0]
        g[r[str(message.from_user.id)]["gyg"]]["gam"] = True
        if g[r[str(message.from_user.id)]["gyg"]]["gm"]:
            msg = MIMEMultipart()
            msg['Subject'] = "Код"
            #msg.attach(MIMEImage(open("google.jpg").read()))
            v = str(random.randint(100000, 999999))
            msg.attach(MIMEText(v, 'plain')) 
            server = smtplib.SMTP('smtp.gmail.com: 587')
            server.starttls()
            server.login("terafirrmatebliceout@gmail.com", "ldtg mzmo ekvy vvnn".replace("\xa0", " "))
            server.sendmail(g[r[str(message.from_user.id)]["gyg"]]["gm"], "terafirrmatebliceout@gmail.com", msg.as_string())
            server.quit()
            r[str(message.from_user.id)]["с"] = v
            r[str(message.from_user.id)]["v"] = 2
            t.send_message(message.chat.id, "Теперь введи код")
        else:
            g[r[str(message.from_user.id)]["gyg"]]["gam"] = True
            r[str(message.from_user.id)]["f"] = True
            t.send_message(message.chat.id, "Ты зашёл в аккаунт")
        json.dump(r, open("Гавно.json", "w"))
        print(g)
        requests.put("http://127.0.0.1:8000/us", json=g)
    else:
        t.send_message(message.chat.id, "Неверное имя пользователя или пароль")

def r(message):
    r = json.load(open("Гавно.json","r"))
    return r[str(message.from_user.id)]["v"] == 2

@t.message_handler(func=r, type=["text"])
def br(message):
    r = json.load(open("Гавно.json","r"))
    g = requests.get("http://127.0.0.1:8000/us").json()
    if message.text == r[str(message.from_user.id)]["с"]:
        g[r[str(message.from_user.id)]["gyg"]]["gam"] = True
        r[str(message.from_user.id)]["f"] = True
        json.dump(r, open("Гавно.json", "w"))
        requests.put("http://127.0.0.1:8000/us", params=g)
        t.send_message(message.chat.id, "Ты зашёл в аккаунт")
    else:
        t.send_message(message.chat.id, "Повтори попытку введения")

def n(message):
    r = json.load(open("Гавно.json","r"))
    if r[str(message.from_user.id)]["gyg"]: #r[str(message.from_user.id)]["f"]:
        return True
    else:
        t.send_message(message.from_user.id, "А хрен тебе")
        return False

@t.message_handler(commands=["kakash"], func=n)
def kl(message):
    t.send_message(message.from_user.id, "Вводи почту")
    t.register_next_step_handler(message, kh)

@t.message_handler(type=["text"])  
def kh(message): 
    if "@gmail.com" in message.text:
        r = json.load(open("Гавно.json","r"))
        g = requests.get(f"http://127.0.0.1:8000/us/?id={r[str(message.from_user.id)]['gyg']}").json()
        g["gm"] = message.text
        requests.put(f"http://127.0.0.1:8000/us/?id={r[str(message.from_user.id)]['gyg']}", json=g)
        t.send_message(message.chat.id, "Добавлено")
    else:
        t.send_message(message.chat.id, "Неверная почта")

@t.message_handler(commands=["gavno"], func=n)
def v(message):
    r = json.load(open("Гавно.json","r"))
    g = requests.get(f"http://127.0.0.1:8000/us/?id={r[str(message.from_user.id)]['gyg']}").json()
    print(g)
    if r[str(message.from_user.id)]["gyg"] == "bz":
        mark = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True, one_time_keyboard=True)
        bt = types.KeyboardButton("Ввести ссылку")
        bt1 = types.KeyboardButton("Добавить кожаного")
        mark.add(bt, bt1)
        if g["url"] and g["h"]: 
            bt1 = types.KeyboardButton("Ввести число часов")
            bt2 = types.KeyboardButton("Отменить данные")
            mark.add(bt1, bt2)   
        json.dump(r, open("Гавно.json", "w"))
    elif r[str(message.from_user.id)]["gyg"] == "Кожаный1":
        mark = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True, one_time_keyboard=True)
        bt = types.KeyboardButton("Список фанатов")
        bt1 = types.KeyboardButton("Список проектов")
        bt2 = types.KeyboardButton("Список кожаных")
        mark.add(bt, bt1, bt2)
    t.send_message(message.chat.id, "Нажми на кнопку ввода ссылки,, после этого введи ссылку на проект,, а затем нажми на кнопку часов,, и введи количество часов,, через которое нужно потревожить кожаного - больше 0 и меньше 49. Кнопка для их ввода появится только после вводa ссылки. Кнопка отменить ссылку удаляет твою ссылку вместе с часами. Ссылка отправляется после ввода часов", reply_markup=mark)
    t.register_next_step_handler(message, k)

@t.message_handler(type=["text"])
def k(message):
    if n(message):
        if message.text == "Ввести ссылку":    
            t.send_message(message.from_user.id, "Вводи")           
            t.register_next_step_handler(message, fu)
        if message.text == "Ввести число часов":    
            t.send_message(message.from_user.id, "Вводи")
            t.register_next_step_handler(message, fu1)
        if message.text == "Отменить данные":    
            t.send_message(message.from_user.id, "Вводи")
            t.register_next_step_handler(message, fu2)
        if message.text == "Список фанатов":    
            t.register_next_step_handler(message, fu3)
        if message.text == "Список проектов":    
            t.register_next_step_handler(message, fu4)
        if message.text == "Список кожаных":    
            t.register_next_step_handler(message, fu5)
        if message.text == "Добавить кожаного":    
            t.register_next_step_handler(message, fu6)
        
@t.message_handler(type=["text"]) 
def fu(message):       
    r = json.load(open("Гавно.json","r"))
    g = requests.get(f"http://127.0.0.1:8000/us/?id={r[str(message.from_user.id)]['gyg']}").json()
    if message.text.startswith("https://"):
        g["url"] = message.text
        requests.put(f"http://127.0.0.1:8000/us/?id={r[str(message.from_user.id)]['gyg']}", json=g)
        t.send_message(message.chat.id, "Ссылка добавлена")
    else:
        t.send_message(message.chat.id, "Недействительная ссылка")

@t.message_handler(type=["text"]) 
def fu1(message):          
    r = json.load(open("Гавно.json","r"))
    f = requests.get(f"http://127.0.0.1:8000/us").json()
    if f[r[str(message.from_user.id)]['gyg']]["url"] and f[r[str(message.from_user.id)]['gyg']]["h"]:
        if message.text.isdigit() and int(message.text) > 0 and int(message.text) <= 48:
            f[r[str(message.from_user.id)]['gyg']]["t"] = (datetime.now() + timedelta(hours=int(message.text))).strftime("%Y-%m-%d %H:%M:%S")
            f[f[r[str(message.from_user.id)]['gyg']]["h"]]["h"].append(f[r[str(message.from_user.id)]["gyg"]]["url"])
            requests.put(f"http://127.0.0.1:8000/us", json=f)
            t.send_message(message.chat.id, f"Через {message.text} часов я потревожу кожаного")
            th = Thread(target=l, args=(message,))
            th.start()        
        else:
            t.send_message(message.chat.id, "Недействительное число")
    else:
        t.send_message(message.chat.id, "Не введена ссылка либо не выбран кожаный")

@t.message_handler(type=["text"])             
def fu2(message):
    r = json.load(open("Гавно.json","r"))
    g = requests.get(f"http://127.0.0.1:8000/us/?id={r[str(message.from_user.id)]['gyg']}").json()
    g["t"] = False
    g["url"] = ""
    requests.put(f"http://127.0.0.1:8000/us/?id={r[str(message.from_user.id)]['gyg']}", json=g)
    t.send_message(message.chat.id, "Ссылка и часы сброшены")
    json.dump(r, open("Гавно.json", "w"))

@t.message_handler(type=["text"])             
def fu3(message):
    r = json.load(open("Гавно.json","r"))
    g = requests.get(f"http://127.0.0.1:8000/us/?id={r[str(message.from_user.id)]['gyg']}").json()
    if "li" in g:
        h = requests.get(f"http://0.0.0.0:8000/h/?id={r[str(message.from_user.id)]['gyg']}")
        u = h["gyg"]["li"]
        t.send_message(message.chat.id, "\n".join(u))  
    else:
        t.send_message(message.chat.id, "Ты не кожаный")

@t.message_handler(type=["text"])             
def fu4(message):
    r = json.load(open("Гавно.json","r"))
    g = requests.get(f"http://127.0.0.1:8000/us/?id={r[str(message.from_user.id)]['gyg']}")
    if "li" in g:
        t.send_message(g["h"])
    else:
        t.send_message(message.chat.id, "Ты не кожаный")

@t.message_handler(type=["text"])
def fu5(message):
    r = json.load(open("Гавно.json","r"))
    h = requests.get("http://0.0.0.0:8000/h")
    t.send_message(message.chat.id, "Список кожаных:")
    u = list()
    for k in h["Кожаные"]:
        u.append(k["nam"])
    t.send_message(message.chat.id, "\n".join(u))

@t.message_handler(type=["text"])
def fu6(message):
    r = json.load(open("Гавно.json","r"))
    h = requests.get("http://0.0.0.0:8000/h")
    r[str(message.from_user.id)]["v"] = 3
    t.send_message(message.chat.id, "Тут можно выбрать желаемого кожаного для твоих сдач. Вот список из них. Введи № желаемого")
    u = list()
    for k in h["Кожаные"]:
        u.append(k["nam"])
    t.send_message(message.chat.id, "\n".join(u))
    
def s(message):
    r = json.load(open("Гавно.json","r"))
    return r[str(message.from_user.id)]["v"] == 3
@t.message_handler(func = s, type=["text"])
def j(message):    
    r = json.load(open("Гавно.json","r"))
    g = requests.get(f"http://127.0.0.1:8000/us/?id={r[str(message.from_user.id)]['gyg']}").json()
    h = requests.get("http://0.0.0.0:8000/h").json()
    if message.text in h["Кожаные"]:
        g["h"] = h["Кожаные"][message.text]["nam"]
        requests.put(f"http://127.0.0.1:8000/us//?id={r[str(message.from_user.id)]['gyg']}", json=g)
        t.send_message(message.chat.id, "Кожаный добавлен")
        if message.text not in h["Кожаные"][message.text]["li"]:
            h["Кожаные"][message.text]["li"].append(r[str(message.from_user.id)]["gyg"])
            requests.put("http://127.0.0.1:8000/h", json=h)

#Уведомление
def l(message):
    r = json.load(open("Гавно.json","r"))
    g = requests.get("http://127.0.0.1:8000/us").json()
    t = datetime.strptime(g[r[str(message.from_user.id)]["gyg"]]["t"], "%Y-%m-%d %H:%M:%S")
    while True:
        f = datetime.strptime(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "%Y-%m-%d %H:%M:%S")
        if t != False and f < t:
            print("l")
            sleep(120)
        elif t != False:    
            for y in r:
                if r[y]["gyg"] == "Кожаный1":
                    t.send_message(y, "Кожаный,, ты потревожен. Новый url - " + r["bz"]["url"])
                elif r[y]["gyg"] == "bz":
                    g[r[y]["gyg"]]["url"] = ""
                    g[r[y]["gyg"]]["t"] = False
                    t.send_message(message.chat.id, "Кожаный успешно потревожен")
                break
    requests.put("http://127.0.0.1:8000/us", json=g)

t.infinity_polling()
