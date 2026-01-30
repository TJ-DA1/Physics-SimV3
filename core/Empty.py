from common import *

class Empty:
    objid = 3
    def __init__(self, x = ctx.pwidth / 2, y = ctx.pheight / 2, angle = 0, spinvel = 0, children = ()):
        self.x = x
        self.y = y
        self.angle = angle
        self.spinvel = spinvel
        self.children = list(children)
        self.selected = False
        self.childselected = False

    def possetter(self, pos):
        change = pos[0] - self.x, pos[1] - self.y
        for i in self.children: #Changes position of all children relative to self
            if i.objid == 3:
               i.possetter((i.x + change[0], i.y + change[1])) #Moves children of children
            elif i.objid == 2:
                i.p1[0] += change[0] #Moves both points of line
                i.p2[0] += change[0]
                i.p1[1] += change[1]
                i.p2[1] += change[1]
            elif i.objid == 1:
                i.x += change[0]
                i.y += change[1]
                i.calcpoints() #Square points must be recalculated immediately
            else:
                i.x += change[0]
                i.y += change[1]

        self.x, self.y = pos

    def anglesetter(self, newangle):
        change = newangle - self.angle
        for i in self.children: #Rotates all children relative to self
            if i.objid == 3: #Empty case
                relpos = i.x - self.x, i.y - self.y
                rotpos = rotatepoint(relpos, change) #Rotate
                i.anglesetter(i.angle + change) #Rotate children
                i.possetter((rotpos[0] + self.x, rotpos[1] + self.y)) #Move child and children of child

            elif i.objid == 2: #Line case
                relpos = i.p1[0] - self.x, i.p1[1] - self.y
                rotpos = rotatepoint(relpos, change) #Rotate point 1
                i.p1[0] = rotpos[0] + self.x #Move point 1
                i.p1[1] = rotpos[1] + self.y

                relpos = i.p2[0] - self.x, i.p2[1] - self.y
                rotpos = rotatepoint(relpos, change) #Rotate point 2
                i.p2[0] = rotpos[0] + self.x #Move point 2
                i.p2[1] = rotpos[1] + self.y

            elif i.objid == 1: #Square case
                relpos = i.x - self.x, i.y - self.y
                rotpos = rotatepoint(relpos, change) #Rotate
                i.x = rotpos[0] + self.x #Move
                i.y = rotpos[1] + self.y
                i.angle += change #Update angle and points
                i.calcpoints()

            else: #Ball case
                relpos = i.x - self.x, i.y - self.y
                rotpos = rotatepoint(relpos, change) #Rotate
                i.x = rotpos[0] + self.x #Move
                i.y = rotpos[1] + self.y
        self.angle = newangle

    def draw(self):
        if ctx.editortoggle: #Empties are invisible when unpaused
            if self.selected and not self.childselected: #Draws blue + symbol to represent selected Empty
                pygame.draw.line(ctx.psurface, (0,0,255), (self.x, self.y + 5), (self.x, self.y - 5), 2)
                pygame.draw.line(ctx.psurface, (0, 0, 255), (self.x + 5, self.y), (self.x - 5, self.y), 2)
            elif self.childselected: #Draws red + symbol to represent Empty with children being edited
                pygame.draw.line(ctx.psurface, (255,0,0), (self.x, self.y + 5), (self.x, self.y - 5), 2)
                pygame.draw.line(ctx.psurface, (255, 0, 0), (self.x + 5, self.y), (self.x - 5, self.y), 2)
            else: #Draws main colour + symbol to represent Empty
                pygame.draw.line(ctx.psurface, ctx.col, (self.x, self.y + 5), (self.x, self.y - 5), 2)
                pygame.draw.line(ctx.psurface, ctx.col, (self.x + 5, self.y), (self.x - 5, self.y), 2)