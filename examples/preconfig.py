import random
from common import *
from core import *

def plinkosetup():
    xcoords = [(ctx.pwidth * i / 5) for i in range(6)]
    ycoords = [(ctx.pheight * i / 10) + 100 for i in range(6)]
    squares = []
    for i in range(len(ycoords)):
        for j in xcoords:
            squares += [Square(y=ctx.pheight - ycoords[i], x=j - (i * ctx.pwidth / 10), angle=45, sizex=20 * ctx.pwidth / 500, sizey=20 * ctx.pheight / 500)]

            squares += [Square(y=ctx.pheight - 20, x=j - (i * ctx.pwidth / 10), sizex=3 * ctx.pwidth / 500, sizey=40 * ctx.pheight / 500)] if (i < 2) else []

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
    "margaret" : [[Square(y =ctx.pheight - 30, x =(ctx.pwidth / 2) - 20, sizex = 5, sizey = 80, angle = 30),
                   Square(y =ctx.pheight - 30, x =(ctx.pwidth / 2) + 20, sizex = 5, sizey = 80, angle = -30),
                   Square(y =ctx.pheight - 100, x = (ctx.pwidth / 2), sizex = 5, sizey = 80, angle = 0),
                   Square(y =ctx.pheight - 100, x =(ctx.pwidth / 2) - 20, sizex = 5, sizey = 80, angle = 30),
                   Square(y =ctx.pheight - 100, x =(ctx.pwidth / 2) + 20, sizex = 5, sizey = 80, angle = -30)],
                  [Ball(y =ctx.pheight - 160, x =ctx.pwidth / 2, radius = 30, static=True, mass = -1)]],
    "conveyor" : [[Square(50 + i * 50, ctx.pheight - 50, 0, 50, 50) for i in range(9)], []],
    "brownian" : [[],[Ball(mass=8, drawtrail=True, radius = 20)]],
    "random" : [[Square(random.randint(0, ctx.pwidth), random.randint(0, ctx.pheight), random.randint(0, 360), sizey = random.randint(5, 80), sizex = random.randint(5, 80)) for i in range(20)], []],
    "kerplunk" : [[Square(100, 380, 15, 30, 250),
               Square(400, 380, -15, 30, 250),
               Square(370, 180, 0, 30, 170),
               Square(130, 180, 0, 30, 170),
               Square(445, 55, 60, 30, 200),
               Square(55, 55, -60, 30, 200),
               ] + kerplunkgen(),
              []],
    "square": [[Square()],[]],
    "null" : [[],[]]

}