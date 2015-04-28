#!/usr/bin/python
""" Samsung TV Control based on Telnet
    to a Global Cache IP-TO_IR device.

    Credit to http://board.homeseer.com/showthread.php?t=153446 for IR Codes.
"""

import argparse
import time
import telnetlib

# To enable "Hotel Mode"
# Mute + 1 8 2 + power
# Control = "hotel"

IR_PWRON = (
    'sendir,1:{ir_port},1,38000,3,1,171,168,22,61,22,61,22,61,22,20,22,20,22,20,22,20,'
    '22,20,22,61,22,61,22,61,22,20,22,20,22,20,22,20,22,20,22,61,22,20,22,20,'
    '22,61,22,61,22,20,22,20,22,61,22,20,22,61,22,61,22,20,22,20,22,61,22,61,'
    '22,20,22,760')

IR_PWROFF = (
    'sendir,1:{ir_port},1,38000,3,1,171,169,22,62,22,62,22,62,22,19,22,19,22,19,22,19,'
    '22,19,22,62,22,62,22,62,22,19,22,19,22,19,22,19,22,19,22,19,22,19,22,19,'
    '22,62,22,62,22,19,22,19,22,62,22,62,22,62,22,62,22,19,22,19,22,62,22,62,'
    '22,19,22,760')

IR_MENU = (
   'sendir,1:{ir_port},1,38000,1,1,171,170,21,64,21,64,21,64,21,21,21,21,21,21,21,21,'
   '21,21,21,64,21,64,21,64,21,21,21,21,21,21,21,21,21,21,21,21,21,64,21,21,21,'
   '64,21,64,21,21,21,21,21,21,21,64,21,21,21,64,21,21,21,21,21,64,21,64,21,64,'
   '21,760')

IR_ENTER = (
    'sendir,1:{ir_port},1,38000,1,1,171,170,21,63,21,63,21,63,21,20,21,20,21,20,21,20,'
    '21,20,21,63,21,63,21,63,21,20,21,20,21,20,21,20,21,20,21,20,21,63,21,20,'
    '21,20,21,20,21,63,21,63,21,20,21,63,21,20,21,63,21,63,21,63,21,20,21,20,'
    '21,63,21,760')

IR_DOWN = (
    'sendir,1:{ir_port},1,38000,1,1,171,170,21,63,21,63,21,63,21,21,21,21,21,21,21,21,'
    '21,21,21,63,21,63,21,63,21,21,21,21,21,21,21,21,21,21,21,63,21,21,21,21,'
    '21,21,21,21,21,63,21,63,21,21,21,21,21,63,21,63,21,63,21,63,21,21,21,21,'
    '21,63,21,760')

IR_UP = (
    'sendir,1:{ir_port},1,38000,1,1,171,170,21,63,21,63,21,63,21,21,21,21,21,21,21,21,'
    '21,21,21,63,21,63,21,63,21,21,21,21,21,21,21,21,21,21,21,21,21,21,21,21,'
    '21,21,21,21,21,63,21,63,21,21,21,63,21,63,21,63,21,63,21,63,21,21,21,21,'
    '21,63,21,760')

IR_LEFT = (
    'sendir,1:{ir_port},1,38000,1,1,171,170,21,63,21,63,21,63,21,21,21,21,21,21,21,21,'
    '21,21,21,63,21,63,21,63,21,21,21,21,21,21,21,21,21,21,21,63,21,21,21,63,'
    '21,21,21,21,21,63,21,63,21,21,21,21,21,63,21,21,21,63,21,63,21,21,21,21,'
    '21,63,21,760')

IR_RIGHT = (
    'sendir,1:{ir_port},1,38000,1,1,171,170,21,63,21,63,21,63,21,20,21,20,21,20,21,20,'
    '21,20,21,63,21,63,21,63,21,20,21,20,21,20,21,20,21,20,21,20,21,63,21,20,'
    '21,20,21,20,21,63,21,63,21,20,21,63,21,20,21,63,21,63,21,63,21,20,21,20,'
    '21,63,21,760')

IR_ENTER = (
    'sendir,1:{ir_port},1,38000,1,1,171,170,21,64,21,64,21,64,21,21,21,21,21,21,21,21,'
    '21,21,21,64,21,64,21,64,21,21,21,21,21,21,21,21,21,21,21,21,21,21,21,21,'
    '21,64,21,21,21,64,21,64,21,21,21,64,21,64,21,64,21,21,21,64,21,21,21,21,'
    '21,64,21,760')

IR_TOOLS = (
    'sendir,1:{ir_port},1,38000,1,1,171,170,21,63,21,63,21,63,21,21,21,21,21,21,21,21,'
    '21,21,21,63,21,63,21,63,21,21,21,21,21,21,21,21,21,21,21,63,21,63,21,21,'
    '21,63,21,21,21,21,21,63,21,21,21,21,21,21,21,63,21,21,21,63,21,63,21,21,'
    '21,63,21,760')

IR_EXIT = (
    'sendir,1:{ir_port},1,38000,1,1,171,169,21,63,21,63,21,63,21,21,21,21,21,21,21,21,'
    '21,21,21,63,21,63,21,63,21,21,21,21,21,21,21,21,21,21,21,63,21,21,21,63,'
    '21,63,21,21,21,63,21,21,21,21,21,21,21,63,21,21,21,21,21,63,21,21,21,63,'
    '21,63,21,760')

MODE_TO_CMDS = {
    'on': IR_PWRON,
    'off': IR_PWROFF,
    'menu': IR_MENU,
    'enter': IR_ENTER,
    'up': IR_UP,
    'down': IR_DOWN,
    'left': IR_LEFT,
    'right': IR_RIGHT,
    'tools': IR_TOOLS,
    'exit': IR_EXIT,
}

ROOMS_TO_PORTS = {
    'living':  1,
    #'bedroom': 2,
    'kitchen': 2,
}

def cli_options():
    usage = (
        '\n\n'
        'modes supported:  {0}\n'
        'rooms supported:  {1}\n'.format(MODE_TO_CMDS.keys(),
                                         ROOMS_TO_PORTS.keys()))
    parser = argparse.ArgumentParser(usage=usage)
    parser.add_argument('--host', default='172.30.0.34',
                        help='Remote host for sending IR commands over Telnet')
    parser.add_argument('--port', default=4998,
                        help='Remote port for sending IR commands over Telnet')
    parser.add_argument('--room', default='living',
                        help='Room to control.  Choices:  {0}'.format(ROOMS_TO_PORTS.keys()))
    parser.add_argument('--logfile', default='/opt/samsungtv.log')
    parser.add_argument('mode')
    options = parser.parse_args()
    return options
                                    

def main():
    options = cli_options()
    log = open(options.logfile, 'a')

    conn = telnetlib.Telnet(options.host, options.port)

    ir_command = MODE_TO_CMDS[options.mode].format(ir_port=ROOMS_TO_PORTS[options.room])
    log.write('sending:  {0}\n'.format(ir_command))
    conn.write('{command}\r\n'.format(command=ir_command))

    output = conn.read_some()
    log.write('received:  {0}\n'.format(output))

    time.sleep(0.2)
    conn.close()
    log.close()


if __name__ == '__main__':
    main()
