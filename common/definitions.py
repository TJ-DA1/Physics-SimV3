import math, random

def boundary_difference(ball, vert, neg, ctx): #Returns multiplier of acceleration
    if vert:
        if neg: #Above simulation border
            return (ball.radius - ball.clipy) / ((ball.prevy - ball.clipy) if (ball.prevy - ball.clipy) != 0 else 0.1)
        else: #Below simulation border
            return (ball.clipy - (ctx.pheight - ball.radius))  / ((ball.clipy - ball.prevy) if (ball.clipy - ball.prevy) != 0 else 0.1)
    else:
        if neg: #Left of simulation border
            return (ball.radius - ball.clipx) / ((ball.prevx - ball.clipx) if (ball.prevx - ball.clipx) != 0 else 0.1)
        else: #Right of simulation border
            return (ball.clipx - (ctx.pwidth - ball.radius))  / ((ball.clipx - ball.prevx) if (ball.clipx - ball.prevx) != 0 else 0.1)

def hide_elements(ele, ele2): #Tider way of hiding elements when selecting object type in editor
    for i in ele:
        i.hide()
    for i in ele2:
        i.show()

def multiplyvector(v, s): #Makes more readable, multiplies component of vector by constant
    return (v[0] * s, v[1] * s)

def calcpoints(sizex, sizey, x, y, angle, offset): #Calculates points of rectangle given size, position, angle
    points = []
    diag = math.dist((0, 0), (sizex, sizey)) / 2 #Diagonal size of rectangle
    rectang = (math.pi / 4) - math.atan2(sizey, sizex) #Angle of first point relative to rectangle

    for i in range(4):
        ang = (math.pi * 0.5 * i) - (math.pi / 4) + math.radians(angle) + (rectang * ((-1) ** i)) #Cycles through angle of each point
        xcoord = x + (diag * math.cos(ang)) + offset #Uses trig to find X and Y position
        ycoord = y + (diag * math.sin(ang)) + offset
        points.append((xcoord, ycoord))
    lines = [(points[i], points[(i + 1) if not (i + 1) >= 4 else 0]) for i in range(4)] #Lines is every combination of adjacent points
    return points, lines

def rotatepoint(point, angle): #Rotates point around (0,0)
    return [point[0] * math.cos(math.radians(angle)) - point[1] * math.sin(math.radians(angle)),
     point[0] * math.sin(math.radians(angle)) + point[1] * math.cos(math.radians(angle))]

def create_ball(obj, num, ctx): #Returns initial list of ball objects
    return [obj(
        dx=random.uniform(-1000, 1000),
        dy=random.uniform(-1000, 1000),
        x=random.randint(0, ctx.pwidth),
        y=random.randint(0, ctx.pheight),
        radius=ctx.radius,
        drawtrail = False
    ) for _ in range(num)]

def resolve_forces(component):
    axtemp, aytemp = 0, 0
    for i in component: #Cycles through components to calculate resultant
        axtemp += i[0] * math.cos(i[1]) #Trig to find X and Y components
        aytemp += i[0] * math.sin(i[1])
    return round(axtemp, 2), round(aytemp,2)


def hexformat(hexstring):
    validsep = [",", ".", " ", "/"] #List of characters used as seperators
    for i in validsep: #Checks string for every valid seperator
        if i in hexstring:
            string2 = hexstring
            string2 = string2.split(i) #To avoid splitting the passed variable
            if len(string2) == 3:
                check = 0 #Initial check for input length
                for i in string2:
                    try:
                        i = int(i) #Fails if element is not integer between -1 - 256
                        if 0 <= i <= 255:
                            check += 1
                    except:
                        check = -1000000
                if check == 3:
                    return list([int(i) for i in string2]) #Valid output
    return None

def updrainbow(context, colour):
    if True not in context.rainbow: #No need to update if no colours are set to rainbow
        return
    if context.up:
        colour[context.c2] += 20 #Increasing intensity of R, G or B
        if colour[context.c2] >= 255:
            colour[context.c2] = 255
            context.up = not context.up
    else:
        colour[context.c1] -= 20 #Decreasing intensity of R, G or B
        if colour[context.c1] <= 0:
            colour[context.c1] = 0
            context.up = not context.up
            context.c1 += 1 if context.c1 != 2 else -2 #Cycles R, G, B values
            context.c2 += 1 if context.c2 != 2 else -2

    for i in range(len(context.rainbow)):
        if context.rainbow[i]:
            match i: #Set valid colour channel to rainbow colour
                case 0: context.col2 = list(context.rcol)
                case 1: context.col = list(context.rcol)
                case 2: context.bgcol = list(context.rcol)