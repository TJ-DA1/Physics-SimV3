from common import *

class Square:
    objid = 1
    def __init__(self, x = ctx.pwidth / 2, y = ctx.pheight / 2, angle = 0, sizex = 100, sizey = 100, spinvel = 0):
        self.x, self.y = x, y
        self.angle = angle
        self.sizex = sizex
        self.sizey = sizey
        self.spinvel = spinvel
        self.points = []
        self.lines = []
        self.calcpoints() #Ensures points are correct when instantiated
        self.selected = False

    def calcpoints(self):
        self.points, self.lines = calcpoints(self.sizex, self.sizey, self.x, self.y, self.angle, ctx.windowpad / 2) #Returns points of square given angle, size, position

    def draw(self):
        if self.selected and ctx.editortoggle:
            pygame.draw.polygon(ctx.psurface, ctx.col2, self.points, 0) #Draws square and blue outline when selected in editor
            pygame.draw.polygon(ctx.psurface, (0, 0, 255), self.points, math.ceil((self.sizex + self.sizey) / 60))
            return
        pygame.draw.polygon(ctx.psurface, ctx.col2, self.points, 0) #Draws square with outline when not selected and not in editor
        pygame.draw.polygon(ctx.psurface, ctx.col, self.points, math.ceil((self.sizex + self.sizey) / 60))


