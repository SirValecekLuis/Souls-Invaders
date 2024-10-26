import pygame
import pygame_menu

from src.managers.screen_manager import ScreenManager
from src.managers.service_manager import ServiceManager
from src.managers.time_manager import TimeManager


class EscMenu:
    def __init__(self):
        self.screen = ServiceManager.get(ScreenManager)
        self.time = ServiceManager.get(TimeManager)
        self.theme = pygame_menu.themes.Theme(
            background_color=(40, 40, 40),
            title_font=pygame.font.Font("./font/OptimusPrinceps.ttf", 70),
            widget_font=pygame.font.Font("./font/OptimusPrinceps.ttf", 45),
            widget_alignment=pygame_menu.locals.ALIGN_CENTER,
            widget_padding=15,
            selection_color=(129, 0, 1),
        )

        self.menu = pygame_menu.Menu(
            'Souls Invaders',
            self.screen.get_width(),
            self.screen.get_height(),
            theme=self.theme,
            onclose=self._on_menu_close
        )

        self.menu.add.button('Continue', self.unpause)
        self.menu.add.button('Settings', self.settings)
        self.menu.add.button('Quit game', pygame_menu.events.EXIT)

    def _on_menu_close(self):
        self.time.toggle_pause()
        return pygame_menu.events.CLOSE

    def handle_menu_event(self, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            self.menu.close()
            return True
        return False

    def unpause(self):
        self.menu.close()

    def settings(self):
        ...

    def start(self):
        self.time.toggle_pause()
        self.menu.mainloop(
            self.screen.get_screen(),
            bgfun=None,
            handle_events=self.handle_menu_event,
            fps_limit=60
        )
