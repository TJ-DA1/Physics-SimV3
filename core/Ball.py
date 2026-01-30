import math

from common import *

class Ball:
    objid = 0
    def __init__(self, radius=5, x = ctx.pwidth / 2, y = ctx.pheight / 2, dx=0, dy=0, ax = 0, ay = 0, mass = 1, drawtrail = False, static = False):
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
        self.forces = []
        self.selected = False

    def movecalc(self, delta): #Applies velocity to position and resets previous positional components
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

        match ctx.gtype:
            case 0: #Uniform gravitational field
                self.forces = [[ctx.gmag * ctx.gflip, math.radians(ctx.deg)]]
            case 1: #Radial - uses inverse square distance from center
                distance = math.dist((self.x, self.y), (ctx.pwidth / 2, ctx.pheight / 2)) / 100
                if distance  < 1:
                    distance = 1
                self.forces = [[ctx.gmag * ctx.gflip / (distance ** 2),math.atan2(self.y - ctx.pheight / 2, self.x - ctx.pwidth / 2) - math.pi]]
            case 2: #Anti-radial - uses inverse square distance from circle touching all corners of sim
                distance = (math.dist((0,0),(ctx.pwidth/2,ctx.pheight/2)) - math.dist((self.x, self.y), (ctx.pwidth / 2, ctx.pheight / 2))) / 100
                if distance < 1:
                    distance = 1
                self.forces = [[ctx.gmag * ctx.gflip / (distance ** 2),math.atan2(self.y - ctx.pheight / 2, self.x - ctx.pwidth / 2)]]
            case 3: #Individual - each ball pulls towards all others
                self.forces = []
                for i in ctx.balls:
                    if i is not self:
                        distance = math.dist((self.x, self.y), (i.x, i.y)) / 100
                        if distance < 2:
                            distance = 2
                        force =  (ctx.gmag * ctx.gflip * i.mass * self.mass) / (distance ** 2)
                        force /= (ctx.bcount) # Reduces force with more balls to prevent weird interactions

                        self.forces += [[force, math.atan2(i.y - self.y, i.x - self.x)]]

        self.ax, self.ay = resolve_forces(self.forces) #Sum of component forces
        if self.xapply: #X and Y apply variables are False when ball is at boundary, reducing application of acceleration when under boundary
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

        if self.radius >= self.y: #Solving for below and above Y boundaries
            self.clipy = self.y
            self.y = self.radius
            self.dy = abs(self.dy) * ctx.restitution #Reflecting velocity
            self.multiy = boundary_difference(self, True, True, ctx) #Returns multiplier of acceleration
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

        if self.radius >= self.x: #Solving for below and above Y boundaries
            self.clipx = self.x
            self.x = self.radius
            self.dx = abs(self.dx) * ctx.restitution #Reflecting velocity
            self.multix = boundary_difference(self, False, True, ctx) #Returns multiplier of acceleration
            self.xapply = False

        else:
            self.clipx = self.x
            self.x = ctx.pwidth - self.radius
            self.dx = abs(self.dx) * ctx.restitution * -1
            self.multix = boundary_difference(self, False, False, ctx)
            self.xapply = False
        self.dy *= ctx.friction


    def draw(self):
        if self.drawtrail: #Draw trail handling
            self.points.append([self.x, self.y]) #Add new point
            for i in range(len(self.points) - 1):
                pygame.draw.line(ctx.psurface,
                                 (0, 0, 10 * min(25.5, math.dist((self.points[i][0], self.points[i][1]), (self.points[i + 1][0], self.points[i + 1][1])) / 2)),
                                 (self.points[i][0] + (ctx.windowpad / 2), self.points[i][1] + (ctx.windowpad / 2)),
                                 (self.points[i + 1][0] + (ctx.windowpad / 2), self.points[i + 1][1] + (ctx.windowpad / 2)),
                                 2
                                 ) #Draws points with colour depending on length (velocity of ball)
            if len(self.points) >= 200:
                self.points.pop(0) #Enforces max length of points to reduce lag

        if self.selected and ctx.editortoggle:
            pygame.draw.circle(ctx.psurface, (0, 0, 255), (self.x + (ctx.windowpad / 2), self.y + (ctx.windowpad / 2)), self.radius) #Draw circle with blue outline when selected in editor
            pygame.draw.circle(ctx.psurface, ctx.col2, (self.x + (ctx.windowpad / 2), self.y + (ctx.windowpad / 2)), self.radius - math.ceil(self.radius / 5))
            return
        pygame.draw.circle(ctx.psurface, ctx.col, (self.x + (ctx.windowpad / 2), self.y + (ctx.windowpad / 2)), self.radius) #Draw circle and outline when not selected / not in editor
        pygame.draw.circle(ctx.psurface, ctx.col2, (self.x + (ctx.windowpad / 2), self.y + (ctx.windowpad / 2)), self.radius - math.ceil(self.radius / 5))