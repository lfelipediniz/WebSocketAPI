# 🛰️ WebSocketAPI

Simple WebSocket server with support for multiple rooms and message broadcasting between clients. Built using `FastAPI` and easily testable via `npx wscat` without needing global installation.



## 📦 Requirements

- Python 3.8+
- `uvicorn` as ASGI server
- `FastAPI` framework
- Virtual environment (recommended)
- Node.js (to use `npx wscat` for testing)



## 🚀 Setup and Execution

### 1. Create and activate a virtual environment

```bash
python3 -m venv venv
source venv/bin/activate  # Linux/macOS
# or
venv\Scripts\activate     # Windows
````

### 2. Install the required dependencies

```bash
pip install fastapi uvicorn
```

### 3. Run the server

```bash
uvicorn main:app --reload
```

> Make sure your file is named `main.py`, or update the command accordingly.



## 🧪 Test with `npx wscat`

Open **two terminals** and run:

### 1. Connect to the WebSocket

```bash
npx wscat -c ws://127.0.0.1:8000/ws/test-room
```

Repeat the command in another terminal to simulate a second client.

### 2. Send messages

* Type a message in one terminal and it will show up in the other.
* To close the room, type `Done` in either terminal.



## 📌 Expected Behavior

* When a client sends `Done`, the room is closed and all connections are terminated.
* When a client disconnects, it is removed from the room.
* If it was the last client, the room is automatically deleted.



## 🛠️ Logging

While running, the server will output logs such as:

```
[2025-11-02 02:30:00] INFO: Client connected to room test-room. Total clients: 2
[2025-11-02 02:30:10] INFO: Received message in room test-room: Hello!
[2025-11-02 02:30:20] INFO: Conversation ended by a participant in room test-room.
[2025-11-02 02:30:21] INFO: Room test-room closed and removed.
```



## 🧹 Tips

* To restart the server quickly, press `CTRL+C` and run the `uvicorn` command again.
* To use a different room name, just change the WebSocket URL:

  ```
  ws://127.0.0.1:8000/ws/another-room
  ```



## ✅ Quick Checklist

* [x] WebSocket server working with FastAPI
* [x] Testable using `npx wscat` (zero install)
* [x] Supports multiple clients and rooms
* [x] Auto room cleanup on disconnect



