import datetime
import time
from typing import Union, Tuple

# root container - holds scrollbars and "view" container
# view container - tracks size of root container and scroll bars. (changes size when scrollbars come / go?)
# scrollable container - the container that gets scrolled around
#

import pygame
from pygame_gui.core import UIFontDictionary, UIAppearanceTheme
from pygame_gui.elements import UILabel, UIScrollingContainer, UIPanel, UIImage, UITextBox

from pycraft import World
from pycraft_gui.gui_app import GuiApp
from pycraft_gui.ui_image_tiled import UIImageTiled


class PycraftWorldMenuItem(UIPanel):
    def __init__(self,
                 icon_path : str,
                 name : str,
                 file_name : str,
                 last_played : datetime.datetime,
                 mode : str,
                 cheats : bool,
                 version: str,
                 menu,
                 relative_rect, starting_layer_height, manager,
                 margin = 10,
                 **kwargs):
        super(PycraftWorldMenuItem, self).__init__(relative_rect, starting_layer_height, manager, **kwargs)
        icon_surface = pygame.image.load(icon_path)
        icon_size = 100
        icon_surface = pygame.transform.smoothscale(icon_surface, (icon_size, icon_size))

        x = margin
        y = relative_rect.height / 2 - icon_surface.get_height() / 2
        icon_rect = pygame.Rect(x, y, icon_surface.get_width(), icon_surface.get_height())
        self._icon = UIImage(
            icon_rect,
            icon_surface, manager, container=self,
            anchors={
                'top': 'top',
                'left': 'left',
                'bottom': 'top',
                'right': 'left'
            }
        )
        self._text = []
        item_width = menu.item_width - icon_surface.get_width() - 3 * margin
        item_height = icon_rect.height / 3
        text = [
            f'{name}',
            f'{file_name} ({last_played.strftime("%m/%d/%Y %I:%M:%S %p")})',
            f'{mode} Mode,{" Cheats," if cheats else ""} Version: {version}'
        ]
        for i in range(3):
            text_rect = pygame.Rect(
                margin,
                margin + i * item_height,
                item_width,
                item_height
            )
            object_id = '@menu_item_text_label' if i == 0 else '@menu_item_text'
            text_item = UILabel(
                text_rect, text[i],
                self.ui_manager,
                container=self,
                object_id=object_id,
                anchors={
                    'top': 'top',
                    'left': 'left',
                    'bottom': 'top',
                    'right': 'left',
                    'left_target': self._icon
                }
            )
            self._text.append(text_item)

    def set_dimensions(self, dimensions: Union[pygame.math.Vector2,
                                               Tuple[int, int],
                                               Tuple[float, float]]):
        print(f'Setting Item Dimensions ({self._text[0].text}): Old: {self.rect.size}, New: {dimensions}')
        super(PycraftWorldMenuItem, self).set_dimensions(dimensions)

class PycraftWorldMenu(UIScrollingContainer):
    def __init__(self, relative_rect, manager, **kwargs):
        print(f'MENU rect: {relative_rect}')
        print(f'menu manager: {manager}')
        print(f'menu args: {kwargs}')
        super(PycraftWorldMenu, self).__init__(relative_rect, manager,
                                               **kwargs
                                               )
        self._items = []

    @property
    def item_margin(self):
        return 5

    @property
    def item_height(self):
        return self.item_margin * 2 + 100

    @property
    def item_width(self):
        return self.viewpane_width

    @property
    def viewpane_width(self):
        return self._view_container.get_rect().width

    def debug(self):
        print(f'  - Root: {self._root_container.rect}')
        print(f'    clip: {self._root_container.get_image_clipping_rect()}')
        print(f'  - View: {self._view_container.rect}')
        print(f'    clip: {self._view_container.get_image_clipping_rect()}')
        print(f'  Scroll: {self.scrollable_container.rect}')
        print(f'  - clip: {self.scrollable_container.get_image_clipping_rect()}')
        if self.vert_scroll_bar:
            print(f' Vert: {self.vert_scroll_bar.rect}')
        if self.horiz_scroll_bar:
            print(f'Horiz: {self.horiz_scroll_bar.rect}')

    def add_item(self, icon : UIImage,
                 name : str,
                 file_name : str,
                 last_played : datetime.datetime,
                 mode :str,
                 cheats : bool,
                 version : str):

        y = len(self._items) * self.item_height
        rr = pygame.Rect(0, y, self.item_width, self.item_height)
        print(f'item rect: {rr}')
        item = PycraftWorldMenuItem(icon, name, file_name, last_played, mode, cheats, version,
                                    self,
                                    rr, 10,
                                    margin=self.item_margin,
                                    manager=self.ui_manager,
                                    container=self.get_container(),
                                    anchors={
                                        'top': 'top',
                                        'left': 'left',
                                        'bottom': 'top',
                                        'right': 'right'
                                    })
        self._items.append(item)

    def fit_scrolling_area_to_items(self):
        """
        Set the scrolling area's width to be the same as the view area (no horiz scrollbar)
        Set the scrolling area's height to the greater of the total height of items or the height of the view area.
        Setting the scroll area height can cause the vertical scrollbar to come and go which changes the
        width of the view panel. Since we are trying to get the scrollable area's width to match the width of the
        view panel, we have to detect this and set the size of the scrolling area a second time.


        """
        h = self.item_height * len(self._items)
        w = self.viewpane_width
        print('----- start ------')
        self.debug()
        # first let the base class adjust the root and view panels.
        self.set_scrollable_area_dimensions((w, h))
        self.debug()
        # if adding or removing the vertical scrollbar changed the width of the view panel,
        # set the size of the scroll panel to reflect this.
        # The height is always the total height of the items
        if w != self.viewpane_width:
            print(f'- Adjust for new scrollbar')
            self.set_scrollable_area_dimensions((self.viewpane_width, h))
            self.debug()
        print('----- end ------')

    def set_items_widths(self):
        """
        Make all of the items have the same width as the view panel
        """
        for item in self._items:
            item.set_dimensions((self.viewpane_width, self.item_height))

    def set_dimensions(self, dimensions: Union[pygame.math.Vector2,
                                               Tuple[int, int],
                                               Tuple[float, float]]):
        """
        When the menu is resized we first make sure the scrolling area size is adjusted
        to fit the width of the view panel and the total height of the items.
        Then we need to make sure all of the items fit the new view panel width.
        """
        old_view_width = self.viewpane_width
        super(PycraftWorldMenu, self).set_dimensions(dimensions)
        self.fit_scrolling_area_to_items()
        if self.viewpane_width != old_view_width:
            self.set_items_widths()

class PycrafterApp(GuiApp):
    def __init__(self, size, framerate=60, ):
        title = 'Pycraft'
        super(PycrafterApp, self).__init__(size, framerate=framerate, title=title)

    def setup(self):
        x = 0
        y = 0
        window_size = self.size
        width = window_size[0]
        height = 150
        # Top Panel:
        # tiled image background panel
        dirt_surface = pygame.image.load('dark_dirt.jpg')
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
        width = self.size[0] - 150
        height = self.size[1] - (self._top_dirt.rect.height + self._bottom_dirt.rect.height)
        x = self.size[0] / 2 - width / 2
        y = 0
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

app = PycrafterApp((1020, 900))
app.ui_manager.get_theme().load_theme('theme.json')
app.setup()
app.run()
