import asyncio, websockets

async def main():
    async with websockets.connect("ws://localhost:8000") as websocket:
        while True:

            message = input("Enter message: ")

            await websocket.send(message)

            response = await websocket.recv()

            print(response)

if __name__ == "__main__":
    asyncio.run(main())