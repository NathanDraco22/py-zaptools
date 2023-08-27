from fastapi import WebSocket

from .wrappers import FastApiWSWrapper
from .models import EventCaller, EventFactory, Context
from .tools import ZaptoolHelper

class FastApiConnector:

    @classmethod
    def start(cls,app, register, path:str= "/" ):
        @app.websocket(path)
        async def endpoint(ws: WebSocket):
            await ws.accept()
            data = await ws.receive_json()
            identifier = ZaptoolHelper.process_init_connection(data)
            client_fast = FastApiWSWrapper(ws, identifier.connection_id)
            event_caller = EventCaller()
            event_caller.add_register(register)
            ctx = Context(identifier.event, client_fast)
            await event_caller.trigger_on_connected(ctx)
            try: 
                while True:
                    data = await ws.receive_json()
                    event = EventFactory.from_dict(data)
                    ctx = Context(event= event, client= client_fast)
                    await event_caller.trigger_event(ctx)
            except Exception as e:
                print(e)
                await event_caller.trigger_on_disconnected(client_fast)