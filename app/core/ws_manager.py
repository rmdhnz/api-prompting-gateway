from asyncio import get_event_loop

class ConnectionManager:
    def __init__(self):
        self.active_connections = {}

    async def connect(self, baus_user_id, websocket):
        await websocket.accept()
        self.active_connections.setdefault(baus_user_id, []).append(websocket)

    def disconnect(self, baus_user_id, websocket):
        self.active_connections.get(baus_user_id, []).remove(websocket)

    async def send_to_user(self, baus_user_id, payload):
        for ws in self.active_connections.get(baus_user_id, []):
            await ws.send_json(payload)

    def send_safe(self, baus_user_id, payload):
        loop = get_event_loop()
        loop.create_task(self.send_to_user(baus_user_id, payload))

manager = ConnectionManager()
