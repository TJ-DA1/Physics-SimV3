from core import *
from interface import *
from examples import *


context = SimulationContext()
collision = CollHandler(context)
interface = GUIHandler(context, Ball, Square)

preconfiguration = "figure"

context.squares += preconfig[preconfiguration][0]
context.balls += preconfig[preconfiguration][1]

context.balls += create_ball(Ball, bcount, rad)

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