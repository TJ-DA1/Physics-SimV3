import random

from common import *
from core import *
def plinkosetup():
    xcoords = [(pwidth * i / 5) for i in range(6)]
    ycoords = [(pheight * i / 10) + 100 for i in range(6)]
    squares = []
    for i in range(len(ycoords)):
        for j in xcoords:
            squares += [Square(y=pheight - ycoords[i], x=j - (i * pwidth / 10), angle=45, sizex=30, sizey=30)]

            squares += [Square(y=pheight - 20, x=j - (i * pwidth / 10), sizex=3, sizey=40)] if (i < 2) else []

        xcoords.pop(0)
    return squares

def kerplunkgen():
    out = []
    for i in range(10):
        sx, sy = random.randint(random.randint(100,150), random.randint(350,400)), random.randint(150, 250)
        szx, szy = 150, 20
        sang = random.randint(-30,30)
        out.append(Square(sx, sy, sang, szx, szy))
    return out


preconfig = {
    "plinko" : [plinkosetup(),[]],
    "margaret" : [[Square(y = pheight - 30, x = (pwidth / 2) - 20, sizex = 5, sizey = 80, angle = 30),
                Square(y = pheight - 30, x = (pwidth / 2) + 20, sizex = 5, sizey = 80, angle = -30),
                Square(y = pheight - 100, x = (pwidth / 2), sizex = 5, sizey = 80, angle = 0),
                Square(y = pheight - 100, x = (pwidth / 2) - 20, sizex = 5, sizey = 80, angle = 30),
                Square(y = pheight - 100, x = (pwidth / 2) + 20, sizex = 5, sizey = 80, angle = -30)],
                [Ball(y = pheight - 160, x = pwidth / 2, radius = 30, static=True, mass = -1)]],
    "conveyor" : [[Square(50 + i * 50, pheight - 50, 0, 50, 50) for i in range(9)], []],
    "brownian" : [[],[Ball(mass=8, drawtrail=True, radius = 20)]],
    "random" : [[Square(random.randint(0, pwidth), random.randint(0, pheight), random.randint(0, 360), sizey = random.randint(5,80), sizex = random.randint(5,80)) for i in range(20)],[]],
    "kerplunk" : [[Square(100, 380, 15, 30, 250),
               Square(400, 380, -15, 30, 250),
               Square(370, 180, 0, 30, 170),
               Square(130, 180, 0, 30, 170),
               Square(445, 55, 60, 30, 200),
               Square(55, 55, -60, 30, 200),
               ] + kerplunkgen(),
              []],
    "null" : [[Square()],[]]

}