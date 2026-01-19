from common import *

class Empty:
    objid = 3
    def __init__(self, x = ctx.pwidth / 2, y = ctx.pheight / 2, angle = 0, spinvel = 0, children = []):
        self.x = x
        self.y = y
        self.angle = angle
        self.spinvel = spinvel
        self.children = children

    def possetter(self, pos):
        change = pos[0] - self.x, pos[1] - self.y
        for i in self.children:
            if i.objid == 3:
               i.possetter((i.x + change[0], i.y + change[1]))
            elif i.objid == 2:
                i.p1[0] += change[0]
                i.p2[0] += change[0]
                i.p1[1] += change[1]
                i.p2[1] += change[1]
            elif i.objid == 1:
                i.x += change[0]
                i.y += change[1]
                i.calcpoints()
            else:
                i.x += change[0]
                i.y += change[1]

        self.x, self.y = pos


    def anglesetter(self, newangle):
        change = newangle - self.angle
        for i in self.children:
            if i.objid == 3:
                relpos = i.x - self.x, i.y - self.y
                rotpos = rotatepoint(relpos, change)
                i.anglesetter(i.angle + change)
                i.possetter((rotpos[0] + self.x, rotpos[1] + self.y))
            elif i.objid == 2:
                relpos = i.p1[0] - self.x, i.p1[1] - self.y
                rotpos = rotatepoint(relpos, change)
                i.p1[0] = rotpos[0] + self.x
                i.p1[1] = rotpos[1] + self.y

                relpos = i.p2[0] - self.x, i.p2[1] - self.y
                rotpos = rotatepoint(relpos, change)
                i.p2[0] = rotpos[0] + self.x
                i.p2[1] = rotpos[1] + self.y
            elif i.objid == 1:
                relpos = i.x - self.x, i.y - self.y
                rotpos = rotatepoint(relpos, change)
                i.x = rotpos[0] + self.x
                i.y = rotpos[1] + self.y
                i.angle += change
                i.calcpoints()
            else:
                relpos = i.x - self.x, i.y - self.y
                rotpos = rotatepoint(relpos, change)
                i.x = rotpos[0] + self.x
                i.y = rotpos[1] + self.y
        self.angle = newangle
    def movecalc(self, delta):
        pass
    def movecalc2(self, delta):
        pass
    def draw(self):
        pass