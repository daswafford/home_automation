#!/usr/bin/python
""" Samsung TV Control based on Telnet
    to a Global Cache IP-TO_IR device.

    Credit to http://board.homeseer.com/showthread.php?t=153446 for IR Codes.
"""

import sys
import time
import telnetlib

GLOBAL_CACHE = '172.30.0.34'
CONTROL_PORT = 4998

IR_PWRON = (
    'sendir,1:1,1,38000,3,1,171,168,22,61,22,61,22,61,22,20,22,20,22,20,22,20,'
    '22,20,22,61,22,61,22,61,22,20,22,20,22,20,22,20,22,20,22,61,22,20,22,20,'
    '22,61,22,61,22,20,22,20,22,61,22,20,22,61,22,61,22,20,22,20,22,61,22,61,'
    '22,20,22,760')

IR_PWROFF = (
    'sendir,1:1,1,38000,3,1,171,169,22,62,22,62,22,62,22,19,22,19,22,19,22,19,'
    '22,19,22,62,22,62,22,62,22,19,22,19,22,19,22,19,22,19,22,19,22,19,22,19,'
    '22,62,22,62,22,19,22,19,22,62,22,62,22,62,22,62,22,19,22,19,22,62,22,62,'
    '22,19,22,760')

IR_MENU = (
   'sendir,1:1,1,38000,1,1,171,170,21,64,21,64,21,64,21,21,21,21,21,21,21,21,'
   '21,21,21,64,21,64,21,64,21,21,21,21,21,21,21,21,21,21,21,21,21,64,21,21,21,'
   '64,21,64,21,21,21,21,21,21,21,64,21,21,21,64,21,21,21,21,21,64,21,64,21,64,'
   '21,760')

IR_ENTER = (
    'sendir,1:1,1,38000,1,1,171,170,21,63,21,63,21,63,21,20,21,20,21,20,21,20,'
    '21,20,21,63,21,63,21,63,21,20,21,20,21,20,21,20,21,20,21,20,21,63,21,20,'
    '21,20,21,20,21,63,21,63,21,20,21,63,21,20,21,63,21,63,21,63,21,20,21,20,'
    '21,63,21,760')

IR_DOWN = (
    'sendir,1:1,1,38000,1,1,171,170,21,63,21,63,21,63,21,21,21,21,21,21,21,21,'
    '21,21,21,63,21,63,21,63,21,21,21,21,21,21,21,21,21,21,21,63,21,21,21,21,'
    '21,21,21,21,21,63,21,63,21,21,21,21,21,63,21,63,21,63,21,63,21,21,21,21,'
    '21,63,21,760')

IR_UP = (
    'sendir,1:1,1,38000,1,1,171,170,21,63,21,63,21,63,21,21,21,21,21,21,21,21,'
    '21,21,21,63,21,63,21,63,21,21,21,21,21,21,21,21,21,21,21,21,21,21,21,21,'
    '21,21,21,21,21,63,21,63,21,21,21,63,21,63,21,63,21,63,21,63,21,21,21,21,'
    '21,63,21,760')

IR_LEFT = (
    'sendir,1:1,1,38000,1,1,171,170,21,63,21,63,21,63,21,21,21,21,21,21,21,21,'
    '21,21,21,63,21,63,21,63,21,21,21,21,21,21,21,21,21,21,21,63,21,21,21,63,'
    '21,21,21,21,21,63,21,63,21,21,21,21,21,63,21,21,21,63,21,63,21,21,21,21,'
    '21,63,21,760')

IR_RIGHT = (
    'sendir,1:1,1,38000,1,1,171,170,21,63,21,63,21,63,21,20,21,20,21,20,21,20,'
    '21,20,21,63,21,63,21,63,21,20,21,20,21,20,21,20,21,20,21,20,21,63,21,20,'
    '21,20,21,20,21,63,21,63,21,20,21,63,21,20,21,63,21,63,21,63,21,20,21,20,'
    '21,63,21,760')

IR_ENTER = (
    'sendir,1:1,1,38000,1,1,171,170,21,64,21,64,21,64,21,21,21,21,21,21,21,21,'
    '21,21,21,64,21,64,21,64,21,21,21,21,21,21,21,21,21,21,21,21,21,21,21,21,'
    '21,64,21,21,21,64,21,64,21,21,21,64,21,64,21,64,21,21,21,64,21,21,21,21,'
    '21,64,21,760')

IR_TOOLS = (
    'sendir,1:1,1,38000,1,1,171,170,21,63,21,63,21,63,21,21,21,21,21,21,21,21,'
    '21,21,21,63,21,63,21,63,21,21,21,21,21,21,21,21,21,21,21,63,21,63,21,21,'
    '21,63,21,21,21,21,21,63,21,21,21,21,21,21,21,63,21,21,21,63,21,63,21,21,'
    '21,63,21,760')

IR_EXIT = (
    'sendir,1:1,1,38000,1,1,171,169,21,63,21,63,21,63,21,21,21,21,21,21,21,21,'
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

USAGE = ('{program} [mode]\n'
         '\n'
         'Modes:  {modes}\n'.format(program=sys.argv[0],
                                    modes=MODE_TO_CMDS.keys()))
                                 

def main():
    f = open('/opt/samsungtv.log', 'a')

    if len(sys.argv) < 2:
        raise SystemExit(USAGE)

    mode = sys.argv[1].lower()
    if mode not in MODE_TO_CMDS:
	raise SystemExit(USAGE)

    f.write('sending:  {0}\n'.format(MODE_TO_CMDS[mode]))
    conn = telnetlib.Telnet(GLOBAL_CACHE, CONTROL_PORT)
    conn.write('{command}\r\n'.format(command=MODE_TO_CMDS[mode]))
    output = conn.read_some()
    f.write('received:  {0}\n'.format(output))
    time.sleep(0.2)
    conn.close()
    f.close()

if __name__ == '__main__':
    main()