'''

Код использует API без шаблонов
Если вы хотите использовать с html шаблонами, вам в -> chat/main.py
@starsden


КОД НЕ РАБОЧИЙ
фак
'''



from fastapi import FastAPI, WebSocket
from starlette.websockets import WebSocketDisconnect
from typing import List

app = FastAPI()
clients: List[WebSocket] = []

@app.get("/")
async def root():
    return {"message": "Congrat! WebSocket chat API is running. Connect via /ws"}

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
        await websocket.close()



