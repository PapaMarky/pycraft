from pycraft_gui.ui_world_selector import UIWorldSelector
from pycraft_gui.gui_app import GuiApp
import pygame
from pygame.event import custom_type

PYCRAFT_WORLD_CHANGED = custom_type()
PYCRAFT_WORLD_SELECTION_CHANGED = custom_type()


class PycraftGuiApp(GuiApp):
    """
    A GuiApp for Pycraft

    Manages Saved location / selection / loading of pycraft.World
    """
    SPACE = 10

    def __init__(self, size, title, resizeable=True):
        """
        Create a PycraftGuiApp object
        Parameters:
        - size: size of the window
        - title: title to display on the window
        """
        super().__init__(size, title=title, resizeable=resizeable, background_color='#101010')
        self._add_world_elements()

    def _add_world_elements(self):
        """
        Add elements for selecting from existing saved worlds.
        """
        self._world_selector = \
            UIWorldSelector(pygame.Rect(PycraftGuiApp.SPACE, PycraftGuiApp.SPACE,
                                        self.root_window_surface.get_width() - 2 * PycraftGuiApp.SPACE,
                                        50),
                            self.ui_manager,
                            anchors={
                                'top': 'top',
                                'left': 'left',
                                'bottom': 'top',
                                'right': 'right'
                            })

    def handle_event(self, event):
        """
        Pass events to the world_selector object for processing
        """
        if super(PycraftGuiApp, self).handle_event(event):
            print(f'Handled by PycraftGuiApp: {event}')
            return True
        return False
