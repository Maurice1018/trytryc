#!/usr/bin/env python
# coding: utf-8

# In[1]:


from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
import json

from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.requests import Request


# In[2]:


class Item(BaseModel):
    運動中心: str
    運動種類: str
    場地: str
    日期: str
    時間: str

app = FastAPI()

# 設定靜態資源與模板目錄
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# 從檔案讀取資料的 API
@app.get("/data/", response_model=List[Item])
async def get_items():
    with open("badminton.json", "r", encoding="utf-8") as f:
        items = json.load(f)
    return items

# 提供運動資料給前端
@app.get("/")
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

