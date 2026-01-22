from interface import *

GUI = GUIHandler()

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

editorgui = EditorElement()
editorgui.initiate()
elegui = Element()
elegui.initiate()

ctx.screen = pygame.display.set_mode((ctx.width, ctx.height), vsync=1)
ctx.psurface = pygame.Surface((ctx.pwidth + ctx.windowpad, ctx.pheight + ctx.windowpad))
ctx.manager.set_window_resolution((ctx.width, ctx.height))
ctx.editormanager.set_window_resolution((ctx.width, ctx.height))
pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

from core import *
from examples import *

collision = CollHandler()

ctx.squares += preconfig[ctx.preconfiguration][0]
ctx.balls += preconfig[ctx.preconfiguration][1]
ctx.lines += preconfig[ctx.preconfiguration][2]
ctx.empties += preconfig[ctx.preconfiguration][3]

ctx.balls += create_ball(Ball, ctx.bcount, ctx)

running = True
def update(delta):
    ctx.psurface.fill(ctx.bgcol)
    ctx.objects = ctx.balls + ctx.squares + ctx.lines + ctx.empties
    ctx.bcount = len(ctx.balls)
    GUI.handle(elegui, Ball)

    if ctx.bring or ctx.editortoggle:
        mousex, mousey = pygame.mouse.get_pos()
        mouserelx, mouserely = pygame.mouse.get_rel()
        mousex, mousey = mousex - (ctx.width / 2), mousey - (ctx.height / 2)
        mousex, mousey = mousex * ((ctx.pwidth + ctx.windowpad) / ctx.width), mousey * (
                    (ctx.pheight + ctx.windowpad) / ctx.height)
        ctx.mouserelx, ctx.mouserely = mouserelx * ((ctx.pwidth + ctx.windowpad) / ctx.width), mouserely * (
                    (ctx.pheight + ctx.windowpad) / ctx.height)
        ctx.mousex, ctx.mousey = mousex + (ctx.pwidth / 2), mousey + (ctx.pheight / 2)

    if not ctx.editortoggle:
        updrainbow(ctx, ctx.rcol)
        ctx.deg += ctx.spinvel
        for i in ctx.objects:
            if i.objid == 3:
                i.anglesetter(i.angle + i.spinvel)
            elif i.objid == 1:
                i.calcpoints()
                i.angle += i.spinvel

    for i in ctx.objects:
        i.draw()
    if ctx.editortoggle:
        GUI.handleeditor(editorgui, [Ball, Square, Line, Empty])

    small_screen = pygame.transform.scale(ctx.psurface, (ctx.scalewidth, ctx.scaleheight))
    pixelated_screen = pygame.transform.scale(small_screen, (ctx.width, ctx.height))
    ctx.screen.blit(pixelated_screen, (0, 0))

    if ctx.editortoggle:
        ctx.editormanager.update(delta)
        ctx.editormanager.draw_ui(ctx.screen)

    if ctx.guitoggle and not ctx.editortoggle:
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

    for i in ctx.balls:
        i.movecalc2(pdelta)

    if ctx.bring:
        for i in ctx.objects:
            if i.objid == 0 and not i.static:
                i.x,i.y = ctx.mousex,ctx.mousey
                i.dx, i.dy = ctx.mouserelx * 50, ctx.mouserely * 50

etime = 0
lastupd = 0
lastphysicsupd = 0
pdtime = 1
ftime = 1 / ctx.framerate

while running:
    etime = time.time()
    if etime - lastupd >= ftime:
        update(etime - lastupd)
        lastupd = time.time()

    if not ctx.editortoggle:
        physicsupdate(pdtime)
        ctx.frames.append(1 / ((time.time() - lastphysicsupd) + 0.0000001))
        ctx.frames.pop(0)
        elegui.framelabel.set_text(f"{round(sum(ctx.frames) / len(ctx.frames))}fps")
    lastphysicsupd = time.time()
    pdtime = lastphysicsupd - etime