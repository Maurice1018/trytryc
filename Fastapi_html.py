#!/usr/bin/env python
# coding: utf-8

# In[1]:

from fastapi import FastAPI , BackgroundTasks
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

from fetch_badminton import fetch_badminton , refresh_sessionID

import asyncio

# In[2]:
class Item(BaseModel):
    運動中心: str
    運動種類: str
    場地: str
    日期: str
    時間: str

class ItemResponse(BaseModel):
    items: List[Item]
    update_time: str

app = FastAPI()

#設定背景程式執行refresh session ID 永遠的活著
async def long_running_task():
    while True:
        refresh_time = 1450
        print('Starting refresh session ID...')
        try:
            refresh_sessionID()
            print('Sucessfully refresh session ID')
        except Exception as e:
            print(f"Failed to refresh session: {str(e)}")

        await asyncio.sleep(refresh_time)

@app.on_event('startup')
async def start_background_task():
    # 啟動背景任務
    asyncio.create_task(long_running_task())

# 設定靜態資源與模板目錄
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# 從檔案讀取資料的 API
@app.get("/data/", response_model=ItemResponse)
async def get_items():
    with open("badminton.json", "r", encoding="utf-8") as f:
        items = json.load(f)
    file_stat = os.stat('./badminton.json')
    update_time = datetime.fromtimestamp(file_stat.st_atime).strftime('%Y/%m/%d %H:%M:%S')
    return {'items':items , 'update_time':update_time}

#打到這個router就會refresh session ID的有效時間
@app.get("/api/refresh-session")
async def refresh_session():
    try:
        refresh_sessionID()
        return {"message": "Session refreshed successfully"}
    except Exception as e:
        return {"message": f"Failed to refresh session: {str(e)}"}

#打到這個router就會執行fetch_data的程式
@app.get("/api/fetch-data")
async def fetch_data():
    try:
        t= time.time()
        fetch_badminton()
        spend_time = round(time.time() - t , 2)
        return {"message": f"Fetch Data successfully. Spend_time : {spend_time} s"}
    except Exception as e:
        return {"message": f"Failed to Fetch Data: {str(e)}"}

#refresh的網頁點擊按鈕
@app.get("/refresh")
async def refresh_page(request: Request):
    return templates.TemplateResponse("refresh.html", {"request": request})

#fetch data的網頁執行按鈕
@app.get("/fetch")
async def fetch_page(request: Request):
    return templates.TemplateResponse("fetch.html", {"request": request})

#提供資料給前端root
@app.get("/")
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})
