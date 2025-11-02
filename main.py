from typing import Dict, Set
import logging

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from starlette.websockets import WebSocketState

logging.basicConfig(level=logging.INFO, format="[%(asctime)s] %(levelname)s: %(message)s")
logger = logging.getLogger("websocket_server")

app = FastAPI()

rooms: Dict[str, Set[WebSocket]] = {}


async def broadcast(room_id: str, message: str) -> None:
    connections = rooms.get(room_id)
    if not connections:
        return

    disconnected: Set[WebSocket] = set()
    for connection in list(connections):
        if connection.application_state != WebSocketState.CONNECTED:
            disconnected.add(connection)
            continue
        try:
            await connection.send_text(message)
        except Exception as exc:  # Connection issues should not bring down the room
            logger.warning("Failed to send message to client in room %s: %s", room_id, exc)
            disconnected.add(connection)

    if disconnected:
        for connection in disconnected:
            connections.discard(connection)
        if not connections:
            rooms.pop(room_id, None)
            logger.info("Room %s removed after all clients disconnected during broadcast.", room_id)


async def close_room(room_id: str) -> None:
    connections = rooms.get(room_id)
    if not connections:
        return

    logger.info("Closing room %s with %d client(s).", room_id, len(connections))
    for connection in list(connections):
        try:
            await connection.close(code=1000)
        except Exception as exc:
            logger.warning("Error closing connection in room %s: %s", room_id, exc)
        finally:
            connections.discard(connection)

    rooms.pop(room_id, None)
    logger.info("Room %s closed and removed.", room_id)


@app.websocket("/ws/{room_id}")
async def websocket_endpoint(websocket: WebSocket, room_id: str) -> None:
    await websocket.accept()

    room_connections = rooms.setdefault(room_id, set())
    room_connections.add(websocket)
    logger.info("Client connected to room %s. Total clients: %d", room_id, len(room_connections))

    try:
        while True:
            message = await websocket.receive_text()
            logger.info("Received message in room %s: %s", room_id, message)

            if message == "Done":
                logger.info("Conversation ended by a participant in room %s.", room_id)
                await broadcast(room_id, "Conversa encerrada por um dos participantes.")
                await close_room(room_id)
                break

            await broadcast(room_id, message)
    except WebSocketDisconnect:
        logger.info("Client disconnected from room %s.", room_id)
    finally:
        connections = rooms.get(room_id)
        if connections and websocket in connections:
            connections.discard(websocket)
            logger.info("Client removed from room %s. Remaining clients: %d", room_id, len(connections))
            if not connections:
                rooms.pop(room_id, None)
                logger.info("Room %s removed after last client left.", room_id)

# Run with: uvicorn main:app --reload
