from typing import Annotated
from pydantic import BaseModel
from fastapi import FastAPI, Query, Path, Body
from fastapi.encoders import jsonable_encoder
import json

app = FastAPI()

@app.get("/us/")
def h(): #id: Annotated[str, Path()]
    k = json.load(open("Резня.json","r"))
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
def t(js):   
    json.dump(js, open("Резня.json", "w"))
    return js

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
def h(): #id: Annotated[str, Path()]
    k = json.load(open("Аш.json","r"))
    return k