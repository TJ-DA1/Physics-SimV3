import pygame_gui.elements

from common import *
preset = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect((0, 0), (150, 20)), placeholder_text="Preset", manager=ctx.prescreen)
gmagset = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect((0, 20), (150, 20)), placeholder_text="Gravity magnitude", manager=ctx.prescreen)
gtypeset = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect((0, 40), (150, 20)), placeholder_text="Gravity type", manager=ctx.prescreen)
degset = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect((0, 60), (150, 20)), placeholder_text="Gravity angle", manager=ctx.prescreen)
spinvelset = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect((0, 80), (150, 20)), placeholder_text="Gravity spin speed", manager=ctx.prescreen)
widthset = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect((0, 100), (150, 20)), placeholder_text="Window width", manager=ctx.prescreen)
heightset = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect((0, 120), (150, 20)), placeholder_text="Window height", manager=ctx.prescreen)
pwidthset = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect((0, 140), (150, 20)), placeholder_text="Physics space width", manager=ctx.prescreen)
pheightset = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect((0, 160), (150, 20)), placeholder_text="Physics space height", manager=ctx.prescreen)
swidthset = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect((0, 180), (150, 20)), placeholder_text="Scale width", manager=ctx.prescreen)
sheightset = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect((0, 200), (150, 20)), placeholder_text="Scale height", manager=ctx.prescreen)
padset = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect((0, 220), (150, 20)), placeholder_text="Window padding", manager=ctx.prescreen)

bcountset = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect((150, 0), (150, 20)), placeholder_text="Ball count", manager=ctx.prescreen)
restset = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect((150, 20), (150, 20)), placeholder_text="Restitution", manager=ctx.prescreen)
fricset = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect((150, 40), (150, 20)), placeholder_text="Friction", manager=ctx.prescreen)
passesset = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect((150, 60), (150, 20)), placeholder_text="Physics passes", manager=ctx.prescreen)
radset = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect((150, 80), (150, 20)), placeholder_text="Radius", manager=ctx.prescreen)

explanationlabel = pygame_gui.elements.UILabel(relative_rect=pygame.Rect((0, 300),(300, 20)), text="Use SPACE to flip gravity", manager = ctx.prescreen)
explanationlabel2 = pygame_gui.elements.UILabel(relative_rect=pygame.Rect((0, 320),(300, 20)), text="Use P to enter scene editor", manager = ctx.prescreen)
explanationlabel3 = pygame_gui.elements.UILabel(relative_rect=pygame.Rect((0, 340),(300, 20)), text="Use W to move objects / instantiate in editor", manager = ctx.prescreen)
explanationlabel4 = pygame_gui.elements.UILabel(relative_rect=pygame.Rect((0, 360),(300, 20)), text="Use L/R to select and BACKSPACE", manager = ctx.prescreen)
explanationlabel5 = pygame_gui.elements.UILabel(relative_rect=pygame.Rect((0, 380),(300, 20)), text="to delete in editor", manager = ctx.prescreen)