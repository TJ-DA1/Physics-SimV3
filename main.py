from core import *
from interface import *
from examples import *


context = SimulationContext()
collision = CollHandler(context)
interface = GUIHandler(context, Ball, Square)

preconfiguration = ("plinko")

context.squares += preconfig[preconfiguration][0]
context.balls += preconfig[preconfiguration][1]

context.balls += create_ball(Ball, bcount, context)

running = True

def fixedupdate(ctx):
    ctx.objects = ctx.squares + ctx.balls
    config.bcount = len(ctx.balls)
    ctx.deg += ctx.spinvel

    updrainbow(ctx, ctx.rcol)

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

    mousex, mousey = pygame.mouse.get_pos()
    mouserelx, mouserely = pygame.mouse.get_rel()
    mousex, mousey = mousex - (width / 2), mousey - (height / 2)
    mousex, mousey = mousex * ((pwidth + windowpad) / width), mousey * ((pheight + windowpad) / height)
    mouserelx, mouserely = mouserelx * ((pwidth + windowpad) / width), mouserely * ((pheight + windowpad) / height)
    mousex, mousey = mousex + (pwidth / 2), mousey + (pheight / 2)

    for i in ctx.objects:
        i.movecalc2()
        if ctx.bring:
            if type(i) == Ball and not i.static:
                i.x,i.y = mousex,mousey
                i.dx, i.dy = mouserelx, mouserely

        i.draw(ctx)

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