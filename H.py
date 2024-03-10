from telebot import TeleBot, types
import requests
from datetime import datetime, timedelta
import json
from time import sleep
from threading import Thread
import random
from email.mime.multipart import MIMEMultipart
#from email.mime.image import MIMEImage
from email.mime.text import MIMEText
import smtplib
from os import getenv
from dotenv import load_dotenv

load_dotenv()
t = TeleBot(getenv("t"))

@t.message_handler(commands=["start"])
def h(message):
    r = json.load(open("Гавно.json","r"))
    if str(message.from_user.id) not in r:
        r[str(message.from_user.id)] = {"v": 0, "gyg": "", "f":False, "c" : 0}
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
            server.login("terafirrmatebliceout@gmail.com", getenv("Gig").replace("\xa0", " "))
            server.sendmail(g[r[str(message.from_user.id)]["gyg"]]["gm"], "terafirrmatebliceout@gmail.com", msg.as_string())
            server.quit()
            r[str(message.from_user.id)]["с"] = v
            r[str(message.from_user.id)]["v"] = 2
            t.send_message(message.chat.id, "Теперь введи код")
            t.register_next_step_handler(message, br)
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
        requests.put("http://127.0.0.1:8000/us", json=g)
        t.send_message(message.chat.id, "Ты зашёл в аккаунт")
    else:
        t.send_message(message.chat.id, "Повтори попытку введения")

def n(message):
    r = json.load(open("Гавно.json","r"))
    if r[str(message.from_user.id)]["f"]:
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
    if "@gmail.com" in message.text or "@mail.ru" in message.text or "@yandex.com" in message.text:
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
    if "tam" not in g[r[str(message.from_user.id)]['gyg']]:
        mark = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True, one_time_keyboard=True)
        bt = types.KeyboardButton("Ввести ссылку")
        bt1 = types.KeyboardButton("Добавить кожаного")
        mark.add(bt, bt1)
        if g["url"] and g["h"]: 
            bt1 = types.KeyboardButton("Ввести число часов")
            bt2 = types.KeyboardButton("Отменить данные")
            mark.add(bt1, bt2)   
        json.dump(r, open("Гавно.json", "w"))
    elif "tam" in g[r[str(message.from_user.id)]['gyg']]:
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
            fu3(message)
        if message.text == "Список проектов":    
            fu4(message)
        if message.text == "Список кожаных":    
            fu5(message)
        if message.text == "Добавить кожаного":    
            fu6(message)
        
@t.message_handler(type=["text"]) 
def fu(message):       
    r = json.load(open("Гавно.json","r"))
    g = requests.get(f"http://127.0.0.1:8000/us/?id={r[str(message.from_user.id)]['gyg']}").json()
    if "tam" in g:
        t.send_message(message.chat.id, "Стоять кавбой")
        return
    if message.text.startswith("https://"):
        g["url"] = message.text
        print(g)
        k = requests.put(f"http://127.0.0.1:8000/us/?id={r[str(message.from_user.id)]['gyg']}", json=g)
        print(k.text)
        t.send_message(message.chat.id, "Ссылка добавлена")
    else:
        t.send_message(message.chat.id, "Недействительная ссылка")

@t.message_handler(type=["text"]) 
def fu1(message):          
    r = json.load(open("Гавно.json","r"))
    g = requests.get(f"http://127.0.0.1:8000/us").json()
    if "tam" in g[r[str(message.from_user.id)]['gyg']]:
        t.send_message(message.chat.id, "Стоять кавбой")
        return
    if g[r[str(message.from_user.id)]['gyg']]["url"] and g[r[str(message.from_user.id)]['gyg']]["h"]:
        if message.text.isdigit() and int(message.text) > 0 and int(message.text) <= 48:
            g[r[str(message.from_user.id)]['gyg']]["t"] = (datetime.now() + timedelta(hours=int(message.text))).strftime("%Y-%m-%d %H:%M:%S")
            if g[r[str(message.from_user.id)]["gyg"]]["url"] not in g[g[r[str(message.from_user.id)]['gyg']]["h"]]["h"]:
                g[g[r[str(message.from_user.id)]['gyg']]["h"]]["h"].append(g[r[str(message.from_user.id)]["gyg"]]["url"])
            else:
                t.send_message(message.chat.id, "Последняя введённая ссылка была отпрвлена раннее")
            requests.put(f"http://127.0.0.1:8000/us", json=g)
            t.send_message(message.chat.id, f"Через {message.text} часов я потревожу кожаного")
            th = Thread(target=le, args=(message,))
            th.start()        
        else:
            t.send_message(message.chat.id, "Недействительное число")
    else:
        t.send_message(message.chat.id, "Не введена ссылка либо не выбран кожаный")

