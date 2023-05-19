import argparse
import asyncio
import json

import serial
from websockets.server import serve

ser = serial.Serial("/dev/cu.usbmodem101", 9600)
async def handler(websocket):
    async for message in websocket:
        blah = json.loads(message)
        print(blah)
        ser.write(bytes(blah["message"], 'utf-8'))

    asyncio.create_task(read_serial(websocket))

async def main(args):
    async with serve(handler, "localhost", args.port):
        await asyncio.Future()

async def read_serial(websocket):
    print("Entering loop")
    while True:
        line = ser.readline()
        print("There is a message")
        await websocket.send(line)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--port", default=4242)
    args = parser.parse_args()
    asyncio.run(main(args))
