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

import argparse
import array
from ola import ClientWrapper
import sys


UNIVERSE = 0

def cli_options():
    parser = argparse.ArgumentParser()
    parser.add_argument('--rgb')
    options = parser.parse_args()
    if options.rgb:
        temp = options.rgb.split(',')
        options.rgb = []
        for rgb_val in temp:
            options.rgb.append(int(rgb_val))
    return options


def scene(rgb, dimmer=1, light_count=2): 
    dimmed_rgb = []
    for color in rgb:
        dimmed_rgb.append(int(color * dimmer))

    dmx_channels = []
    for light in range(light_count):
        dmx_channels.extend(dimmed_rgb)
    return dmx_channels


def compile_dmx_data(dmx_channels):
    fade_in = []
    fade_steps= 5
    for fade_step in range(fade_steps):
        if fade_step == 0:
            continue

        # Build an array of all DMX channels-to-values to send
        # for example, if you use 6 channels, then send something for all
        # six, even if you only intend to change the lights running on 4-6.
        # (You would need to re-send the existing values for 1-3 to avoid
        # changing that fixture).
        data = array.array('B')
        for channel_value in dmx_channels:
            # Fade is buggy right now.  My math is probably off here.
            channel_value = channel_value #* float(1 / (fade_steps - fade_step))
            data.append(int(channel_value))
        fade_in.append(data)
    return fade_in


def send_dmx(dmx_data):
    def _callback(state):
       wrapper.Stop()

    wrapper = ClientWrapper.ClientWrapper()
    client = wrapper.Client()
    client.SendDmx(UNIVERSE, dmx_data, _callback)
    wrapper.Run()


def main():
#    options = cli_options()
#    Options of ArgV... to pick

    if len(sys.argv) > 1:
	if sys.argv[1].lower() == 'off':
            dmx_channels = scene([0, 0, 0])
        else:  # dimmer value specified
	    dimmer = float(sys.argv[1])
	    dmx_channels = scene([0, 40, 30], dimmer)
    else:
        dmx_channels = scene(rgb=[0, 40, 30])

    dmx_data = compile_dmx_data(dmx_channels)
    for fade_set in dmx_data:
        print(fade_set)
    	send_dmx(fade_set)


if __name__ == '__main__':
    main()
