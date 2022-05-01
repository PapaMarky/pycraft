import pygame
import pygame_gui
from pygame_gui.ui_manager import UIManager
from pycraft_gui.ui_world_selector import UIWorldSelector
from pygame.event import custom_type

MAPAPP_WORLD_CHANGED = custom_type()


class GuiApp:
    """
    Base class for any pygame_gui app
    """

    def __init__(self, appsize, title=None, flags=0):
        """
        Create a GuiApp

        Parameters:
        appsize: how big to make the root window
        title:   Title of the window
        flags:   pygame flags to pass into pygame.display.set_mode (pygame.RESIZABLE)
        """
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
        """
        Size of the root window
        """
        return self._size

    @property
    def ui_manager(self):
        """
        The UIManager of the application
        """
        return self._ui_manager

    def handle_event(self, event):
        """
        Override this function to handle custom events
        """
        return False

    def event_loop(self):
        """
        Run the event loop once.

        This is a handy way to get the screen to update during long operations when you are too lazy
        to make it work with threading.
        """
        time_delta = self.clock.tick(60) / 1000.0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.is_running = False
            elif event.type == pygame.WINDOWRESIZED:
                print('handle WINDOWRESIZED')
                self.size = self.root_window_surface.get_rect().size
                self.background_surface = pygame.Surface(self.size).convert()
                self.background_surface.fill(pygame.Color('#303030'))
                self.ui_manager.set_window_resolution(self.size)
            else:
                self.handle_event(event)
            self._ui_manager.process_events(event)

        self._ui_manager.update(time_delta)

        self.root_window_surface.blit(self.background_surface, (0, 0))
        self._ui_manager.draw_ui(self.root_window_surface)

        pygame.display.update()

    def run(self):
        """
        Run the app
        """
        while self.is_running:
            self.event_loop()


class PycraftGuiApp(GuiApp):
    """
    A GuiApp for Pycraft

    Manages Saved location / selection / loading of pycraft.World
    """

    def __init__(self, size, title, flags=0):
        """
        Create a PycraftGuiApp object
        Parameters:
        - size: size of the window
        - title: title to display on the window
        """
        super().__init__(size, title, flags=flags)
        self._add_world_elements()

    def _add_world_elements(self):
        """
        Add elements for selecting from existing saved worlds.
        """
        space = 10
        self._world_selector = \
            UIWorldSelector(pygame.Rect(space, space,
                                        self.root_window_surface.get_width() - 2 * space,
                                        50),
                           self.ui_manager,
                            anchors={
                                'top': 'top',
                                'left': 'left',
                                'bottom': 'top',
                                'right': 'right'
                            }
                            )
    def handle_event(self, event):
        """
        Pass events to the world_selector object for processing
        """
        if super(PycraftGuiApp, self).handle_event(event):
            print(f'Handled by PycraftGuiApp: {event}')
            return True
        return False
