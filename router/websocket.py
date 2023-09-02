import json
import configparser as parser
from fastapi import APIRouter, WebSocket, WebSocketDisconnect, HTTPException
import requests
from os.path import os, join, dirname

from dotenv import load_dotenv, find_dotenv

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(find_dotenv())

properties = parser.ConfigParser()
properties.read("config.ini")

ws_router = APIRouter()

@ws_router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    chunk_count = int(properties["AUDIO_DATA"]["chunk_count"])  
    top_channel_arr = []
    bottom_channel_arr = []
    await websocket.accept()
    print("WebSocket connected.")
    try:
        while True:
            data = await websocket.receive_text()
            json_data = json.loads(data)

            top_channel, bottom_channel, uid = json_data["top_channel"], json_data["bottom_channel"], json_data["uid"]
            filtered_class = [json_data["class_0"], json_data["class_1"], json_data["class_2"], json_data["class_3"], True]
            if len(top_channel) == 0 or len(bottom_channel) == 0:
                continue
            top_channel_arr.append(top_channel)
            bottom_channel_arr.append(bottom_channel)

            if len(top_channel_arr) == chunk_count and len(bottom_channel_arr) == chunk_count:
                data = {"top_channel" : ''.join(top_channel_arr), "bottom_channel" : ''.join(bottom_channel_arr), "uid" : uid, "filtered_class": filtered_class, "websocket": websocket}
                requests.post(os.getenv("MODEL_SERVER_URL") + "/prediction", json=data, headers={'accept': 'application/json','Content-Type': 'application/json'})
                top_channel_arr.pop(0)
                bottom_channel_arr.pop(0)

    except WebSocketDisconnect:
        print("WebSocket closed.")

@ws_router.post("/get_model_prediction")
async def get_model_prediction(model_result: dict):
    if connected_websocket:
        await connected_websocket.send_text(json.dumps(model_result)) 
    else:
        raise HTTPException(status_code=400, detail="연결된 웹소켓이 존재하지 않습니다.")