from fastapi import FastAPI,status,HTTPException,Request
from pydantic import BaseModel
from random import randint
from typing import Optional
from .routers import recognise, users
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from pathlib import Path


#TODO: fix output schema

app=FastAPI()
app.include_router(users.router)
app.include_router(recognise.router)



BASE_DIR = Path(__file__).resolve().parent
templates = Jinja2Templates(directory=str(Path(BASE_DIR, 'templates')))

@app.get('/')
async def root(request: Request):
    return templates.TemplateResponse('item.html', {"request": request, "id": "id"})

