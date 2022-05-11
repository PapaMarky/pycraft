"""
GuiApp module
"""
from typing import Union

import pygame
from pygame_gui import UIManager
from abc import ABCMeta, abstractmethod

# TODO Separate the "HostWindow" from the "GuiApp" - try to make multi-window application possible.


class IUpdateObject(metaclass=ABCMeta):
    """
    Metaclass for defining objects that can be updated.
    """
    @abstractmethod
    def update(self, time_delta: float):
        """
        Update the object

        Parameters:
            time_delta:float: Seconds elapsed since previous update.
        """


class GuiApp:
    """
        Base class for creating python scripts with GUI interfaces.

        ``pygame_gui`` is a full-featured and fairly easy to use python package for adding
        Graphical User Interfaces (GUI) to python applications. There is a lot of boilerplate setup
        that is required for creating a ``pygame_gui`` based application. This class does all the setup
        for you so you can focus on your application and its interface.

        This class requires pygame and pygame_gui and is intended to simplify the process of creating
        GUI applications using those packages.

        Being familiar with pygame will be helpful. Learning
        the basics of pygame_gui is essential because to create anything useful you will want to
        add your own UI elements.

        How To Use This Class
        =====================
        The best way to use this class is to derive your own App class from it and override these functions to
        implement your own application:

        * setup: to add UI elements to the root window and do any other application
          initialization. See :func: `setup`
        * update: to update application data. Called from the `main_loop`
          See :func: `update`
        * handle_events: to handle UI and custom events. Called from the `main_loop`

        This design lets you focus on the parts of your application that are
        different from other applications and takes care of the basic framework of the
        graphical user interface.

        How This Class Works
        ====================
        The basic workflow is
            * setup the objects and user interface of the applications
            * then update objects and handle events in a loop.

        Assuming you have created a subclass `MyAppClass` that overrides `setup`, `update` and
        `handle_event`, the program to use it should look something like this::

            app = MyAppClass()
            app.setup()
            app.run()
    """

    def __init__(self, window_size, background_color = '#303030', framerate: int = 60, title: str = None, resizeable=True):
        """
        Create an instance of GuiApp

        Parameters:
            window_size: The size of the window to be created for the application.
            title:   Title of the window which is display in the frame of the application.
            resizeable: Whether the window created for the application should be resizable. Defaults to True.
            framerate: Speed at which updates occur. Unit: FPS. Default: 60
        """
        self._background_color = pygame.Color(background_color)
        self._framerate = framerate
        self.title = title
        pygame.init()
        if title:
            pygame.display.set_caption(title)
        flags = 0
        # TODO: Other interesting flags:
        # SHOWN / HIDDEN - create multi-window apps? Dialogs windows?
        # NOFRAME
        # FULLSCREEN
        if resizeable:
            flags |= pygame.RESIZABLE
        self.root_window_surface = pygame.display.set_mode(window_size, flags)

        self.background_surface = pygame.Surface(self.size).convert()
        self.background_surface.fill(pygame.Color(self._background_color))
        self._ui_manager = UIManager(self.size)
        self.clock = pygame.time.Clock()
        self.is_running = False
        self._update_objects = []

    def setup(self):
        """
        Setup / initialize application data.
        This is where you should create any UI elements specific to your application.

        Override this member function to create panels, buttons, etc. as required to create the user
        interface for your application. It can also be used to create and initialize any other objects required for
        your application.
        """
        pass

    def add_update_object(self, update_object: IUpdateObject):
        """
        Helper function that registers an object to be updated via the `main_loop`. This lets
        you create objects with an `update` function and register them with the application so
        that they get updated automatically via the applications `main_loop`.
        """
        self._update_objects.append(update_object)

    def update(self, time_delta: float):
        """
        Update the application specific data prior to rendering the user interface.

        If you override this class be sure to call ``super().update(time_delta)`` to take
        advantage of the already written loop that will call update on all of your updatable
        objects.

        This is done by calling ``update(time_delta)`` on each of the registered
        IUpdatableObject instances.

        Parameters:
            time_delta:float: Fractional seconds that have passed since the last update.
        """
        for obj in self._update_objects:
            obj.update(time_delta)

    def handle_event(self, event):
        """
        Override this function to handle your application specific events.

        Currently the base class version does nothing, but that could change in future releases.
        When overriding this function it is a good idea to add this at the beginning of your
        override::
            if super().handle_event(event):
                return True

        Parameters:
            event: The event to be handled.

        Returns:
            True if the event was handled. False if not. This tells the caller whether
                the event needs further processing
        """
        return False

    def on_shutdown(self):
        """
        Called when app is shutting down. Override with application specific clean up.
        """
        pass

    @property
    def size(self):
        """
        The size of the root window surface. (i.e. the host window of the app)

        This value is useful for calculating the layout of UI components.
        """
        return self.root_window_surface.get_rect().size

    @property
    def ui_manager(self):
        """
        The UIManager of the application.

        Useful when creating new user interface elements on the root window.
        """
        return self._ui_manager

    @property
    def framerate(self) -> int:
        return self._framerate

    def _main_loop(self):
        """
        Run the main loop once.

        This is a handy way to get the screen to update during long operations when you are too lazy
        to make it work with threading.

        This function does the following:

        1. Calculates the time_delta which can be used for animations, etc
        2. Calls ``update_application_data``. Override this function to update application specific data.
        3. For each event in the pygame event queue:
            3.1. Handles generic application / window events
            3.2. calls ``handle_event`` passing in any unprocessed events. Override this function to handle application
                specific events.
            3.3 Passes any unprocessed events to the UIManager.
        4. Updates the UIManager with the current time_delta
        5. Updates the Display

        If you override :func:`.update` and :func:`.handle_event` you should not need to override this
        function.
        """
        time_delta = self.clock.tick(self.framerate) / 1000.0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.on_shutdown()
                self.is_running = False
            elif event.type == pygame.WINDOWRESIZED:
                self.background_surface = pygame.Surface(self.size).convert()
                self.background_surface.fill(pygame.Color(self._background_color))
                self.ui_manager.set_window_resolution(self.size)
            else:
                self.handle_event(event)
            self._ui_manager.process_events(event)

        self._ui_manager.update(time_delta)
        self.update(time_delta)

        self.root_window_surface.blit(self.background_surface, (0, 0))
        self._ui_manager.draw_ui(self.root_window_surface)

        pygame.display.update()

    def run(self):
        """
        Run the app by continuously calling the main_loop
        """
        if self.is_running:
            return
        self.is_running = True
        while self.is_running:
            self._main_loop()
