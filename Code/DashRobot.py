"""
NOTICE:
Adapted from original source code Copyright 2016 Ilya Sukhanov
distributed under Apache 2.0 license
https://github.com/IlyaSukhanov/morseapi


and 2018 Russ Buchanan
https://github.com/havnfun/python-dash-robot
"""

from __future__ import division

from constants import HANDLES, COMMANDS, NOISES, COMMAND1_CHAR_UUID, COMMAND2_CHAR_UUID
import sys
import uuid
import os
import select
import time
from uuid import UUID
from sensors import DashSense

import asyncio
import struct
from bleak import BleakScanner
from bleak import BleakClient



import time
import logging
import binascii
import math
from collections import defaultdict
from colour import Color

def one_byte_array(value):
    """
    Convert Int to a one byte bytearray

    :param value: value 0-255
    """
    return bytearray(struct.pack(">B", value))

def two_byte_array(value):
    """
    Convert Int to a two byte bytearray

    :param value: value 0-65535
    """
    return bytearray(struct.pack(">H", value))

def color_byte_array(color_value):
    """
    convert color into a 3 byte bytearray

    :param color_value: 6-digit (e.g. #fa3b2c), 3-digit (e.g. #fbb),
    fully spelled color (e.g. white)
    """
    color = Color(color_value)
    return bytearray([
        int(round(color.get_red()*255)),
        int(round(color.get_green()*255)),
        int(round(color.get_blue()*255)),
    ])

def angle_array(angle):
    """
    Convert angle to a bytearray

    :param angle: Angle -127-127
    """
    if angle < 0:
        angle = (abs(angle) ^ 0xff) + 1
    return bytearray([angle & 0xff])

