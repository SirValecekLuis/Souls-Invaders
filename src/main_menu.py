import pygame
import pygame_menu


class MainMenu:
    def __init__(self, screen: pygame.display):
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

        self.menu.add.button('Play', self.new_game)
        self.menu.add.button('Settings', self.settings)
        self.menu.add.button('Quit', pygame_menu.events.EXIT)

    def new_game(self):
        self.menu.disable()

    def settings(self):
        ...

    def start(self):
        self.menu.mainloop(self.screen)
