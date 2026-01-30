import pygame, pygame_gui

# Render window
width = 500
height = 500
pwidth = 500
pheight = 500
scalewidth = 500
scaleheight = 500
windowpad = 0
framerate = 120
screen = pygame.display.set_mode((300, 400), flags=pygame.SCALED, vsync=1)
preconfiguration = ("square")

# Gravity
gmag = 1000
gtype = 0
deg = 90
spinvel = 0

# Colours
col = [0,0,0]
col2 = [255,255,255]
bgcol = [255,255,255]

# Balls
radius = 10
passes = 1
restitution = 0.5
friction = 0.8
bcount = 1
