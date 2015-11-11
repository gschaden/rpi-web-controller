import logging

BCM=1

HIGH=1
LOW=0

IN=0
OUT=1

status = {}

def setmode(mode):
    logging.debug("setmode %s" % mode)

def setup(port, direction):
    logging.debug("setup %s %s" % (port, dir))

def output(port, value):
    logging.debug("output %s %s" % (port, value))
    status[port] = value

def input(port):
    if not status.has_key(port):
        status[port] = 0
    value = status[port]
    #logging.debug("input %s %s" % (port, value))
    return value
