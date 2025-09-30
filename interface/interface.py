from common.config import *

glabel = pygame_gui.elements.UILabel(relative_rect=pygame.Rect((0, 0), (200, 20)), text=f"Gravity magnitude: {gmag}", manager=manager)
gslider = pygame_gui.elements.UIHorizontalSlider(relative_rect=pygame.Rect((0, 20), (200, 20)), start_value=gmag, value_range=(-10, 10), manager=manager)

deglabel = pygame_gui.elements.UILabel(relative_rect=pygame.Rect((0, 40), (200, 20)), text=f"Gravity angle: {deg - 90}", manager=manager)
degslider = pygame_gui.elements.UIHorizontalSlider(relative_rect=pygame.Rect((0, 60), (200, 20)), start_value=deg - 90, value_range=(-180, 180), manager=manager)

restlabel = pygame_gui.elements.UILabel(relative_rect=pygame.Rect((0, 80), (200, 20)), text=f"Restitution: {restitution}", manager=manager)
restslider = pygame_gui.elements.UIHorizontalSlider(relative_rect=pygame.Rect((0, 100), (200, 20)), start_value=restitution * 10, value_range=(0, 10), manager=manager)

friclabel = pygame_gui.elements.UILabel(relative_rect=pygame.Rect((0, 120), (200, 20)), text=f"Friction: {friction}", manager=manager)
fricslider = pygame_gui.elements.UIHorizontalSlider(relative_rect=pygame.Rect((0, 140), (200, 20)), start_value=friction * 10, value_range=(0, 10), manager=manager)

balllabel = pygame_gui.elements.UILabel(relative_rect=pygame.Rect((width - 200, 0), (200, 20)), text=f"Balls: {bcount}", manager=manager)
ballcount = pygame_gui.elements.UIHorizontalSlider(relative_rect=pygame.Rect((width - 200, 20), (200, 20)), start_value=bcount, value_range=(1, 200), manager=manager)

radlabel = pygame_gui.elements.UILabel(relative_rect=pygame.Rect((width - 200, 40), (200, 20)), text=f"Radius: {rad}", manager=manager)
radslider = pygame_gui.elements.UIHorizontalSlider(relative_rect=pygame.Rect((width - 200, 60), (200, 20)), start_value=rad, value_range=(1, 50), manager=manager)

colourentry = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect((0, height - 20), (100, 20)), manager=manager)
colourselector = pygame_gui.elements.UIDropDownMenu(relative_rect=pygame.Rect((0, height - 45),(100, 25)), options_list = ["Background", "Outline", "Main"], starting_option = "Main", manager = manager)

framelabel = pygame_gui.elements.UILabel(relative_rect=pygame.Rect((width - 50, height-20), (50, 20)), text=f"{framerate}fps", manager=manager)