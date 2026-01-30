from common import *
class Line:
    objid = 2
    def __init__(self, p1 = (0,0), p2 = (ctx.pwidth, ctx.pheight)):
        self.p1 = list(p1)
        self.p2 = list(p2)
        self.static = True
        self.selected = False

    def draw(self):
        if self.selected and ctx.editortoggle:
            pygame.draw.line(ctx.psurface,
                             (0,0,255),
                             (self.p1[0] + (ctx.windowpad / 2), self.p1[1] + (ctx.windowpad / 2)),
                             (self.p2[0] + (ctx.windowpad / 2), self.p2[1] + (ctx.windowpad / 2)),
                             3
                             ) #Draws blue line when selected in editor
            return
        pygame.draw.line(ctx.psurface,
                         ctx.col,
                         (self.p1[0] + (ctx.windowpad / 2), self.p1[1] + (ctx.windowpad / 2)),
                         (self.p2[0] + (ctx.windowpad / 2), self.p2[1] + (ctx.windowpad / 2)),
                         3
                         ) #Draws main colour line when not selected / not in editor






