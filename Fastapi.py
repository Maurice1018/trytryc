#!/usr/bin/env python
# coding: utf-8

# In[1]:


from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
import json


# In[2]:


class Item(BaseModel):
    運動中心: str
    運動種類: str
    場地: str
    日期: str
    時間: str

app = FastAPI()
@app.get("/items", response_model=List[Item])
async def get_items():
    with open('badminton.json' , 'r' , encoding = 'utf-8') as f:
        items = json.load(f)
    return items

