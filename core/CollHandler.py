import math

from common import *

class CollHandler:
    def collide(self, one, two):
        if one.objid == 3 or two.objid == 3:
            return
        elif (one.objid == 1 or one.objid == 2) and (two.objid == 1 or two.objid == 2):
            return

        if one.objid == 1:
            self.checkcirclesquare(two, one)
        elif two.objid == 1:
            self.checkcirclesquare(one, two)

        elif one.objid == 2:
            self.checkcircleline(two, one)
        elif two.objid == 2:
            self.checkcircleline(one, two)

        elif self.checkcircle(one, two):
            if (one.massless and two.massless) or (one.infmass and two.infmass):
                return
            elif one.infmass or two.massless:
                self.colledgecase(two, one)
                self.overlapedgecase(two, one)
            elif two.infmass or one.massless:
                self.colledgecase(one, two)
                self.overlapedgecase(one, two)
            else:
                self.collcircle(one, two)
                self.overlapcircle(one, two)
        return

    def checkcircle(self, b1, b2):
        if math.dist((b1.x, b1.y), (b2.x, b2.y)) <= b1.radius + b2.radius:
            return True
        else:
            return False

    def checkcirclesquare(self, b, s):
        if b.static:
            return
        #pygame.draw.rect(psurface,col,(windowpad/2,windowpad/2, s.sizex, s.sizey), 3)
        if math.dist((b.x, b.y), (s.x, s.y)) > (max(s.sizex, s.sizey) * 0.5 * (2 ** (1 / 2))) + b.radius:
            return

        relbpos = [b.x - s.x, b.y - s.y]
        relcpos = rotatepoint(relbpos, -s.angle)
        relcpos[0] += s.sizex / 2
        relcpos[1] += s.sizey / 2

        #pygame.draw.circle(psurface, col, (relcpos[0], relcpos[1]), b.radius, 3)

        testx = relcpos[0]
        testy = relcpos[1]

        if relcpos[0] < 0:
            testx = 0
        elif relcpos[0] > s.sizex:
            testx = s.sizex

        if relcpos[1] < 0:
            testy = 0
        elif relcpos[1] > s.sizey:
            testy = s.sizey

        distx = relcpos[0] - testx
        disty = relcpos[1] - testy

        dist = math.dist((0, 0), (distx, disty))

        if dist <= b.radius:
            relcpos[0] *= s.sizey / s.sizex
            temp = [math.dist((relcpos[0], relcpos[1]), (s.sizey / 2, 0)),
                    math.dist((relcpos[0], relcpos[1]), (0, s.sizey / 2)),
                    math.dist((relcpos[0], relcpos[1]), (s.sizey, s.sizey / 2)),
                    math.dist((relcpos[0], relcpos[1]), (s.sizey / 2, s.sizey))]
            side = [2, 3, 4, 1][temp.index(max(temp))]

            self.collcirclesquare(b, s, side, dist)

    def checkcircleline(self, b, l):
        if b.static:
            return
        center = (l.p2[0] + l.p1[0]) / 2, (l.p2[1] + l.p1[1]) / 2
        dist = abs((b.x * (l.p2[1] - l.p1[1])) - (b.y * (l.p2[0] - l.p1[0])) + (l.p2[0] * l.p1[1]) - (l.p2[1] * l.p1[0]))
        dist /= math.dist(l.p1,l.p2)
        if (dist < b.radius) and (math.dist((b.x, b.y), center) <= b.radius + (math.dist(l.p1, center))):
            self.collcircleline(b, l, dist)

    def overlapcircle(self, b1, b2):
        diffx, diffy = b2.x - b1.x, b2.y - b1.y
        collangle = math.atan2(diffy, diffx)
        distance = math.dist((b1.x, b1.y), (b2.x, b2.y))
        overlap = (b1.radius + b2.radius - distance) / 2
        correctionx = overlap * math.cos(collangle)
        correctiony = overlap * math.sin(collangle)

        b1.x -= correctionx
        b1.y -= correctiony
        b2.x += correctionx
        b2.y += correctiony

    def overlapcirclesquare(self, b, dist, s, side):
        overlap = dist - b.radius
        collangle = math.radians([s.angle + 90, s.angle + 270, s.angle + 180, s.angle][side - 1])

        b.x += overlap * math.cos(collangle)
        b.y += overlap * math.sin(collangle)

    def overlapcircleline(self, b, l, dist):
        direction = math.copysign(-1,(b.prevx - l.p1[0]) * (l.p2[1] - l.p1[1]) - (b.prevy - l.p1[1]) * (l.p2[0] - l.p1[0]))
        overlap = dist - b.radius
        corrangle = math.atan2(l.p2[1] - l.p1[1], l.p2[0] - l.p1[0]) - direction * math.pi / 2
        b.x -= overlap * math.cos(corrangle)
        b.y -= overlap * math.sin(corrangle)

    def collcircle(self, b1, b2):
        diffx, diffy = b2.x - b1.x, b2.y - b1.y
        collangle = math.atan2(diffy, diffx)
        b1norm = (b1.dx * math.cos(collangle)) + (b1.dy * math.sin(collangle))
        b1tan = (-1 * b1.dx * math.sin(collangle)) + (b1.dy * math.cos(collangle))
        b2norm = (b2.dx * math.cos(collangle)) + (b2.dy * math.sin(collangle))
        b2tan = (-1 * b2.dx * math.sin(collangle)) + (b2.dy * math.cos(collangle))

        b1normtemp = (b1.mass * b1norm + b2.mass * b2norm - b2.mass * ctx.restitution * (b1norm - b2norm)) / (b1.mass + b2.mass)
        b2normtemp = ctx.restitution * (b1norm - b2norm) + b1normtemp
        b1norm, b2norm = b1normtemp, b2normtemp

        b1.dx = (b1norm * math.cos(collangle)) - (b1tan * math.sin(collangle))
        b1.dy = (b1norm * math.sin(collangle)) + (b1tan * math.cos(collangle))
        b2.dx = (b2norm * math.cos(collangle)) - (b2tan * math.sin(collangle))
        b2.dy = (b2norm * math.sin(collangle)) + (b2tan * math.cos(collangle))

    def collcirclesquare(self, b, s, side, dist):
        collangle = math.radians([s.angle + 90, s.angle + 270, s.angle, s.angle + 180][side - 1])
        b1norm = (b.dx * math.cos(collangle)) + (b.dy * math.sin(collangle))
        b1tan = (-1 * b.dx * math.sin(collangle)) + (b.dy * math.cos(collangle))
        rest = ctx.restitution ** (1 / ctx.passes)
        fric = ctx.friction ** (1 / ctx.passes)
        b.dx = -rest * b1norm * math.cos(collangle) - b1tan * math.sin(collangle) * fric
        b.dy = -rest * b1norm * math.sin(collangle) + b1tan * math.cos(collangle) * fric

        self.overlapcirclesquare(b,dist,s,side)

    def collcircleline(self, b, l, dist):
        e = ctx.restitution
        x, y = l.p2[0] - l.p1[0], l.p2[1] - l.p1[1]
        ux, uy = b.dx, b.dy
        v1 = (ux * (x ** 2 - e * y ** 2) + (uy * x * y * (1 + e)))
        v2 = (uy * (y ** 2 - e * x ** 2) + (ux * x * y * (1 + e)))
        vector = (v1, v2)
        scalar = 1 / (x ** 2 + y ** 2)
        b.dx, b.dy = multiplyvector(vector, scalar)

        self.overlapcircleline(b,l,dist)

    def colledgecase(self, b1, b2):
        diffx, diffy = b2.x - b1.x, b2.y - b1.y
        collangle = math.atan2(diffy, diffx)
        b1norm = (b1.dx * math.cos(collangle)) + (b1.dy * math.sin(collangle))
        b1tan = (-1 * b1.dx * math.sin(collangle)) + (b1.dy * math.cos(collangle))
        b1.dx = -ctx.restitution * b1norm * math.cos(collangle) - b1tan * math.sin(collangle)
        b1.dy = -ctx.restitution * b1norm * math.sin(collangle) + b1tan * math.cos(collangle)

    def overlapedgecase(self, b1, b2):
        diffx, diffy = b2.x - b1.x, b2.y - b1.y
        distance = math.dist((b1.x, b1.y), (b2.x, b2.y))
        overlap = b1.radius + b2.radius - distance

        if distance == 0:
            diffx = 0.1 if b2.prevx >= b1.prevx else -0.1
            diffy = 0.1 if b2.prevy >= b1.prevy else -0.1
            distance = 0.1

        nx, ny = diffx / distance, diffy / distance

        b1.x -= (overlap * nx)
        b1.y -= (overlap * ny)