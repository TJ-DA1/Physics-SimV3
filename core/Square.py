from common import *

class Square:
    objid = 1
    def __init__(self, x =ctx.pwidth / 2, y =ctx.pheight / 2, angle = 0, sizex = 100, sizey = 100):
        self.x, self.y = x, y
        self.angle = angle
        self.sizex = sizex
        self.sizey = sizey
        self.points = []
        self.lines = []
        self.calcpoints()
        self.selected = False

    def calcpoints(self):
        self.points = []
        self.lines = []
        diag = math.dist((0,0),(self.sizex,self.sizey)) / 2
        rectang = math.radians(45) - math.atan2(self.sizey, self.sizex)

        for i in range(4):
            ang = (math.pi * 0.5 * i) - math.radians(45) + math.radians(self.angle) + (rectang * ((-1) ** i))
            xcoord = self.x + (diag * math.cos(ang)) + ctx.windowpad / 2
            ycoord = self.y + (diag * math.sin(ang)) + ctx.windowpad / 2
            self.points.append((xcoord, ycoord))
        self.lines = [(self.points[i], self.points[(i+1) if not (i+1) >= 4 else 0]) for i in range(4)]

    def draw(self):
        if self.selected:
            pygame.draw.polygon(ctx.psurface, ctx.col2, self.points, 0)
            pygame.draw.polygon(ctx.psurface, (0, 0, 255), self.points, math.ceil((self.sizex + self.sizey) / 60))
            return
        pygame.draw.polygon(ctx.psurface, ctx.col2, self.points, 0)
        pygame.draw.polygon(ctx.psurface, ctx.col, self.points, math.ceil((self.sizex + self.sizey) / 60))

    def movecalc(self, delta):
        pass
    def movecalc2(self, delta):
        pass
    def boundarycheckx(self):
        pass
    def boundarychecky(self):
        pass

