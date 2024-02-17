from telebot import TeleBot, types
import requests
from datetime import datetime, date, time, timedelta
import json
from pydantic import BaseModel
from time import sleep
from threading import Thread

t = TeleBot("6370938616:AAGKNWr66eB3e36e7a2CI90LAQmXhpfGB-o")

@t.message_handler(commands=["start"])
def h(message):
    r = json.load(open("Гавно.json","r"))
    if str(message.from_user.id) not in r:
        r[str(message.from_user.id)] = {"v": 0, "gyg": ""}
    t.send_message(message.chat.id, "Введи имя пользователя и пароль через пробел")
    json.dump(r, open("Гавно.json", "w"))
    r[str(message.from_user.id)]["v"] = 1

def r(message):
    r = json.load(open("Гавно.json","r"))
    return r[str(message.from_user.id)]["v"] == 1

@t.message_handler(func=r)
def b(message):
    g = requests.get("http://127.0.0.1:8000/us").json()
    r = json.load(open("Гавно.json","r"))
    l = message.text.split()
    print(g)
    if len(l) != 2:
        t.send_message(message.chat.id, "Неверный формат сообщения. Введи имя пользователя и пароль через пробел. Для повторной повытки - /start")
    elif l[0] in g and g[l[0]]["gam"]:
        t.send_message(message.chat.id, "Похоже кто - то уже в аккаунте")
    elif l[0] in g and l[1] == g[l[0]]["pass"]:
        if r[str(message.from_user.id)]["gyg"]:
            g[r[str(message.from_user.id)]["gyg"]]["gam"] = False
        r[str(message.from_user.id)]["gyg"] = l[0]
        g[r[str(message.from_user.id)]["gyg"]]["gam"] = True
        t.send_message(message.chat.id, "Ты вошёл")
    else:
        t.send_message(message.chat.id, "Неверное имя пользователя или пароль")
    json.dump(r, open("Гавно.json", "w"))
    requests.put("http://127.0.0.1:8000/us", params=g)

def n(message):
    r = json.load(open("Гавно.json","r"))
    if r[str(message.from_user.id)]["gyg"]:
        return True
    else:
        t.send_message(message.from_user.id, "А хрен тебе")
        return False
        
@t.message_handler(commands=["gavno"], func=n)
def v(message):
    g = requests.get("http://127.0.0.1:8000/us").json()
    r = json.load(open("Гавно.json","r"))
    if r[str(message.from_user.id)]["gyg"] == "bz":
        mark = types.InlineKeyboardMarkup(row_width=2)
        bt = types.InlineKeyboardButton("Ввести ссылку", callback_data="Ссылка")
        mark.add(bt)
        if g[r[str(message.from_user.id)]["gyg"]]["url"]: 
            bt1 = types.InlineKeyboardButton("Ввести число часов", callback_data="Часы")
            bt2 = types.InlineKeyboardButton("Отменить ссылку", callback_data="Отмена ссылки")
            mark.add(bt1, bt2)   
        json.dump(r, open("Гавно.json", "w"))
        t.send_message(message.chat.id, "Нажми на кнопку ввода ссылки,, после этого введи ссылку на проект,, а затем нажми на кнопку часов,, и введи количество часов,, через которое нужно потревожить кожаного - больше или равно 0 и меньше 49. Кнопка для их ввода появится только после вводa ссылки. Кнопка отменить ссылку удаляет твою ссылку вместе с часами", reply_markup=mark)
    elif r[str(message.from_user.id)]["gyg"] == "Кожаный1":
        mark = types.InlineKeyboardMarkup(row_width=1)
        bt = types.InlineKeyboardButton("Список фанатов", callback_data="Фанаты")
        bt1 = types.InlineKeyboardButton("Список проектов", callback_data="Юрлы")
        mark.add(bt)

@t.callback_query_handler(lambda ob: ob.data == "Ссылка")
def k(obj):
    t.send_message(obj.from_user.id, "Вводи")
    return n(obj)
@t.callback_query_handler(lambda ob: ob.data == "Часы")
def x(obj):
    t.send_message(obj.from_user.id, "Вводи")
    return n(obj)
@t.callback_query_handler(lambda ob: ob.data == "Отмена ссылки")
def z(obj):
    return n(obj)
@t.callback_query_handler(lambda ob: ob.data == "Фанаты")
def jo(obj):
    return n(obj)
@t.callback_query_handler(lambda ob: ob.data == "Юрлы")
def jojo(obj):
    return n(obj)
        
@t.message_handler(func=k) 
def fu(message):       
    g = requests.get("http://127.0.0.1:8000/us").json()
    r = json.load(open("Гавно.json","r"))
    if message.text.startswith("https://"):
        g[r[str(message.from_user.id)]["gyg"]]["url"] = message.text
        requests.put("http://127.0.0.1:8000/us", json=g)
        json.dump(r, open("Гавно.json", "w"))
        t.send_message(message.chat.id, "Ссылка добавлена")
    else:
        t.send_message(message.chat.id, "Недействительная ссылка. Попробуй ещё раз")

