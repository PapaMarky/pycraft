import glob
import os
import platform
from pathlib import Path
import re

import  pycraft
from pycraft.map import Map
from pycraft import World
from pycraft.colors import get_map_color

from typing import List, Union, Tuple, Dict, Any, Callable, Set

import pygame
import pygame_gui

from pygame_gui.ui_manager import UIManager
from pygame_gui.core.interfaces import IContainerLikeInterface, IUIManagerInterface
from pygame_gui.elements.ui_panel import UIPanel
from pygame_gui.elements.ui_button import UIButton
from pygame_gui.elements.ui_image import UIImage
from pygame_gui.elements.ui_label import UILabel

from pygame_gui.elements.ui_drop_down_menu import UIDropDownMenu
from pygame_gui._constants import UI_DROP_DOWN_MENU_CHANGED

from pygame.event import custom_type

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
    def __init__(self, appsize, title=None, flags=pygame.RESIZABLE):
        '''
        Create a GuiApp

        Parameters:
        appsize: how big to make the root window
        title:   Title of the window
        flags:   pygame flags to pass into pygame.display.set_mode
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

class PycraftMapElement(UIImage):
    '''
    Screen object for displaying a single Minecraft map.
    '''
    def __init__(self,
                 rr: pygame.Rect,
                 manager: UIManager,
                 container: Union[IContainerLikeInterface, None],
                 image_dir: str,
                 pycraft_map: Map):
        '''
        Create a PycraftMapElement object. Creates an image using PIL,
        saves the image to a PNG then loads the image into a surface.

        Probably more efficient ways to do this, but this was quick and seems
        to be performant enough for my needs.

        Parameters:
        - rr: Relative Rectangle
        - manager: the UIManager for the app
        - container: The continer object.
        - image_dir: directory where temporary map PNG files are stored.
        - pycraft_map: A pycraft.Map object with the map loaded into it
        '''
        self._pycraft_map = pycraft_map
        img = pycraft_map.create_image()
        outpath = os.path.join(image_dir, os.path.basename(pycraft_map.path)[:-4] + '.png')
        img.save(outpath)
        surface = pygame.image.load_extended(outpath)
        super().__init__(rr, surface, manager)
        self._width = img.width

    def get_origin(self):
        '''
        Return the origin of the map in Minecraft world (block) coordinates.
        '''
        return self._pycraft_map.get_origin()

    @property
    def width(self):
        '''
        Width of the image in pixels. The map images are square, so this is also the height.
        '''
        return self._width

    @property
    def map_file_path(self):
        '''
        Path to the map file displayed by this object.
        '''
        return self._pycraft_map.path

class PycraftMapPanel(UIPanel):
    '''
    A UIPanel that holds a grid of maps

    Parameters:
    - rr: Relative Rectangle that describes where to put the element on the screen
    - manager: The UI manager object
    '''
    def __init__(self, rr, manager):
        super().__init__(rr, 0, manager)
        self._tops = []
        self._lefts = []
        self._map_elements = []
        self._image_dir = os.path.join(str(Path.home()), '.pycraft/maps/')
        if not os.path.exists(self._image_dir):
            os.makedirs(self._image_dir)

    def reset(self):
        '''
        Reset the map panel.

        Delete all of the existing maps and layout information.
        '''
        for e in self._map_elements:
            e.kill()
        self._tops = []
        self._lefts = []
        self._map_elements = []

    def add_map(self, pycraft_map: Map):
        '''
        Add a map to the Map Panel.

        Parameters:
        - pycraft_map: a pycraft map object
        '''
        origin = pycraft_map.get_origin()

        map_block_left = origin[0]
        self._insert_left(map_block_left)

        map_block_top = origin[1]
        self._insert_top(map_block_top)

        rr = pygame.Rect(0, 0, 128, 128)
        map_element = PycraftMapElement(rr, self.ui_manager, self, self._image_dir, pycraft_map)
        self._map_elements.append(map_element)

        self._do_layout()

    def _do_layout(self):
        '''
        Layout the maps in the grid.

        As new maps are added to the grid, they existing maps may need to be moved around
        to maintain correct relative position on the screen.
        '''
        for m in self._map_elements:
            map_origin = m.get_origin()
            # Adding one to m.width leaves a one pixel gap between the maps
            pixel_width = m.width + 1
            top = None
            for i in range(len(self._tops)):
                if self._tops[i] == map_origin[1]:
                    top = self.get_abs_rect().top + GAP + pixel_width * i
                    break
            if top is None:
                print(f'ERROR: this map is not in top list: {os.path.basename(m.map_file_path)}')

            left = None
            for i in range(len(self._lefts)):
                if self._lefts[i] == map_origin[0]:
                    left = self.get_abs_rect().left + GAP + pixel_width * i
                    break
            if left is None:
                print(f'ERROR: this map is not in left list: {os.path.basename(m.map_file_path)}')

            if left is None or top is None:
                continue
            m.set_position((left, top))

    def _insert_top(self, value):
        '''
        Helper function for maintaining the list of map "tops" used for aligning the maps
        within the grid.

        Parameters:
        - value: a map top (y of the map's origin)
        '''
        l = len(self._tops)
        if l > 0:
            for i in range(l):
                if value < self._tops[i]:
                    self._tops.insert(i, value)
                    return i
                if value == self._tops[i]:
                    return i
        self._tops.append(value)
        return l

    def _insert_left(self, value):
        '''
        Helper function for maintaining the list of map "lefts" used for aligning the maps
        within the grid.

        Parameters:
        - value: a map top (x of the map's origin)
        '''
        l = len(self._lefts)
        if l > 0:
            for i in range(l):
                if value < self._lefts[i]:
                    self._lefts.insert(i, value)
                    return i
                if value == self._lefts[i]:
                    return i
        self._lefts.append(value)
        return l

class PycraftMapToolApp(PycraftGuiApp):
    '''
    Application class for pycraft map tool.
    '''
    def __init__(self, size):
        '''
        Create and instance of PycraftMapToolApp

        Parameters:
        - size: sets the size of the root window
        '''
        super().__init__(size, 'Pycraft Map Tool')
        self._map_dict = {}

        y = self._world_selector.bottom + GAP
        x = GAP
        dw = self.size[0] - 2 * GAP
        dh = self.size[1] - y - GAP
        rr = pygame.Rect((x, y), (dw, dh))
        self._map_panel = PycraftMapPanel(rr, self.ui_manager)

    def handle_event(self, event):
        '''
        Handle events from the UIWorldSelector (inherited from the base class)
        '''
        if super().handle_event(event):
            return True
        if event.type == MAPAPP_WORLD_CHANGED:
            # the selected world has been changed. Load the map data for the new world.
            self.load_world(event.text)
            return True
        return False

    def load_world(self, world: pycraft.world.World):
        '''
        Load the maps from the new world.

        Parameters:
        - world: The pycraft world object of the saved world.
        '''
        world = self._world_selector.world
        # load the map files
        self._map_dict = {}
        mappath = world.mappath
        mapfilelist = glob.glob(os.path.join(mappath, 'map*.dat'))
        self._map_panel.reset()
        for f in mapfilelist:
            mobj = Map(f)
            # currently we only look at fully zoomed maps (zoom = 4)
            if mobj.get_zoom() == 4:
                self._map_panel.add_map(mobj)
                # run the event loop once so that the screen updates
                # It would probably be better to use threads, but this
                # way worked and it was easy.
                self.event_loop()

if __name__ == '__main__':
    app = PycraftMapToolApp((1024, 800))
    app.run()
