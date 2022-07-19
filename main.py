#!/usr/bin/env python
from fastapi import FastAPI, Form #, WebSocket
from loguru import logger
from fastapi.responses import Response
import socket
import json
import asyncio


app = FastAPI()


# constants
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
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)                  # TCP; SOCK_STREAM: int; 
    server_socket.bind((IP, PORT))                                                     # tuple
    server_socket.listen(5)
    while True:
        client_socket, address = server_socket.accept() 
        logger.info("new connect, receive data from the socket")
        request_data = client_socket.recv(1024).decode('utf-8')
        
        
        if request_data.split()[0] == "POST": 
            logger.info(f"{request_data.split()[0]=}")
            content = send_message_from_form(request_data)
        else:                                                                           # request_data.split()[0] == "GET":
            logger.info(f"{request_data.split()[0]=}")
            content = reload_page_get_query(request_data)
        # send message
        client_socket.send(content)
        # exit
        client_socket.close()
    # except KeyboardInterrupt:
    #     server_socket.close()
    #     print("Server was disconnected, KeyboardInterrupt")


@app.get("/")                                                                           # get <- main page                                                               
def reload_page_get_query(data):
    ''' reload web page GET-query '''
    response = ''
    try:
        with open('app/index.html', 'rb') as file:
            logger.debug("читаем файл")
            response = file.read()
        return HDRS.encode('utf-8') + response
    except FileNotFoundError:
        logger.error("Exception файл не найден")
        return HDRS_404.encode('utf-8') + "\nPage Not Found"


@app.post("/")                                                                  # post -> main page
def send_message_from_form(message: str = Form(...)):
    '''возвращаем данные сообщения из формы POST-методом'''
    return f"{message}".encode('utf-8')


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
            logger.debug(f"start new connection FROM MAIN to server on {IP}:{PORT}")
            start_server()
    except KeyboardInterrupt:
        print("Server was disconnected, KeyboardInterrupt")