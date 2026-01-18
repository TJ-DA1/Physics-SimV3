import pygame
from common import *
from interface import *

class GUIHandler:
    def __init__(self, ball):
        self.Ball = ball
        self.selind = 0
        self.selid = 0

    def objsel(self, id, l, r):
        sellist = [None, ctx.balls, ctx.squares][id]
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
        for i in ctx.balls:
            if i.selected:
                self.selind -= (1 if self.selind >= 1 else 0)
                ctx.balls.remove(i)
                self.objsel(self.selid, False, True)

        for i in ctx.squares:
            if i.selected:
                self.selind -= (1 if self.selind >= 1 else 0)
                ctx.squares.remove(i)
                self.objsel(self.selid, False, True)
    
    def handle(self, elegui):
        events = pygame.event.get()
        keys = pygame.key.get_pressed()

        if keys[pygame.K_ESCAPE]:
            pygame.quit()
            raise SystemExit

        ctx.gflip = -1 if keys[pygame.K_SPACE] else 1
        ctx.bring = True if keys[pygame.K_w] else False

        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    self.objsel(self.selid, keys[pygame.K_LEFT], keys[pygame.K_RIGHT])

                elif event.key == pygame.K_g:
                    ctx.guitoggle = not ctx.guitoggle

                elif event.key == pygame.K_BACKSPACE:
                    self.objdel()

            elif event.type == pygame.QUIT:
                pygame.quit()
                raise SystemExit

        if not ctx.guitoggle:
            return

        for event in events:
            if event.type == pygame_gui.UI_DROP_DOWN_MENU_CHANGED:
                if event.ui_element == elegui.colourselector:
                    ctx.colid = ["Main", "Outline", "Background"].index(event.selected_option_id)
                    elegui.rainbowcheck.set_state(ctx.rainbow[ctx.colid])
                else:
                    self.selid = ["None", "Ball", "Rectangle"].index(event.selected_option_id)
                    self.selind = 0
                    for i in ctx.objects:
                        i.selected = False
                    self.objsel(self.selid, True, False)

            elif event.type == pygame_gui.UI_TEXT_ENTRY_FINISHED:
                match ctx.colid:
                    case 0:
                        ctx.col2 = hexformat(event.text)
                    case 1:
                        ctx.col = hexformat(event.text)
                    case 2:
                        ctx.bgcol = hexformat(event.text)

            elif event.type == pygame_gui.UI_HORIZONTAL_SLIDER_MOVED:
                if event.ui_element == elegui.gslider:
                    ctx.gmag = event.value * 1000
                    elegui.glabel.set_text(f"Gravity magnitude: {ctx.gmag / 1000}")
                elif event.ui_element == elegui.degslider:
                    ctx.deg = event.value + 90
                    elegui.deglabel.set_text(f"Gravity angle: {ctx.deg - 90}")
                elif event.ui_element == elegui.restslider:
                    ctx.restitution = round(event.value, 0) / 10
                    elegui.restlabel.set_text(f"Restitution: {ctx.restitution}")
                elif event.ui_element == elegui.fricslider:
                    ctx.friction = round(event.value, 0) / 10
                    elegui.friclabel.set_text(f"Friction: {ctx.friction}")
                elif event.ui_element == elegui.radslider:
                    for i in ctx.balls:
                        if not i.static:
                            i.radius = event.value
                    ctx.radius = event.value
                    elegui.radlabel.set_text(f"Radius: {ctx.radius}")
                elif event.ui_element == elegui.ballcount:
                    if len(ctx.balls) < event.value:
                        ctx.balls += create_ball(self.Ball, event.value - len(ctx.balls), ctx)
                    elif len(ctx.balls) > event.value:
                        for i in range(len(ctx.balls) - event.value):
                            ctx.balls.pop()

            elif event.type == pygame_gui.UI_CHECK_BOX_CHECKED:
                ctx.rainbow[ctx.colid] = True
            elif event.type == pygame_gui.UI_CHECK_BOX_UNCHECKED:
                ctx.rainbow[ctx.colid] = False

            ctx.manager.process_events(event)

        ctx.bcount = len(ctx.balls)
        elegui.balllabel.set_text(f"Balls: {ctx.bcount}")
        elegui.ballcount.set_current_value(ctx.bcount)

    def handleprescreen(self):
        keys = pygame.key.get_pressed()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                raise SystemExit

            elif keys[pygame.K_ESCAPE]:
                return True

            elif event.type == pygame_gui.UI_TEXT_ENTRY_FINISHED:
                match event.ui_element:
                    case prescreen.preset:
                        ctx.preconfiguration = event.text
                    case prescreen.gmagset:
                        ctx.gmag = int(event.text) * 1000
                    case prescreen.degset:
                        ctx.deg = int(event.text) + 90
                    case prescreen.spinvelset:
                        ctx.spinvel = int(event.text)
                    case prescreen.widthset:
                        ctx.width = int(event.text)
                    case prescreen.heightset:
                        ctx.height = int(event.text)
                    case prescreen.pwidthset:
                        ctx.pwidth = int(event.text)
                    case prescreen.pheightset:
                        ctx.pheight = int(event.text)
                    case prescreen.swidthset:
                        ctx.scalewidth = int(event.text)
                    case prescreen.sheightset:
                        ctx.scaleheight = int(event.text)
                    case prescreen.bcountset:
                        ctx.bcount = int(event.text)
                    case prescreen.fricset:
                        ctx.friction = int(event.text)
                    case prescreen.restset:
                        ctx.restitution = int(event.text)
                    case prescreen.passesset:
                        ctx.passes = int(event.text)
                    case prescreen.radset:
                        ctx.radius = int(event.text)
                    case prescreen.padset:
                        ctx.windowpad = int(event.text)
            ctx.prescreen.process_events(event)


