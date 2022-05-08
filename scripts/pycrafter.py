import itertools
from typing import Union

import pygame
import pygame_gui
from pygame_gui.elements import UIPanel, UIImage, UILabel

from pycraft_gui.gui_app import GuiApp
from pycraft_gui.ui_image_tiled import UIImageTiled


class PycrafterApp(GuiApp):
    def __init__(self, size, framerate=60, ):
        title = 'Pycraft'
        super(PycrafterApp, self).__init__(size, framerate=framerate, title=title)

    def setup(self):
        x = 0
        y = 0
        window_size = self.size
        width = window_size[0]
        height = 200
        # Top Panel:
        # tiled image background panel
        dirt_surface = pygame.image.load('dirt.jpg')
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
        y = self.size[1] - height
        rect = pygame.Rect(0, -height, width, height)
        print(f'size: {self.size}')
        print(f'rect: {rect}')
        self._bottom_dirt = UIImageTiled(
            rect,
            dirt_surface,
            self.ui_manager,
            #object_id='@dirt_background',
            anchors={
                'top': 'bottom',
                'left': 'left',
                'bottom': 'bottom',
                'right': 'right'
            }
        )

app = PycrafterApp((1020, 900))
app.ui_manager.get_theme().load_theme('theme.json')

app.setup()
app.run()
