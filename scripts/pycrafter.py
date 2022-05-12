import os

import pygame
from pygame_gui.elements import UILabel

import pycraft_gui
from pycraft import World
from pycraft_gui.gui_app import GuiApp
from pycraft_gui.constants import PYCRAFT_WORLD_MENU_HOVERED, PYCRAFT_WORLD_MENU_UNHOVERED, \
    PYCRAFT_WORLD_MENU_SELECTED
from pycraft_gui.pycraft_world_menu import PycraftWorldMenu
from pycraft_gui.ui_image_tiled import UIImageTiled

print(f'Pycraft GUI Installed at "{pycraft_gui.install_path}"')
print(f' - Data Dir: {pycraft_gui.get_data_dir()}')
# root container - holds scrollbars and "view" container
# view container - tracks size of root container and scroll bars. (changes size when scrollbars come / go?)
# scrollable container - the container that gets scrolled around
#


class PycrafterApp(GuiApp):
    def __init__(self, size, framerate=60, ):
        self._world_menu = None
        self._bottom_dirt = None
        self._dirt_label = None
        self._top_dirt = None
        title = 'Pycraft'
        super(PycrafterApp, self).__init__(size, framerate=framerate, title=title)
        themes_dir = pycraft_gui.get_themes_dir()
        print(f'themes dir: {themes_dir}')
        if themes_dir:
            self.ui_manager.get_theme().load_theme(os.path.join(themes_dir, 'pycraft_theme.json'))


    def setup(self):
        x = 0
        y = 0
        window_size = self.size
        width = window_size[0]
        height = 150
        # Top Panel:
        # tiled image background panel
        data_dir = pycraft_gui.get_data_dir()
        if data_dir:
            dirt_image_path = os.path.join(data_dir, 'dark_dirt.jpg')
        dirt_surface = pygame.image.load(dirt_image_path)
        dirt_rect = pygame.Rect(x, y, width, height)
        dirt_anchors = {
            'top': 'top',
            'left': 'left',
            'bottom': 'top',
            'right': 'right'
        }
        self._top_dirt = UIImageTiled(
            dirt_rect,
            dirt_surface,
            self.ui_manager,
            object_id='@dirt_background',
            anchors=dirt_anchors
        )
        label_rect = pygame.Rect(dirt_rect)
        self._dirt_label = UILabel(
            label_rect,
            'PyCraft', self.ui_manager,
            object_id='@title_label',
            anchors=dirt_anchors
        )
        rect = pygame.Rect(0, -height, width, height)
        print(f'size: {self.size}')
        print(f'rect: {rect}')
        self._bottom_dirt = UIImageTiled(
            rect,
            dirt_surface,
            self.ui_manager,
            # object_id='@dirt_background',
            anchors={
                'top': 'bottom',
                'left': 'left',
                'bottom': 'bottom',
                'right': 'right'
            }
        )
        width = self.size[0] - 150
        height = self.size[1] - (self._top_dirt.rect.height + self._bottom_dirt.rect.height)
        x = self.size[0] / 2 - width / 2
        rr = pygame.Rect(x, 0, width, height)
        print(f'rr: {rr}')
        self._world_menu = PycraftWorldMenu(
            rr, self.ui_manager,
            starting_height=5,
            anchors={
                'top': 'top',
                'left': 'left',
                'bottom': 'bottom',
                'right': 'right',
                'top_target': self._top_dirt,
                'bottom_target': self._bottom_dirt
            }
        )

        saved_worlds = World.get_saved_worlds()
        for world in saved_worlds:
            print(f'World: {world["name"]}')
            self._world_menu.add_item(
                world['icon_path'],
                world['name'], world['file_name'],
                world['last_played'], world['mode'], world['cheats'], world['version']
            )
        self._world_menu.fit_scrolling_area_to_items()

    def handle_event(self, event):
        if event.type == PYCRAFT_WORLD_MENU_HOVERED:
            print(f'PYCRAFT_WORLD_MENU_HOVERED: {event.world_data["name"]}')
        if event.type == PYCRAFT_WORLD_MENU_UNHOVERED:
            print(f'PYCRAFT_WORLD_MENU_UNHOVERED: {event.world_data["name"]}')
        if event.type == PYCRAFT_WORLD_MENU_SELECTED:
            print(f'PYCRAFT_WORLD_MENU_SELECTED: {event.world_data["name"]}')

app = PycrafterApp((1020, 900))
app.setup()
app.run()
