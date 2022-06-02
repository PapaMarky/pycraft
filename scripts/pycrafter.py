import pygame

import pycraft_gui
from pycraft_gui.gui_app import GuiApp
from pycraft_gui.pycrafter_main_panel import PycrafterMainPanel

print(f'Pycraft GUI Installed at "{pycraft_gui.install_path}"')
print(f' - Data Dir: {pycraft_gui.get_data_dir()}')

class PycrafterApp(GuiApp):
    def __init__(self, size, framerate=60, ):
        title = 'Pycraft'
        super(PycrafterApp, self).__init__(size, framerate=framerate, title=title)
        themes_file = pycraft_gui.get_themes_file_path('pycraft_theme.json')
        print(f'themes file: {themes_file}')
        if themes_file:
            self.ui_manager.get_theme().load_theme(themes_file)
        else:
            print(f'WARNING: theme file not found')

        self._main_panel = PycrafterMainPanel(
            pygame.Rect((0, 0), size),
            1,
            self.ui_manager,
            app=self,
            object_id='@main_panel',
            anchors={
                'top': 'top', 'left': 'left',
                'bottom': 'bottom', 'right': 'right'
            }
        )
    def show_map(self):
        print(f'Show map')

    def show_data(self):
        print(f'show data')

    def show_configuration(self):
        print(f'show config')

    def show_main(self):
        print(f'show main menu')

app = PycrafterApp((1020, 900))
app.setup()
app.run()
