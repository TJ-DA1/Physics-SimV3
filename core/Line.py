from common import *
class Line:
    objid = 2
    def __init__(self, p1 = (0,0), p2 = (ctx.pwidth, ctx.pheight)):
        self.p1 = list(p1)
        self.p2 = list(p2)
        self.static = True
    def draw(self):
        pygame.draw.line(ctx.psurface, ctx.col, self.p1, self.p2, 3)
    def movecalc(self, delta):
        pass
    def movecalc2(self, delta):
        pass