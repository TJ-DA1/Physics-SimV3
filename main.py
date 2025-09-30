import random
from sqlite3 import SQLITE_AUTH

from core import *
from interface import *


context = SimulationContext()
context.test = []
collision = CollHandler(context)
interface = GUIHandler(context, Ball, Square)

context.balls = create_ball(Ball, bcount, rad)

'''
for i in range(9):
    context.squares += [Square(40 + i * 50, pheight - 50, 0, 50)]

for i in range(20):
    context.squares += [Square(random.randint(0, pwidth), random.randint(0, pheight), random.randint(0, 360), 40)]

heavy = create_ball(Ball, 1, 30)
heavy[0].mass = 8
heavy[0].drawtrail = True
context.balls.append(heavy[0])
'''
xcoords = [(pwidth * i/5) for i in range(6)]
ycoords = [(pheight * i/10) + 100 for i in range(6)]

for i in range(len(ycoords)):
    for j in xcoords:
        context.squares += [Square(y=pheight - ycoords[i], x=j - (i * pwidth / 10), angle=45, sizex=30, sizey = 30)]

        context.squares += [Square(y=pheight - 20, x=j - (i * pwidth / 10), sizex = 3, sizey = 40)]

    try:
        xcoords.pop(0)

    except:
        pass



'''
context.squares += [Square(y = pheight - 30, x = (pwidth / 2) - 20, sizex = 5, sizey = 80, angle = 30)]
context.squares += [Square(y = pheight - 30, x = (pwidth / 2) + 20, sizex = 5, sizey = 80, angle = -30)]
context.squares += [Square(y = pheight - 100, x = (pwidth / 2), sizex = 5, sizey = 80, angle = 0)]
context.squares += [Square(y = pheight - 100, x = (pwidth / 2) - 20, sizex = 5, sizey = 80, angle = 30)]
context.squares += [Square(y = pheight - 100, x = (pwidth / 2) + 20, sizex = 5, sizey = 80, angle = -30)]
context.balls += [Ball(y = pheight - 160, x = pwidth / 2, radius = 30, static=True, mass = -1)]
'''
running = True

def fixedupdate(ctx):
    global square
    ctx.objects = ctx.balls + ctx.squares
    ctx.deg += ctx.spinvel
    psurface.fill(ctx.bgcol)

    interface.handle()

    for i in ctx.balls:
        i.movecalc()

    for _ in range(passes):
        for i in range(len(ctx.objects)):
            for j in range(i + 1, len(ctx.objects)):
                o1, o2 = ctx.objects[i], ctx.objects[j]
                collision.collide(o1,o2)

        for ball in ctx.balls:
            ball.boundarycheckx()
            ball.boundarychecky()

    for i in ctx.squares:
        i.angle += 0
        i.calcpoints()

    for i in ctx.objects:
        if ctx.bring: i.x, i.y = pygame.mouse.get_pos() if type(i) == Ball else (i.x, i.y)
        i.movecalc2()
        i.draw(ctx.col, ctx.col2)

    for i in context.test:
        pygame.draw.line(psurface, col2, i[0], i[1], 3)

    small_screen = pygame.transform.scale(psurface, scalesize)
    pixelated_screen = pygame.transform.scale(small_screen, (width, height))
    screen.blit(pixelated_screen, (0, 0))

    if ctx.guitoggle:
        manager.update(dtime - ctx.etime)
        manager.draw_ui(screen)

    pygame.display.flip()

while running:
    dtime = time.time()
    if dtime - context.etime >= 1 / framerate:
        context.frames.append(1 / (dtime - context.etime))
        context.frames.pop(0)
        fixedupdate(context)
        framelabel.set_text(f"{round(sum(context.frames) / len(context.frames))}fps")
        context.etime += dtime - context.etime