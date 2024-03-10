from typing import Annotated
from pydantic import BaseModel
from fastapi import FastAPI, Query, Path, Body, HTTPException
from fastapi.encoders import jsonable_encoder
import json

app = FastAPI()

class It(BaseModel):
    passs: str
    gm: str 
    url: str 
    t: str | bool
    gam: bool 
    h: str

class H(BaseModel):
    num: str
    l: list
    
@app.get("/us/")
def h(id:str|None = None):
    k = json.load(open("Резня.json","r"))
    if id != None:
        return k[id]
    else:
        return k

@app.post("/us/")
def g(url: str, t = False):
    if not url:
        print("Кожаный,, ты сдурел,, где юрл")
        return
    k = json.load(open("Резня.json","r"))
    #k[id] = k[id].update(dict(url, t))
    
    #it = k[id].update(dict(url, t))
    #k[id] = jsonable_encoder(it)
    json.dump(k, open("Резня.json", "w"))
    return k

@app.put("/us/")
def t(r: Annotated[It | dict, Body()], id:str|None = None):  
    if id != None and r is It:
        if id in k:
            k = json.load(open("Резня.json","r"))
            k[id] = r.model_dump()
            json.dump(k, open("Резня.json", "w"))
            return r           
        else:
            pass
            #raise HTTPException(status_code=404, detail="Неверно введён id", headers="Ничего")
    elif id == None and r is dict:
        json.dump(r, open("Резня.json", "w"))
        return r
    elif id != None and r is not It:
        pass
        #raise HTTPException(status_code=402, detail="При запросе без id нужен словарь с данными всех пользователей пользователя", headers="Ничего")
    elif id == None and r is not dict:
        pass
        #raise HTTPException(status_code=402, detail="При введении id нужен словарь с данными 1 пользователя", headers="Ничего")

@app.delete("/us/")
def t(url: str, t = False):
    k = json.load(open("Резня.json","r"))
    if url:
        k[id]["url"] = None
    if t:
        k[id]["t"] = None
    json.dump(k, open("Резня.json", "w"))
    return k

@app.get("/h/")
def h(id:str|None = None):
    k = json.load(open("Аш.json","r"))
    if id != None:
        return k[id]
    else:
        return k

@app.put("/h/")
def h(h: Annotated[H | dict, Body()], id: str | None = None):
    k = json.load(open("Аш.json","r"))
    if id != None and h is H:
        if id in k["Кожаные"]:
            k = json.load(open("Аш.json","r"))
            k["Кожаные"][id] = h.model_dump() 
            json.dump(k, open("Аш.json", "w"))
            return h           
        else:
            pass
            #raise HTTPException(status_code=404, detail="Неверно введён id", headers="Ничего")
    elif id == None and h is dict:
        json.dump(h, open("Аш.json", "w"))
        return h
    elif id != None and h is not H:
        pass
        #raise HTTPException(status_code=402, detail="При введении id нужен словарь с данными 1 пользователя", headers="Ничего")
    elif id == None and h is not dict:
        pass
        #raise HTTPException(status_code=402, detail="При запросе без id нужен словарь с данными всех пользователей пользователя", headers="Ничего")