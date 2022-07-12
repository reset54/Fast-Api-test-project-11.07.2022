#!/usr/bin/env python
from fastapi import FastAPI, WebSocket
from fastapi.responses import HTMLResponse # ,Response
# import json

app = FastAPI()

@app.get("/")               # reload webpage
async def get():
    with open('app/index.html', 'r') as file:
        html = file.read()
    return HTMLResponse(html)


@app.websocket("/ws")      
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        data = await websocket.receive_text()
        await websocket.send_text(f"{data}")