# Connections:
# xxPy | WS2812
# -----|-------
# Vin  |  Vcc
# GND  |  GND
# P11  |  DATA
from paddo import Paddo
from utime import sleep
from uos import urandom

p = Paddo()

white = (200, 200, 200)

def iterate_rgb(delay=5):
  for i in range(4):
    p.iterate_reverse_sync(3 - i, lambda v: (255, 0, 0), delay)

  for i in range(4):
    p.iterate_reverse_sync(3 - i, lambda v: (0, 255, 0), delay)

  for i in range(4):
    p.iterate_reverse_sync(3 - i, lambda v: (0, 0, 255), delay)

def coolblue():
    p.ring(0, (0, 0, 255))
    p.ring(1, (255, 0, 0))
    p.ring(2, (255, 0, 0))
    p.ring(3, (200, 200, 200))


def mushroom():
  # -- generate state
  data = 128 * [(255, 0, 0)]
  
  for i in range(15):
    d = int((urandom(1)[0] / 265) * 63)
    
    r = 0
    j = d
    if (d >= 28): 
      r = 1
      j = d - 28
    if (d >= 48):
      r = 2
      j = d - 48
    if (d >= 60):
      r = 3
      j = d - 60

    pos, r_pos = p.resolve(r, j)
    data[pos] = white
    data[r_pos] = white

  p.flush(data)
  sleep(5)


while True:
  for i in range(15):
        iterate_rgb(delay=100)

  coolblue()
  sleep(60 * 5)

