'''

Код работает на html шаблоне!
Если вы хотите использовать API, вам в -> chat/api_methods/main.py
@starsden

'''

from fastapi import FastAPI, WebSocket, Request
from fastapi.templating import Jinja2Templates
from starlette.websockets import WebSocketDisconnect
from typing import List

app = FastAPI()
templates = Jinja2Templates(directory="templates")
clients: List[WebSocket] = []

@app.get("/")
async def get_chat(request: Request):
    return templates.TemplateResponse("chat.html", {"request": request})

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    clients.append(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            for client in clients:
                if client != websocket:
                    await client.send_text(data)
    except WebSocketDisconnect:
        clients.remove(websocket)
