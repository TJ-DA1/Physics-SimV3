from core import *
from interface import *
from examples import *

elegui = Element()
GUI = GUIHandler(Ball)

def setupscreen():
    finalise = False
    while not finalise:
        ctx.screen.fill((255,255,255))
        finalise = GUI.handleprescreen()
        time.sleep(1/60)
        ctx.prescreen.update(1/60)
        ctx.prescreen.draw_ui(ctx.screen)
        pygame.display.flip()

setupscreen()

ctx.screen = pygame.display.set_mode((ctx.width, ctx.height), vsync=1)
ctx.psurface = pygame.Surface((ctx.pwidth + ctx.windowpad, ctx.pheight + ctx.windowpad))
ctx.manager.set_window_resolution((ctx.width, ctx.height))
elegui.initiate()
pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

collision = CollHandler()

ctx.squares += preconfig[ctx.preconfiguration][0]
ctx.balls += preconfig[ctx.preconfiguration][1]

ctx.balls += create_ball(Ball, ctx.bcount, ctx)

newnew = []
new = [[Square(250, 250, 0, 100, 10), Square(250, 250, 0, 10, 100)] for i in range(4)]
for i in new:
    for j in i:
        newnew += [j]

ctx.squares += newnew
emp1 = Empty(250,250, 0, newnew[0:2])
emp2 = Empty(250,250, 0, newnew[2:4])
emp3 = Empty(250,250, 0, newnew[4:6])
emp4 = Empty(250,250, 0, newnew[6:8])
emp1.possetter((150,350))
emp2.possetter((150,150))
emp3.possetter((350,150))
emp4.possetter((350,350))
emp = Empty(250,250,0,[emp1,emp2,emp3,emp4])

running = True
def update(delta):
    for i in [emp,emp1,emp2,emp3,emp4]:
        i.anglesetter(i.angle + 1)

    updrainbow(ctx, ctx.rcol)
    ctx.psurface.fill(ctx.bgcol)
    ctx.deg += ctx.spinvel
    ctx.objects = ctx.squares + ctx.balls
    ctx.bcount = len(ctx.balls)
    GUI.handle(elegui)

    if ctx.bring:
        mousex, mousey = pygame.mouse.get_pos()
        mouserelx, mouserely = pygame.mouse.get_rel()
        mousex, mousey = mousex - (ctx.width / 2), mousey - (ctx.height / 2)
        mousex, mousey = mousex * ((ctx.pwidth + ctx.windowpad) / ctx.width), mousey * ((ctx.pheight + ctx.windowpad) / ctx.height)
        ctx.mouserelx, ctx.mouserely = mouserelx * ((ctx.pwidth + ctx.windowpad) / ctx.width), mouserely * ((ctx.pheight + ctx.windowpad) / ctx.height)
        ctx.mousex, ctx.mousey = mousex + (ctx.pwidth / 2), mousey + (ctx.pheight / 2)

    for i in ctx.objects:
        i.draw()

    for i in ctx.squares:
        i.calcpoints()
        i.angle += 0

    small_screen = pygame.transform.scale(ctx.psurface, (ctx.scalewidth, ctx.scaleheight))
    pixelated_screen = pygame.transform.scale(small_screen, (ctx.width, ctx.height))
    ctx.screen.blit(pixelated_screen, (0, 0))

    if ctx.guitoggle:
        ctx.manager.update(delta)
        ctx.manager.draw_ui(ctx.screen)

    pygame.display.flip()

def physicsupdate(pdelta):
    for i in ctx.balls:
        i.movecalc(pdelta)

    for _ in range(ctx.passes):
        for i in range(len(ctx.objects)):
            for j in range(i + 1, len(ctx.objects)):
                o1, o2 = ctx.objects[i], ctx.objects[j]
                collision.collide(o1,o2)

        for ball in ctx.balls:
            ball.boundarycheckx()
            ball.boundarychecky()

    for i in ctx.objects:
        i.movecalc2(pdelta)
        if ctx.bring:
            if i.objid == 0 and not i.static:
                i.x,i.y = ctx.mousex,ctx.mousey
                i.dx, i.dy = ctx.mouserelx * 50, ctx.mouserely * 50

etime = 0
lastupd = 0
lastphysicsupd = 0
pdtime = 1

while running:
    etime = time.time()

    if etime - lastupd >= 1 / ctx.framerate:
        update(etime - lastupd)
        lastupd = time.time()

    physicsupdate(pdtime)
    ctx.frames.append(1 / (time.time() - lastphysicsupd))
    ctx.frames.pop(0)
    elegui.framelabel.set_text(f"{round(sum(ctx.frames) / len(ctx.frames))}fps")
    lastphysicsupd = time.time()
    pdtime = lastphysicsupd - etime