class robotDash:
    def __init__(self):

        self.address = ''
        self.device = ''
        self.is_connected = False
        # sensor
        #self.sensor_state = defaultdict(int)
        #self.state = self.sensor_state
        #self.sense = None
        # sensor


        loop = asyncio.get_event_loop()
        loop.run_until_complete(self.discover())
        time.sleep(0.5)
        loop.run_until_complete(self.connect())
        """
        if not self.is_connected :
            loop = asyncio.get_event_loop()
            loop.run_until_complete(self.discover())
            time.sleep(0.5)
            loop.run_until_complete(self.connect())
        """

        print('Returning robot:', self.device)
        print("Connecting to robot Characteristics.")


        #self.device.discover_characteristics([ROBOT_SERVICE_UUID], [COMMAND1_CHAR_UUID, COMMAND2_CHAR_UUID,  SENSOR1_CHAR_UUID, SENSOR2_CHAR_UUID, INFO_CHAR_UUID])


    #===============================================================================
    #
    #                              ROBOT CONNECTION
    #
    #===============================================================================

    async def discover(self):

        address = ''
        devices = await BleakScanner.discover()
        await asyncio.sleep(0.5)
        for d in devices:
            if 'Dash' in d.name:
                address = d.address
                print("Found Dash at: " + address +  " name " + d.name)

        if address != '':
            print('Discover:', address)
            self.device = BleakClient(address)
            self.address = address
        else:
            print('Dash not found!')


    async def connect (self):

        print('Connecting to:', self.address)
        try:
            await self.device.connect()
            await asyncio.sleep(0.5)
            print('is connected: ', self.device.is_connected)
            self.is_connected = self.device.is_connected




            #blocks random behaviors
            #initialCommand = b"\x50\x02\x01"
            #await client.write_gatt_char("8903136c-5f13-4548-a885-c58779136703", initialCommand, response=False)
            #await behavior(client)

        except Exception as e:
            print(e)


    async def CloseDisconnect (self):
        print('Disconnecting to:', self.address)
        try:
            await self.device.disconnect()
            await asyncio.sleep(0.5)
            print('is connected: ', self.device.is_connected)
            self.is_connected = self.device.is_connected

            #blocks random behaviors
            #initialCommand = b"\x50\x02\x01"
            #await client.write_gatt_char("8903136c-5f13-4548-a885-c58779136703", initialCommand, response=False)
            #await behavior(client)

        except Exception as e:
            print(e)

    def closeDash(self): # validar com erros

        endingLoop = asyncio.new_event_loop()
        endingLoop.run_until_complete(self.CloseDisconnect())
        time.sleep(0.5)

    #===============================================================================
    #
    #                              ROBOT BASIC COMMANDs
    #
    #===============================================================================

    def name(self):
        return self.device

    async def command(self, command_name, command_values, sequence = True):
        """
        (from morseapi)
        Send a command to robot

        :param command_name: command name, COMMANDS
        :param command_values: bytearray with command parameters
        """
        # message = bytearray(HANDLES["command"]) + bytearray([COMMANDS[command_name]]) + command_values
        message = bytearray([COMMANDS[command_name]]) + command_values
        # print(command_name )
        # print (message)

        logging.debug(binascii.hexlify(message))
        if self.device:

            #await self.device.start_notify(COMMAND2_CHAR_UUID, notification_handler)
            #self.device.char_write_handle(HANDLES["command"], message)
            await self.device.write_gatt_char(COMMAND1_CHAR_UUID, message, response = False)
            # print ("escreveu")
            if sequence : await asyncio.sleep(0.2)  # Sleeping just to make sure the response is not missed...
            #await asyncio.sleep(0.5)
            #await client.stop_notify(COMMAND2_CHAR_UUID)

        # client.write_gatt_char
        #await client.write_gatt_char("8903136c-5f13-4548-a885-c58779136702", command, response=False)

        return


    def reset(self, mode=4):
        """
        Reset robot

        ?? not sure about this

        :param mode: Reset
        30003-879d-6186-1f49-deca0e85d9c1"),
        }30003-879d-6186-1f49-deca0e85d9c1"),
        }30003-879d-6186-1f49-deca0e85d9c1"),
        }30003-879d-6186-1f49-deca0e85d9c1"),
        }30003-879d-6186-1f49-deca0e85d9c1"),
        }30003-879d-6186-1f49-deca0e85d9c1"),
        }

        mode

        Available modes:
        1 some kind of debug/reflash mode?
        3 reboot
        4 zero out leds/head
        """
        loop = asyncio.new_event_loop()
        loop.run_until_complete(self.command("reset", bytearray([mode])))
        loop.stop()

    def eye(self, value):
        """
        Turn on and off the Iris LEDs. There are 12 of them. Top one is the
        first and they are incremeted clockwise.

        Light bottom LED
        >>> bot.eye(1<<6)

        Light alternate LEDs
        >>> bot.eye(0b1010101010101)

        light all LEDs
        >>> bot.eye(8191)

        :param value: bitmask to which light to light up 0-8191
        """
        loop = asyncio.new_event_loop()
        loop.run_until_complete(self.command("eye", two_byte_array(value), False)) # not sequence
        loop.stop()

    def eye_brightness(self, value):
        """
        Set brightness of the eye backlight.

        :param value: Brightness value 0-255
        """
        loop = asyncio.new_event_loop()
        loop.run_until_complete(self.command("eye_brightness", one_byte_array(value)))
        loop.stop()

    def neck_color(self, color):
        """
        Set color Neck light on Dash, and Eye backlight on Dot.

        :param color: 6-digit (e.g. #fa3b2c), 3-digit (e.g. #fbb),
        fully spelled color (e.g. white)
        """
        loop = asyncio.new_event_loop()
        loop.run_until_complete(self.command("neck_color", color_byte_array(color)))
        loop.stop()

    def left_ear_color(self, color):
        """
        Set color of left ear.

        :param color: 6-digit (e.g. #fa3b2c), 3-digit (e.g. #fbb),
        fully spelled color (e.g. white)
        """
        loop = asyncio.new_event_loop()
        loop.run_until_complete(self.command("left_ear_color", color_byte_array(color)))
        loop.stop()

    def right_ear_color(self, color):
        """
        Set color of right ear.

        :param color: 6-digit (e.g. #fa3b2c), 3-digit (e.g. #fbb),
        fully spelled color (e.g. white)
        """
        loop = asyncio.new_event_loop()
        loop.run_until_complete(self.command("right_ear_color", color_byte_array(color)))
        loop.stop()

    def ear_color(self, color):
        """
        Set color of both ears.

        :param color: 6-digit (e.g. #fa3b2c), 3-digit (e.g. #fbb),
        fully spelled color (e.g. white)
        """
        self.left_ear_color(color)

        self.right_ear_color(color)

    def head_color(self, color):
        """
        Set color of top LED.

        :param color: 6-digit (e.g. #fa3b2c), 3-digit (e.g. #fbb),
        fully spelled color (e.g. white)
        """
        loop = asyncio.new_event_loop()
        loop.run_until_complete(self.command("head_color", color_byte_array(color)))
        loop.stop()

    def all_color(self, color):
        """
        Set color Neck light on Dash, and Eye backlight on Dot.

        :param color: 6-digit (e.g. #fa3b2c), 3-digit (e.g. #fbb),
        fully spelled color (e.g. white)
        """
        loop = asyncio.new_event_loop()
        loop.run_until_complete(self.command("neck_color", color_byte_array(color), False))
        loop.run_until_complete(self.command("left_ear_color", color_byte_array(color), False))
        loop.run_until_complete(self.command("head_color", color_byte_array("black"), False))
        loop.run_until_complete(self.command("right_ear_color", color_byte_array(color), True))
        loop.stop()

    def say(self, sound_name):
        """
        Play a sound from sound bank file

        :param sound_name: Name of sound to play

        List available noies
        # >>> from morseapi import NOISES
        # >>> NOISES.keys()
        """
        loop = asyncio.new_event_loop()
        loop.run_until_complete(self.command("say", bytearray(NOISES[sound_name])))
        loop.stop()

    # All the subsequent commands are Dash specific

    def tail_brightness(self, value):
        """
        Set brightness of the tail backlight.

        :param value: Brightness value 0-255
        """
        loop = asyncio.new_event_loop()
        loop.run_until_complete(self.command("tail_brightness", one_byte_array(value)))
        loop.stop()


    def head_yaw(self, angle):
        """
        Turn Dash's head left or right

        :param angle: distance to turn in degrees from -53 to 53
        """
        angle = max(-53, angle)
        angle = min(53, angle)
        loop = asyncio.new_event_loop()
        loop.run_until_complete(self.command("head_yaw", angle_array(angle)))
        loop.stop()

    def head_pitch(self, angle):
        """
        Tilt Dash's head up or down.

        :param angle: distance to turn from -5 to 10
        """
        angle = max(-5, angle)
        angle = min(10, angle)
        loop = asyncio.new_event_loop()
        loop.run_until_complete(self.command("head_pitch", angle_array(angle)))
        loop.stop()

    def stop(self):
        """
        Stop moving Dash.
        """
        loop = asyncio.new_event_loop()
        loop.run_until_complete(self.command("drive", bytearray([0, 0, 0])))
        loop.stop()

    def drive(self, speed):
        """
        Start moving Dash forward or backward.

        Dash will continue moving until another drive(), spin() or stop()
        command is issued.

        :param speed: Speed at which to move, 200 is a resonable value.
        Negative speed drives Dash backwards.
        """
        speed = max(-2048, speed)
        speed = min(2048, speed)
        if speed < 0:
            speed = 0x800 + speed
        loop = asyncio.new_event_loop()
        loop.run_until_complete(
        self.command("drive", bytearray([
            speed & 0xff,
            0x00,
            (speed & 0x0f00) >> 8
        ])))
        loop.stop()

    def spin(self, speed):
        """
        Start spinning Dash left or right.

        Dash will continue spinning until another drive(), spin() or stop()
        command is issued.

        :param speed: Speed at which to spin, 200 is a reasonable value.
        Positive values spin clockwise and negative counter-clockwise.
        """
        speed = max(-2048, speed)
        speed = min(2048, speed)
        if speed < 0:
            speed = 0x800 + speed
        loop = asyncio.new_event_loop()
        loop.run_until_complete(self.command("drive", bytearray([
            0x00,
            speed & 0xff,
            (speed & 0xff00) >> 5
        ])))
        loop.stop()

    def turn(self, degrees, speed_dps=(360/2.094)):
        """
        Turn Dash specified distance.

        This is a blocking call.

        :param degrees: How many degrees to turn.
        Positive values spin clockwise and negative counter-clockwise.
        :param speed_dps: Speed to turn at, in degrees/second
        """
        if abs(degrees) > 360:
            raise NotImplementedError("Cannot turn more than one rotation per move")
        if degrees:
            seconds = abs(degrees/speed_dps)
            byte_array = self._get_move_byte_array(degrees=degrees, seconds=seconds)
            loop = asyncio.new_event_loop()
            loop.run_until_complete(self.command("move", byte_array))
            logging.debug("turn sleeping {0} @ {1}".format(seconds, time.time()))
            logging.debug(binascii.hexlify(byte_array))
            # self.sleep does not work and api says not to use time.sleep...
            time.sleep(seconds)
            logging.debug("turn finished sleeping {0} @ {1}".format(seconds, time.time()))
            loop.stop()



    def move(self, distance_mm, speed_mmps=1000, no_turn=True):
        """
        Move specified distance at a particular speed.

        This is a blocking call.

        :param distance_mm: How far to move in mm. Negative values to go backwards
        :param speed_mmps: Speed at which to move in mm/s.
        """
        speed_mmps = abs(speed_mmps)
        seconds = abs(distance_mm / speed_mmps)
        if no_turn and distance_mm < 0:
            byte_array = self._get_move_byte_array(
                distance_mm=distance_mm,
                seconds=seconds,
                eight_byte=0x81,
            )
        else:
            byte_array = self._get_move_byte_array(
                distance_mm=distance_mm,
                seconds=seconds,
            )
        loop = asyncio.new_event_loop()
        loop.run_until_complete(self.command("move", byte_array))
        logging.debug("move sleeping {0} @ {1}".format(seconds, time.time()))
        logging.debug(binascii.hexlify(byte_array))
        # self.sleep does not work and api says not to use time.sleep...
        time.sleep(seconds)
        logging.debug("move finished sleeping {0} @ {1}".format(seconds, time.time()))
        loop.stop()




    @staticmethod
    def _get_move_byte_array(distance_mm=0, degrees=0, seconds=1.0, eight_byte=0x80):
        # Sixth byte is mixed use
        # * turning
        #   * high nibble is turn distance high byte<<2
        #   * low nibble is 0
        # * driving straight
        #   * whole byte is high byte of drive distance
        # unclear if these can be combined
        # Eight byte is weird.
        # * On subsequent move commands its usually 0x40
        # * On first command its usually 0x80, but not required
        # * When driving backwards without turning around last bit is 1
        if distance_mm and degrees:
            raise NotImplementedError("Cannot turn and move concurrently")

        sixth_byte = 0
        seventh_byte = 0

        distance_low_byte = distance_mm & 0x00ff
        distance_high_byte = (distance_mm & 0x3f00) >> 8
        sixth_byte |= distance_high_byte

        centiradians = int(math.radians(degrees) * 100.0)
        turn_low_byte = centiradians & 0x00ff
        turn_high_byte = (centiradians & 0x0300) >> 2
        sixth_byte |= turn_high_byte
        if centiradians < 0:
            seventh_byte = 0xc0

        time_measure = int(seconds * 1000.0)
        time_low_byte = time_measure & 0x00ff
        time_high_byte = (time_measure & 0xff00) >> 8

        return bytearray([
            distance_low_byte,
            0x00,  # unknown
            turn_low_byte,
            time_high_byte,
            time_low_byte,
            sixth_byte,
            seventh_byte,
            eight_byte,
        ])



"""
Original code 
def get_dashub():
    adapter = pygatt.GATTToolBackend()
    address = ''

    adapter.start()
    devices = adapter.scan(run_as_root=True, timeout=3)
    for device in devices:
        if device['name'] == 'Dash':
            address = device['address']
            print('Found Dash at:', address)

    if address != '':
        print('Connecting to:', address)
        x = adapter.connect(address, address_type=pygatt.BLEAddressType.random)
        dash = robot(x)
    else:
        print('Dash not found!')
        dash = None

    return dash

"""




