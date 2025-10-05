import math

from common import *
from .Square import *

class CollHandler:
    def __init__(self, context):
        self.ctx = context

    def collide(self, one, two):
        if one is two:
            return
        elif type(one) is Square and type(two) is Square:
            return

        if type(one) is Square:
            self.checkcirclesquare(two, one)
        elif type(two) is Square:
            self.checkcirclesquare(one, two)

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
        relcpos = [relbpos[0] * math.cos(math.radians(-s.angle)) - relbpos[1] * math.sin(math.radians(-s.angle)),
                   relbpos[0] * math.sin(math.radians(-s.angle)) + relbpos[1] * math.cos(math.radians(-s.angle))]
        relcpos[0] += s.sizex / 2
        relcpos[1] += s.sizey / 2

        # pygame.draw.circle(psurface, col, (relcpos[0], relcpos[1]), b.radius, 3)

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

    def overlapcircle(self, b1, b2):
        diffx, diffy = b2.x - b1.x, b2.y - b1.y
        distance = math.dist((b1.x, b1.y), (b2.x, b2.y))
        overlap = b1.radius + b2.radius - distance

        if distance == 0:
            diffx = 0.1 if b2.prevx >= b1.prevx else -0.1
            diffy = 0.1 if b2.prevy >= b1.prevy else -0.1
            distance = 0.1

        nx, ny = diffx / distance, diffy / distance
        correction = overlap / 2
        b1.x -= (correction * nx)
        b1.y -= (correction * ny)
        b2.x += (correction * nx)
        b2.y += (correction * ny)

    def overlapcirclesquare(self, b, dist, s, side):
        overlap = dist - b.radius
        collangle = math.radians([s.angle + 90, s.angle + 270, s.angle + 180, s.angle][side - 1])

        b.x += overlap * math.cos(collangle)
        b.y += overlap * math.sin(collangle)

    def collcirclesquare(self, b, s, side, dist):
        collangle = math.radians([s.angle + 90, s.angle + 270, s.angle, s.angle + 180][side - 1])
        b1norm = (b.dx * math.cos(collangle)) + (b.dy * math.sin(collangle))
        b1tan = (-1 * b.dx * math.sin(collangle)) + (b.dy * math.cos(collangle))
        rest = b.rest ** (1 / passes)
        fric = b.fric ** (1 / passes)
        b.dx = -rest * b1norm * math.cos(collangle) - b1tan * math.sin(collangle) * fric
        b.dy = -rest * b1norm * math.sin(collangle) + b1tan * math.cos(collangle) * fric

        self.overlapcirclesquare(b, dist, s, side)

    def collcircle(self, b1, b2):
        diffx, diffy = b2.x - b1.x, b2.y - b1.y
        collangle = math.atan2(diffy, diffx)
        b1norm = (b1.dx * math.cos(collangle)) + (b1.dy * math.sin(collangle))
        b1tan = (-1 * b1.dx * math.sin(collangle)) + (b1.dy * math.cos(collangle))
        b2norm = (b2.dx * math.cos(collangle)) + (b2.dy * math.sin(collangle))
        b2tan = (-1 * b2.dx * math.sin(collangle)) + (b2.dy * math.cos(collangle))

        b1normtemp = (b1.mass * b1norm + b2.mass * b2norm - b2.mass * b1.rest * (b1norm - b2norm)) / (b1.mass + b2.mass)
        b2normtemp = b1.rest * (b1norm - b2norm) + b1normtemp
        b1norm, b2norm = b1normtemp, b2normtemp

        b1.dx = (b1norm * math.cos(collangle)) - (b1tan * math.sin(collangle))
        b1.dy = (b1norm * math.sin(collangle)) + (b1tan * math.cos(collangle))
        b2.dx = (b2norm * math.cos(collangle)) - (b2tan * math.sin(collangle))
        b2.dy = (b2norm * math.sin(collangle)) + (b2tan * math.cos(collangle))


    def colledgecase(self, b1, b2):
        diffx, diffy = b2.x - b1.x, b2.y - b1.y
        collangle = math.atan2(diffy, diffx)
        b1norm = (b1.dx * math.cos(collangle)) + (b1.dy * math.sin(collangle))
        b1tan = (-1 * b1.dx * math.sin(collangle)) + (b1.dy * math.cos(collangle))
        b1.dx = -b1.rest * b1norm * math.cos(collangle) - b1tan * math.sin(collangle)
        b1.dy = -b1.rest * b1norm * math.sin(collangle) + b1tan * math.cos(collangle)

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