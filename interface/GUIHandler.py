import pygame

from common import *
from interface import *
class GUIHandler:
    def __init__(self, context, Ball, Square):
        self.context = context
        self.Ball = Ball
        self.Square = Square
        self.guiswitch = False
    
    def handle(self,):
        keys = pygame.key.get_pressed()
        events = pygame.event.get()

        if keys[pygame.K_ESCAPE]:
            pygame.quit()
            raise SystemExit

        if keys[pygame.K_g] and self.guiswitch:
            self.context.guitoggle = not self.context.guitoggle
            self.guiswitch = False
        elif not keys[pygame.K_g]:
            self.guiswitch = True

        self.context.gflip = -1 if keys[pygame.K_SPACE] else 1
        self.context.bring = True if keys[pygame.K_w] else False

        self.Ball.forces = [[self.context.gmag * self.context.gflip, self.context.deg]]

        if not self.context.guitoggle:
            return

        for event in events:
            if event.type == pygame_gui.UI_DROP_DOWN_MENU_CHANGED:
                self.context.colid = ["Main", "Outline", "Background"].index(event.selected_option_id)
                rainbowcheck.set_state(self.context.rainbow[self.context.colid])

            if event.type == pygame_gui.UI_TEXT_ENTRY_FINISHED:
                match self.context.colid:
                    case 0:
                        self.context.col2 = hexformat(event.text)
                    case 1:
                        self.context.col = hexformat(event.text)
                    case 2:
                        self.context.bgcol = hexformat(event.text)

            elif event.type == pygame_gui.UI_HORIZONTAL_SLIDER_MOVED:
                if event.ui_element == gslider:
                    self.context.gmag = event.value
                    glabel.set_text(f"Gravity magnitude: {self.context.gmag}")
                elif event.ui_element == degslider:
                    self.context.deg = event.value + 90
                    deglabel.set_text(f"Gravity angle: {self.context.deg - 90}")
                elif event.ui_element == restslider:
                    self.Ball.rest = round(event.value, 0) / 10
                    restlabel.set_text(f"Restitution: {self.Ball.rest}")
                elif event.ui_element == fricslider:
                    self.Ball.fric = round(event.value, 0) / 10
                    friclabel.set_text(f"Friction: {self.Ball.fric}")
                elif event.ui_element == radslider:
                    for i in self.context.balls:
                        i.radius = event.value
                        config.radius = event.value
                    radlabel.set_text(f"Radius: {config.rad}")
                elif event.ui_element == ballcount:
                    if len(self.context.balls) < event.value:
                        self.context.balls += create_ball(self.Ball, event.value - len(self.context.balls), config.rad)
                    elif len(self.context.balls) > event.value:
                        for i in range(len(self.context.balls) - event.value):
                            self.context.balls.pop()

                    config.bcount = len(self.context.balls)
                    balllabel.set_text(f"Balls: {config.bcount}")

            elif event.type == pygame_gui.UI_CHECK_BOX_CHECKED:
                self.context.rainbow[self.context.colid] = True
            elif event.type == pygame_gui.UI_CHECK_BOX_UNCHECKED:
                self.context.rainbow[self.context.colid] = False

            if event.type == pygame.QUIT:
                pygame.quit()
                raise SystemExit

            manager.process_events(event)