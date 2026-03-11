import random

import pygame
import pygame_gui

from common import *
from interface import *
from saves import *

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

        self.emptyindex = []
        self.emptychild = False

        self.name = ""

    def objsel(self, id, l):
        sellist = [None, ctx.balls, ctx.squares, ctx.lines, ctx.empties][id] #Object channel to select from
        if sellist == None: #No objects being selected
            return
        try:
            sellist[self.selind].selected = False #Deselect selected object
            if l:
                self.selind -= (1 if self.selind != 0 else 0) #Select previous object
            else:
                self.selind += (1 if self.selind != len(sellist) - 1 else 0) #Select next object
            sellist[self.selind].selected = True #Select new object
        except:
            self.selid = 0 #Reset for edge cases

    def objdel(self, editorgui):
        for i in ctx.objects:
            if i.selected: #Find selected object
                self.selind -= (1 if self.selind >= 1 else 0) #Update index
                [ctx.balls, ctx.squares, ctx.lines, ctx.empties][i.objid].remove(i) #Remove object
                ctx.objects = ctx.balls + ctx.squares + ctx.lines + ctx.empties  # Update objects list
                if i.objid == 3 and self.emptychild: #Handle deleting child mode selected empty object
                    self.emptychild = False
                    self.emptyindex = []
                    editorgui.childlabel.hide()
        self.objsel(self.selid, False) #Select next object
    
    def handle(self, elegui, Ball):
        self.events = pygame.event.get()
        keys = pygame.key.get_pressed()

        if keys[pygame.K_ESCAPE]:
            pygame.quit() #Program exit key bind
            raise SystemExit

        ctx.gflip = -1 if keys[pygame.K_SPACE] else 1 #Flip gravity when SPACEBAR is held
        ctx.bring = True if keys[pygame.K_w] else False #Bring object to cursor when W is held

        for event in self.events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_g:
                    ctx.guitoggle = not ctx.guitoggle #Toggle GUI

                elif event.key == pygame.K_p:
                    ctx.editortoggle = not ctx.editortoggle #Toggle editor

            elif event.type == pygame.QUIT:
                pygame.quit() #Program exit
                raise SystemExit

        if not ctx.guitoggle: #Only handle keys when GUI toggled off
            return

        for event in self.events:
            if event.type == pygame_gui.UI_DROP_DOWN_MENU_CHANGED:
                if event.ui_element == elegui.colourselector: #Select colour channel
                    ctx.colid = ["Main", "Outline", "Background"].index(event.selected_option_id)
                    elegui.rainbowcheck.set_state(ctx.rainbow[ctx.colid])

            elif event.type == pygame_gui.UI_TEXT_ENTRY_FINISHED:
                if event.ui_element == elegui.colourentry: #Change colour of channel
                    match ctx.colid:
                        case 0:
                            ctx.col2 = hexformat(event.text)
                        case 1:
                            ctx.col = hexformat(event.text)
                        case 2:
                            ctx.bgcol = hexformat(event.text)

            elif event.type == pygame_gui.UI_HORIZONTAL_SLIDER_MOVED:
                if event.ui_element == elegui.gslider:
                    ctx.gmag = event.value * 1000 #Update magntiude of gravitational force
                    elegui.glabel.set_text(f"Gravity magnitude: {ctx.gmag / 1000}")
                if event.ui_element == elegui.gtypeslider:
                    ctx.gtype = event.value // 10 #Update gravity type
                    elegui.gtypelabel.set_text(f"Gravity type: {["Uniform", "Radial", "Anti-radial", "Individual"][ctx.gtype]}")
                elif event.ui_element == elegui.degslider:
                    ctx.deg = event.value + 90 #Update gravity angle, offset by 90 so 0 is straight down
                    elegui.deglabel.set_text(f"Gravity angle: {ctx.deg - 90}")
                elif event.ui_element == elegui.restslider: #Update restitution
                    ctx.restitution = round(event.value, 0) / 10
                    elegui.restlabel.set_text(f"Restitution: {ctx.restitution}")
                elif event.ui_element == elegui.fricslider:
                    ctx.friction = round(event.value, 0) / 10 #Update friction
                    elegui.friclabel.set_text(f"Friction: {ctx.friction}")
                elif event.ui_element == elegui.radslider:
                    for i in ctx.balls:
                        if not i.static: #Change radius of all non-static ball objects
                            i.radius = event.value
                    ctx.radius = event.value
                    elegui.radlabel.set_text(f"Radius: {ctx.radius}")
                elif event.ui_element == elegui.ballcount:
                    if len(ctx.balls) < event.value: #Instantiate new balls
                        ctx.balls += create_ball(Ball, event.value - len(ctx.balls), ctx)
                    elif len(ctx.balls) > event.value: #Remove balls from sim
                        for i in range(len(ctx.balls) - event.value):
                            ctx.balls.pop()
                    ctx.objects = ctx.balls + ctx.squares + ctx.lines + ctx.empties  # Update objects list

            elif event.type == pygame_gui.UI_CHECK_BOX_CHECKED or event.type == pygame_gui.UI_CHECK_BOX_UNCHECKED:
                ctx.rainbow[ctx.colid] = elegui.rainbowcheck.get_state() #Make colour channel rainbow
            if not ctx.editortoggle:
                ctx.manager.process_events(event)

        elegui.balllabel.set_text(f"Balls: {ctx.bcount}") #Update ball count UI elements
        elegui.ballcount.set_current_value(ctx.bcount)

    def handleeditor(self, editorgui, objs):
        for i in ctx.empties: #Ensure only one empty is shown as selected
            i.childselected = False
        if len(self.emptyindex):
            ctx.empties[self.emptyindex[-1]].childselected = True

        for event in self.events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w and not self.drawing:
                    self.startpos = ctx.mousex, ctx.mousey #Begin instantiating object
                    self.drawing = True

                elif event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    self.objsel(self.selid, event.key == pygame.K_LEFT) #Select object of next / previous index

                elif event.key == pygame.K_BACKSPACE:
                    self.objdel(editorgui) #Delete object when BACKSPACE pressed

                elif event.key == pygame.K_RETURN:
                    if self.emptychild: #Enter child mode for next child in recently instantiated empties
                        self.emptyindex.pop(-1)
                        if len(self.emptyindex) < 1: #Exit child mode if no empties left to edit children of
                            self.emptychild = False
                            editorgui.childlabel.hide()

            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_w:
                    endpos = ctx.mousex, ctx.mousey #Finish instantiating an object
                    self.drawing = False
                    match self.editorselid:
                        case 0: #Instantiate new ball
                            ctx.balls += [objs[0](x = self.startpos[0], y = self.startpos[1], radius = math.dist(self.startpos, endpos), drawtrail = self.drawtrailparam, mass = self.massparam if not (self.infmassparam) else -1, static = self.staticparam)]
                            if self.emptychild: #Make child of empty
                                ctx.empties[self.emptyindex[-1]].children += [ctx.balls[len(ctx.balls) - 1]]

                        case 1: #Instantiate new rectangle
                            relx, rely = ctx.mousex - self.startpos[0], ctx.mousey - self.startpos[1] #Find relative mouse position to determine side lengths
                            relx, rely = rotatepoint((relx, rely), -self.angleparam)
                            xside, yside = abs(relx * 2), abs(rely * 2)
                            ctx.squares += [objs[1](x = self.startpos[0], y = self.startpos[1], sizex = xside, sizey = yside, angle = self.angleparam, spinvel = self.spinvelparam)]
                            if self.emptychild: #Make child of empty
                                ctx.empties[self.emptyindex[-1]].children += [ctx.squares[len(ctx.squares) - 1]]

                        case 2: #Instantiate new line
                            ctx.lines += [objs[2](self.startpos, endpos)]
                            if self.emptychild: #Make child of empty
                                ctx.empties[self.emptyindex[-1]].children += [ctx.lines[len(ctx.lines) - 1]]

                        case 3: #Instantiate new empty
                            newempty = objs[3](ctx.mousex, ctx.mousey, 0, self.spinvelparam)

                            if self.emptychild: #Make child of empty
                                ctx.empties[self.emptyindex[-1]].children += [newempty]
                            ctx.empties += [newempty]

                            self.emptyindex += [len(ctx.empties) - 1] #Enter child mode for new empty
                            self.emptychild = True
                            editorgui.childlabel.show()

            elif event.type == pygame_gui.UI_BUTTON_PRESSED:

                if event.ui_element == editorgui.childbutton:
                    if not len(self.emptyindex) and len(ctx.empties): #Do nothing if already editing children
                        for i in range(len(ctx.empties)):
                            self.emptyindex += [i] #Add all empties to list to edit
                        self.emptychild = True
                        editorgui.childlabel.show()

                elif event.ui_element == editorgui.savebutton:
                    save(ctx, self.name) #Save to file with input name

                elif event.ui_element == editorgui.loadbutton:
                    self.selid = 0 #Reset selection
                    self.emptyindex = []
                    self.emptychild = False
                    editorgui.childlabel.hide()
                    load(ctx, self.name, objs) #Load file

                elif event.ui_element == editorgui.delbutton:
                    self.objdel(editorgui) #Delete selected object if delete button pressed

            elif event.type == pygame_gui.UI_CHECK_BOX_CHECKED or event.type == pygame_gui.UI_CHECK_BOX_UNCHECKED:
                if event.ui_element == editorgui.staticcheck: #Set static boolean of instantiated object
                    self.staticparam = editorgui.staticcheck.get_state()
                elif event.ui_element == editorgui.trailcheck: #Set draw trail boolean of instantiated object
                    self.drawtrailparam = editorgui.trailcheck.get_state()
                elif event.ui_element == editorgui.infmasscheck: #Set infinite mass boolean of instantiated object
                    self.infmassparam = editorgui.infmasscheck.get_state()

            elif event.type == pygame_gui.UI_HORIZONTAL_SLIDER_MOVED:
                if self.editorselid == 0: #Set mass of instantiated object
                    self.massparam = event.value
                    editorgui.masslabel.set_text(f"Mass: {self.massparam}")
                elif event.ui_element == editorgui.spinvelslider: #Set spin velocity of instantiated object
                    self.spinvelparam = event.value
                    editorgui.spinvellabel.set_text(f"Spin velocity: {self.spinvelparam}")
                else: #Set angle of instantiation
                    self.angleparam = event.value
                    editorgui.anglelabel.set_text(f"Angle: {self.angleparam}")


            elif event.type == pygame_gui.UI_DROP_DOWN_MENU_CHANGED:
                if event.ui_element == editorgui.typeselector:
                    self.editorselid = ["Circle", "Rectangle", "Line", "Empty"].index(event.selected_option_id) #Object type to instantiate
                    match self.editorselid:
                        case 0: #Hide and show elements for ball instantiation
                            hide, show = (
                                [editorgui.anglelabel, editorgui.angleslider, editorgui.spinvellabel, editorgui.spinvelslider, editorgui.childbutton],
                                [editorgui.masslabel, editorgui.massslider, editorgui.staticcheck, editorgui.trailcheck, editorgui.infmasscheck]
                            )
                        case 1: #Hide and show elements for rectangle instantiation
                            editorgui.spinvellabel.set_position((0,40))
                            editorgui.spinvelslider.set_position((0,60))
                            hide, show = (
                                [editorgui.masslabel, editorgui.massslider, editorgui.staticcheck, editorgui.trailcheck, editorgui.infmasscheck, editorgui.childbutton],
                                [editorgui.anglelabel, editorgui.angleslider,  editorgui.spinvellabel, editorgui.spinvelslider]
                            )
                        case 2: #Hide and show elements for line instantiation
                            hide, show = (
                                [editorgui.anglelabel, editorgui.angleslider, editorgui.masslabel, editorgui.massslider, editorgui.staticcheck, editorgui.trailcheck, editorgui.infmasscheck, editorgui.spinvellabel, editorgui.spinvelslider, editorgui.childbutton],
                                []
                            )

                        case 3: #Hide and show elements for empty instantiation
                            editorgui.spinvellabel.set_position((0, 0))
                            editorgui.spinvelslider.set_position((0, 20))
                            hide, show = (
                                [editorgui.anglelabel, editorgui.angleslider, editorgui.masslabel, editorgui.massslider, editorgui.staticcheck, editorgui.trailcheck, editorgui.infmasscheck],
                                [editorgui.spinvellabel, editorgui.spinvelslider, editorgui.childbutton]
                            )
                    hide_elements(hide, show)

                elif event.ui_element == editorgui.objselector:
                    self.selid = ["None", "Ball", "Rectangle", "Line", "Empty"].index(event.selected_option_id) #Object type to be selected
                    self.selind = 0 #Reset index selected
                    for i in ctx.objects:
                        i.selected = False #Reset selection
                    self.objsel(self.selid, True)

            elif event.type == pygame_gui.UI_TEXT_ENTRY_CHANGED:
                self.name = event.text #Name of file to load / save to

            ctx.editormanager.process_events(event)

        if self.drawing:
            match self.editorselid:
                case 0: #Draw circle preview
                    pygame.draw.circle(ctx.psurface, (0, 0, 255), self.startpos, math.dist(self.startpos, (ctx.mousex, ctx.mousey)), 2)

                case 1: #Draw square preview
                    relx, rely = ctx.mousex - self.startpos[0], ctx.mousey - self.startpos[1]
                    relx, rely = rotatepoint((relx, rely), -self.angleparam) #Rotate mouse position
                    xside, yside = relx * 2, rely * 2
                    points = calcpoints(xside, yside, self.startpos[0], self.startpos[1], self.angleparam, 0)[0] #Calculate points of preview rectangle
                    pygame.draw.polygon(ctx.psurface, (0,0,255), points, 2)

                case 2: #Draw line preview
                    pygame.draw.line(ctx.psurface,
                                     (0, 0, 255),
                                     (self.startpos[0] + (ctx.windowpad / 2), self.startpos[1] + (ctx.windowpad / 2)),
                                     (ctx.mousex + (ctx.windowpad / 2), ctx.mousey + (ctx.windowpad / 2)),
                                     2
                                     )

                case 3: #Draw empty preview
                    pygame.draw.line(ctx.psurface, (0, 0, 255), (ctx.mousex, ctx.mousey + 5), (ctx.mousex, ctx.mousey - 5), 2)
                    pygame.draw.line(ctx.psurface, (0, 0, 255), (ctx.mousex + 5, ctx.mousey), (ctx.mousex - 5, ctx.mousey), 2)

        ctx.objects = ctx.balls + ctx.squares + ctx.lines + ctx.empties  # Update objects list

    def handleprescreen(self):
        keys = pygame.key.get_pressed()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                raise SystemExit

            elif keys[pygame.K_ESCAPE]: #Stopping case for pre-screen
                return True

            elif event.type == pygame_gui.UI_TEXT_ENTRY_FINISHED:
                match event.ui_element: #Handles input in pre-screen, to set simulation context variables
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