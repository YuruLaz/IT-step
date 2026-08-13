import websockets, asyncio

clients = {}  # shecvlili

async def broadcast(message):
    for client in clients:  # shecvlili
        await client.send(message)

async def handler(websocket):
    username = await websocket.recv()  # damatebuli
    clients[websocket] = username  # shecvlili

    await broadcast(f"** {username} შემოუერთდა ჩატს **")  # damatebuli

    try:
        async for message in websocket:
            print(f"{username}: {message}")  # shecvlili

            await broadcast(f"{username}: {message}")  # shecvlili

    finally:
        del clients[websocket]  # shecvlili
        await broadcast(f"** {username} გავიდა ჩატიდან **")  # damatebuli

async def main():
    async with websockets.serve(handler, "localhost", 8000):
        print("Server started...")
        await asyncio.Future()

if __name__ == "__main__":
    asyncio.run(main())