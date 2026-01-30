import random
from common import *
from core import *

def plinkogen(): #Scales plinko preconfig to size of surface
    xcoords = [(ctx.pwidth * i / 5) for i in range(6)]
    ycoords = [(ctx.pheight * i / 10) + 100 for i in range(6)]
    squares = []
    for i in range(len(ycoords)):
        for j in xcoords:
            squares += [Square(y=ctx.pheight - ycoords[i], x=j - (i * ctx.pwidth / 10), angle=45, sizex=20 * ctx.pwidth / 500, sizey=20 * ctx.pheight / 500)]

            squares += [Square(y=ctx.pheight - 20, x=j - (i * ctx.pwidth / 10), sizex=3 * ctx.pwidth / 500, sizey=40 * ctx.pheight / 500)] if (i < 2) else []

        xcoords.pop(0)
    return squares

def kerplunkgen(): #Generates new kerplunk board
    out = []
    for i in range(10):
        sx, sy = random.randint(random.randint(100,150), random.randint(350,400)), random.randint(150, 250)
        szx, szy = 150, 20
        sang = random.randint(-30,30)
        out.append(Square(sx, sy, sang, szx, szy))
    return out

def rotategen(): #Scales rotate preconfig to size of surface
    childsquares = []
    new = [[Square(ctx.pwidth / 2, ctx.pheight / 2, 0, ctx.pwidth / 5, 10), Square(ctx.pwidth / 2, ctx.pheight / 2, 0, 10, ctx.pheight / 5)] for i in range(4)]
    for i in new:
        for j in i:
            childsquares += [j]

    emp1 = Empty(ctx.pwidth / 2, ctx.pheight / 2, 0, 1, childsquares[0:2])
    emp2 = Empty(ctx.pwidth / 2, ctx.pheight / 2, 0, 1, childsquares[2:4])
    emp3 = Empty(ctx.pwidth / 2, ctx.pheight / 2, 0, 1, childsquares[4:6])
    emp4 = Empty(ctx.pwidth / 2, ctx.pheight / 2, 0, 1, childsquares[6:8])

    emp1.possetter((3 * ctx.pwidth / 10, 7 * ctx.pwidth / 10))
    emp2.possetter((3 * ctx.pwidth / 10, 3 * ctx.pwidth / 10))
    emp3.possetter((7 * ctx.pwidth / 10, 3 * ctx.pwidth / 10))
    emp4.possetter((7 * ctx.pwidth / 10, 7 * ctx.pwidth / 10))

    empmain = Empty(ctx.pwidth / 2, ctx.pheight / 2, 0, 1, [emp1, emp2, emp3, emp4])

    return childsquares,[],[],[empmain, emp1, emp2, emp3, emp4]

preconfig = {
    "plinko" : [plinkogen(),[],[],[]], #Plinko board - pegs and baskets at botton
    "margaret" : [[Square(y =ctx.pheight - 30, x =(ctx.pwidth / 2) - 20, sizex = 5, sizey = 80, angle = 30),
                   Square(y =ctx.pheight - 30, x =(ctx.pwidth / 2) + 20, sizex = 5, sizey = 80, angle = -30),
                   Square(y =ctx.pheight - 100, x = (ctx.pwidth / 2), sizex = 5, sizey = 80, angle = 0),
                   Square(y =ctx.pheight - 100, x =(ctx.pwidth / 2) - 20, sizex = 5, sizey = 80, angle = 30),
                   Square(y =ctx.pheight - 100, x =(ctx.pwidth / 2) + 20, sizex = 5, sizey = 80, angle = -30)],
                  [Ball(y =ctx.pheight - 160, x =ctx.pwidth / 2, radius = 30, static=True, mass = -1)],[],[]],
    "conveyor" : [[Square(50 + i * 50, ctx.pheight - 50, 0, 50, 50, spinvel=1) for i in range(9)], [],[],[]], #Rotating squares move balls across sim
    "brownian" : [[],[Ball(mass=8, drawtrail=True, radius = 20)],[],[]], #Setup for Brownian motion simulation
    "random" : [[Square(random.randint(0, ctx.pwidth), random.randint(0, ctx.pheight), random.randint(0, 360), sizey = random.randint(5, 80), sizex = random.randint(5, 80)) for i in range(20)],
                [],[],[]], #Random squares
    "kerplunk" : [[Square(100, 380, 15, 30, 250),
               Square(400, 380, -15, 30, 250),
               Square(370, 180, 0, 30, 170),
               Square(130, 180, 0, 30, 170),
               Square(445, 55, 60, 30, 200),
               Square(55, 55, -60, 30, 200),
               ] + kerplunkgen(),
              [],[],[]], #Interactive recreation of Kerplunk!, a board game
    "square": [[Square(ctx.pwidth / 2, ctx.pheight / 2)],[],[],[]], #Single square in center
    "rotate": rotategen(), #Empty test - square plus signs rotating around their own center, around center
    "null" : [[],[],[],[]] #Empty sim
}