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


def do_connect():
  import network
  wlan = network.WLAN(network.STA_IF)
  wlan.active(True)
  if not wlan.isconnected():
    print('connecting to network...')
    wlan.connect('ORBI', 'phobicviolin114')
    while not wlan.isconnected():
      pass
  
  print('network config:', wlan.ifconfig())


def do_nats_connect():
  import mpynats
  c = mpynats.Connection(
    url='nats://192.168.1.69:4222', 
    name='swift', 
    ssl_required=False, 
    verbose=True, 
    pedantic=False, 
    socket_keepalive=True, 
    raw=False, 
    debug=True)
  c.connect()
  
  return c

p = Paddo()
p.clear()
p.ring(3, [0, 255, 255])

do_connect()
p.ring(2, [0, 255, 255])

c = do_nats_connect()
p.ring(1, [0, 255, 255])

proto = Protocol(p)

subscription = c.subscribe('paddo', lambda msg : proto.handle(msg) )
p.ring(0, [0, 255, 255])

p.all([0, 255, 0])

c.wait()