@t.message_handler(type=["text"])             
def fu2(message):
    r = json.load(open("Гавно.json","r"))
    g = requests.get(f"http://127.0.0.1:8000/us/?id={r[str(message.from_user.id)]['gyg']}").json()
    if "tam" in g:
        t.send_message(message.chat.id, "Стоять кавбой")  
        return
    g["t"] = False
    g["url"] = ""
    requests.put(f"http://127.0.0.1:8000/us/?id={r[str(message.from_user.id)]['gyg']}", json=g)
    t.send_message(message.chat.id, "Ссылка и часы сброшены")
    json.dump(r, open("Гавно.json", "w"))
            
def fu3(message):
    r = json.load(open("Гавно.json","r"))
    g = requests.get(f"http://127.0.0.1:8000/us/?id={r[str(message.from_user.id)]['gyg']}").json()
    h = requests.get(f"http://0.0.0.0:8000/h/?id={r[str(message.from_user.id)]['gyg']}").json()
    if "tam" in g:
        t.send_message(message.chat.id, "Фанаты:\n\n" + "\n".join(h["li"]))  
        return
    t.send_message(message.chat.id, "Ты не кожаный")
          
def fu4(message):
    r = json.load(open("Гавно.json","r"))
    g = requests.get(f"http://127.0.0.1:8000/us/?id={r[str(message.from_user.id)]['gyg']}").json()
    if "tam" in g:
        t.send_message(message.chat.id, "Ссылки:\n\n" + "\n".join(g["h"]))
        return
    t.send_message(message.chat.id, "Ты не кожаный")

def fu5(message):
    r = json.load(open("Гавно.json","r"))
    h = requests.get("http://0.0.0.0:8000/h").json()
    if r[str(message.from_user.id)]["gyg"] not in h["Кожаные"]:
        t.send_message(message.chat.id, "Ты не кожаный")
        return
    u = list()
    for k in h["Кожаные"]:
        u.append(f"{k}. " + h["Кожаные"][k]["nam"])
    t.send_message(message.chat.id, "Список кожаных:\n\n" + "\n".join(u))

def fu6(message):
    r = json.load(open("Гавно.json","r"))
    h = requests.get("http://0.0.0.0:8000/h").json()
    if r[str(message.from_user.id)]["gyg"] in h["Кожаные"]:
        t.send_message(message.chat.id, "Стоять кавбой")
        return
    r[str(message.from_user.id)]["v"] = 3
    json.dump(r, open("Гавно.json", "w"))
    u = list()
    for k in h["Кожаные"]:
        u.append(f"{k}." + h["Кожаные"][k]["nam"])
    t.send_message(message.chat.id, "Тут можно выбрать желаемого кожаного для твоих сдач. Вот список из них. Введи № желаемого")
    t.send_message(message.chat.id, "\n".join(u))
    t.register_next_step_handler(message, j)
    
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
def le(message):
    r = json.load(open("Гавно.json","r"))
    g = requests.get("http://127.0.0.1:8000/us").json()
    if "tam" in g[r[str(message.from_user.id)]['gyg']]:
        return
    if g[r[str(message.from_user.id)]["gyg"]]["t"] != False:
        u = datetime.strptime(g[r[str(message.from_user.id)]["gyg"]]["t"], "%Y-%m-%d %H:%M:%S")
    else:
        return
    while True:
        f = datetime.strptime(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "%Y-%m-%d %H:%M:%S")
        if f < u:
            sleep(5)
        else:    
            for y in r:
                if r[y]["gyg"] == g[r[str(message.from_user.id)]["gyg"]]["h"]:
                    t.send_message(y, "Кожаный,, ты потревожен. Новый url - " + g[r[str(message.from_user.id)]["gyg"]]["url"])
                    break                    
            g[r[str(message.from_user.id)]["gyg"]]["url"] = ""
            g[r[str(message.from_user.id)]["gyg"]]["t"] = False
            t.send_message(message.chat.id, "Кожаный успешно потревожен")
            break
    requests.put("http://127.0.0.1:8000/us", json=g)

if __name__ == "__main__":
    t.infinity_polling()
