import pygame
import time
from .config import *
class SimulationContext:
    def __init__(self):
        self.width = width
        self.height = height
        self.pwidth = pwidth
        self.pheight = pheight
        self.scalewidth = scalewidth
        self.scaleheight = scaleheight
        self.windowpad = windowpad

        self.psurface = None
        self.screen = pygame.display.set_mode((300,400), flags=pygame.SCALED, vsync=1)

        self.guitoggle = True
        self.editortoggle = False
        self.manager = pygame_gui.UIManager((self.width,self.height), "interface/theme.json")
        self.editormanager = pygame_gui.UIManager((self.width,self.height), "interface/theme.json")
        self.prescreen = pygame_gui.UIManager((300,400), "interface/theme.json")
        self.framerate = framerate
        self.frames = [framerate for _ in range(5)]

        self.gmag = gmag
        self.gtype = gtype
        self.gflip = 1
        self.deg = deg
        self.spinvel = spinvel
        self.bring = False

        self.col = col
        self.col2 = col2
        self.bgcol = bgcol
        self.rcol = [0,0,0]
        self.rainbow = [False, False, False]
        self.colid = 0
        self.c1 = 0
        self.c2 = 1
        self.up = True

        self.preconfiguration = preconfiguration
        self.radius = rad
        self.bcount = bcount
        self.restitution = restitution
        self.friction = friction
        self.passes = passes
        self.balls = []
        self.squares = []
        self.lines = []
        self.empties = []
        self.objects = []