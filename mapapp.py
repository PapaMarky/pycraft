import glob
import os
from pathlib import Path

import  pycraft
import pycraft_gui

from pycraft.map import Map
from pycraft import World
from pycraft.colors import get_map_color

from typing import List, Union, Tuple, Dict, Any, Callable, Set

import pygame
import pygame_gui

from pygame_gui.ui_manager import UIManager
from pygame_gui.core.interfaces import IContainerLikeInterface
from pygame_gui.elements.ui_panel import UIPanel
from pygame_gui.elements.ui_image import UIImage

from pygame.event import custom_type

GAP = 10

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

class PycraftMapToolApp(pycraft_gui.PycraftGuiApp):
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
        if event.type == pycraft_gui.MAPAPP_WORLD_CHANGED:
            # the selected world has been changed. Load the map data for the new world.
            self.load_world_maps(event.text)
            return True
        return False

    def load_world_maps(self, world: pycraft.world.World):
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
