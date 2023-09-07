import json
import configparser as parser
from fastapi import APIRouter, WebSocket, WebSocketDisconnect, HTTPException
import requests
from os.path import os, join, dirname

from dotenv import load_dotenv, find_dotenv

dotenv_path = join(dirname(__file__), ".env")
load_dotenv(find_dotenv())

properties = parser.ConfigParser()
properties.read("config.ini")

ws_router = APIRouter()

connected_websockets = []


@ws_router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    chunk_count = int(properties["AUDIO_DATA"]["chunk_count"])
    top_channel_arr = []
    bottom_channel_arr = []
    await websocket.accept()
    global connected_websocket
    websocket_idx = len(connected_websockets)
    connected_websockets.append(websocket)
    print("WebSocket connected.")
    try:
        while True:
            data = await websocket.receive_text()
            json_data = json.loads(data)

            top_channel, bottom_channel, uid = (
                json_data["top_channel"],
                json_data["bottom_channel"],
                json_data["uid"],
            )
            filtered_class = [
                json_data["class_0"],
                json_data["class_1"],
                json_data["class_2"],
                json_data["class_3"],
                True,
                True,
            ]
            if len(top_channel) == 0 or len(bottom_channel) == 0:
                continue
            top_channel_arr.append(top_channel)
            bottom_channel_arr.append(bottom_channel)

            if (
                len(top_channel_arr) == chunk_count
                and len(bottom_channel_arr) == chunk_count
            ):
                data = {
                    "top_channel": "".join(top_channel_arr),
                    "bottom_channel": "".join(bottom_channel_arr),
                    "uid": uid,
                    "filtered_class": filtered_class,
                    "websocket_idx": websocket_idx,
                }
                requests.post(
                    os.getenv("MODEL_SERVER_URL") + "/prediction",
                    json=data,
                    headers={
                        "accept": "application/json",
                        "Content-Type": "application/json",
                    },
                )
                top_channel_arr.pop(0)
                bottom_channel_arr.pop(0)

    except WebSocketDisconnect:
        print("WebSocket closed.")
        connected_websocket = None


@ws_router.post("/get_model_prediction")
async def get_model_prediction(model_result: dict):
    websocket = connected_websockets[model_result["websocket_idx"]]
    if websocket:
        await websocket.send_text(json.dumps(model_result))
    else:
        raise HTTPException(status_code=400, detail="연결된 웹소켓이 존재하지 않습니다.")
