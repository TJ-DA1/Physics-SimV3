import random

import pygame
import pygame_gui

from common import *
from interface import *

class GUIHandler:
    def __init__(self):
        self.selind = 0
        self.selid = 0
        self.editorselid = 0
        self.startpos = None,None
        self.angleparam = 0
        self.spinvelparam = 0
        self.massparam = 1
        self.infmassparam = False
        self.staticparam = False
        self.drawtrailparam = False
        self.drawing = False

        self.emptyindex = -1
        self.emptychild = False

    def objsel(self, id, l):
        sellist = [None, ctx.balls, ctx.squares, ctx.lines, ctx.empties][id]
        if sellist == None:
            return
        try:
            sellist[self.selind].selected = False
            if l:
                self.selind -= (1 if self.selind != 0 else 0)
            else:
                self.selind += (1 if self.selind != len(sellist) - 1 else 0)
            sellist[self.selind].selected = True
        except:
            self.selid = 0

    def objdel(self):
        for i in ctx.objects:
            if i.selected:
                self.selind -= (1 if self.selind >= 1 else 0)
                [ctx.balls, ctx.squares, ctx.lines, ctx.empties][i.objid].remove(i)
                if i.objid == 3 and self.emptychild:
                    self.emptychild = False
                    self.emptyindex -= 1
        self.objsel(self.selid, False)
    
    def handle(self, elegui, Ball):
        self.events = pygame.event.get()
        keys = pygame.key.get_pressed()

        if keys[pygame.K_ESCAPE]:
            pygame.quit()
            raise SystemExit

        ctx.gflip = -1 if keys[pygame.K_SPACE] else 1
        ctx.bring = True if keys[pygame.K_w] else False

        for event in self.events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_g:
                    ctx.guitoggle = not ctx.guitoggle

                elif event.key == pygame.K_p:
                    ctx.editortoggle = not ctx.editortoggle

            elif event.type == pygame.QUIT:
                pygame.quit()
                raise SystemExit

        if not ctx.guitoggle:
            return

        for event in self.events:
            if event.type == pygame_gui.UI_DROP_DOWN_MENU_CHANGED:
                if event.ui_element == elegui.colourselector:
                    ctx.colid = ["Main", "Outline", "Background"].index(event.selected_option_id)
                    elegui.rainbowcheck.set_state(ctx.rainbow[ctx.colid])

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
                if event.ui_element == elegui.gtypeslider:
                    ctx.gtype = event.value // 10
                    elegui.gtypelabel.set_text(f"Gravity type: {ctx.gtype}")
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
                        ctx.balls += create_ball(Ball, event.value - len(ctx.balls), ctx)
                    elif len(ctx.balls) > event.value:
                        for i in range(len(ctx.balls) - event.value):
                            ctx.balls.pop()

            elif event.type == pygame_gui.UI_CHECK_BOX_CHECKED or event.type == pygame_gui.UI_CHECK_BOX_UNCHECKED:
                ctx.rainbow[ctx.colid] = elegui.rainbowcheck.get_state()
            if not ctx.editortoggle:
                ctx.manager.process_events(event)

        elegui.balllabel.set_text(f"Balls: {ctx.bcount}")
        elegui.ballcount.set_current_value(ctx.bcount)

    def handleeditor(self, editorgui, objs):
        for event in self.events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w and not self.drawing:
                    self.startpos = ctx.mousex, ctx.mousey
                    self.drawing = True

                elif event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    self.objsel(self.selid, event.key == pygame.K_LEFT)

                elif event.key == pygame.K_BACKSPACE:
                    self.objdel()

                elif event.key == pygame.K_RETURN:
                    self.emptychild = False
                    editorgui.childlabel.hide()

            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_w:
                    endpos = ctx.mousex, ctx.mousey
                    self.drawing = False
                    match self.editorselid:
                        case 0:
                            ctx.balls += [objs[0](x = self.startpos[0], y = self.startpos[1], radius = math.dist(self.startpos, endpos), drawtrail = self.drawtrailparam, mass = self.massparam if not (self.infmassparam or self.staticparam) else -1, static = self.staticparam)]
                            if self.emptychild:
                                ctx.empties[self.emptyindex].children += [ctx.balls[len(ctx.balls) - 1]]
                        case 1:
                            relx, rely = ctx.mousex - self.startpos[0], ctx.mousey - self.startpos[1]
                            relx, rely = rotatepoint((relx, rely), -self.angleparam)
                            xside, yside = abs(relx * 2), abs(rely * 2)
                            ctx.squares += [objs[1](x = self.startpos[0], y = self.startpos[1], sizex = xside, sizey = yside, angle = self.angleparam)]
                            if self.emptychild:
                                ctx.empties[self.emptyindex].children += [ctx.squares[len(ctx.squares) - 1]]
                        case 2:
                            ctx.lines += [objs[2](self.startpos, endpos)]
                            if self.emptychild:
                                ctx.empties[self.emptyindex].children += [ctx.lines[len(ctx.lines) - 1]]
                        case 3:
                            newempty = objs[3](self.startpos[0], self.startpos[1], 0, self.spinvelparam)

                            if self.emptychild:
                                ctx.empties[self.emptyindex].children += [newempty]
                            ctx.empties += [newempty]

                            self.emptyindex = len(ctx.empties) - 1
                            self.emptychild = True
                            editorgui.childlabel.show()


            elif event.type == pygame_gui.UI_CHECK_BOX_CHECKED or event.type == pygame_gui.UI_CHECK_BOX_UNCHECKED:
                if event.ui_element == editorgui.staticcheck:
                    self.staticparam = editorgui.staticcheck.get_state()
                elif event.ui_element == editorgui.trailcheck:
                    self.drawtrailparam = editorgui.trailcheck.get_state()
                elif event.ui_element == editorgui.infmasscheck:
                    self.infmassparam = editorgui.infmasscheck.get_state()

            elif event.type == pygame_gui.UI_HORIZONTAL_SLIDER_MOVED:
                if self.editorselid == 0:
                    self.massparam = event.value
                    editorgui.masslabel.set_text(f"Mass: {self.massparam}")
                elif self.editorselid == 1:
                    self.angleparam = event.value
                    editorgui.anglelabel.set_text(f"Angle: {self.angleparam}")
                else:
                    self.spinvelparam = event.value
                    editorgui.spinvellabel.set_text(f"Spin velocity: {self.spinvelparam}")

            elif event.type == pygame_gui.UI_DROP_DOWN_MENU_CHANGED:
                if event.ui_element == editorgui.typeselector:
                    self.editorselid = ["Circle", "Rectangle", "Line", "Empty"].index(event.selected_option_id)
                    match self.editorselid:
                        case 0:
                            hide, show = [editorgui.anglelabel, editorgui.angleslider, editorgui.spinvellabel, editorgui.spinvelslider],[editorgui.masslabel, editorgui.massslider, editorgui.staticcheck, editorgui.trailcheck, editorgui.infmasscheck]
                        case 1:
                            hide, show = [editorgui.masslabel, editorgui.massslider, editorgui.staticcheck, editorgui.trailcheck, editorgui.infmasscheck, editorgui.spinvellabel, editorgui.spinvelslider], [editorgui.anglelabel, editorgui.angleslider]
                        case 2:
                            hide, show = [editorgui.anglelabel, editorgui.angleslider, editorgui.masslabel, editorgui.massslider, editorgui.staticcheck, editorgui.trailcheck, editorgui.infmasscheck, editorgui.spinvellabel, editorgui.spinvelslider], []
                        case 3:
                            hide, show = [editorgui.anglelabel, editorgui.angleslider, editorgui.masslabel, editorgui.massslider, editorgui.staticcheck, editorgui.trailcheck, editorgui.infmasscheck], [editorgui.spinvellabel, editorgui.spinvelslider]
                    hide_elements(hide, show)

                elif event.ui_element == editorgui.objselector:
                    self.selid = ["None", "Ball", "Rectangle", "Line", "Empty"].index(event.selected_option_id)
                    self.selind = 0
                    for i in ctx.objects:
                        i.selected = False
                    self.objsel(self.selid, True)

            ctx.editormanager.process_events(event)

        if self.drawing:
            match self.editorselid:
                case 0:
                    pygame.draw.circle(ctx.psurface, (0, 0, 255), self.startpos, math.dist(self.startpos, (ctx.mousex, ctx.mousey)), 2)
                case 1:
                    relx, rely = ctx.mousex - self.startpos[0], ctx.mousey - self.startpos[1]
                    relx, rely = rotatepoint((relx, rely), -self.angleparam)
                    xside, yside = relx * 2, rely * 2
                    points = calcpoints(xside, yside, self.startpos[0], self.startpos[1], self.angleparam, 0)[0]
                    pygame.draw.polygon(ctx.psurface, (0,0,255), points, 2)
                case 2:
                    pygame.draw.line(ctx.psurface, (0, 0, 255), self.startpos, (ctx.mousex, ctx.mousey), 2)

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
                    case prescreen.gtypeset:
                        ctx.gtype = int(event.text)
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


