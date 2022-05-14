"""
Another way to choose one of the worlds saved locally
"""
import datetime
from typing import Union, Tuple

import pygame
from pygame_gui.elements import UIScrollingContainer, UIImage, UIPanel, UILabel

from pycraft_gui.constants import PYCRAFT_WORLD_MENU_HOVERED, PYCRAFT_WORLD_MENU_UNHOVERED, PYCRAFT_WORLD_MENU_SELECTED


class PycraftMenuItemItem(UIPanel):
    """
    The part of the menu item that displays the world's information.
    """
    def __init__(self,
                 icon_path: str,
                 name: str,
                 file_name: str,
                 last_played: datetime,
                 mode: str,
                 cheats: bool,
                 version: str,
                 outer_item,
                 margin,
                 relative_rect, starting_layer_height,
                 manager,
                 **kwargs):
        self._world_info = {
            'name': name,
            'icon_path': icon_path,
            'file_name': file_name,
            'last_played': last_played,
            'mode': mode,
            'cheats': cheats,
            'version': version
        }

        self.outer_item = outer_item
        print(f'item rect: {relative_rect}')
        super(PycraftMenuItemItem, self).__init__(relative_rect,
                                                  starting_layer_height,
                                                  manager,
                                                  **kwargs)

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
        self._icon.disable()
        arrow_surface = pygame.image.load('PlayButton.png')
        arrow_surface = pygame.transform.smoothscale(arrow_surface, (icon_size, icon_size))
        self._arrow = UIImage(
            icon_rect,
            arrow_surface, manager, container=self,
            visible=0,
            anchors={
                'top': 'top',
                'left': 'left',
                'bottom': 'top',
                'right': 'left'
            }
        )
        self._arrow.disable()
        self._text = []
        item_width = self.outer_item.menu.item_width - icon_surface.get_width() - 3 * margin
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
            text_item.disable()
            self._text.append(text_item)

    @property
    def world_name(self):
        return self._world_info['name']

    def on_hovered(self):
        event_data = {'world_data': self._world_info,
                      'ui_element': self}
        pygame.event.post(pygame.event.Event(PYCRAFT_WORLD_MENU_HOVERED, event_data))
        self._arrow.show()

    def on_unhovered(self):
        event_data = {'world_data': self._world_info,
                      'ui_element': self}
        pygame.event.post(pygame.event.Event(PYCRAFT_WORLD_MENU_UNHOVERED, event_data))
        self._arrow.hide()

    def process_event(self, event: pygame.event.Event) -> bool:
        if event.type == pygame.MOUSEBUTTONUP and event.button == pygame.BUTTON_LEFT:
            x, y = pygame.mouse.get_pos()
            if self.rect.left < x and self.rect.right > x and self.rect.top < y and self.rect.bottom > y:
                event_data = {'world_data': self._world_info,
                              'ui_element': self}
                pygame.event.post(pygame.event.Event(PYCRAFT_WORLD_MENU_SELECTED, event_data))
                self.outer_item.menu.select_item(self.outer_item)
                return True

        return False


