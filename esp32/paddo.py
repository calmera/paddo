from utime import sleep_ms

from machine import Pin
from neopixel import NeoPixel


class Paddo:
    def __init__(self, pin=16):
        self.pin = Pin(pin, Pin.OUT)
        self.np = NeoPixel(self.pin, 128)
        
        self.mapping = [
            [ 0,  1,  2,  3,  4,  5,  6,  7, 15, 23, 31, 39, 47, 55, 63, 62, 61, 60, 59, 58, 57, 56, 48, 40, 32, 24, 16, 8],
            [ 9, 10, 11, 12, 13, 14, 22, 30, 38, 46, 54, 53, 52, 51, 50, 49, 41, 33, 25, 17],
            [18, 19, 20, 21, 29, 37, 45, 44, 43, 42, 34, 26],
            [27, 28, 36, 35]
        ]
        
    def flush(self):
        self.np.write()

    def clear(self, flush=True):
        for i in range(128):
            self.np[i] = (0, 0, 0)

        if flush:
            self.np.write()

    def all(self, value, flush=True):
        for i in range(128):
            self.np[i] = value

        if flush:
            self.np.write()

    def strand(self, ring, pos, value, flush=True):
        upper_pos, lower_pos = self.resolve(ring, pos)
        
        self.np[upper_pos] = value
        self.np[lower_pos] = value
        
        if flush:
            self.np.write()

    def ring(self, ring, value, flush=True):
        for i in range(len(self.mapping[ring])):
            pos = self.mapping[ring][i]
            r_pos = self.mapping[ring][i * -1]
            self.np[pos] = value
            self.np[r_pos + 64] = value
        
        if flush:
            self.np.write()
        
    def resolve(self, ring, index):
        pos = self.mapping[ring][index]
        r_pos = self.mapping[ring][-index]
        return pos, r_pos + 64

    def iterate(self, side, ring, cb, delay=5):
        for i in range(len(self.mapping[ring])):
            pos = self.mapping[ring][i] + (side * 64)
            self.np[pos] = cb(self.np[pos])
            sleep_ms(delay)
            self.np.write()

    def iterate_sync(self, ring, cb, delay=5):
        for i in range(len(self.mapping[ring])):
            pos = self.mapping[ring][i]
            r_pos = self.mapping[ring][i * -1]
            self.np[pos] = cb(self.np[pos])
            self.np[r_pos + 64] = cb(self.np[r_pos])
            self.np.write()
            sleep_ms(delay)

    def iterate_reverse_sync(self, ring, cb, delay=5):
        for i in range(len(self.mapping[ring])):
            pos = self.mapping[ring][-i]
            r_pos = self.mapping[ring][i]
            self.np[pos] = cb(self.np[pos])
            self.np[r_pos + 64] = cb(self.np[r_pos])
            self.np.write()
            sleep_ms(delay)

    def count(self, ring):
        return len(self.mapping[ring])
