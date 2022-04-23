import os
import platform
from pathlib import Path

import pygame
import pygame_gui

from pygame_gui.ui_manager import UIManager
from pygame_gui.core.interfaces import IUIManagerInterface
from pygame_gui.elements.ui_window import UIWindow
from pygame_gui.elements.ui_button import UIButton
from pygame_gui.elements.ui_text_box import UITextBox

from pygame_gui.elements.ui_image import UIImage
from pygame_gui.elements.ui_drop_down_menu import UIDropDownMenu
from pygame_gui._constants import UI_DROP_DOWN_MENU_CHANGED

from pygame.event import custom_type
MAPAPP_WORLD_CHANGED = custom_type()
MAPAPP_WORLD_SELECTED = custom_type()

class UIWorldSelector(UIWindow):
    def __init__(self,
                 rect: pygame.Rect,
                 manager: IUIManagerInterface,
                 visible: int = 0
                 ):
        super().__init__(rect,
                         manager,
                         window_display_title = 'Select Mincraft World',
                         visible = visible)
        # Add the WorldSelectorMenu
        # <HOMEDIR>/Library/Application Support/minecraft/saves
        savepaths = (
            '%HOME%/Library/Application Support/minecraft/saves',
            '%APPDATA%\.minecraft'
            '%HOME%\.minecraft'
        )
        plat = platform.system()
        home = str(Path.home())
        savedir = ''
        for path in savepaths:
            p = path.replace('%HOME%', home)
            print(f' - {p}')
            if os.path.exists(p):
                savedir = p
                break

        self._world_paths = {}
        options = []
        for fname in os.listdir(savedir):
            options.append(fname)
            self._world_paths[fname] = os.path.join(savedir, fname)
        options.sort()

        rr = pygame.Rect((10,10), (self.rect.width - 50, 30))
        element = UIDropDownMenu(options, options[0], rr, self.ui_manager, container=self, visible=True)
        self.selected_world = options[0]

    @property
    def world(self):
        return self.selected_world

    def get_world_path(self, world=None):
        if world is None:
            world = self.selected_world
        return self._world_paths.get(world, None)

    def process_event(self, event: pygame.event.Event) -> bool:
        if super().process_event(event):
            return True
        if event.type == UI_DROP_DOWN_MENU_CHANGED:
            self.selected_world = event.text
            event_data = {'text': event.text,
                          'ui_element': self}
            pygame.event.post(pygame.event.Event(MAPAPP_WORLD_CHANGED, event_data))

    def on_close_window_button_pressed(self):
        self.hide()
        event_data = {'text': self.selected_world,
                      'ui_element': self}
        pygame.event.post(pygame.event.Event(MAPAPP_WORLD_SELECTED, event_data))

class GuiApp():
    def __init__(self, appsize, title=None):
        self.title = title
        self._size = appsize
        self._elements = {}
        pygame.init()

        if title:
            pygame.display.set_caption(title)
        self.root_window_surface = pygame.display.set_mode(self.size)

        self.background_surface = pygame.Surface(self.size).convert()
        self.background_surface.fill(pygame.Color('#303030'))
        # self.ui_manager = UIManager((1024, 600), 'data/themes/theme_3.json')
        self._ui_manager = UIManager(self.size)
        self.clock = pygame.time.Clock()
        self.is_running = True

    def add_element(self, el_name, el):
        self._elements[el_name] = el

    @property
    def size(self):
        return self._size

    @property
    def ui_manager(self):
        return self._ui_manager

    def handle_event(self, event):
        '''
        Override this function to handle custome events
        '''
        pass

    def run(self):
        while self.is_running:
            time_delta = self.clock.tick(60)/1000.0
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.is_running = False
                self._ui_manager.process_events(event)
                self.handle_event(event)

            self._ui_manager.update(time_delta)

            self.root_window_surface.blit(self.background_surface, (0, 0))
            self._ui_manager.draw_ui(self.root_window_surface)

            pygame.display.update()

class MapApp(GuiApp):
    def __init__(self, size):
        super().__init__(size, 'MapApp')
        bw = 200
        bh = 30
        gap = 10
        rr = pygame.Rect(gap, gap, self.size[0]/2, bh)
        self.world_label = UITextBox('', rr, self.ui_manager)
        w = self.size[0]/2
        h = self.size[1]/2
        x = self.size[0]/2 - w/2
        y = self.size[1]/2 - h/2
        rr = pygame.Rect((x, y), (w, h))
        self.world_selector = UIWorldSelector(rr, self.ui_manager)
        self.set_world(self.world_selector.world)
        rr = pygame.Rect(self.size[0] - (bw + gap), self.size[1] - (bh + gap), bw, bh)
        self.change_world_button = UIButton(rr, text='Select World', manager=self.ui_manager)

    def set_world(self, world):
        print(f'Set World to "{world}"')
        self.world_label.set_text(f'<b>World: </b>{world}')

    def load_world(self, world):
        print(f'Loading World... ({world})')
        worldpath = self.world_selector.get_world_path()
        print(f'  - Path: "{worldpath}"')
        
    def handle_event(self, event):
        if event.type == MAPAPP_WORLD_CHANGED:
            self.set_world(event.text)
        if event.type == MAPAPP_WORLD_SELECTED:
            self.load_world(event.text)
        if event.type == pygame_gui.UI_BUTTON_PRESSED and event.ui_element == self.change_world_button:
            self.world_selector.show()

if __name__ == '__main__':
    app = MapApp((1024, 600))
    app.run()
