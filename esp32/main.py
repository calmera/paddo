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
    verbose=False,
    pedantic=False, 
    socket_keepalive=True, 
    raw=False, 
    debug=False)
  c.connect()
  
  return c

do_connect()
p.ring(2, [0, 255, 255])

c = do_nats_connect()
p.ring(1, [0, 255, 255])

if config["mode"] == "command":
  proto = Protocol(p)

  subscription = c.subscribe('paddo', lambda msg: proto.handle(msg))
  p.ring(0, [0, 255, 255])
else:
  color = config["color"]
  def randomize(msg):
    # print("msg received ...")

    # -- get a random ring
    ring, strand = p.random()

    # print("going for ring %d, strand %d" % (ring, strand))

    value, lower_value = p.get(ring, strand)
    # print("current value", value)

    if value[0] == 0 and value[1] == 0 and value[2] == 0:
      p.strand(ring, strand, color)
      # print("coloring")
    else:
      p.strand(ring, strand, [0, 0, 0])
      # print("clearing")

  print("subscribing to %s" % config["subject"])
  subscription = c.subscribe(config["subject"], lambda msg: randomize(msg))

  p.ring(0, [0, 255, 255])

p.clear()

c.wait()
