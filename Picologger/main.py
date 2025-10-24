from picologger import start
from filetransfer import startimport

SIE_STATUS=const(0x50110000+0x50)
CONNECTED=const(1<<16)
SUSPENDED=const(1<<4)

if (machine.mem32[SIE_STATUS] & (CONNECTED | SUSPENDED))==CONNECTED:
    startimport()
else:
    print('starting programm')
    start()