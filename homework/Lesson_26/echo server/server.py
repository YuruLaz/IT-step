import websockets
import asyncio

async def echo(websocket):
    print("Client connected")

    async for message in websocket:
        print(f"Client: {message}")
        await websocket.send(f"Server: {message.upper()}")

async def main():
    async with websockets.serve(echo, "localhost", 8000):
        print("Server started")
        await asyncio.Future()

if __name__ == "__main__":
    asyncio.run(main())