import pygame
import pygame_menu

class EscMenu:
    def __init__(self, screen: pygame.display, clock: pygame.time.Clock):
        self.clock = clock

        self.clock.tick(0)

        self.screen = screen
        self.theme = pygame_menu.themes.Theme(
            background_color=(40, 40, 40),
            title_font=pygame.font.Font("./font/OptimusPrinceps.ttf", 70),
            widget_font=pygame.font.Font("./font/OptimusPrinceps.ttf", 45),
            widget_alignment=pygame_menu.locals.ALIGN_CENTER,
            widget_padding=15,
            selection_color=(129, 0, 1),
        )

        self.menu = pygame_menu.Menu('Souls Invaders', self.screen.get_width(), self.screen.get_height(),
                                     theme=self.theme)

        self.menu.add.button('Continue', self.unpause)
        self.menu.add.button('Settings', self.settings)
        self.menu.add.button('Quit game', pygame_menu.events.EXIT)

    def unpause(self):
        self.clock.tick(60)
        self.menu.disable()

    def settings(self):
        ...

    def start(self):
        self.menu.mainloop(self.screen)

