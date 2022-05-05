import glob
import json
import os

import pygame
from pygame_gui import UI_DROP_DOWN_MENU_CHANGED
from pygame_gui.elements import UIPanel, UILabel, UIImage
from pygame_gui_extras.app import GuiApp

from pycraft_gui import PYCRAFT_WORLD_CHANGED
from pycraft_gui.pycraft_app import PYCRAFT_WORLD_SELECTION_CHANGED
from pycraft_gui.ui_world_selector import UIWorldSelector


class WorldDataViewerApp(GuiApp):
    def __init__(self, size):
        super(WorldDataViewerApp, self).__init__(size, title='World Data Viewer', )
        self._entities_count_text = None
        self._world_data = None
        self._top_panel = None
        self._world_selector = None
        self._selected_world = ''

    @property
    def world_menu(self):
        return self._world_selector.world_menu

    def handle_event(self, event):
        if super().handle_event(event):
            return True
        if event.type == PYCRAFT_WORLD_SELECTION_CHANGED:
            # the selected world has been changed. Load the map data for the new world.
            self.on_select_world()
            return True
        return False

    def setup_world_info_panel(self, x, y, width, height):
        margin = 5
        panel_width = width - self._world_selector.rect.width

        self._world_info_panel = UIPanel(
            pygame.Rect(x, y, panel_width, height), 0,
            self.ui_manager, margins={'top': margin, 'left': margin, 'bottom': margin, 'right': margin},
            anchors={
                'top': 'top',
                'left': 'left',
                'bottom': 'top',
                'right': 'right',
                'left_target': self._world_selector
            }
        )
        # ICON
        icon_width = 70
        icon_height = 70
        ix = 5
        iy = 5
        self.world_icon = UIImage(
            pygame.Rect(ix, iy, icon_width, icon_height),
            self.blank_icon(), self.ui_manager,
            container=self._world_info_panel,
            anchors={
                'top': 'top',
                'left': 'left',
                'bottom': 'top',
                'right': 'left'
            }
        )
        x += icon_width + 5 + ix
        label_width = 80
        field_width = 70
        label_height = 20
        # ENTITIES
        entities_label = UILabel(
            pygame.Rect(x, y+3, label_width, label_height),
            'Entities:', self.ui_manager,
            container=self._world_info_panel,
            object_id='@TextFieldLabel',
            anchors={
                'top': 'top',
                'left': 'left',
                'bottom': 'top',
                'right': 'left'
            }
        )
        self._entities_count_text = UILabel(
            pygame.Rect(0, 3, field_width, label_height),
            '', self.ui_manager,
            container=self._world_info_panel,
            object_id='@TextField',
            anchors={
                'top': 'top',
                'left': 'left',
                'bottom': 'top',
                'right': 'left',
                'left_target': entities_label
            }
        )
        # REGIONS
        region_label = UILabel(
            pygame.Rect(x, y + 3, label_width, label_height),
            'Regions:', self.ui_manager,
            container=self._world_info_panel,
            object_id='@TextFieldLabel',
            anchors={
                'top': 'top',
                'left': 'left',
                'bottom': 'top',
                'right': 'left',
                'top_target': entities_label
            }
        )
        self._regions_count_text = UILabel(
            pygame.Rect(0, 3, field_width, label_height),
            '', self.ui_manager,
            container=self._world_info_panel,
            object_id='@TextField',
            anchors={
                'top': 'top',
                'left': 'left',
                'bottom': 'top',
                'right': 'left',
                'left_target': region_label,
                'top_target': self._entities_count_text
            }
        )
        # POIs
        poi_label = UILabel(
            pygame.Rect(x, y + 3, label_width, label_height),
            'POIs:', self.ui_manager,
            container=self._world_info_panel,
            object_id='@TextFieldLabel',
            anchors={
                'top': 'top',
                'left': 'left',
                'bottom': 'top',
                'right': 'left',
                'top_target': region_label
            }
        )
        self._poi_count_text = UILabel(
            pygame.Rect(0, 3, field_width, label_height),
            '', self.ui_manager,
            container=self._world_info_panel,
            object_id='@TextField',
            anchors={
                'top': 'top',
                'left': 'left',
                'bottom': 'top',
                'right': 'left',
                'left_target': poi_label,
                'top_target': self._regions_count_text
            }
        )

        maps_label = UILabel(
            pygame.Rect(0, y+3, label_width, label_height),
            'Maps:', self.ui_manager,
            container=self._world_info_panel,
            object_id='@TextFieldLabel',
            anchors={
                'top': 'top',
                'left': 'left',
                'bottom': 'top',
                'right': 'left',
                'left_target': self._regions_count_text
            }
        )
        self._maps_count_text = UILabel(
            pygame.Rect(0, 3, field_width, label_height),
            '', self.ui_manager,
            container=self._world_info_panel,
            object_id='@TextField',
            anchors={
                'top': 'top',
                'left': 'left',
                'bottom': 'top',
                'right': 'left',
                'left_target': maps_label
            }
        )


    def setup(self):
        width = self.size[0]
        height = 100
        x = 0
        y = 1
        self._world_selector = UIWorldSelector(
            pygame.Rect(x, y, width/2, height),
            self.ui_manager,
            anchors={
                'top': 'top',
                'left': 'left',
                'bottom': 'top',
                'right': 'left'
            }
        )
        self.setup_world_info_panel(x, y, width, height)

    def blank_icon(self):
        icon = pygame.surface.Surface((64,64))
        icon.fill('#8080E0')
        return icon

    def get_world_info(self):
        path = self._world_selector.get_world_path()
        self._world_data = {
            'files': {
                'maps': [],
                'entities': [],
                'poi': [],
                'region': []
            },
            'players': []
        }
        if path is None:
            self._maps_count_text.set_text('')
            self._entities_count_text.set_text('')
            self._regions_count_text.set_text('')
            self._poi_count_text.set_text('')
            return
        mappath = os.path.join(path, 'data')
        file_list = glob.glob(os.path.join(mappath, 'map*.dat'))
        self._world_data['files']['maps'] = file_list
        self._maps_count_text.set_text(str(len(file_list)))

        region_path = os.path.join(path, 'region')
        file_list = glob.glob(os.path.join(region_path, 'r.*.mca'))
        self._world_data['files']['region'] = file_list
        self._regions_count_text.set_text(str(len(file_list)))

        entity_path = os.path.join(path, 'entities')
        print(f'entities: {entity_path}')
        file_list = glob.glob(os.path.join(entity_path, 'r.*.mca'))
        self._world_data['files']['entity'] = file_list
        self._entities_count_text.set_text(str(len(file_list)))

        poi_path = os.path.join(path, 'poi')
        file_list = glob.glob(os.path.join(poi_path, 'r.*.mca'))
        self._world_data['files']['poi'] = file_list
        self._poi_count_text.set_text(str(len(file_list)))

        icon_path = os.path.join(path, 'icon.png')
        if os.path.exists(icon_path):
            icon = pygame.image.load(icon_path)
        else:
            icon = self.blank_icon()
        self.world_icon.set_image(icon)

    def on_select_world(self):
        print(f'world selected: {self._world_selector.selected_world}...')
        self.get_world_info()

    def load_world(self):
        print(f'loading world...')

app = WorldDataViewerApp((1020, 900))
app.ui_manager.get_theme().load_theme('themes/pycraft.json')
app.setup()
app.run()
