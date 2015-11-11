"""
http server for controlling rpi GPIOs

"""

import SocketServer
import SimpleHTTPServer
import urllib
import os, json, logging, time
from threading import Thread
import utils

from config import CMD_PORT_MAP, PORT

# Logging Configuration
FORMAT = '%(asctime)-15s %(message)s'
logging.basicConfig(format=FORMAT, level=logging.DEBUG)


# use MOCK if not running on rpio
if utils.isRPI():
    import RPi.GPIO as GPIO
else:
    import mock as GPIO

# init GPIO
GPIO.setmode(GPIO.BCM)
# init output ports
for (cmd, port) in CMD_PORT_MAP.iteritems():
    logging.debug("setup port %2d for cmd %s" % (port, cmd))
    GPIO.setup(port,  GPIO.OUT)


#return curren pin status
def status():
    r = dict(map(lambda (cmd, port): (cmd, GPIO.input(port)), CMD_PORT_MAP.iteritems() ))
    #logging.debug(r)
    return r


def blink(port):
    for i in range(3):
        GPIO.output(port, 1)
        time.sleep(0.05)
        GPIO.output(port, 0)
        time.sleep(0.2)

class ServerRequestHandler(SimpleHTTPServer.SimpleHTTPRequestHandler):
    # called for direction cmds (blink)
    def cmd_direction(self, direction):
        logging.debug("cmd %s" % direction)
        if CMD_PORT_MAP.has_key(direction):
            Thread(target=blink, args=(CMD_PORT_MAP[direction],)).start()

    # called for function cmds (toggle)
    def cmd_fn(self, fn):
        logging.debug("cmd %s" % fn)
        if CMD_PORT_MAP.has_key(fn):
            port = CMD_PORT_MAP[fn]
            GPIO.output(port,  ~GPIO.input(port) & 0x1 ) # toggle

    # webserver handler routine
    def do_GET(self):
        if self.path.startswith("/cmd"):
            cmd = self.path[4:]
            if cmd == "/up":
                self.cmd_direction("up")
            elif cmd == "/down":
                self.cmd_direction("down")
            elif cmd == "/left":
                self.cmd_direction("left")
            elif cmd == "/right":
                self.cmd_direction("right")
            elif cmd == "/fn1":
                self.cmd_fn("fn1")
            elif cmd == "/fn2":
                self.cmd_fn("fn2")
            elif cmd == "/fn3":
                self.cmd_fn("fn3")
            # respond with current status
            json.dump(status(), self.wfile)
        else:
            if self.path == "/":
                self.path += "index.html"
            path = "www" + self.path
            if os.path.exists(path):
                self.copyfile(urllib.urlopen("www" + self.path), self.wfile)
            else:
                self.send_response(404)



httpd = SocketServer.ThreadingTCPServer(('', PORT), ServerRequestHandler)
logging.info("starting on port %d" % PORT)
httpd.serve_forever()
