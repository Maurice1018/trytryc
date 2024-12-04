#!/usr/bin/env python
# coding: utf-8

# In[1]:


from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
import time
from datetime import datetime
import json
import os

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

# 定義返回的模型，包括 items 和 update_time
class ResponseData(BaseModel):
    items: List[Item]
    update_time: str

app = FastAPI()

# 設定靜態資源與模板目錄
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# 從檔案讀取資料的 API
@app.get("/data/", response_model=ResponseData)
async def get_items():
    with open("badminton.json", "r", encoding="utf-8") as f:
        items = json.load(f)
    file_stat = os.stat('./badminton.json')
    update_time = datetime.fromtimestamp(file_stat.st_mtime).strftime('%Y/%m/%d %H:%M:%S')
    return {'items':items , 'update_time':update_time}

# 提供運動資料給前端
@app.get("/")
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})
