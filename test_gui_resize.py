import pygame
import pygame_gui
from pygame_gui.elements import UIButton, UIPanel, UIDropDownMenu, UILabel

WINDOW_SIZE = (800, 600)



pygame.init()

pygame.display.set_caption('Resize Testing')
window_surface = pygame.display.set_mode(WINDOW_SIZE, flags=pygame.RESIZABLE)
manager = pygame_gui.UIManager(WINDOW_SIZE)

background_surface = pygame.Surface(WINDOW_SIZE)
BGFILL = manager.ui_theme.get_colour('dark_bg')

clock = pygame.time.Clock()
is_running = True

def handle_resize():
    new_size = window_surface.get_size()
    print(f'NEW SIZE: {new_size}')
    manager.set_window_resolution(new_size)
    background_surface = pygame.Surface(new_size)
    return background_surface

margin = 10
butt_w = 300
butt_h = 75
butt_x = window_surface.get_width() - margin - butt_w
butt_y = window_surface.get_height() - margin - butt_h
br_rect = pygame.Rect(0, 0, butt_w, butt_h)
br_rect.bottomright = (-margin, -margin)
br_button = UIButton(
    br_rect,
    'bottom right',
    manager,
    anchors={
        'top': 'bottom',
        'bottom': 'bottom',
        'left': 'right',
        'right': 'right'
    }
)
panel_x = margin
panel_y = margin
panel_w = window_surface.get_width() - (2 * margin)
panel_h = window_surface.get_height() / 3
top_panel = UIPanel(
    pygame.Rect(panel_x, panel_y, panel_w, panel_h),
    1,
    manager,
    anchors={
        'top': 'top',
        'bottom': 'top',
        'left': 'left',
        'right': 'right'
    },

)

label = UILabel(pygame.Rect(0,0,200, butt_h),
                'Some Options:',
                manager,
                container=top_panel,
                anchors={
                    'top': 'top',
                    'left': 'left',
                    'bottom': 'top',
                    'right': 'right'
                }

)
drop_down = UIDropDownMenu(
    ['option 1', 'option 2', 'option 3', 'option 4', 'option 5', 'option 6'],
    'option 2',
    pygame.Rect(0, 0, 200, butt_h),
    manager,
    container=top_panel,
    anchors={
        'top': 'top',
        'left': 'left',
        'bottom': 'top',
        'right': 'right',
        'left_target': label
    }
)
mid_panel = UIPanel(
    pygame.Rect(panel_x, panel_y, panel_w, panel_h),
    1,
    manager,
    anchors={
        'top': 'top',
        'bottom': 'top',
        'left': 'left',
        'right': 'right',
        'top_target': top_panel
    }
)
while is_running:
    time_delta = clock.tick(60) / 1000.0
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            is_running = False
        if event.type == pygame.WINDOWRESIZED:
            background_surface = handle_resize()
        manager.process_events(event)
    background_surface.fill(BGFILL)
    manager.update(time_delta)

    window_surface.blit(background_surface, (0, 0))
    manager.draw_ui(window_surface)

    pygame.display.update()