class PycraftWorldMenuItem():
    """
    A menu item that displays information about a single saved world.

    Layout:
    The menu item is meant to mimic the world selection menu items in Minecraft itself.
    The icon of the world is displayed on the right side of the menu item.
    The right side of the menu item contains three text items:
    - The name of the World in bold
    - The name of the directory where the world is saved,  followed by the date the world was most recently played
    - The mode of the World (Survival, etc.), the word "Cheats" if commands are enabled, and the Minecraft version
       of the world

    Behavior:
    When the mouse is hovered over the menu item, a "play" icon is displayed over the world icon.
    When the menu item is clicked, the item is "selected" and a border is displayed around the item. the previously
    "selected" item is unselected.

    I wanted to mimic Minecraft's behavior so I want to highlight menu items when you click on them.
    The only way I could figure out how to do this was to have a lower panel that was just the highlight.
    To highlight the menu item I show() the underlying highlight panel.

    """
    HIGHLIGHT_WIDTH = 3

    def __init__(self,
                 icon_path: str,
                 name: str,
                 file_name: str,
                 last_played: datetime.datetime,
                 mode: str,
                 cheats: bool,
                 version: str,
                 menu,
                 relative_rect, starting_layer_height, manager,
                 margin=0,
                 **kwargs):
        self.menu = menu
        self.name = name
        # This is the underlying panel that is shown/hidden to show that the item is selected.
        self.highlight = UIPanel(relative_rect, starting_layer_height,
                                 manager,
                                 visible=1,
                                 object_id='@menu_item_highlight',
                                 **kwargs)
        self.highlight.hide()
        rr = pygame.Rect(relative_rect)
        # Shrink the internal item so that the highlight peeks out
        rr.width = rr.width - PycraftWorldMenuItem.HIGHLIGHT_WIDTH * 2
        rr.height = rr.height - PycraftWorldMenuItem.HIGHLIGHT_WIDTH * 2
        rr.top += PycraftWorldMenuItem.HIGHLIGHT_WIDTH
        rr.left += PycraftWorldMenuItem.HIGHLIGHT_WIDTH
        self.item = PycraftMenuItemItem(icon_path,
                                        name,
                                        file_name,
                                        last_played,
                                        mode,
                                        cheats,
                                        version,
                                        self,
                                        margin,
                                        rr,
                                        # we add 1 to the layer so that we get hover events when highlighted
                                        starting_layer_height + 1,
                                        manager,
                                        object_id='@menu_item',
                                        visible=1,
                                        **kwargs)

    def set_dimensions(self, dimensions: Union[pygame.math.Vector2,
                                               Tuple[int, int],
                                               Tuple[float, float]]):
        # set the dimensions of the two items we manage.
        # NOTE: If I made the Item itself a UIPanel, I could do this with clever anchoring. I think
        self.highlight.set_dimensions(dimensions)
        self.item.set_dimensions((dimensions[0] - PycraftWorldMenuItem.HIGHLIGHT_WIDTH * 2,
                                  dimensions[1] - PycraftWorldMenuItem.HIGHLIGHT_WIDTH * 2))


class PycraftWorldMenu(UIScrollingContainer):
    """
    A menu of PycraftWorldMenuItems

    The menu is a UIScrollingContainer. The menu items track the width of the viewpanel so there should never be
    a horizontal scrollbar.
    """
    def __init__(self, relative_rect, manager, **kwargs):
        """
        Create an empty PycraftWorldMenu.
        """
        super(PycraftWorldMenu, self).__init__(relative_rect, manager,
                                               **kwargs
                                               )
        self._items = []
        self.selected_item = None

    def select_item(self, item):
        for i in self._items:
            if i == item:
                i.highlight.show()
                self.selected_item = i
            else:
                i.highlight.hide()

    @property
    def item_margin(self):
        return 5

    @property
    def item_height(self):
        return self.item_margin * 2 + 106

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

    def add_item(self, icon: str,
                 name: str,
                 file_name: str,
                 last_played: datetime.datetime,
                 mode: str,
                 cheats: bool,
                 version: str):
        """
        Add an item to the menu.

        Parameters:
            name: The name of the saved world
            file_name: The name of the directory where the world is saved.
            last_played: The last time the world wos played.
            mode: The GameType (Survival, Creative, Adventure, or Spectator)
            cheats: True if commands are enabled
            version: the version of Minecraft that created the world
        """
        y = len(self._items) * self.item_height
        rr = pygame.Rect(0, y, self.item_width, self.item_height)
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
        Set the scrolling area's width to be the same as the view area (no horizontal scrollbar)
        Set the scrolling area's height to the greater of the total height of items or the height of the view area.
        Setting the scroll area height can cause the vertical scrollbar to come and go which changes the
        width of the view panel. Since we are trying to get the scrollable area's width to match the width of the
        view panel, we have to detect this and set the size of the scrolling area a second time.


        """
        h = self.item_height * len(self._items)
        w = self.viewpane_width
        self.set_scrollable_area_dimensions((w, h))

        # if adding or removing the vertical scrollbar changed the width of the view panel,
        # set the size of the scroll panel to reflect this.
        # The height is always the total height of the items
        if w != self.viewpane_width:
            self.set_scrollable_area_dimensions((self.viewpane_width, h))

    def set_items_widths(self):
        """
        Make all the items have the same width as the view panel
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

    def process_event(self, event: pygame.event.Event) -> bool:
        """
        Process events that affect the menu.

        Passes MOUSEWHEEL events to the scrollbars so that MOUSEWHEEL events anywhere on the menu (not just on the
        scrollbors cause the menu to scroll.
        """
        if event.type == pygame.MOUSEWHEEL:
            if event.y and self.vert_scroll_bar:
                self.vert_scroll_bar.scroll_wheel_moved = True
                self.vert_scroll_bar.scroll_wheel_amount += event.y
            if event.x and self.horiz_scroll_bar:
                self.horiz_scroll_bar.scroll_wheel_moved = True
                self.horiz_scroll_bar.scroll_wheel_amount += event.x
        return True
