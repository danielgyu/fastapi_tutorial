from fastapi.responses import HTMLResponse
from fastapi import (Cookie, Depends, FastAPI, Query, WebSocket,
WebSocketDisconnect, status)

from static.chat_html import html, advanced_html, broadcast_html
from connection_manager import ConnectionManager
from typing import Optional

manager = ConnectionManager()

app = FastAPI()

async def get_cookie_or_token(
        websocket: WebSocket,
        session: Optional[str] = Cookie(None),
        token: Optional[str] = Query(None),
        ):
    if session is None and token is None:
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
    return session or token

@app.get('/')
async def chat():
    return HTMLResponse(html)

@app.get('/adv')
async def advanced():
    return HTMLResponse(advanced_html)

@app.get('/broadcast')
async def broadcast():
    return HTMLResponse(broadcast_html)

@app.websocket('/ws')
async def ws(websocket: WebSocket):
    await manager.connect(websocket)
    while True:
        data = await manager.receive_personal_message()
        await manager.send_personal_message(f'sent: {data}')

@app.websocket('/items/{item_id}/ws')
async def ws_item(
        websocket: WebSocket,
        item_id: str,
        q: Optional[str] = None,
        cookie_or_token: str = Depends(get_cookie_or_token)
        ):
    await websocket.accept()
    while True:
        data = await websocket.receive_text()
        await websocket.send_text(
                f'Value for cookie or token is : {cookie_or_token}'
                )
        if q is not None:
            await websocket.send_text(f'Query param q is : {q}')
        await websocket.send_text(f'Message text was: {data}, item: {item_id}')

@app.websocket('/ws/{client_id}')
async def ws_add_broadcast(
        websocket: WebSocket,
        client_id: int
        ):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            await manager.send_personal_message(f'send: {data}', websocket)
            await manager.broadcast(f'{client_id} says: {data}')
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        await manager.broadcast(f'{client_id} has left')
