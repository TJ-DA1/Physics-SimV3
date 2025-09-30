import math, random
from .config import *

def boundary_difference(ball, vert, neg):
    if vert:
        if neg:
            return (ball.radius - ball.clipy) / ((ball.prevy - ball.clipy) if (ball.prevy - ball.clipy) != 0 else 0.1)
        else:
            return (ball.clipy - (pheight - ball.radius))  / ((ball.clipy - ball.prevy) if (ball.clipy - ball.prevy) != 0 else 0.1)
    else:
        if neg:
            return (ball.radius - ball.clipx) / ((ball.prevx - ball.clipx) if (ball.prevx - ball.clipx) != 0 else 0.1)
        else:
            return (ball.clipx - (pwidth - ball.radius))  / ((ball.clipx - ball.prevx) if (ball.clipx - ball.prevx) != 0 else 0.1)

def create_ball(obj, num, radius):
    return [obj(
        dx=random.uniform(-10, 10),
        dy=random.uniform(-10, 10),
        x=random.randint(0, pwidth),
        y=random.randint(0, pheight),
        radius=radius,
        padding = pad,
        drawtrail = False
    ) for _ in range(num)]

def resolve_forces(component):
    axtemp, aytemp = 0, 0
    for i in component:
        axtemp += i[0] * math.cos(math.radians(i[1]))
        aytemp += i[0] * math.sin(math.radians(i[1]))
    return round(axtemp, 2), round(aytemp,2)


def hexformat(hexstring):
    validsep = [",", ".", " ", "/"]
    for i in validsep:
        if i in hexstring:
            string2 = hexstring
            string2 = string2.split(i)
            if len(string2) == 3:
                check = 0
                for i in string2:
                    try:
                        i = int(i)
                        if 0 <= i <= 255:
                            check += 1
                    except:
                        check = -1000000
                if check == 3:
                    return list([int(i) for i in string2])            
    return None