#!/usr/bin/python
import smbus
import time
import struct

DEV_ADDR = 0x04

bus = smbus.SMBus(1)
reads = 0
errs = 0

while True:
    reads += 1
    try:
        a_val = bus.read_word_data(DEV_ADDR, 0)
	i = struct.unpack('>h', struct.pack('<H', a_val))[0] / 256.0
        print("Power draw: %.1fA; no. of reads [%s]; no. of errors [%s]" % (i, reads, errs))
    except Exception as ex:
        errs += 1
        print("Exception [%s]" % (ex))

    time.sleep(1)
