from fastapi import FastAPI, WebSocket
from zaptools.tools import EventRegister, EventContext
from zaptools.connectors import FastApiConnector

app:FastAPI = FastAPI()
reg: EventRegister = EventRegister()

@reg.on_event("connected")
async def connected_trigger(ctx: EventContext):
    await ctx.connection.send("connected", "LIVE", {"myHeader": "I'm a header"})

@reg.on_event("disconnected")
async def disconnected_trigger(ctx:EventContext):
    print(f"connection left -> {ctx.connection.id}")

@reg.on_event("header")
async def headers( ctx:EventContext):
    test_header = ctx.headers["clientHeader"]
    await ctx.connection.send(
        "headerTest", "headerTest", {"isOk" : test_header=="client"}
)

@reg.on_event("event1")
async def event1_triger(ctx: EventContext):
    await ctx.connection.send("event1_completed", "HELLO FROM SERVER")

@reg.on_event("event2")
async def event2_triger(ctx: EventContext):
    await ctx.connection.send("event2_completed", "HELLO FROM SERVER 2")

@reg.on_event("exit")
async def exit_event( ctx: EventContext ):
    await ctx.connection.close()

@reg.on_event("hb")
async def hello_and_bye(ctx:EventContext):
    conn = ctx.connection
    await conn.send("h", "h event")
    await conn.close()

@app.websocket("/")
async def websocket_endpoint(ws: WebSocket):
    await FastApiConnector.plug_and_start(reg,ws)