import time

import pygame
import pygame_gui
from pygame_gui.elements import UIButton, UILabel, UIPanel

from pycraft_gui.gui_app import GuiApp
import queue
import threading

def thread_launcher(**kwargs):
    obj = kwargs.get('obj')
    print(f'obj: {obj}')
    queue = kwargs.get('queue')
    print(f'queue: {queue}')

    thread_running = True
    while thread_running:
        if not queue.empty():
            task = queue.get()
            cmd = task.get('command')
            print(f'got task: {task["command"]}')
            if cmd == 'quit':
                thread_running = False
            if cmd == 'increment':
                obj.increment_clicks()


margin = 5
class ThreadTestApp(GuiApp):
    def __init__(self):
        super().__init__((640,480), title='Thread Test')

        self._panel = UIPanel(
            pygame.Rect(margin, margin, 640 - 2 * margin, 480 - 2 * margin), 1,
            anchors={
                'top': 'top', 'left': 'left',
                'bottom': 'bottom', 'right': 'right'
            },
            margins={'top': margin, 'left': margin, 'bottom': margin, 'right': margin},
            manager=self.ui_manager
        )
        self._button = UIButton(
            pygame.Rect(margin, margin, 200, 30),
            'Do Something',
            manager=self.ui_manager,
            container=self._panel,
            anchors={
                'top': 'top',
                'left': 'left',
                'bottom': 'top',
                'right': 'left'
            }
        )

        self._nclicks = 0
        rr = pygame.Rect((margin, self._button.rect.bottom + margin), (-1, -1))
        print(f'rr: {rr}')
        self._status = UILabel(
            rr,
            f'Clicks: {self._nclicks}',
            self.ui_manager,
            container=self._panel,
            anchors={
                'top': 'top',
                'left': 'left',
                'bottom': 'top',
                'right': 'left'
            }
        )
        self._worker_queue = queue.Queue()
        self._worker_thread = threading.Thread(name='worker', target=thread_launcher, kwargs={'obj': self, 'queue': self._worker_queue})
        self._worker_thread.start()

    def increment_clicks(self):
        # this gets called from threads. Should probably use critical section
        self._nclicks += 1
        self._status.set_text(f'Clicks: {self._nclicks}')

    def on_shutdown(self):
        self._worker_queue.put({'command': 'quit'})
        self._worker_thread.join()

    def handle_event(self, event):
        if event.type == pygame_gui.UI_BUTTON_PRESSED and event.ui_element == self._button:
            task = {
                'command': 'increment'
            }
            self._worker_queue.put(task)

app = ThreadTestApp()

app.setup()
app.run()
