from ws2812_spi import WS2812
from utime import sleep_ms

class Paddo:
    def __init__(self):
        self.data = 128 * [(0, 0, 0)]
        self.chain = WS2812(128)
        self.mapping = [
            [ 0,  1,  2,  3,  4,  5,  6,  7, 15, 23, 31, 39, 47, 55, 63, 62, 61, 60, 59, 58, 57, 56, 48, 40, 32, 24, 16, 8],
            [ 9, 10, 11, 12, 13, 14, 22, 30, 38, 46, 54, 53, 52, 51, 50, 49, 41, 33, 25, 17],
            [18, 19, 20, 21, 29, 37, 45, 44, 43, 42, 34, 26],
            [27, 28, 36, 35]
        ]

    def clear(self):
        for i in range(128):
            self.data[i] = (0, 0, 0)

        self.chain.show(self.data)

    def all(self, value):
        for i in range(128):
            self.data[i] = value

        self.chain.show(self.data)

    def ring(self, ring, value):
        for i in range(len(self.mapping[ring])):
            pos = self.mapping[ring][i]
            r_pos = self.mapping[ring][i * -1]
            self.data[pos] = value
            self.data[r_pos + 64] = value
        
        self.chain.show(self.data)
        

    def flush(self, data):
        self.data = data
        self.chain.show(self.data)

    def resolve(self, ring, index):
        pos = self.mapping[ring][index]
        r_pos = self.mapping[ring][-index]
        return pos, r_pos + 64

    def set(self, ring, position, value):
        self.data[ring][position] = value
        self.chain.show(self.data)

    def iterate(self, side, ring, cb, delay=5):
        for i in range(len(self.mapping[ring])):
            pos = self.mapping[ring][i] + (side * 64)
            self.data[pos] = cb(self.data[pos])
            sleep_ms(delay)
            self.chain.show(self.data)

    def iterate_sync(self, ring, cb, delay=5):
        for i in range(len(self.mapping[ring])):
            pos = self.mapping[ring][i]
            r_pos = self.mapping[ring][i * -1]
            self.data[pos] = cb(self.data[pos])
            self.data[r_pos + 64] = cb(self.data[r_pos])
            self.chain.show(self.data)
            sleep_ms(delay)

    def iterate_reverse_sync(self, ring, cb, delay=5):
        for i in range(len(self.mapping[ring])):
            pos = self.mapping[ring][-i]
            r_pos = self.mapping[ring][i]
            self.data[pos] = cb(self.data[pos])
            self.data[r_pos + 64] = cb(self.data[r_pos])
            self.chain.show(self.data)
            sleep_ms(delay)

    def count(self, ring):
        return len(self.mapping[ring])
