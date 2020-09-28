# Connections:
# xxPy | WS2812
# -----|-------
# Vin  |  Vcc
# GND  |  GND
# P16  |  DATA

from paddo import Paddo
from protocol import Protocol
from utime import sleep
from uos import urandom

import machine
import ujson

p = Paddo()
p.clear()
p.ring(3, [0, 255, 255])

config = None
with open('/config.json', 'r') as f:
  config = ujson.loads(str(f.read()))

if config is None:
  p.all([255, 0, 0])

def do_connect():
  import network
  wlan = network.WLAN(network.STA_IF)
  wlan.active(True)
  if not wlan.isconnected():
    print('connecting to network...')
    wlan.connect(config["network"]["ssid"], config["network"]["pwd"])
    while not wlan.isconnected():
      pass
  
  print('network config:', wlan.ifconfig())


def do_nats_connect():
  import mpynats
  c = mpynats.Connection(
    url=config["nats"],
    name='swift', 
    ssl_required=False, 
    verbose=True, 
    pedantic=False, 
    socket_keepalive=True, 
    raw=False, 
    debug=True)
  c.connect()
  
  return c

do_connect()
p.ring(2, [0, 255, 255])

c = do_nats_connect()
p.ring(1, [0, 255, 255])

proto = Protocol(p)

subscription = c.subscribe('paddo', lambda msg: proto.handle(msg))
p.ring(0, [0, 255, 255])

p.all([0, 255, 0])

c.wait()
