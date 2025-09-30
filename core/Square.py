from common.definitions import *

class Square:
    col = col
    col2 = col2
    rest = restitution
    fric = friction
    def __init__(self, x = pwidth / 2, y = pheight / 2, angle = 0, sizex = 100, sizey = 100):
        self.x, self.y = x, y
        self.angle = angle
        self.sizex = sizex
        self.sizey = sizey
        self.points = []
        self.lines = []
        self.calcpoints()
        self.radius = rad

    def calcpoints(self):
        self.points = []
        self.lines = []
        diag = math.dist((0,0),(self.sizex,self.sizey)) / 2
        rectang = math.radians(45) - math.atan2(self.sizey, self.sizex)

        for i in range(4):
            ang = (math.pi * 0.5 * i) - math.radians(45) + math.radians(self.angle) + (rectang * ((-1) ** i))
            xcoord = self.x + (diag * math.cos(ang)) + windowpad / 2
            ycoord = self.y + (diag * math.sin(ang)) + windowpad / 2
            self.points.append((xcoord, ycoord))
        self.lines = [(self.points[i], self.points[(i+1) if not (i+1) >= 4 else 0]) for i in range(4)]

    def draw(self, colour, colour2):
        pygame.draw.polygon(psurface, colour, self.points, 0)
        pygame.draw.polygon(psurface, colour2, self.points, math.ceil((self.sizex + self.sizey) / 60))

    def movecalc(self):
        pass
    def movecalc2(self):
        pass
    def boundarycheckx(self):
        pass
    def boundarychecky(self):
        pass

