#!/usr/bin/env python
from fastapi import FastAPI #, WebSocket
from loguru import logger
from fastapi.responses import Response
import socket
import json


app = FastAPI()


# const
IP = "127.0.0.1"
PORT = 8000
HDRS = 'HTTP/1.1 200 OK\r\nContent-Type: text/html; charset=utf-8\r\n\r\n'
HDRS_404 = 'HTTP/1.1 404 OK\r\nContent-Type: text/html; charset=utf-8\r\n\r\n'


def start_server():    
    """ 
    Run socket server on http://IP:PORT 
    if enter "ctrl + C" in terninal -> KeyboardInterrupt and Disconnect
    """
    # try:
    logger.info("start server")
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)                  # TCP; SOCK_STREAM: int; 
    server.bind((IP, PORT))                                                     # tuple
    server.listen(5)
    while True:
        logger.info("Start working...")
        client_socket, address = server.accept()                                # if connection Receive data from the socket.
        data = client_socket.recv(1024).decode('utf-8')
        content = reload_page_get_query(data)
        # return response
        client_socket.send(content)
        # exit
        client_socket.shutdown(socket.SHUT_WR)
    # except KeyboardInterrupt:
    #     server.close()
    #     print("Server was disconnected, KeyboardInterrupt")


@app.get("/")                                                                   # main page                                                               
def reload_page_get_query(request_data):
    ''' reload web page GET-query '''
    logger.info(f"{request_data=}")
    response = ''
    try:
        with open('app/index.html', 'rb') as file:
            logger.debug("читаем файл")
            response = file.read()
            # здесь должна быть отправка данных из формы POST-method
        return HDRS.encode('utf-8') + response
    except FileNotFoundError:
        logger.error("Exception файл не найден")
        return HDRS_404.encode('utf-8') + "\nPage Not Found"


@app.post("/")                                                                  # main page
def send_message_from_form(data):
    return Response(data)


# @app.websocket("/ws")
# async def websocket_endpoint(websocket: WebSocket):
#     await websocket.accept()
#     while True:
#         data = await websocket.receive_text()
#         await websocket.send_text(f"{data}")



# run server and autorun server
if __name__ == '__main__':
    try:
        while not start_server():
            logger.debug(f"start new connection to server on {IP}:{PORT}")
            start_server()
    except KeyboardInterrupt:
        print("Server was disconnected, KeyboardInterrupt")