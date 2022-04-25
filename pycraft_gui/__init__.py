import os
import platform
from pathlib import Path
import re

from pycraft import World

import pygame
import pygame_gui

from pygame.event import custom_type

from pygame_gui.core.interfaces import IUIManagerInterface
from pygame_gui.ui_manager import UIManager
from pygame_gui.elements.ui_button import UIButton
from pygame_gui.elements.ui_drop_down_menu import UIDropDownMenu
from pygame_gui.elements.ui_label import UILabel
from pygame_gui._constants import UI_DROP_DOWN_MENU_CHANGED


MAPAPP_WORLD_CHANGED = custom_type()

GAP = 10

class UIWorldSelector():
    '''
    A Collection of elements for finding / selecting Minecraft save data.

    Parameters
      rect (pygame.Rect): Relative rect for contained widgets
      manager (IUIManagerInterface): the UI manager for the app
    '''
    def __init__(self,
                 rect: pygame.Rect,
                 manager: IUIManagerInterface
                 ):
        rr = pygame.Rect(GAP, GAP, -1, -1)

        self.world_label = UILabel(rr, 'Saved World:', manager)
        self.options = []
        self._find_worlds()
        selection = self.options[0]
        # make a copy so we don't change world_label's rect
        rr = pygame.Rect(self.world_label.rect)
        self._bottom = rr.bottom
        rr.left = rr.right + GAP
        rr.width = 500
        UIDropDownMenu(self.options, selection, rr, manager, visible=True)
        self._loaded_world = None
        self._selected_world = selection
        rr.left = rr.right + GAP
        rr.width = rr.height = -1
        self._load_world_button = UIButton(rr, text='Load World', manager=manager)
        bottom = self._load_world_button.rect.height
        if bottom > self._bottom:
            self._bottom = bottom
        self.set_load_world_button_enabled()
        self._world = None

    def _find_worlds(self):
        '''
        Find the Minecraft saved world data folders.

        Creates a list of World names which it stores in 'self.options'

        Only tested on MacOS so far.
        '''
        # Add the WorldSelectorMenu
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
            if os.path.exists(p):
                savedir = p
                break

        self._world_paths = {}
        self.options = []
        for fname in os.listdir(savedir):
            self.options.append(fname)
            self._world_paths[fname] = os.path.join(savedir, fname)
        self.options.sort()

    @property
    def loaded_world(self):
        '''
        The string name of the currently loaded Minecraft world. Can be None.
        '''
        return self._loaded_world

    @property
    def selected_world(self):
        '''
        The string name of the currently selected Minecraft world.
        '''
        return self._selected_world

    def get_world_path(self, world:str = None):
        '''
        Get the full path to the specified world save folder.
        '''
        if world is None:
            world = self.selected_world
        return self._world_paths.get(world, None)

    def set_load_world_button_enabled(self):
        '''
        Set the visiblity of the "Load World" button.

        When the selected and loaded worlds are the same, the button is disabled.
        '''
        if self._selected_world != self._loaded_world:
            self._load_world_button.enable()
        else:
            self._load_world_button.disable()

    def handle_event(self, event: pygame.event.Event) -> bool:
        '''
        Handle events specific to this widget.
        '''
        if event.type == UI_DROP_DOWN_MENU_CHANGED:
            self._selected_world = event.text
            self.set_load_world_button_enabled()
            return True
        if event.type == pygame_gui.UI_BUTTON_PRESSED and event.ui_element == self._load_world_button:
            self.load_world(self.selected_world)
            return True
        return False

    def load_world(self, world):
        '''
        Load the world data for the app. Called when the world selection is completed.

        Override this function to load pycraft data required by App
        '''
        worldpath = self.get_world_path()
        self._world = World(worldpath)
        self._loaded_world = world
        self.set_load_world_button_enabled()
        # Send event so App will actually load the new world
        event_data = {'text': self.selected_world,
                      'ui_element': self}
        pygame.event.post(pygame.event.Event(MAPAPP_WORLD_CHANGED, event_data))

    @property
    def world(self):
        '''
        Return the pycraft.World object currently loaded.

        Can be None.
        '''
        return self._world

    @property
    def bottom(self):
        '''
        Return the Y coordinate of the bottom of this element.

        Useful for laying out elements below this one.
        '''
        return self._bottom

class GuiApp():
    '''
    Base class for any pygame_gui app
    '''
    def __init__(self, appsize, title=None, flags=0):
        '''
        Create a GuiApp

        Parameters:
        appsize: how big to make the root window
        title:   Title of the window
        flags:   pygame flags to pass into pygame.display.set_mode (pygame.RESIZABLE)
        '''
        self.title = title
        self._size = appsize
        pygame.init()

        if title:
            pygame.display.set_caption(title)
        self.root_window_surface = pygame.display.set_mode(self.size, flags)

        self.background_surface = pygame.Surface(self.size).convert()
        self.background_surface.fill(pygame.Color('#303030'))
        self._ui_manager = UIManager(self.size)
        self.clock = pygame.time.Clock()
        self.is_running = True

    @property
    def size(self):
        '''
        Size of the root window
        '''
        return self._size

    @property
    def ui_manager(self):
        '''
        The UIManager of the application
        '''
        return self._ui_manager

    def handle_event(self, event):
        '''
        Override this function to handle custom events
        '''
        pass

    def event_loop(self):
        '''
        Run the event loop once.

        This is a handy way to get the screen to update during long operations when you are too lazy
        to make it work with threading.
        '''
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

    def run(self):
        '''
        Run the app
        '''
        while self.is_running:
            self.event_loop()

class PycraftGuiApp(GuiApp):
    '''
    A GuiApp for Pycraft

    Manages Saved location / selection / loading of pycraft.World
    '''

    def __init__(self, size, title):
        '''
        Create a PycraftGuiApp object
        Parameters:
        - size: size of the window
        - title: title to display on the window
        '''
        super().__init__(size, title)
        self._add_world_elements()

    def _add_world_elements(self):
        '''
        Add elements for selecting from existing saved worlds.
        '''
        bh = 60
        rr = pygame.Rect(GAP, GAP, self.size[0]/2, bh)
        self._world_selector = UIWorldSelector(rr, self.ui_manager)

    def handle_event(self, event):
        '''
        Pass events to the world_selector object for processing
        '''
        return self._world_selector.handle_event(event)
