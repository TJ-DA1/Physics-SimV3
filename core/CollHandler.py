import math
from common import *

class CollHandler:
    def collide(self, one, two):
        if ctx.bring or one.objid == 3 or two.objid == 3:
            return

        elif (one.objid == 1 or one.objid == 2) and (two.objid == 1 or two.objid == 2):
            return

        elif one.objid == 1:
            self.checkcirclesquare(two, one)
        elif two.objid == 1:
            self.checkcirclesquare(one, two)

        elif one.objid == 2:
            self.checkcircleline(two, one)
        elif two.objid == 2:
            self.checkcircleline(one, two)

        elif (one.massless and two.massless) or (one.infmass and two.infmass):
            return
        elif one.infmass or two.massless or one.static:
            self.checkcircle(two, one, True)
        elif two.infmass or one.massless or two.static:
            self.checkcircle(one, two, True)
        else:
            self.checkcircle(one, two, False)

    def checkcircle(self, b1, b2, edge): #Checks the distance against sum of radii
        if ((b2.x - b1.x) ** 2) + ((b2.y - b1.y) ** 2) <= (b1.radius + b2.radius) ** 2:
            if edge:
                self.colledgecase(b1, b2)
            else:
                self.collcircle(b1, b2)

    def checkcirclesquare(self, b, s):
        if b.static:
            return
        #pygame.draw.rect(psurface,col,(windowpad/2,windowpad/2, s.sizex, s.sizey), 3)
        if ((s.x - b.x) ** 2) + ((s.y - b.y) ** 2) > ((max(s.sizex, s.sizey) * 0.5 * (2 ** (1 / 2))) + b.radius) ** 2: #Heuristic check
            return

        relbpos = [b.x - s.x, b.y - s.y] #Tranlate circle position to square reference frame
        relcpos = rotatepoint(relbpos, -s.angle)
        relcpos[0] += s.sizex / 2
        relcpos[1] += s.sizey / 2

        #pygame.draw.circle(psurface, col, (relcpos[0], relcpos[1]), b.radius, 3)

        testx = relcpos[0]
        testy = relcpos[1]

        if relcpos[0] < 0: #Check ball position against square horizontal sides
            testx = 0
        elif relcpos[0] > s.sizex:
            testx = s.sizex

        if relcpos[1] < 0: #Check ball position against square vertical sides
            testy = 0
        elif relcpos[1] > s.sizey:
            testy = s.sizey

        distx = relcpos[0] - testx
        disty = relcpos[1] - testy

        dist = math.dist((0, 0), (distx, disty)) #Final distance check

        if dist <= b.radius:
            relcpos[0] *= s.sizey / s.sizex #Finds which side ball has collided with using distance
            temp = [math.dist((relcpos[0], relcpos[1]), (s.sizey / 2, 0)),
                    math.dist((relcpos[0], relcpos[1]), (0, s.sizey / 2)),
                    math.dist((relcpos[0], relcpos[1]), (s.sizey, s.sizey / 2)),
                    math.dist((relcpos[0], relcpos[1]), (s.sizey / 2, s.sizey))]
            side = [2, 3, 4, 1][temp.index(max(temp))]

            self.collcirclesquare(b, s, side, dist)

    def checkcircleline(self, b, l):
        if b.static:
            return
        center = (l.p2[0] + l.p1[0]) / 2, (l.p2[1] + l.p1[1]) / 2 #Distance of closest approach formulae
        dist = abs((b.x * (l.p2[1] - l.p1[1])) - (b.y * (l.p2[0] - l.p1[0])) + (l.p2[0] * l.p1[1]) - (l.p2[1] * l.p1[0]))
        dist /= math.dist(l.p1,l.p2)
        if (dist < b.radius) and (math.dist((b.x, b.y), center) + 1 <= b.radius + (math.dist(l.p1, center))): #Extra condition to check circle is not at end of line segment
            self.collcircleline(b, l, dist)

    def overlapcircle(self, b1, b2, collangle, distance): #Finds overlap and uses trig to move balls away from each other
        overlap = (b1.radius + b2.radius - distance) / 2
        correctionx = overlap * math.cos(collangle)
        correctiony = overlap * math.sin(collangle)

        b1.x -= correctionx #Each gets half the overlap to ensure no overlap
        b1.y -= correctiony
        b2.x += correctionx
        b2.y += correctiony

    def overlapcirclesquare(self, b, dist, s, side):
        overlap = dist - b.radius #Uses distance calculated in checking to push ball out of square
        collangle = math.radians([s.angle + 90, s.angle + 270, s.angle + 180, s.angle][side - 1])

        b.x += overlap * math.cos(collangle)
        b.y += overlap * math.sin(collangle)

    def overlapcircleline(self, b, l, dist):
        direction = math.copysign(-1,(b.prevx - l.p1[0]) * (l.p2[1] - l.p1[1]) - (b.prevy - l.p1[1]) * (l.p2[0] - l.p1[0])) #Uses previous position to check which way to correct
        overlap = dist - b.radius #Uses distance calculated in checking to push ball out of line
        corrangle = math.atan2(l.p2[1] - l.p1[1], l.p2[0] - l.p1[0]) - direction * math.pi / 2
        b.x -= overlap * math.cos(corrangle)
        b.y -= overlap * math.sin(corrangle)

    def collcircle(self, b1, b2):
        diffx, diffy = b2.x - b1.x, b2.y - b1.y
        collangle = math.atan2(diffy, diffx)
        sin = math.sin(collangle)
        cos = math.cos(collangle)
        b1norm = (b1.dx * cos) + (b1.dy * sin) #Split ball velocity into tangential and normal components
        b1tan = (-1 * b1.dx * sin) + (b1.dy * cos)
        b2norm = (b2.dx * cos) + (b2.dy * sin)
        b2tan = (-1 * b2.dx * sin) + (b2.dy * cos)

        b1normtemp = (b1.mass * b1norm + b2.mass * b2norm - b2.mass * ctx.restitution * (b1norm - b2norm)) / (b1.mass + b2.mass) #Restitution calculations
        b2normtemp = ctx.restitution * (b1norm - b2norm) + b1normtemp
        b1norm, b2norm = b1normtemp, b2normtemp

        b1.dx = (b1norm * cos) - (b1tan * sin) #Combine normal and tangential into X and Y
        b1.dy = (b1norm * sin) + (b1tan * cos)
        b2.dx = (b2norm * cos) - (b2tan * sin)
        b2.dy = (b2norm * sin) + (b2tan * cos)

        self.overlapcircle(b1, b2, collangle, math.dist((0,0), (diffx, diffy)))

    def collcirclesquare(self, b, s, side, dist):
        collangle = math.radians([s.angle + 90, s.angle + 270, s.angle, s.angle + 180][side - 1])
        sin = math.sin(collangle)
        cos = math.cos(collangle)
        b1norm = (b.dx * cos) + (b.dy * sin) #Split velocity into tangential and normal
        b1tan = (-1 * b.dx * sin) + (b.dy * cos)
        rest = ctx.restitution #Apply energy loss - reduced for higher passes due to repeated collisions
        fric = ctx.friction ** (1 / ctx.passes)

        b.dx = -rest * b1norm * cos - b1tan * sin * fric #Combine into X and Y components
        b.dy = -rest * b1norm * sin + b1tan * cos * fric

        self.overlapcirclesquare(b,dist - 0.5,s,side)

    def collcircleline(self, b, l, dist):
        e = ctx.restitution #Oblique collision formulae
        x, y = l.p2[0] - l.p1[0], l.p2[1] - l.p1[1]
        ux, uy = b.dx, b.dy
        v1 = (ux * (x ** 2 - e * y ** 2) + (uy * x * y * (1 + e)))
        v2 = (uy * (y ** 2 - e * x ** 2) + (ux * x * y * (1 + e)))
        vector = (v1, v2)
        scalar = 1 / (x ** 2 + y ** 2)
        b.dx, b.dy = multiplyvector(vector, scalar)

        self.overlapcircleline(b,l,dist )

    def colledgecase(self, b1, b2):
        diffx, diffy = b2.x - b1.x, b2.y - b1.y
        collangle = math.atan2(diffy, diffx)
        sin = math.sin(collangle)
        cos = math.cos(collangle)
        b1norm = (b1.dx * cos) + (b1.dy * sin) #Split velocity into tangential and normal
        b1tan = (-1 * b1.dx * sin) + (b1.dy * cos)
        b1.dx = -ctx.restitution * b1norm * cos - b1tan * sin #Combine into X and Y components
        b1.dy = -ctx.restitution * b1norm * sin + b1tan * cos

        self.overlapedgecase(b1, b2, collangle, math.dist((0,0), (diffx, diffy)))

    def overlapedgecase(self, b1, b2, collangle, distance):
        overlap = (b1.radius + b2.radius - distance) / 2 #Same as normal but only correct one ball
        correctionx = overlap * math.cos(collangle)
        correctiony = overlap * math.sin(collangle)

        b1.x -= correctionx #Push ball away from unaffected ball
        b1.y -= correctiony