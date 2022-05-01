import os
from pathlib import Path

import pygame
import pygame_gui
from pygame_gui import UI_DROP_DOWN_MENU_CHANGED
from pygame_gui.core.interfaces import IUIManagerInterface
from pygame_gui.elements import UIPanel, UILabel, UIButton, UIDropDownMenu

import pycraft_gui
from pycraft import World

GAP = 10


class UIWorldSelector(UIPanel):
    """
    A Collection of elements for finding / selecting Minecraft save data.

    Parameters
      rect (pygame.Rect): Relative rect for contained widgets
      manager (IUIManagerInterface): the UI manager for the app
    """

    def __init__(self,
                 relative_rect,
                 manager: IUIManagerInterface,
                 container=None,
                 anchors=None
                 ):
        super().__init__(relative_rect, 1, manager,
                         container=container, anchors=anchors,
                         margins={
                             'top': GAP, 'left': GAP,
                             'bottom': GAP, 'right': GAP
                         })
        h = 30
        rr = pygame.Rect(0, 0, -1, h)

        self._world_label = UILabel(rr,
                                   'Saved World:',
                                   manager,
                                   container=self,
                                   anchors={
                                       'top': 'top',
                                       'left': 'left',
                                       'bottom': 'top',
                                       'right': 'left'
                                   })

        butt_w = 150
        butt_h = h
        rr = pygame.Rect(0, 0, butt_w, butt_h)
        rr.topright = (0,0)
        self._load_world_button = UIButton(relative_rect=rr,
                                           text='Load World',
                                           manager=manager,
                                           container=self,
                                           visible=True,
                                           anchors={'left': 'right',
                                                    'right': 'right',
                                                    'top': 'top',
                                                    'bottom': 'top'}
                                           )
        self.options = []
        self._find_worlds()
        self.options.insert(0,'None')
        selection = self.options[0]
        x = 0
        y = self._world_label.get_abs_rect().y
        w = self._load_world_button.rect.left - self._world_label.rect.right
        rr = pygame.Rect(x, y, w, h)
        print(f'RR: {rr}')
        self._world_menu = UIDropDownMenu(self.options, selection,
                                          rr,
                                          manager, container=container,
                                          anchors={
                                              'left': 'left',
                                              'right': 'right',
                                              'top': 'top',
                                              'bottom': 'top',
                                              'left_target': self._world_label,
                                              'right_target': self._load_world_button
                                          },
                                          expansion_height_limit=150)
        self._loaded_world = None
        self._selected_world = selection
        self._world = None
        self.set_load_world_button_enabled()

    def process_event(self, event: pygame.event.Event) -> bool:
        if event.type == UI_DROP_DOWN_MENU_CHANGED and event.ui_element == self._world_menu:
            print(f'drop down')
            self._selected_world = event.text
            self.set_load_world_button_enabled()
            return True
        if event.type == pygame_gui.UI_BUTTON_PRESSED and event.ui_element == self._load_world_button:
            print(f'Got')
            self.load_world(self.selected_world)
            return True
        return False

    def _find_worlds(self):
        """
        Find the Minecraft saved world data folders.

        Creates a list of World names which it stores in 'self.options'

        Only tested on MacOS so far.
        """
        # Add the WorldSelectorMenu
        savepaths = (
            '%HOME%/Library/Application Support/minecraft/saves',
            '%APPDATA%.minecraft'
            '%HOME%.minecraft'
        )
        # plat = platform.system()
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
        """
        The string name of the currently loaded Minecraft world. Can be None.
        """
        return self._loaded_world

    @property
    def selected_world(self):
        """
        The string name of the currently selected Minecraft world.
        """
        return self._selected_world

    def get_world_path(self, world: str = None):
        """
        Get the full path to the specified world save folder.
        """
        if world is None:
            world = self.selected_world
        return self._world_paths.get(world, None)

    def set_load_world_button_enabled(self):
        """
        Set the visiblity of the "Load World" button.

        When the selected and loaded worlds are the same, the button is disabled.
        """
        if self._selected_world != self._loaded_world and self._selected_world != 'None':
            self._load_world_button.show()
        else:
            self._load_world_button.hide()

    def load_world(self, world):
        """
        Load the world data for the app. Called when the world selection is completed.

        Override this function to load pycraft data required by App
        """
        worldpath = self.get_world_path()
        self._world = World(worldpath)
        self._loaded_world = world
        self.set_load_world_button_enabled()
        # Send event so App will actually load the new world
        event_data = {'text': self.selected_world,
                      'ui_element': self}
        pygame.event.post(pygame.event.Event(pycraft_gui.MAP_APP_WORLD_CHANGED, event_data))

    @property
    def world(self):
        """
        Return the pycraft.World object currently loaded.

        Can be None.
        """
        return self._world

    @property
    def bottom(self):
        """
        Return the Y coordinate of the bottom of this element.

        Useful for laying out elements below this one.
        """
        return self.rect.bottom
