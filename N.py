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

class K(BaseModel):
    passs: str
    gm: str
    tam: bool
    gam: bool
    h: list

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
def g(r: Annotated[dict, Body()], id:str|None = None):
    if id != None: 
        if type(r) == dict:
            k = json.load(open("Резня.json","r"))
            if id in k:
                k[id].update(r)
                json.dump(k, open("Резня.json", "w"))
                return r           
            else:
                raise HTTPException(status_code=404, detail="Неверно введён id", headers={"data":"Nothing"})
        else:
            raise HTTPException(status_code=400, detail="Нужен словарь", headers={"data":"Nothing"})
    if id == None: 
        if type(r) == dict:
            json.dump(r, open("Резня.json", "w"))
            return r
        else:
            raise HTTPException(status_code=400, detail="Нужен словарь", headers={"data":"Nothing"})

@app.put("/us/")
def t(r: Annotated[It | dict, Body()], id:str|None = None):  
    if id != None: 
        if type(r) == It:
            k = json.load(open("Резня.json","r"))
            if id in k:
                k[id] = r.model_dump()
                json.dump(k, open("Резня.json", "w"))
                return r           
            else:
                raise HTTPException(status_code=404, detail="Неверно введён id", headers={"data":"Nothing"})
        else:
            raise HTTPException(status_code=400, detail="При введении id нужен словарь с данными 1 пользователя", headers={"data":"Nothing"})
    if id == None: 
        if type(r) == dict:
            json.dump(r, open("Резня.json", "w"))
            return r
        else:
            raise HTTPException(status_code=400, detail="При запросе без id нужен словарь с данными всех пользователей пользователя", headers={"data":"Nothing"})

@app.delete("/us/")
def t(r: Annotated[list | dict, Body()], id:str|None = None):
    if id != None: 
        if type(r) == list:
            k = json.load(open("Резня.json","r"))
            if id in k:
                for i in r:
                    if i in r:
                        del k[id][i]
                    else:
                        raise HTTPException(status_code=404, detail="Указан отсутствующий в базе элемент", headers={"data":"Nothing"})
                json.dump(k, open("Резня.json", "w"))
                return r           
            else:
                raise HTTPException(status_code=404, detail="Неверно введён id", headers={"data":"Nothing"})
        else:
            raise HTTPException(status_code=400, detail="Нужен список", headers={"data":"Nothing"})
    elif id == None: 
        if type(r) == dict:
            json.dump(r, open("Резня.json", "w"))
            return r
        else:
            raise HTTPException(status_code=400, detail="Нужен словарь", headers={"data":"Nothing"})

@app.get("/h/")
def h(id:str|None = None):
    k = json.load(open("Аш.json","r"))
    if id != None:
        return k["Кожаные"][id]
    else:
        return k
    
@app.post("/h/")
def g(r: Annotated[dict, Body()], id:str|None = None):
    if id != None: 
        if type(r) == dict:
            k = json.load(open("Аш.json","r"))
            if id in k["Кожаные"]:
                k["Кожаные"][id].update(r)
                json.dump(k, open("Аш.json", "w"))
                return r           
            else:
                raise HTTPException(status_code=404, detail="Неверно введён id", headers={"data":"Nothing"})
        else:
            raise HTTPException(status_code=400, detail="Нужен словарь", headers={"data":"Nothing"})
    if id == None: 
        if type(r) == dict:
            json.dump(r, open("Аш.json", "w"))
            return r
        else:
            raise HTTPException(status_code=400, detail="Нужен словарь", headers={"data":"Nothing"})

@app.put("/h/")
def h(h: Annotated[H | dict, Body()], id: str | None = None):
    if id != None: 
        if type(h) == H:
            k = json.load(open("Аш.json","r"))
            if id in k["Кожаные"]:
                k["Кожаные"][id] = h.model_dump()
                json.dump(k, open("Аш.json", "w"))
                return h           
            else:
                raise HTTPException(status_code=404, detail="Неверно введён id", headers={"data":"Nothing"})
        else:
            raise HTTPException(status_code=400, detail="При введении id нужен словарь с данными 1 пользователя", headers={"data":"Nothing"})
    if id == None: 
        if type(h) == dict:
            json.dump(h, open("Аш.json", "w"))
            return h
        else:
            raise HTTPException(status_code=400, detail="При запросе без id нужен словарь с данными всех пользователей пользователя", headers={"data":"Nothing"})
        
@app.delete("/h/")
def t(r: Annotated[list | dict, Body()], id:str|None = None):
    if id != None: 
        if type(r) == list:
            k = json.load(open("Аш.json","r"))
            if id in k["Кожаные"]:
                for i in r:
                    if i in r:
                        del k["Кожаные"][id][i]
                    else:
                        raise HTTPException(status_code=404, detail="Указан отсутствующий в базе элемент", headers={"data":"Nothing"})
                json.dump(k, open("Аш.json", "w"))
                return r           
            else:
                raise HTTPException(status_code=404, detail="Неверно введён id", headers={"data":"Nothing"})
        else:
            raise HTTPException(status_code=400, detail="Нужен список", headers={"data":"Nothing"})
    elif id == None: 
        if type(r) == dict:
            json.dump(r, open("Аш.json", "w"))
            return r
        else:
            raise HTTPException(status_code=400, detail="Нужен словарь", headers={"data":"Nothing"})