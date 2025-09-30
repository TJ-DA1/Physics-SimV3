import pygame, pygame_gui

# Render window
width, height = 500,500
pwidth, pheight = 500,500
scalesize = 500,500
windowpad = 0
framerate = 60
screentoggle = False
psurface = pygame.Surface((pwidth + windowpad, pheight + windowpad))
screen = pygame.display.set_mode((width, height), flags=pygame.SCALED, vsync=1)
manager = pygame_gui.UIManager((width, height), "interface/theme.json")

# Gravity
gmag = 2
deg = 90
spinvel = 0

# Colours
col = [255,255,255]
col2 = [0,0,0]
bgcol = [255,255,255]

# Balls
rad = 15
pad = 0
passes = 5
restitution = 0.5
friction = 0.5
bcount = 50
