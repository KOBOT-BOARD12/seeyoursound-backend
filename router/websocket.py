import wave
import json
import base64
import configparser as parser
from fastapi import APIRouter, WebSocket, WebSocketDisconnect, HTTPException, UploadFile, File, Body

properties = parser.ConfigParser()
properties.read("config.ini")

ws_router = APIRouter()
model_predictions_router = APIRouter()

connected_websocket = None
def bytes_to_wav(bytes_data, file_name):
    wav_detail = properties["WAV_DETAIL"]
    with wave.open("data/" + file_name, 'wb') as wf:
        wf.setnchannels(int(wav_detail["num_channels"]))
        wf.setsampwidth(int(wav_detail["sample_width"]))
        wf.setframerate(int(wav_detail["sample_rate"]))
        wf.writeframes(bytes_data)
    wf.close()

@ws_router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    chunk_count = int(properties["AUDIO_DATA"]["chunk_count"])  
    top_channel_arr = []
    bottom_channel_arr = []
    await websocket.accept()
    global connected_websocket
    connected_websocket = websocket
    print("WebSocket connected.")
    try:
        while True:
            data = await websocket.receive_text()
            json_data = json.loads(data)

            top_channel, bottom_channel = json_data["top_channel"], json_data["bottom_channel"]
            top_channel_data, bottom_channel_data = bytes(base64.b64decode(top_channel.encode('utf-8'))), bytes(base64.b64decode(bottom_channel.encode('utf-8')))
            if len(top_channel_data) == 0 or len(bottom_channel_data) == 0:
                continue
            top_channel_arr.append(top_channel_data)
            bottom_channel_arr.append(bottom_channel_data)
            if len(top_channel_arr) == chunk_count and len(bottom_channel_arr) == chunk_count:
                bytes_to_wav(bytes(bytearray(b''.join(top_channel_arr))), "top_channel.wav")
                bytes_to_wav(bytes(bytearray(b''.join(bottom_channel_arr))), "bottom_channel.wav")
                top_channel_arr.pop(0)
                bottom_channel_arr.pop(0)

            gy_x, gy_y, gy_z = json_data["gy_x"], json_data["gy_y"], json_data["gy_z"]
            ma_x, ma_y, ma_z = json_data["ma_x"], json_data["ma_y"], json_data["ma_z"]

    except WebSocketDisconnect:
        print("WebSocket closed.")
        connected_websocket = None

@model_predictions_router.post("/model_predictions")
async def model_predictions(model_result: dict = Body(None)):
    prediction = await model_result.read()
    if connected_websocket:
        await connected_websocket.send_text(prediction) 
    else:
        raise HTTPException(status_code=400, detail="연결된 웹소켓이 존재하지 않습니다.")