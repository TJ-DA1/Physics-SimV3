from common.definitions import *

class Ball:
    col = col
    col2 = col2
    rest = restitution
    fric = friction
    forces = []
    def __init__(self, radius=5, padding=0, x=pwidth / 2, y=pheight / 2, dx=0, dy=0, ax = 0, ay = 0, mass = 1, drawtrail = False, static = False):
        self.x, self.y = x, y
        self.prevx, self.prevy = x, y
        self.dx, self.dy = dx, dy
        self.ax, self.ay = ax,ay
        self.padding = padding
        self.radius = radius
        self.yapply, self.xapply = True, True
        self.multix, self.multiy = 0.5, 0.5
        self.mass = mass
        self.massless = True if mass == 0 else False
        self.infmass = True if mass == -1 else False
        self.static = static
        self.drawtrail = drawtrail
        self.points = []

    def movecalc(self):
        if self.static:
            return
        self.prevy, self.prevx = self.y, self.x
        self.multix, self.multiy = 0.5, 0.5
        self.yapply, self.xapply = True, True

        self.x += self.dx
        self.y += self.dy

        if self.drawtrail:
            self.points.append([self.x, self.y])
            for i in range(len(self.points) - 1):
                pygame.draw.line(psurface, (0, 0, 10 * min(25.5, math.dist((self.points[i][0], self.points[i][1]), (self.points[i + 1][0], self.points[i + 1][1])) / 2)),(self.points[i][0] + (windowpad / 2), self.points[i][1] + (windowpad / 2)),(self.points[i + 1][0] + (windowpad / 2), self.points[i + 1][1] + (windowpad / 2)), 2)
            if len(self.points) >= 200:
                self.points.pop(0)

    def movecalc2(self):
        if self.static:
            return
        self.ax, self.ay = resolve_forces(self.forces)
        if self.xapply:
            self.dx += self.ax
        else:
            self.dx += self.ax * self.multix
        if self.yapply:
            self.dy += self.ay
        else:
            self.dy += self.ay * self.multiy


    def boundarychecky(self):
        if self.radius <= self.y <= pheight - self.radius:
            return

        if self.radius >= self.y:
            self.clipy = self.y
            self.y = self.radius
            self.dy = abs(self.dy) * self.fric
            self.multiy = boundary_difference(self, True, True)
            self.yapply = False

        else:
            self.clipy = self.y
            self.y = pheight - self.radius
            self.dy = abs(self.dy) * self.fric * -1
            self.multiy = boundary_difference(self, True, False)
            self.yapply = False
        self.dx *= self.fric

    def boundarycheckx(self):
        if self.radius <= self.x <= pwidth - self.radius:
            return

        if self.radius >= self.x:
            self.clipx = self.x
            self.x = self.radius
            self.dx = abs(self.dx) * self.fric
            self.multix = boundary_difference(self, False, True)
            self.xapply = False

        else:
            self.clipx = self.x
            self.x = pwidth - self.radius
            self.dx = abs(self.dx) * self.fric * -1
            self.multix = boundary_difference(self, False, False)
            self.xapply = False
        self.dy *= self.fric


    def draw(self, colour, colour2):
        pygame.draw.circle(psurface, colour2, (self.x + (windowpad / 2), self.y + (windowpad / 2)), self.radius + self.padding)
        pygame.draw.circle(psurface, colour, (self.x + (windowpad / 2), self.y + (windowpad / 2)), self.radius - math.ceil(self.radius / 5) + self.padding)