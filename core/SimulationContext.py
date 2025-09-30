from common import *
import time
class SimulationContext:
    def __init__(self):
        self.guitoggle = True
        self.frames = [framerate for _ in range(5)]
        self.etime = time.time()

        self.gmag = gmag
        self.gflip = 1
        self.deg = deg
        self.spinvel = spinvel
        self.bring = False

        self.col = col
        self.col2 = col2
        self.bgcol = bgcol
        self.colid = 0

        self.balls = []
        self.squares = []
        self.objects = []

