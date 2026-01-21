from common import *
class EditorElement:
    def initiate(self):
        self.objselector = pygame_gui.elements.UIDropDownMenu(relative_rect=pygame.Rect((ctx.width - 100, ctx.height - 25), (100, 25)), options_list = ["None", "Ball", "Rectangle", "Line", "Empty"], starting_option ="None", manager = ctx.editormanager)

        self.typeentry = pygame_gui.elements.UILabel(relative_rect=pygame.Rect((0, ctx.height - 40), (100, 20)), text="Object type", manager=ctx.editormanager)
        self.typeselector = pygame_gui.elements.UIDropDownMenu(relative_rect=pygame.Rect((0, ctx.height - 20), (100, 25)), options_list = ["Circle", "Rectangle", "Line", "Empty"], starting_option ="Circle", manager = ctx.editormanager)

        self.masslabel = pygame_gui.elements.UILabel(relative_rect=pygame.Rect((0, 0), (200, 20)),text=f"Mass: 1", manager=ctx.editormanager)
        self.massslider = pygame_gui.elements.UIHorizontalSlider(relative_rect=pygame.Rect((0, 20), (200, 20)), start_value=1, value_range=(1, 20),manager=ctx.editormanager)

        self.anglelabel = pygame_gui.elements.UILabel(relative_rect=pygame.Rect((0, 0), (200, 20)), text=f"Angle: 0",manager=ctx.editormanager)
        self.angleslider = pygame_gui.elements.UIHorizontalSlider(relative_rect=pygame.Rect((0, 20), (200, 20)),start_value=0, value_range=(0, 180),manager=ctx.editormanager)

        self.spinvellabel = pygame_gui.elements.UILabel(relative_rect=pygame.Rect((0, 0), (200, 20)), text=f"Spin velocity: 0",manager=ctx.editormanager)
        self.spinvelslider = pygame_gui.elements.UIHorizontalSlider(relative_rect=pygame.Rect((0, 20), (200, 20)),start_value=0, value_range=(0, 10),manager=ctx.editormanager)

        self.anglelabel.hide()
        self.angleslider.hide()
        self.spinvelslider.hide()
        self.spinvellabel.hide()

        self.staticcheck = pygame_gui.elements.UICheckBox(relative_rect=pygame.Rect((0, 40), (25, 25)),text="Static", initial_state=False, manager=ctx.editormanager)
        self.trailcheck = pygame_gui.elements.UICheckBox(relative_rect=pygame.Rect((0, 65), (25, 25)),text="Draw trail", initial_state=False, manager=ctx.editormanager)
        self.infmasscheck = pygame_gui.elements.UICheckBox(relative_rect=pygame.Rect((0, 90), (25, 25)),text="Infinite mass", initial_state=False, manager=ctx.editormanager)

        self.childlabel = pygame_gui.elements.UILabel(relative_rect=pygame.Rect((240, 0), (300, 20)), text=f"Child mode, press ENTER to exit",manager=ctx.editormanager)
        self.childlabel.hide()