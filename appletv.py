import sys
import time
import telnetlib

GLOBAL_CACHE = '172.30.0.34'
CONTROL_PORT = 4998

IR_MENU = (
    'sendir,1:3,1,38000,1,1,341,172,21,21,21,65,21,65,21,65,21,21,21,65,21,65,'
    '21,65,21,65,21,65,21,65,21,21,21,21,21,21,21,21,21,65,21,21,21,65,21,21,'
    '21,21,21,21,21,21,21,21,21,21,21,21,21,21,21,21,21,21,21,21,21,65,21,65,'
    '21,21,21,1594,341,85,21,3652')

IR_PREV = (
    'sendir,1:3,4,38000,1,1,342,172,22,22,22,65,22,65,22,64,22,22,22,65,22,64,'
    '22,65,22,65,22,64,22,65,22,22,22,22,22,22,22,22,22,65,22,65,22,22,22,22,'
    '22,64,22,22,22,22,22,22,22,22,22,22,22,64,22,65,22,22,22,64,22,65,22,65,'
    '22,22,22,1421,342,85,22,3656,342,85,22,172')

IR_NEXT = (
    'sendir,1:3,2,38000,1,1,342,172,22,22,22,64,22,64,22,65,22,22,22,64,22,64,'
    '22,64,22,65,22,65,22,64,22,22,22,22,22,22,22,22,22,65,22,22,22,64,22,64,'
    '22,22,22,22,22,22,22,22,22,22,22,22,22,65,22,65,22,22,22,65,22,65,22,65,'
    '22,22,22,1421,342,85,22,3656,342,85,22,172')

IR_PLAY = (
    'sendir,1:3,3,38000,1,1,342,172,22,22,22,64,22,64,22,64,22,22,22,65,22,65,'
    '22,65,22,65,22,65,22,65,22,22,22,22,22,22,22,22,22,65,22,64,22,22,22,64,'
    '22,22,22,22,22,22,22,22,22,22,22,22,22,64,22,64,22,22,22,64,22,64,22,64,'
    '22,22,22,1421,342,85,22,172')

IR_UP = (
    'sendir,1:3,5,38000,1,1,342,172,22,22,22,65,22,64,22,64,22,22,22,65,22,65,'
    '22,65,22,64,22,64,22,64,22,22,22,22,22,22,22,22,22,65,22,22,22,64,22,22,'
    '22,64,22,22,22,22,22,22,22,22,22,22,22,64,22,64,22,22,22,64,22,64,22,64,'
    '22,22,22,1421,342,85,22,172')

IR_DOWN = (
    'sendir,1:3,7,38000,1,1,342,172,22,22,22,65,22,64,22,64,22,22,22,65,22,65,'
    '22,65,22,65,22,65,22,64,22,22,22,22,22,22,22,22,22,65,22,22,22,22,22,64,'
    '22,65,22,22,22,22,22,22,22,22,22,22,22,65,22,65,22,22,22,64,22,64,22,64,'
    '22,22,22,1421,342,85,22,172')

MODE_TO_CMDS = {
    'menu': IR_MENU,
    'prev': IR_PREV,
    'next': IR_NEXT,
    'play': IR_PLAY,
    'up': IR_UP,
    'down': IR_DOWN,
}

USAGE = ('{program} [mode]\n'
         '\n'
         'Modes:  {modes}\n'.format(program=sys.argv[0],
                                    modes=MODE_TO_CMDS.keys()))
                                 

def main():
    if len(sys.argv) < 2:
        raise SystemExit(USAGE)

    mode = sys.argv[1].lower()
    if mode not in MODE_TO_CMDS:
	raise SystemExit(USAGE)

    conn = telnetlib.Telnet(GLOBAL_CACHE, CONTROL_PORT)
    conn.write('{command}\r\n'.format(command=MODE_TO_CMDS[mode]))
    time.sleep(0.2)
    conn.close()


if __name__ == '__main__':
    main()
