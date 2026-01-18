from common import *

class Ball:
    forces = []
    objid = 0
    def __init__(self, radius=5, x=ctx.pwidth / 2, y=ctx.pheight / 2, dx=0, dy=0, ax = 0, ay = 0, mass = 1, drawtrail = False, static = False):
        self.x, self.y = x, y
        self.prevx, self.prevy = x, y
        self.dx, self.dy = dx, dy
        self.ax, self.ay = ax,ay
        self.radius = radius
        self.yapply, self.xapply = True, True
        self.multix, self.multiy = 0.5, 0.5
        self.mass = mass
        self.massless = True if mass == 0 else False
        self.infmass = True if mass == -1 else False
        self.static = static
        self.drawtrail = drawtrail
        self.points = []
        self.selected = False

    def movecalc(self, delta):
        if self.static:
            return
        self.prevy, self.prevx = self.y, self.x
        self.multix, self.multiy = 0.5, 0.5
        self.yapply, self.xapply = True, True

        self.x += self.dx * delta
        self.y += self.dy * delta

    def movecalc2(self, delta):
        if self.static:
            return
        self.forces = [[ctx.gmag * ctx.gflip, ctx.deg]]
        self.ax, self.ay = resolve_forces(self.forces)
        if self.xapply:
            self.dx += self.ax * delta
        else:
            self.dx += self.ax * self.multix * delta
        if self.yapply:
            self.dy += self.ay * delta
        else:
            self.dy += self.ay * self.multiy * delta


    def boundarychecky(self):
        if self.radius <= self.y <= ctx.pheight - self.radius:
            return

        if self.radius >= self.y:
            self.clipy = self.y
            self.y = self.radius
            self.dy = abs(self.dy) * ctx.restitution
            self.multiy = boundary_difference(self, True, True, ctx)
            self.yapply = False

        else:
            self.clipy = self.y
            self.y = ctx.pheight - self.radius
            self.dy = abs(self.dy) * ctx.restitution * -1
            self.multiy = boundary_difference(self, True, False, ctx)
            self.yapply = False
        self.dx *= ctx.friction

    def boundarycheckx(self):
        if self.radius <= self.x <= ctx.pwidth - self.radius:
            return

        if self.radius >= self.x:
            self.clipx = self.x
            self.x = self.radius
            self.dx = abs(self.dx) * ctx.restitution
            self.multix = boundary_difference(self, False, True, ctx)
            self.xapply = False

        else:
            self.clipx = self.x
            self.x = ctx.pwidth - self.radius
            self.dx = abs(self.dx) * ctx.restitution * -1
            self.multix = boundary_difference(self, False, False, ctx)
            self.xapply = False
        self.dy *= ctx.friction


    def draw(self):
        if self.drawtrail:
            self.points.append([self.x, self.y])
            for i in range(len(self.points) - 1):
                pygame.draw.line(ctx.psurface, (0, 0, 10 * min(25.5, math.dist((self.points[i][0], self.points[i][1]), (self.points[i + 1][0], self.points[i + 1][1])) / 2)),
                                 (self.points[i][0] + (ctx.windowpad / 2), self.points[i][1] + (ctx.windowpad / 2)),
                                 (self.points[i + 1][0] + (ctx.windowpad / 2), self.points[i + 1][1] + (ctx.windowpad / 2)), 2)
            if len(self.points) >= 200:
                self.points.pop(0)

        if self.selected:
            pygame.draw.circle(ctx.psurface, (0, 0, 255), (self.x + (ctx.windowpad / 2), self.y + (ctx.windowpad / 2)), self.radius)
            pygame.draw.circle(ctx.psurface, ctx.col2, (self.x + (ctx.windowpad / 2), self.y + (ctx.windowpad / 2)), self.radius - math.ceil(self.radius / 5))
            return
        pygame.draw.circle(ctx.psurface, ctx.col, (self.x + (ctx.windowpad / 2), self.y + (ctx.windowpad / 2)), self.radius)
        pygame.draw.circle(ctx.psurface, ctx.col2, (self.x + (ctx.windowpad / 2), self.y + (ctx.windowpad / 2)), self.radius - math.ceil(self.radius / 5))