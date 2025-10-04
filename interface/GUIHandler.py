import pygame

from common import *
from interface import *
class GUIHandler:
    def __init__(self, context, Ball, Square):
        self.context = context
        self.Ball = Ball
        self.Square = Square
        self.selind = 0
        self.selid = 0

    def objsel(self, id, l, r):
        sellist = [None, self.context.balls, self.context.squares][id]
        if sellist == None:
            return
        try:
            sellist[self.selind].selected = False

            if l:
                self.selind -= (1 if self.selind != 0 else 0)
            if r:
                self.selind += (1 if self.selind != len(sellist) - 1 else 0)
            sellist[self.selind].selected = True
        except:
            self.selid = 0

    def objdel(self):
        for i in self.context.balls:
            if i.selected:
                self.selind -= (1 if self.selind >= 1 else 0)
                self.context.balls.remove(i)
                self.objsel(self.selid, False, True)

        for i in self.context.squares:
            if i.selected:
                self.selind -= (1 if self.selind >= 1 else 0)
                self.context.squares.remove(i)
                self.objsel(self.selid, False, True)
    
    def handle(self):
        events = pygame.event.get()
        keys = pygame.key.get_pressed()

        if keys[pygame.K_ESCAPE]:
            pygame.quit()
            raise SystemExit

        self.context.gflip = -1 if keys[pygame.K_SPACE] else 1
        self.context.bring = True if keys[pygame.K_w] else False

        self.Ball.forces = [[self.context.gmag * self.context.gflip, self.context.deg]]

        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    self.objsel(self.selid, keys[pygame.K_LEFT], keys[pygame.K_RIGHT])

                elif event.key == pygame.K_g:
                    self.context.guitoggle = not self.context.guitoggle

                elif event.key == pygame.K_BACKSPACE:
                    self.objdel()

            elif event.type == pygame.QUIT:
                pygame.quit()
                raise SystemExit

            if not self.context.guitoggle:
                return

            elif event.type == pygame_gui.UI_DROP_DOWN_MENU_CHANGED:
                if event.ui_element == colourselector:
                    self.context.colid = ["Main", "Outline", "Background"].index(event.selected_option_id)
                    rainbowcheck.set_state(self.context.rainbow[self.context.colid])
                else:
                    self.selid = ["None", "Ball", "Rectangle"].index(event.selected_option_id)
                    self.selind = 0
                    for i in self.context.objects:
                        i.selected = False
                    self.objsel(self.selid, True, False)

            elif event.type == pygame_gui.UI_BUTTON_PRESSED:
                self.objdel()

            elif event.type == pygame_gui.UI_TEXT_ENTRY_FINISHED:
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
                        self.context.radius = event.value
                    radlabel.set_text(f"Radius: {self.context.radius}")
                elif event.ui_element == ballcount:
                    if len(self.context.balls) < event.value:
                        self.context.balls += create_ball(self.Ball, event.value - len(self.context.balls), self.context)
                    elif len(self.context.balls) > event.value:
                        for i in range(len(self.context.balls) - event.value):
                            self.context.balls.pop()

            elif event.type == pygame_gui.UI_CHECK_BOX_CHECKED:
                self.context.rainbow[self.context.colid] = True
            elif event.type == pygame_gui.UI_CHECK_BOX_UNCHECKED:
                self.context.rainbow[self.context.colid] = False

            manager.process_events(event)

        self.context.bcount = len(self.context.balls)
        balllabel.set_text(f"Balls: {self.context.bcount}")
        ballcount.set_current_value(self.context.bcount)