'''
@t.message_handler(func=x) 
def fu1(message):          
    g = requests.get("http://127.0.0.1:8000/us").json()
    r = json.load(open("Гавно.json","r"))
    if message.text.isdigit() and int(message.text) > 0 and int(message.text) <= 48:
        g[r[str(message.from_user.id)]["gyg"]]["t"] = (datetime.now() + timedelta(hours=int(message.text))).strftime("%Y-%m-%d %H:%M:%S")
        requests.put("http://127.0.0.1:8000/us", json=g)
        json.dump(r, open("Гавно.json", "w"))
        t.send_message(message.chat.id, f"Через {message.text} часов я потревожу кожаного")
        th = Thread(target=l, args=(message))
        th.start()        
    else:
        t.send_message(message.chat.id, "Недействительное число. Попробуй ещё раз")
'''

@t.message_handler(func=z)             
def fu2(message):
    g = requests.get("http://127.0.0.1:8000/us").json()
    r = json.load(open("Гавно.json","r"))
    g[r[str(message.from_user.id)]["gyg"]]["t"] = False
    g[r[str(message.from_user.id)]["gyg"]]["url"] = ""
    json.dump(r, open("Гавно.json", "w"))
    requests.put("http://127.0.0.1:8000/us", json=g)
    t.send_message(message.chat.id, "Ссылка и часы сброшены")

@t.message_handler(func=jo)             
def fu3(message):
    g = requests.get("http://127.0.0.1:8000/us").json()
    r = json.load(open("Гавно.json","r"))
    h = requests.get("http://0.0.0.0:8000/h")
    u = h["Кожаные"][r[str(message.from_user.id)]["gyg"]]["li"]
    t.send_message(message.chat.id, "\n".join(u))    

@t.message_handler(func=jojo)             
def fu4(message):
    g = requests.get("http://127.0.0.1:8000/us").json()
    r = json.load(open("Гавно.json","r"))
    t.send_message(g[r[str(message.from_user.id)]["gyg"]]["h"])
       
@t.message_handler(commands=["dermo"])
def а(message):
    h = requests.get("http://0.0.0.0:8000/h")
    r = json.load(open("Гавно.json","r"))
    r[str(message.from_user.id)]["v"] = 2
    t.send_message(message.chat.id, "Тут можно выбрать желаемого кожаного для твоих сдач. Вот список из них")
    for k in h["Кожаные"]:
        t.send_message(message.chat.id, k["nam"])
    
def s(message):
    r = json.load(open("Гавно.json","r"))
    return r[str(message.from_user.id)]["v"] == 2
@t.message_handler(func = s)
def j(message):    
    g = requests.get("http://127.0.0.1:8000/us").json()
    h = requests.get("http://0.0.0.0:8000/h")
    r = json.load(open("Гавно.json","r"))
    if message.text in h["Кожаные"]:
        g[r[str(message.from_user.id)]["gyg"]]["h"] = h["Кожаные"][message.text]["nam"]
        if message.text not in h["Кожаные"][message.text]["li"]:
            h["Кожаные"][message.text]["li"].append(r[str(message.from_user.id)]["gyg"])
    requests.put("http://127.0.0.1:8000/us", params=g)

@t.message_handler(commands=["time"]) 
def fu0(message):
    r = json.load(open("Гавно.json","r"))
    r[str(message.from_user.id)]["v"] = 3
    t.send_message(message.chat.id, "Давай")
def s1(message):
    r = json.load(open("Гавно.json","r"))
    return r[str(message.from_user.id)]["v"] == 3
@t.message_handler(func=s1) 
def fu1(message):          
    g = requests.get("http://127.0.0.1:8000/us").json()
    r = json.load(open("Гавно.json","r"))
    if message.text.isdigit() and int(message.text) > 0 and int(message.text) <= 48:
        g[r[str(message.from_user.id)]["gyg"]]["t"] = (datetime.now() + timedelta(hours=int(message.text))).strftime("%Y-%m-%d %H:%M:%S")
        requests.put("http://127.0.0.1:8000/us", json=g)
        json.dump(r, open("Гавно.json", "w"))
        t.send_message(message.chat.id, f"Через {message.text} часов я потревожу кожаного")
        th = Thread(target=l, args=(message))
        th.start()        
    else:
        t.send_message(message.chat.id, "Недействительное число. Попробуй ещё раз")

#Уведомление
def l(message):
    g = requests.get("http://127.0.0.1:8000/us").json()
    r = json.load(open("Гавно.json","r"))
    t = datetime.strptime(g[r[str(message.from_user.id)]]["t"], "%Y-%m-%d %H:%M:%S")
    p = r[str(message.from_user.id)]["gyg"]
    while True:
        f = datetime.strptime(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "%Y-%m-%d %H:%M:%S")
        if t != False and t < f:
            print("l")
            sleep(5)
        elif t != False:    
            for y in r:
                if r[y]["gyg"] == "фу":
                    g[r[y]["gyg"]]["h"] = r[y]["url"]
                    t.send_message(y, "Кожаный,, ты потревожен. Новый url - " + r[y]["url"])
                elif r[y]["gyg"] == "bz":
                    g[p]["t"] = False
                    t.send_message(message.chat.id, "Кожаный успешно потревожен")
                break
    requests.put("http://127.0.0.1:8000/us", params=g)

t.polling()
