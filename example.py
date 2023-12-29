from pythonosc.osc_server import AsyncIOOSCUDPServer
from pythonosc.udp_client import SimpleUDPClient
from pythonosc.dispatcher import Dispatcher
import asyncio
import math

import random
"""
pip install python-osc
"""

TRACKER_X = "/tracker_1:vals:pos_x"
TRACKER_Y = "/tracker_1:vals:pos_y"

values = {
    TRACKER_X: 1.0,
    TRACKER_Y: 1.0,
}



def sendHeart():

    heartPositions = [
            (0.0, 5.0),
            (0.55, 7.01),
            (3.71, 10.71),
            (9.39, 11.77),
            (14.58, 8.4),
            (15.84, 2.42),
            (12.29, -3.64),
            (6.37, -8.98),
            (1.73, -13.6),
            (0.07, -16.58),
            (-0.07, -16.58),
            (-1.73, -13.6),
            (-6.37, -8.98),
            (-12.29, -3.64),
            (-15.84, 2.42),
            (-14.58, 8.4),
            (-9.39, 11.77),
            (-3.71, 10.71),
            (-0.55, 7.01),
            (-0.0, 5.0),
    ]

    MAX_RANGE = 21
    for i in range(0, MAX_RANGE):

        DELTA = 1
        variation = random.randint(-DELTA, DELTA)/100

        new_intensity = light_parameters["intensity"] + \
            (light_parameters["intensity"] * variation)
        new_color = light_parameters["color"] + \
            (light_parameters["color"] * variation)
        new_frost = light_parameters["frost"] + \
            (light_parameters["frost"] * variation)

        position_x = TRACKER_X + str((heartPositions[i-1][0]) * 0.2)
        position_y = TRACKER_Y + str((heartPositions[i-1][1]) * 0.2)
        # print(f"Debugging X: {position_x}")
        # print(f"Debugging Y: {position_y}")

        client.send_message(f"/light{i}/xpos", position_x)
        client.send_message(f"/light{i}/ypos", position_y)
        client.send_message(f"/light{i}/intensity", new_intensity)
        client.send_message(f"/light{i}/color", new_color)
        client.send_message(f"/light{i}/frost", new_frost)
        client.send_message(f"/light{i}/height", 0.0)

        light_parameters["intensity"] = new_intensity
        light_parameters["color"] = new_color
        light_parameters["frost"] = new_frost




def update_handler(address, *args):
    values[str(address)] = args[0]


dispatcher = Dispatcher()
# dispatcher.map("*", update_handler)
dispatcher.set_default_handler(update_handler)

client = SimpleUDPClient("192.168.0.232", 22223)

ip = "0.0.0.0"
port = 10000


light_parameters = {
    "intensity": 1.0,
    "color": 0.5,
    "frost": 1,
}


def send():
    MAX_RANGE = 21
    for i in range(1, MAX_RANGE):

        DELTA = 1
        variation = random.randint(-DELTA, DELTA)/100

        new_intensity = light_parameters["intensity"] + \
            (light_parameters["intensity"] * variation)
        new_color = light_parameters["color"] + \
            (light_parameters["color"] * variation)
        new_frost = light_parameters["frost"] + \
            (light_parameters["frost"] * variation)

        angle = 360/MAX_RANGE * i
        position_x = values[TRACKER_X] + math.cos(angle) * 2
        position_y = values[TRACKER_Y] + math.sin(angle) * 2
        print(f"Debugging X: {position_x}")
        print(f"Debugging Y: {position_y}")

        client.send_message(f"/light{i}/xpos", position_x)
        client.send_message(f"/light{i}/ypos", position_y)
        client.send_message(f"/light{i}/intensity", new_intensity)
        client.send_message(f"/light{i}/color", new_color)
        client.send_message(f"/light{i}/frost", new_frost)
        client.send_message(f"/light{i}/height", 0.0)

        light_parameters["intensity"] = new_intensity
        light_parameters["color"] = new_color
        light_parameters["frost"] = new_frost


async def loop():
    while True:
        print(f"X: {values[TRACKER_X]}\tY: {values[TRACKER_Y]}")
        sendHeart()
        await asyncio.sleep(0.1)


async def init_main():
    # noinspection PyTypeChecker
    server = AsyncIOOSCUDPServer(
        (ip, port), dispatcher, asyncio.get_event_loop())
    # Create datagram endpoint and start serving
    transport, protocol = await server.create_serve_endpoint()

    await loop()  # Enter main loop of program

    transport.close()  # Clean up serve endpoint


if __name__ == '__main__':
    asyncio.run(init_main())
