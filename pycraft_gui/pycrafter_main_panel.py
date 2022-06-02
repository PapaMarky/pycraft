# root container - holds scrollbars and "view" container
# view container - tracks size of root container and scroll bars. (changes size when scrollbars come / go?)
# scrollable container - the container that gets scrolled around
#
import pycraft_gui
import pygame
from pygame_gui import UI_BUTTON_PRESSED
from pygame_gui.elements import UILabel, UIPanel

from pycraft import World
from pycraft_gui.constants import PYCRAFT_WORLD_MENU_SELECTED, PYCRAFT_WORLD_MENU_UNHOVERED, PYCRAFT_WORLD_MENU_HOVERED
from pycraft_gui.pycraft_world_menu import PycraftWorldMenu
from pycraft_gui.ui_image_tiled import UIImageTiled

class PycrafterHeader:
    def __init__(self, manager, container):
        self._label = None
        self._top_dirt = None
        # Top Panel:
        # tiled image background panel
        x = 0
        y = 0
        window_size = container.rect.size
        width = window_size[0]
        height = 150
        dirt_image_path = pycraft_gui.get_data_file_path('dark_dirt.jpg')
        dirt_surface = pygame.image.load(dirt_image_path)
        dirt_rect = pygame.Rect(x, y, width, height)
        dirt_anchors = {
            'top': 'top', 'left': 'left',
            'bottom': 'top', 'right': 'right'
        }
        self._top_dirt = UIImageTiled(
            dirt_rect,
            dirt_surface,
            manager,
            container=container,
            object_id='@dirt_background',
            anchors=dirt_anchors
        )
        label_rect = pygame.Rect(dirt_rect)
        self._label = UILabel(
            label_rect,
            'PyCraft', manager,
            object_id='@title_label',
            container=container,
            anchors=dirt_anchors
        )

    @property
    def rect(self):
        return self._top_dirt.rect

    def get_abs_rect(self):
        return self._top_dirt.get_abs_rect()

    @property
    def image(self):
        return self._top_dirt


class PycrafterFooter:
    def __init__(self, manager, container):
        dirt_image_path = pycraft_gui.get_data_file_path('dark_dirt.jpg')
        dirt_surface = pygame.image.load(dirt_image_path)
        window_size = container.rect.size
        width = window_size[0]
        height = 150
        rect = pygame.Rect(0, -height, width, height)
        print(f'size: {container.rect.size}')
        print(f'rect: {rect}')
        self._bottom_dirt = UIImageTiled(
            rect,
            dirt_surface,
            manager,
            container=container,
            object_id='@dirt_background',
            anchors={
                'top': 'bottom',
                'left': 'left',
                'bottom': 'bottom',
                'right': 'right'
            }
        )
        # add buttons to bottom pain
        btn_width = 150
        btn_height = 50
        n_buttons = 3
        btn_gap = 30
        btn_y = self._bottom_dirt.rect.center[1] - btn_height / 2
        btn_x = self._bottom_dirt.rect.width/2 - (n_buttons * btn_width + (n_buttons - 1) * btn_gap)/2

        ## Map button
        from pygame_gui.elements import UIButton
        self._map_button = UIButton(
            pygame.Rect(btn_x, btn_y, btn_width, btn_height),
            'Map Data',
            manager,
            container=container,
            tool_tip_text='View Map Data',
            anchors={
                'top': 'top',
                'left': 'left',
                'bottom': 'bottom',
                'right': 'left'
            },
            visible=0
        )
        ## data button
        btn_x += btn_width + btn_gap
        self._data_button = UIButton(
            pygame.Rect(btn_x, btn_y, btn_width, btn_height),
            'View World Data',
            manager,
            container=container,
            anchors={
                'top': 'top',
                'left': 'left',
                'bottom': 'bottom',
                'right': 'left'
            }
        )
        ## configuration button
        btn_x += btn_width + btn_gap
        self._configuration_button = UIButton(
            pygame.Rect(btn_x, btn_y, btn_width, btn_height),
            'Configuration',
            manager,
            container=container,
            anchors={
                'top': 'top',
                'left': 'left',
                'bottom': 'bottom',
                'right': 'left'
            },
            tool_tip_text='Set Pycraft Configuration',
            starting_height=3
        )
        self._configuration_button.enable()

    @property
    def rect(self):
        return self._bottom_dirt.rect

    @property
    def image(self):
        return self._bottom_dirt

class PycrafterMainPanel(UIPanel):
    def __init__(self, *args, **kwargs):
        self._app = kwargs.pop('app', None)
        super(PycrafterMainPanel, self).__init__(*args, **kwargs)
        self._world_menu = None
        self._bottom_dirt = None
        self._top_dirt = PycrafterHeader(self.ui_manager, self)
        self._bottom_dirt = PycrafterFooter(self.ui_manager, self)

        width = self.rect.width - 150
        height = self.rect.height - (self._top_dirt.rect.height + self._bottom_dirt.rect.height)
        x = self.rect.width / 2 - width / 2
        rr = pygame.Rect(x, 0, width, height)
        print(f'rr: {rr}')
        self._world_menu = PycraftWorldMenu(
            rr, self.ui_manager,
            container=self,
            anchors={
                'top': 'top',
                'left': 'left',
                'bottom': 'bottom',
                'right': 'right',
                'top_target': self._top_dirt.image,
                'bottom_target': self._bottom_dirt.image
            }
        )

        saved_worlds = World.get_saved_worlds()
        for world in saved_worlds:
            print(f'World: {world["name"]}')
            self._world_menu.add_item(
                world['icon_path'],
                world['name'], world['file_name'],
                world['last_played'], world['mode'], world['cheats'], world['version'], world['has_maps']
            )
        self._world_menu.fit_scrolling_area_to_items()

    def process_event(self, event: pygame.event.Event) -> bool:
        if event.type == PYCRAFT_WORLD_MENU_HOVERED:
            print(f'PYCRAFT_WORLD_MENU_HOVERED: {event.world_data["name"]}, has maps: {event.world_data["has_maps"]}')
            if self._world_menu.selected_item is None:
                if event.world_data['has_maps']:
                    self._bottom_dirt._map_button.show()
                else:
                    self._bottom_dirt._map_button.hide()
        if event.type == PYCRAFT_WORLD_MENU_UNHOVERED:
            print(f'PYCRAFT_WORLD_MENU_UNHOVERED: {event.world_data["name"]}, selection: {self._world_menu.selected_item}')
            if self._world_menu.selected_item is None:
                self._bottom_dirt._map_button.hide()
        if event.type == PYCRAFT_WORLD_MENU_SELECTED:
            print(f'PYCRAFT_WORLD_MENU_SELECTED: {event.world_data["name"]}')
            if event.world_data['has_maps']:
                self._bottom_dirt._map_button.show()
            else:
                self._bottom_dirt._map_button.hide()
        if event.type == UI_BUTTON_PRESSED:
            if event.ui_element == self._bottom_dirt._map_button:
                print(f'Do Map Button')
                self._app.show_map()
                return True
            elif event.ui_element == self._bottom_dirt._data_button:
                print(f'Do Data Button')
                self._app.show_data()
                return True
            elif event.ui_element == self._bottom_dirt._configuration_button:
                print(f'Do Config Button')
                self._app.show_configuration()
                return True
