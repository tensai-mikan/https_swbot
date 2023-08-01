import asyncio
from bleak import *
import json
import sys


#pressは、toggleと同じ信号らしい。
commands = {
    'press': b'\x57\x01\x00',
    'toggle': b'\x57\x01\x00',
    'on': b'\x57\x01\x01',
    'off': b'\x57\x01\x02',
    'open': b'\x57\x0F\x45\x01\x05\xFF\x00',
    'close': b'\x57\x0F\x45\x01\x05\xFF\x64',
    'pause': b'\x57\x0F\x45\x01\x00\xFF',
}


def switchBot(address, cmd):
    UUID = "cba20002-224d-11e6-9fb8-0002a5d5c51b"
    print(cmd)
    async def run(address, loop):
        async with BleakClient(address) as client:
            y = await client.read_gatt_char(UUID)
            await client.write_gatt_char(UUID, bytearray(commands[cmd]))
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run(address, loop))


if len(sys.argv) < 2:
    print("ERROR 引数が不足しています。")
    sys.exit()
    
cmd = sys.argv[1]

# JSONファイルのパス
file_path = 'device.json'

# JSONファイルを読み込む
with open(file_path, 'r') as f:
    data = json.load(f)

    
if not cmd in data:
    print(f"ERROR ${cmd} は存在しません")
    sys.exit()

device = data[cmd]

switchBot(device["macaddress"], device["command"])