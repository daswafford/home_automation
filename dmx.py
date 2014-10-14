#!/usr/bin/python
""" DMX Lighting Control based on the Open Lighting Project
    (http://www.openlighting.org/ola/developer-documentation/python-api/)

    Initial credit for the proof-of-concept that this is based on goes
    to nomis52@gmail.com (Simon Newton) from ola/python/examples/ola_send_dmx.py.

    Build Notes:
        < build / install OLA server w/ python extensions >
            ./configure --enable-python-libs --with-protoc=/home/dswafford/ola/protoc
	git clone https://github.com/google/protobuf.git protoc
            < build / install protoc for both C++ and Python >
        wget https://protobuf-socket-rpc.googlecode.com/files/protobuf.socketrpc-1.3.2.tar.gz
            < build / install protobuf socket rpc extension >
        generate proto buffs for OLA
            protoc common/rpc/Rpc.proto --python_out=/home/dswafford/
            protoc ./protocol/Ola.proto --python_out=/home/dswafford/
"""

import array
from ola import ClientWrapper
import sys
import time

UNIVERSE = 0


def color_map(color):
    rgb_vals = {
        'off':  [0, 0, 0],
        'blue':  [0, 0, 40],
        'teal':  [0, 40, 30],
        'purple': [50, 0, 50],
        'orange': [90, 20, 0],
        'white': [30, 30, 30],
    }
    if color not in rgb_vals:
	color = 'off'
    return rgb_vals[color]


def scene(color, dimmer=1):
    rgb = color_map(color)
    dimmed_rgb = []
    for color in rgb:
        dimmed_value = int(color * dimmer)
        if dimmed_value <= 255:
            dimmed_rgb.append(dimmed_value)
    return dimmed_rgb


def expand_light_count(dimmed_rgb, count):
    dmx_channels = []
    for light in range(count):
        dmx_channels.extend(dimmed_rgb)
    return dmx_channels


def compile_dmx_data(dmx_channels):
    fade_in_steps = []
    fade_steps = 10
    for fade_step in range(fade_steps):
        # Build an array of all DMX channels-to-values to send
        # for example, if you use 6 channels, then send something for all
        # six, even if you only intend to change the lights running on 4-6.
        # (You would need to re-send the existing values for 1-3 to avoid
        # changing that fixture).
        data = array.array('B')
        for channel_value in dmx_channels:
            # Fade is buggy right now.  My math is probably off here.
            if channel_value == 0:
                data.append(channel_value)
	    else:
		dimmed_value = channel_value / (fade_steps - fade_step)
                data.append(dimmed_value)
    	fade_in_steps.append(data)
    return fade_in_steps


def send_dmx(dmx_data):
    def _callback(state):
       wrapper.Stop()
    wrapper = ClientWrapper.ClientWrapper()
    client = wrapper.Client()
    client.SendDmx(UNIVERSE, dmx_data, _callback)
    wrapper.Run()


def main():
    if len(sys.argv) != 2:
        raise SystemExit('scene?')
    else:
        color = sys.argv[1].lower()

    dimmed_rgb = scene(color, dimmer=1.0)

    dmx_channels = expand_light_count(dimmed_rgb, count=2)

    fade_in_steps = compile_dmx_data(dmx_channels)

    previous_fade_set = []
    for fade_set in fade_in_steps:
        if fade_set == previous_fade_set:
            continue
	#print(fade_set)
	send_dmx(fade_set)
	time.sleep(0.02)
        previous_fade_set = fade_set 


if __name__ == '__main__':
    main()
