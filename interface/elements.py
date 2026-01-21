from common import *
class Element:
    def initiate(self):
        self.glabel = pygame_gui.elements.UILabel(relative_rect=pygame.Rect((0, 0), (200, 20)), text=f"Gravity magnitude: {int(ctx.gmag / 1000)}", manager=ctx.manager)
        self.gslider = pygame_gui.elements.UIHorizontalSlider(relative_rect=pygame.Rect((0, 20), (200, 20)), start_value=int(ctx.gmag / 1000), value_range=(-10, 10), manager=ctx.manager)

        self.gtypelabel = pygame_gui.elements.UILabel(relative_rect=pygame.Rect((0, 40), (200, 20)), text=f"Gravity type: {ctx.gtype}", manager=ctx.manager)
        self.gtypeslider = pygame_gui.elements.UIHorizontalSlider(relative_rect=pygame.Rect((0, 60), (200, 20)), start_value=ctx.gtype * 10, value_range=(0, 29), manager=ctx.manager)

        self.deglabel = pygame_gui.elements.UILabel(relative_rect=pygame.Rect((0, 80), (200, 20)), text=f"Gravity angle: {ctx.deg - 90}", manager=ctx.manager)
        self.degslider = pygame_gui.elements.UIHorizontalSlider(relative_rect=pygame.Rect((0, 100), (200, 20)), start_value=ctx.deg - 90, value_range=(-180, 180), manager=ctx.manager)

        self.restlabel = pygame_gui.elements.UILabel(relative_rect=pygame.Rect((0, 120), (200, 20)), text=f"Restitution: {ctx.restitution}", manager=ctx.manager)
        self.restslider = pygame_gui.elements.UIHorizontalSlider(relative_rect=pygame.Rect((0, 140), (200, 20)), start_value=ctx.restitution * 10, value_range=(0, 10), manager=ctx.manager)

        self.friclabel = pygame_gui.elements.UILabel(relative_rect=pygame.Rect((0, 160), (200, 20)), text=f"Friction: {ctx.friction}", manager=ctx.manager)
        self.fricslider = pygame_gui.elements.UIHorizontalSlider(relative_rect=pygame.Rect((0, 180), (200, 20)), start_value=ctx.friction * 10, value_range=(0, 10), manager=ctx.manager)

        self.balllabel = pygame_gui.elements.UILabel(relative_rect=pygame.Rect((ctx.width - 200, 0), (200, 20)), text=f"Balls: {ctx.bcount}", manager=ctx.manager)
        self.ballcount = pygame_gui.elements.UIHorizontalSlider(relative_rect=pygame.Rect((ctx.width - 200, 20), (200, 20)), start_value=ctx.bcount, value_range=(1, 200), manager=ctx.manager)

        self.radlabel = pygame_gui.elements.UILabel(relative_rect=pygame.Rect((ctx.width - 200, 40), (200, 20)), text=f"Radius: {ctx.radius}", manager=ctx.manager)
        self.radslider = pygame_gui.elements.UIHorizontalSlider(relative_rect=pygame.Rect((ctx.width - 200, 60), (200, 20)), start_value=ctx.radius, value_range=(1, 50), manager=ctx.manager)

        self.colourentry = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect((0, ctx.height - 20), (100, 20)), placeholder_text="Colour code", manager=ctx.manager)
        self.colourselector = pygame_gui.elements.UIDropDownMenu(relative_rect=pygame.Rect((0, ctx.height - 45), (100, 25)), options_list = ["Main", "Outline", "Background"], starting_option ="Main", manager = ctx.manager)
        self.rainbowcheck = pygame_gui.elements.UICheckBox(relative_rect=pygame.Rect((100, ctx.height - 25), (25, 25)), text="Rainbow", initial_state = False, manager=ctx.manager)

        self.framelabel = pygame_gui.elements.UILabel(relative_rect=pygame.Rect((ctx.width - 70, ctx.height - 20), (70, 20)), text=f"{ctx.framerate}fps", manager=ctx.manager)