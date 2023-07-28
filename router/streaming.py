from fastapi import APIRouter, WebSocket, WebSocketDisconnect

ws_router = APIRouter()

@ws_router.websocket("/audio_ws")
async def audio_websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        print("Audio WebSocket connected.")
        while True:
            data = await websocket.receive_text()
            # TODO: data processing
            pass

    except WebSocketDisconnect:
        print("Audio WebSocket disconnected.")
        pass

@ws_router.websocket("/gyro_ws")
async def gyro_websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        print("Gyro WebSocket connected.")
        while True:
            data = await websocket.receive_text()
            # TODO: data processing
            pass

    except WebSocketDisconnect:
        print("Gyro WebSocket disconnected.")
        pass
